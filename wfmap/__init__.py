"""
Plot numerical and categorical wafer heatmaps customized with *matplotlib* and *seaborn*.
Wafer data built in the form of Pandas DataFrame, [MAP_COL,MAP_ROW] as default x,y coordinates for mapping.

Author: Leon Xiao

"""

__version_info__ = ('0', '0', '7', 'dev')
__date__ = '14 Feb 2020'
__version__ = '.'.join(__version_info__)
__author__ = 'Leon Xiao'
__contact__ = 'i@xlhaw.com'
__homepage__ = 'https://github.com/xlhaw/wfmap'


import seaborn as sb,matplotlib,matplotlib.pyplot as plt,numpy as np,pandas as pd
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

def wafermap(data,value,row='MAP_ROW',col='MAP_COL',code_dict=None,title=None,limit=14,**kwargs): #**arg as spec
    '''
    Args
    -------
    data : pandas.DataFrame
        data for the plot.
    value: string
        value column
    row,col: string
        x,y coordinate column
    title: string
        title for the plot
    limit: int
        maximal category/color number for the plot
    kwargs : other keyword arguments
        All other keyword arguments are passed to matplotlib `ax.pcolormesh`.

    Returns
    -------
    fig : matplotlib Figure
        Figure object with the wafer heatmap.
        
    '''
    df=data.copy()
    fig=plt.figure()
    gs=fig.add_gridspec(1, 2, width_ratios=[10,2])
    ax1=plt.subplot(gs[0])
    ax2=plt.subplot(gs[1])

    if df[value].dtype=='O':
        counts=df[value].value_counts()
        if not code_dict:
            code_dict,labels=category2num(counts,limit=limit)
            df[value]=df[value].replace(code_dict) #14 blocks
        else:
            labels=list(code_dict.keys())

        # Customize dicrete heatmap
        colors=['lightgreen','red','orange', 'purple','cyan', 'pink', 'yellow', 'blue', 'lightblue','green','darkblue','gray','darkred','black']
        color=colors[:len(labels)]
        cmap=matplotlib.colors.ListedColormap(color)
        boundaries =np.arange(len(labels))
        ticks=np.linspace(boundaries[0]+0.5,boundaries[-1]-0.5,len(boundaries))
        norm = matplotlib.colors.BoundaryNorm(boundaries, cmap.N, clip=True)
        vmin=boundaries[0]
        vmax=boundaries[-1]
        sb.heatmap(df.pivot(row,col,value),cmap=cmap,vmin=vmin,vmax=vmax,ax=ax1)
        colorbar = ax1.collections[0].colorbar
        colorbar.set_ticks(ticks)
        colorbar.set_ticklabels(labels)

        # Add pie chart inset
        axins=inset_axes(ax1,width='90%',height='40%',bbox_to_anchor=(1.18,0.5,0.5,0.5),bbox_transform=ax1.transAxes,borderpad=0)
        explode=np.linspace(0,0.42,len(labels))
        axins.pie(counts[:len(labels)],explode=explode,startangle=180,colors=color)
        #axins.pie(counts,labels=counts.index,explode=explode,autopct='%1.1f%%',startangle=180)

        # Add histogram but exclude the most frequent category
        #ax2.barh(counts.index,counts,log=True,color=colors[:len(labels)])
        ax2.barh(counts.index[1:len(labels)],counts[1:len(labels)],color=colors[1:len(labels)])
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.yaxis.set_visible(False)
        ax2.spines['left'].set_visible(False)

    elif df[value].dtype in ['int','float','int64','float64','float32','float16']: 

        # Customize continuous heatmap
        p10,p90=np.percentile(df[value].dropna(),[10,90])
        majority=df[value].where((df[value]>=p10)&(df[value]<=p90),np.nan)
        #vmax=mean+4sigma@(80%population),vmin= mean-4sigma @(80%population)
        vmax=majority.mean()+4*majority.std()
        vmin=majority.mean()-4*majority.std()
        sb.heatmap(data.pivot(row,col,value),cmap='jet',vmin=vmin,vmax=vmax,robust=True,ax=ax1) #use data instead of df

        # avoid the impact of outlier to the histogram plot
        df[value]=df[value].where(df[value]>=vmin,vmin-majority.std())
        df[value]=df[value].where(df[value]<=vmax,vmax+majority.std())

        # Customize histogram with colorbar fillin
        N, bins, patches = ax2.hist(df[value].dropna(), bins=120,orientation='horizontal')
        norm = matplotlib.colors.Normalize(vmin=vmin,vmax=vmax)
        for xbin, patch in zip(bins, patches):
            color = matplotlib.cm.jet(norm(xbin))
            patch.set_facecolor(color)
        ax2.set_ylim(vmin,vmax) #ValueError: Axis limits cannot be NaN or Inf
        ax2.set_axis_off()

    else:
         print('Data Format Not Supported!')
         return 
    
    ax1.set_axis_off()
    plt.tight_layout()
    title=value if not title else title
    plt.suptitle(value,x=0.52)
    plt.subplots_adjust(top=0.92,wspace=0)
    #plt.savefig(title+'.jpg')
    return fig

def category2num(counts,limit=10): # columns rank
    '''
    Args
    -------
    counts(pd.Series): unique value count 
    limit (int):  category qty upper limit
    
    Returns
    -------
    code_dict(dict): convert value count to dict{label(string): code(int)}
    labels(list):  labels of top 10 categories, 'Others' for minor categories
    
    '''
    labels=list(counts.index)
    boundaries = np.arange(limit)
    code_dict={}
    indx=0
    for i,j in counts.items():
        code_dict[i]=boundaries[-1] if indx > limit-1 else boundaries[indx]
        indx+=1
    if len(labels)<limit:
        boundaries=boundaries[:len(labels)]
    else:
        labels=labels[:limit]
        labels[-1]='Others'
    return code_dict,labels
