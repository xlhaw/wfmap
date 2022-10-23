"""
Useful script for data cleansing and explanation
Get/Load->Clean/Calc 

Author: Leon Xiao, i@xlhaw.com
"""

import os,pandas as pd,numpy as np

def get_list(fpath,suffix='',join=True,strict=False):
    '''
    Extract list from text file or directory
    Args
    ------
    fpath: str
    suffix: in lowercase
    strict: bool, default using the lowercase to match the suffix
    
    Returns
    ------
    lists: list
        file/content in the folder/txtfile    
    '''
    lists=[]
    if os.path.isfile(fpath):
        with open(fpath) as f:
            while True:
                line=f.readline()
                if line=='':
                     break
                elif line[-1]=='\n':
                     lists.append(line[:-1])
                else:
                    lists.append(line)
    elif os.path.isdir(fpath):
        if suffix=='': #return folder list
            lists=next(os.walk(fpath))[1]
        else:
            if strict:
                lists=[i for i in os.listdir(fpath) if i.endswith(suffix)]
            else:
                lists=[i for i in os.listdir(fpath) if i.lower().endswith(suffix.lower())]
        if join:
            return [f'{fpath}\\{item}' for item in lists]
    return lists

def get_wflist(fpath):
    wflist=[]
    original=get_list(fpath)
    for wf in original:
        if wf[0].upper()!="H":
            wf="H"+wf
        wf=wf[:6]
        if wf not in wflist:
            wflist.append(wf.upper())
    return wflist

def num_filter(df,items=[],specs={},iqr=False,sig=None):
    '''
    Clean numeric data by lower/upper limits, IQR and Sigma Filter
    Args
    ------
    df: pd.DataFrame
    items: list
    specs: dict  optional
        {item:(LSL,USL)}
    iqr: bool
    sig: float
    Returns
    ------
    data: pd.DataFrame
        cleaned data
    '''
    def iqr_filter(series):
        UCL=2.5*series.quantile(0.75)-1.5*series.quantile(0.25)
        LCL=2.5*series.quantile(0.25)-1.5*series.quantile(0.75)
        return series.where((series<=UCL)&(series>=LCL),np.nan)
    
    data=df.copy()
    if len(items)==0 and len(specs)>0:
        for item in specs:
            if item in data.columns:
                LSL,USL=specs[item]
                data[item]=data[item].where((data[item]>=LSL)&(data[item]<=USL),np.nan)        
        return data
    for item in items:
        if item in specs:
            LSL,USL=specs[item]
            data[item]=data[item].where((data[item]>=LSL)&(data[item]<=USL),np.nan)
        if iqr:
            data[item]=iqr_filter(data[item])
        if sig:
            m=data[item].mean() 
            std=data[item].std()
            data[item].where((data[item]>=m-sig*std)&(data[item]<=m+sig*std),np.nan,inplace=True)
    return data


def uni_qty_filter(df,column,grp_by=[],min_qty=10):
    return pd.concat([data for _,data in df.groupby(grp_by) if len(data[column].unique())>min_qty])


def ttl_qty_filter(df,column,grp_by=[],min_qty=40):
    '''
    Add NaN values support for quantile estimation
    Args
    -----
    df: pd.DataFrame
    column: str
    grp_by: list
    min_qty: int

    Returns
    -----
    pd.DataFrame

    '''
    valid=[]
    for _,data in df.groupby(grp_by):
        if data[column].count()>min_qty:
            valid.append(data)
    return pd.concat(valid)


def string_filter(df,column,remove=['XA','XS','XB','T0','SEM'],keep=[]): #column='CONTROL_NO',remove=['XA','XS','XB','T0'],keep=['DW','PTP'], if tilt: keep=['XA','XS','T01','T03','SEM']
    '''
    Filter data base on string match scheme
    Args
    -----
    df (pd.DataFrame):
    item (str):
    quantile (float):

    Returns
    -----
    float or np.nan

    '''
    if remove:
        for i in remove:
            df=df[~df[column].str.contains(i)]
            #df=df.query(f'{i} not in {column}')
    if keep:
        data=[]
        for i in keep:
            data.append(df[df[column].str.contains(i)])
        df=pd.concat(data)
    return df

def code_filter(df,value,flag_col,use_code): return df[value].where(df[flag_col]==use_code,np.nan)

def flag_filter(df,flags={}): # scheme: {value:(col,flag)}
    '''
    Args
    -----
    df: pd.DataFrame
    flags: dict
        {'value_col':('flag_col',use_code)}

    Returns
    -----
    df: pd.DataFrame
    '''
    for value,(col,flag) in flags.items():
        if value in df.columns:
            df[value].where(df[col]==flag,np.nan,inplace=True)
    return df

def cop_filter(series,level=80,sig=None):
    '''
    Filter numeric data by Center of Population(COP)
    Args
    -----
    series: pd.Series
    level: float 0->100
    sig: float >0
    '''
    ll=(100-level)/2
    ll,ul=np.percentile(series.dropna(),[ll,100-ll])    
    if sig:
        cop_avg=series.where((series>=ll)&(series<=ul)).mean()
        cop_std=series.where((series>=ll)&(series<=ul)).std()
        return series.where((series>=cop_avg-sig*cop_std)&(series<=cop_avg+sig*cop_std),np.nan)
    else:
        return series.where((series>=ll)&(series<=ul),np.nan)

def na_iqr(df,item,quantile=0.5): 
    '''
    Add NaN values support for quantile estimation
    Args
    -----
    df (pd.DataFrame):
    item (str):
    quantile (float):

    Returns
    -----
    float or np.nan

    '''
    return np.quantile(df[item].dropna(),quantile) if len(df[item].dropna())>=1 else np.nan

def merge_cols(df,col_pairs=[],col_dict={}):
    '''
     
    Args
    -----
    df (pd.DataFrame):
    item (str):
    quantile (float):

    Returns
    -----
    float or np.nan

    '''
    for (keep,drop) in col_pairs:
        try:
            df[keep].loc[df[keep].isnull()]=df[drop].loc[df[keep].isnull()] #alternative df.update(other,overwrite=False)
            df=df.drop(drop,axis=1)
        except:
            pass
    if len(col_dict)>0:
        df=df.rename(columns=col_dict)
    return df

def numerify(value,int_=False,round_=None,): # pd.to_numeric??
    '''
    Add NaN values support for quantile estimation
    Args
    -----
    df (pd.DataFrame):
    item (str):
    quantile (float):

    Returns
    -----
    float or np.nan

    '''  
    try:
        if int_:
            value=int(value)        
        else:
            value=float(value)
            if round_:
                value=round(value,round_)
    except: #TypeError: float() argument must be a string or a number, not 'NoneType'
        value=np.nan
    return value



def edge_mark(map_data,row='MAP_ROW',col='MAP_COL',edge=4):
    '''
    Add NaN values support for quantile estimation
    Args
    -----
    df (pd.DataFrame):
    item (str):
    quantile (float):

    Returns
    -----
    float or np.nan

    '''
    ocr_list=[]
    for row_,df in map_data.groupby(row):
        cmin,cmax=int(df[col].min()),int(df[col].max())
        for col_ in range(cmin,cmin+edge):
            ocr_list.append([row_,col_])
        for col_ in range(cmax-edge+1,cmax+1):
            ocr_list.append([row_,col_])
    ocr=pd.DataFrame(ocr_list,columns=[row,col])
    ocr=ocr.merge(map_data.reset_index())[['OCR',row,col]]
    return ocr.set_index('OCR')

def read_excel(fpath,**kwargs):
    try:
        return pd.read_csv(fpath,**kwargs)
    except:
        return pd.read_excel(fpath,**kwargs)
