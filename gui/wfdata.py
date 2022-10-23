"""
Wafer data wrangling for visualization

Author: Leon Xiao i@xlhaw.com
"""

import os
import numpy as np
import pandas as pd
from lhafile import Lhafile
from io import BytesIO


def drop_dummy(func):  # = drop_dummy(fun(*arg,**kwarg))
    def wrapped(*arg, **kwarg):
        df = func(*arg, **kwarg)
        return df.where(df['ELG_STATUS'] != 'X', np.nan).dropna(subset=['ELG_STATUS'])
    return wrapped


class Wafer:
    '''
    Read and Extract Wafer Incoming Data from .LZH file

    '''

    def __init__(self,
                 waferno,
                 SRC=r'\\dn2prod11\FSPDC\INCOMING\HDWY',
                 DIE_QTY={66312: 'UP', 73800: 'UP2', 79380: 'UP3'},
                 FF_ROWS={'UP': 84, 'UP2': 68, 'UP3': 78},
                 FF_OFFSET={'UP': (8, 7), 'UP2': (18, 5), 'UP3': (40, 6)},
                 FF_COLS=24,
                 FF_QTY={'UP': (6, 8), 'UP2': (8, 8), 'UP3': (
                     8, 8), 'UP2E': (12, 10), 'UP3E': (12, 10)},
                 ):
        assert len(waferno) == 6 and waferno[0] == 'H', 'Incorrect WaferNo!'
        self.ID = waferno.upper()
        self.lzhfile = Lhafile(SRC+'/'+self.ID+'.LZH')
        self.format = DIE_QTY.get(self.die_count(), 'UP2')
        self.ff_bars = FF_ROWS.get(self.format)
        self.ff_cols = FF_COLS
        self.ff_offset = FF_OFFSET

    def __repr__(self):
        return f"{self.ID}'s Wafer Incoming Data"

    @staticmethod
    def make_ocr(df, row, col):
        df['OCR'] = df[row].map(lambda x: x[-2:]+x[0]) + \
            df[col].str.rjust(2, '0')  # A001, 1 -> 01A01
        return df.set_index(['OCR'])

    def read_lzh(self, suffix): return BytesIO(
        self.lzhfile.read(self.ID+suffix))

    def die_count(self): return len(pd.read_csv(self.read_lzh('.ELG')))

    @drop_dummy
    def read_fpd(self):
        header = ['BLOCK', 'ELG_STATUS', 'ELG_RES', 'WRT_RES', 'WRT_IND', 'MR', 'CODE', 'HR',
                  'HDI', 'MR2', 'HRW', 'ELG_CODE', 'WELG_STATUS', 'WELG_RES', 'WELG_CODE', 'OSR']
        # KeyError: "['MR2' 'HRW'] not in index", old wafers do not have R2
        fpd = pd.read_csv(self.read_lzh('.FPD'), dtype={'COLUMN': str})
        fpd = self.make_ocr(fpd, 'ROW', 'COLUMN')
        fpd['ROW'] = fpd['ROW'].map(lambda x: str(x)[0])
        fpd.rename(columns={'ROW': 'BLOCK'}, inplace=True)
        return fpd[header]

    @drop_dummy
    def read_elg(self):
        header = ['MAP_ROW', 'MAP_COL', 'BLOCK', 'ELG_RES', 'ELG_STATUS', 'WELG_RES',
                  'WELG_STATUS', 'ELG_FLAG', 'WELG_FLAG', 'FF_ROW', 'FF_COL', 'FF_ID', 'WIF_COL', 'WIF_ROW']
        elg = pd.read_csv(self.read_lzh('.ELG'), dtype={'BLOCK_COL': str})
        elg = self.make_ocr(elg, 'BLOCK_ROW', 'BLOCK_COL')
        elg.rename({'ELG_R_RES': 'ELG_RES'}, inplace=True, axis='columns')
        row_offset, col_offset = self.ff_offset[self.format]
        elg['FF_ROW'] = ((elg['MAP_ROW']+row_offset-1) //
                         self.ff_bars+1).astype(int)
        elg['FF_COL'] = ((elg['MAP_COL']+col_offset-1) //
                         self.ff_cols+1).astype(int)
        elg['FF_ID'] = 'R' + \
            elg['FF_ROW'].astype(str)+'C'+elg['FF_COL'].astype(str)
        elg['WIF_COL'] = elg['MAP_COL'].map(
            lambda x: np.mod(x+col_offset-1, self.ff_cols)+1)
        elg['WIF_ROW'] = elg['MAP_ROW'].map(
            lambda x: np.mod(x+row_offset-1, self.ff_bars)+1)
        return elg[header]

    def map_data(self):
        return self.read_elg()[['MAP_ROW', 'MAP_COL', 'FF_ROW', 'FF_COL', 'BLOCK', 'WIF_COL', 'WIF_ROW', 'FF_ID', 'ELG_STATUS']]

    @drop_dummy
    def read_teg(self):
        header = ['MAP_ROW', 'MAP_COL', 'BLOCK', 'ELG_RES', 'ELG_STATUS', 'WELG_RES',
                  'WELG_STATUS', 'ELG_FLAG', 'WELG_FLAG', 'FF_ROW', 'FF_COL', 'FF_ID']
        shot2blk = {'13': 'E', '14': 'J', '15': 'J', '16': 'G', '22': 'J', '23': 'J', '24': 'J', '25': 'J', '26': 'J', '27': 'J',
                    '31': 'P', '32': 'P', '33': 'P', '34': 'P', '35': 'R', '36': 'R', '37': 'R', '38': 'R', '41': 'A', '42': 'A',
                    '43': 'A', '44': 'A', '45': 'C', '46': 'C', '47': 'C', '48': 'C', '51': 'B', '52': 'B', '53': 'B', '54': 'B',
                    '55': 'D', '56': 'D', '57': 'D', '58': 'D', '61': 'Q', '62': 'Q', '63': 'Q', '64': 'Q', '65': 'S', '66': 'S',
                    '67': 'S', '68': 'S', '72': 'F', '73': 'F', '74': 'F', '75': 'H', '76': 'H', '77': 'H', '83': 'K', '84': 'K', '85': 'K', '86': 'K'}  # eclude this
        # though #13 and #16 locate in Blk J, but they are generally dummy, use those 2 dummy shot to repesent E/G to keep the length same as R4
        teg = pd.read_csv(self.read_lzh('.TEG'), dtype={
                          'SHOT_NUM': str, 'SHOT_COL': str})
        teg['TMP'] = teg['SHOT_NUM']+teg['SHOT_COL']
        # since TEG map_row starts from SHOT boundary while ELG map_row starts from block boundary
        teg['MAP_ROW'] = teg['TMP'].map(
            lambda x: (int(x[0])-1)*self.ff_bars-6.5)
        teg['MAP_COL'] = teg['TMP'].map(
            lambda x: (int(x[1])-1)*24+int(x[2:])-6)
        teg['BLOCK'] = teg['SHOT_NUM'].replace(
            shot2blk)  # UP3 @35th  UP2 @27th  UP None
        teg['FF_ROW'] = teg['SHOT_NUM'].map(lambda x: int(x[0]))
        teg['FF_COL'] = teg['SHOT_NUM'].map(lambda x: int(x[1]))
        teg['FF_ID'] = 'R' + \
            teg['FF_ROW'].astype(str)+'C'+teg['FF_COL'].astype(str)
        teg.rename({'ELG': 'ELG_RES', 'WELG': 'WELG_RES'},
                   axis='columns', inplace=True)
        return teg[header]

    def read_psr(self):
        return pd.read_csv(self.read_lzh('.PSR'), skiprows=2, na_values=['        ', 50000000000, 72361580], index_col='BarNo')

    def read_ovl(self):
        return pd.read_csv(self.read_lzh('M.OVL'), skiprows=1)[['WAFER', 'DIE_X', 'DIE_Y', 'Y_OVERLAY', 'TEST']].rename(columns={'Y_OVERLAY': 'Y_OVL', 'TEST': 'SITE'})

    def read_sto(self):
        return pd.read_csv(self.read_lzh('.STO'))[['WAFER', 'DIE_X', 'DIE_Y', 'STA_X_OVERLAY',
                                                   'SS1_X_OVERLAY', 'SITE', 'SLIDER_ID']].rename(
            columns={'STA_X_OVERLAY': 'STA_X_OVL', 'SS1_X_OVERLAY': 'SS1_X_OVL', 'SLIDER_ID': 'OCR'})

    def read_rwm(self):
        rwm = pd.read_csv(self.read_lzh('.RWM'), skiprows=1, na_values=[
                          'ZZZ', 'XXX', 'DDD'], skipfooter=65, engine='python')
        # rwm.fillna('OK')
        rwm.set_index('BarNo', inplace=True)
        rwm = rwm.unstack().reset_index()
        rwm.columns = ['MAP_COL', 'MAP_ROW', 'DEFECT']
        rwm.MAP_COL = rwm.MAP_COL.map(lambda x: int(x))
        return rwm

    def read_dt(self):
        dt = pd.read_csv(self.read_lzh('.DT'), skiprows=2)
        dt.set_index(['TC_ROW', 'TC_COL'], inplace=True)
        # dta=dt[dt['DT_TYPE']=='DTA'][['DT_R1','DT_R2']]
        # dtb=dt[dt['DT_TYPE']=='DTB'][['DT_R1','DT_R2']]
        dt_sum = pd.read_csv(self.read_lzh('.DT'))
        dt_avg = [float(dt_sum['MR1DT1_AVG'][0]),
                  float(dt_sum['MR2DT1_AVG'][0])]
        return dt, dt_avg

    def read_pcm(self):  # only for RW wafer
        pcm = pd.read_csv(self.read_lzh('.PCM'), dtype={'COLUMN': str})
        pcm['OCR'] = self.make_ocr(pcm, 'ROW', 'COLUMN')
        return pcm[['PCM', 'PCM2', 'PCM_FDP_CODE', 'PCM2_FDP_CODE']]

    def read_ff(self):
        try:
            ff = pd.read_csv(self.read_lzh('_FF.CSV'))[['FLW', 'FLW2']]
            return ff.mean()
        except:  # FileNotFoundError
            return [0, 0]

    def inc_data(self):
        fpd = self.read_fpd()
        maps = self.map_data().drop('BLOCK', axis=1)
        try:
            pcm = self.read_pcm()
            fpd = pd.concat([fpd, pcm], axis=1)
        except:   # FileNotFoundError
            fpd['PCM'] = np.nan
            fpd['PCM_FDP_CODE'] = np.nan
        data = pd.concat(
            [fpd, maps.drop('ELG_STATUS', axis=1)], join='inner', axis=1)
        data = data.reset_index()
        data.rename(columns={'index': 'OCR'}, inplace=True)
        data = data.merge(self.read_rwm(), on=['MAP_ROW', 'MAP_COL'])
        data['DEFECT'] = data['DEFECT'].fillna('OK')

        data = data.set_index('OCR')
        return data.dropna(subset=['BLOCK']).sort_values(['MAP_ROW', 'MAP_COL'])

    def clean_inc(self):
        data = self.inc_data()
        code_dict = {'MR': 'CODE', 'ELG_RES': 'ELG_CODE', 'WELG_RES': 'WELG_CODE',
                     'PCM': 'PCM_FDP_CODE', 'HDI': 'CODE', 'OSR': 'CODE'}
        for item in code_dict:
            data[item] = data[item].where(data[code_dict[item]] == 0, np.nan)
        data['ELG_RES'] = data['ELG_RES'].where(
            data['ELG_STATUS'] == 'R2', np.nan)
        data['WELG_RES'] = data['WELG_RES'].where(
            data['WELG_STATUS'] == 'W2', np.nan)
        return data


def gen_wfdata(ff_size=(72, 24), num_params=3, code_qty=10):
    ff_shape = (8, 8)
    ring_offset = (4, 4)

    raw = pd.DataFrame(np.random.random(
        (ff_size[0]*ff_shape[0], ff_size[1]*ff_shape[1])))  # try other distribution
    all_ = raw.unstack().reset_index().rename(
        columns={'level_0': 'MAP_COL', 'level_1': 'MAP_ROW'})
    all_['MASK'] = all_.apply(lambda x: 1 if (x.MAP_COL-ff_size[1]*ff_shape[1]/2+0.5)**2/(ff_size[1]*ff_shape[1]/2+ring_offset[1])**2
                              + (x.MAP_ROW-ff_size[0]*ff_shape[0]/2+0.5)**2/(ff_size[0]*ff_shape[0]/2+ring_offset[0])**2 < 1 else np.nan, axis=1)
    all_['MAP_ROW'] = all_['MAP_ROW']+1
    all_.eval('MAP_COL=MAP_COL+1', inplace=True)
    mask = all_.dropna()[['MAP_ROW', 'MAP_COL']]
    mask = mask.assign(WIF_ROW=mask['MAP_ROW'] % ff_size[0], WIF_COL=mask['MAP_COL'] % ff_size[1],
                       FF_ROW=(mask['MAP_ROW']/ff_size[0]
                               ).apply(np.ceil).astype(int),
                       FF_COL=(mask['MAP_COL']/ff_size[1]).apply(np.ceil).astype(int))
    mask['WIF_ROW'] = mask['WIF_ROW'].replace({0: ff_size[0]})
    mask['WIF_COL'] = mask['WIF_COL'].replace({0: ff_size[1]})

    dummy_ff = [(1, 1), (1, 2), (1, 7), (1, 8), (2, 1), (2, 8),
                (7, 1), (7, 8), (8, 1), (8, 2), (8, 7), (8, 8)]
    mask['MASK'] = mask.apply(lambda x: 1 if (
        x.FF_ROW, x.FF_COL) not in dummy_ff else np.nan, axis=1)
    mask = mask.dropna()
    mask.index = np.arange(len(mask))
    df = pd.DataFrame(np.random.normal(size=(len(mask), num_params)), columns=[
                      f'S{i}' for i in range(1, num_params+1)])
    data = mask.merge(df, left_index=True, right_index=True)

    codes = []
    total = len(mask)
    arr = np.arange(1, 1+code_qty)
    np.random.shuffle(arr)
    for code in arr:
        codes += [code]*(total//2)
        total -= total//2
    codes += [arr[0]]*total
    data['X'] = ((data['MAP_COL']-data['MAP_COL'].max()/2) *
                 (data['MAP_ROW'].max()/data['MAP_COL'].max())).astype(int)
    data['Y'] = data['MAP_ROW']-data['MAP_ROW'].max()/2
    data['radius'] = np.sqrt(data['X'].to_numpy()**2+data['Y'].to_numpy()**2)
    data['t'] = np.arctan2(data['Y'].to_numpy(), data['X'].to_numpy())
    data = data.sort_values(['radius', 't'])
    data['CODE'] = list(map(lambda x: f'C{x}', codes))
    data.index = np.arange(len(data))
    return data.drop(['MASK', 'X', 'Y', 'radius', 't'], axis=1).sort_values(['MAP_ROW', 'MAP_COL'])


def merge_wfmap(df, ocr_col='SLIDER_OCR_NO', mode='AUTO', join='outer', inc_data=False, map_path=r'D:/Python'):
    assert mode in ['AUTO', 'UP', 'UP2', 'UP3', 'UP2E',
                    'UP3E'], print('Wafer Format Not Suppported!!')
    assert join in ['inner', 'outer'], print('Merge Method Not Suppported!!')

    df['Wafer'] = df[ocr_col].map(lambda x: x[:5])
    df['OCR'] = df[ocr_col].map(lambda x: x[-5:])
    df.set_index('OCR', inplace=True)
    result = []
    for wf, dff in df.groupby('Wafer'):
        if mode == 'AUTO':
            wf = "H"+wf
            if inc_data:
                map_data = Wafer(wf).inc_data()
            else:
                map_data = Wafer(wf).map_data()
        else:
            map_data = pd.read_pickle(f'{map_path}/{mode}')
        if 'BLOCK' in df.columns:
            df = df.drop('BLOCK', axis=1)
        merged = pd.merge(map_data, dff, right_index=True,
                          left_index=True, how=join)
        merged = merged.drop_duplicates(subset=['MAP_ROW', 'MAP_COL'])
        result.append(merged)
    return pd.concat(result)
