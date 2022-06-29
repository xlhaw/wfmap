
__version_info__ = ('1', '0', '2', 'dev')
__date__ = '29 June 2022'
__version__ = '.'.join(__version_info__)
__author__ = 'Leon Xiao'
__contact__ = 'i@xlhaw.com'
__homepage__ = 'https://github.com/xlhaw/wfmap'

import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

__all__ = ['num_heatmap', 'cat_heatmap', 'create_incmap',
           'wafermap', 'defectmap', 'wif_trend', 'wif_trends', 'twin_trends']

plt.style.use('ggplot')
TAB10_COLOR = plt.cm.tab10.colors
DEFECT_COLORS = ['lightgreen', 'red', 'orange', 'blue', 'purple', 'cyan',
                 'pink', 'yellow', 'lightblue', 'gold', 'darkblue', 'gray', 'darkred', 'black']
FF_BOUNDARY = {'UP': ([17, 41, 65, 89, 113, 137, 161], [76, 160, 244, 328, 412, 482]),
               'UP2': ([19, 43, 67, 91, 115, 139, 163], [50, 118, 186, 254, 322, 390, 458]),
               'UP3': ([18, 42, 66, 90, 114, 138, 162], [38, 116, 194, 272, 350, 428, 506]),
               'UP2E': (),
               'UP3E': (),
               }


def base_axe(plot_fn):
    """
    Decorator to create default axe if not provided
    """
    import functools

    @functools.wraps(plot_fn)
    def wrapped(*args, **kwargs):
        ax = kwargs.get("ax", None)
        figsize = kwargs.get("figsize", (8, 6))
        if not ax:
            ax = plt.figure(figsize=figsize).gca()
        kwargs = {**kwargs, **{'ax': ax}}
        return plot_fn(*args, **kwargs)
    return wrapped


def auto_vlim(series, majority=94, n_sigma=3, vsigma=None, vrange=None):
    """
    Infer the best range of a series for plotting
    """
    low, high = np.percentile(series.dropna(), [50-majority/2, 50+majority/2])
    centers = series.where((series >= low) & (series <= high), np.nan)
    if vsigma == None:
        vsigma = centers.std()
    if vrange:
        vmin = (low+high-vrange)/2
        vmax = (low+high+vrange)/2
    else:
        vmax = centers.mean()+n_sigma*vsigma
        vmin = centers.mean()-n_sigma*vsigma
    return vmin, vmax


@base_axe
def num_heatmap(df, value, row='MAP_ROW', col='MAP_COL', cmap='jet', title=None, vlim=None, vsigma=None,  vrange=None, ax=None):
    """Create Wafer Heatmap for Numerical Variable

    Args:
        df (pd.DataFrame): Wafer Data
        value (str): Column name of the numeric variable
        row (str, optional): Wafer Map Row (Y Coordinate)
        col (str, optional): Wafer Map Col (X Coordinate)
        cmap (str, optional): ColorMap
        title (str, optional): Title
        vlim (tuple, optional): (zmin,zmax) limits of the colorbar, will ignore the vsigma/vrange if provided
        zsigma (float, optional): colorbar range is median±3*vsigma if vsigma is provided    
        vrange (float, optional): Range of the colorbar, works when vlim is not available and ignore the zsigma
        ax (matplotlib.axes, optional): Axe to plot on

    Returns:
       ax (matplotlib.axes):  Matplotlib Axes
    """
    vlim = auto_vlim(df[value], vrange=vrange,
                     vsigma=vsigma) if vlim == None else vlim
    sb.heatmap(df.pivot(row, col, value), cmap=cmap,
               vmin=vlim[0], vmax=vlim[1], robust=True, ax=ax)
    ax.set_axis_off()
    ax.set_title(title) if title != None else None
    return ax


@base_axe
def cat_heatmap(df, item, row='MAP_ROW', col='MAP_COL', title=None, code_dict=None,
                qty_limit=10, colors=DEFECT_COLORS, verbose=False, ax=None):
    """Create Wafer Heatmap for Categorical Variable

    Args:
        df (pd.DataFrame): Wafer Data
        item (str): Column name of the categorical variable
        row (str, optional): Wafer Map Row (Y Coordinate)
        col (str, optional): Wafer Map Col (X Coordinate)
        title (str, optional): Title
        code_dict (dict, optional): {'orignal':'new_code'} Replace original code with code_dict
        qty_limit (int, optional): add restrictions on the total unique variables to plot
        colors (list, optional): ['lightgreen', 'red', 'orange', 'blue', 'purple', 'cyan', 'pink', 'yellow', 'lightblue', 'gold', 'darkblue', 'gray', 'darkred', 'black']
        verbose (bool, optional): Return the summary of categorical data or not.
        ax (matplotlib.axes, optional): Axe to plot on

    Returns:
        ax (matplotlib.axes):  Matplotlib Axes and additional data if verbose is True
    """
    counts, labels, cat2num = _cat_counts(
        df, item, qty_limit=qty_limit, code_dict=code_dict)
    colors = colors[:len(labels)]
    cmap = mcolors.ListedColormap(colors)
    boundaries = np.arange(len(labels))
    param = min(qty_limit, len(labels))
    ticks = np.linspace(boundaries[0]+0.25*param**0.25,
                        boundaries[-1]-0.25*param**0.25, len(boundaries))
    _ = mcolors.BoundaryNorm(boundaries, cmap.N, clip=True)
    vmin = boundaries[0]
    vmax = boundaries[-1]
    df[f'{item}_'] = df[item].replace(cat2num)
    sb.heatmap(df.pivot(row, col, f'{item}_'),
               cmap=cmap, vmin=vmin, vmax=vmax, ax=ax)
    colorbar = ax.collections[0].colorbar
    colorbar.set_ticks(ticks)
    colorbar.set_ticklabels(labels)
    ax.set_axis_off()
    ax.set_title(title) if title != None else None
    if verbose:
        return ax, counts, labels, cat2num
    else:
        return ax


@base_axe
def _color_distplot(df, value, vertical=False, n_bin=60, vlim=None, vrange=None, ax=None):
    """
    Distribution plot for continous variable
    """
    orient = 'vertical' if vertical else 'horizontal'
    vlim = auto_vlim(df[value], vrange=vrange) if vlim == None else vlim
    _, bins, patches = ax.hist(df[value].dropna(), bins=np.linspace(
        vlim[0], vlim[1], n_bin), orientation=orient)
    norm = mcolors.Normalize(vmin=vlim[0], vmax=vlim[1])
    for xbin, patch in zip(bins, patches):
        color = plt.cm.jet(norm(xbin))
        patch.set_facecolor(color)
    ax.set_axis_off()
    ax.set_xlim(vlim) if vertical else ax.set_ylim(vlim)
    return ax


@base_axe
def _color_barplot(counts, colors, annotate=True, ax=None, title=None):
    '''
    Distribution plot for discrete variable
    '''
    labels = list(counts.index)
    axins = inset_axes(ax, width="90%", height='60%', bbox_to_anchor=(
        0.4, 0.5, 0.8, 0.5), bbox_transform=ax.transAxes, borderpad=0)  # [left, bottom, width, height]
    explode = np.linspace(0, 0.42, len(labels))
    axins.pie(counts, explode=explode, startangle=180, colors=colors)
    ax.barh(counts.index[1:len(labels)],
            counts[1:len(labels)], color=colors[1:len(labels)])
    _, xmax = ax.get_xlim()
    if annotate:
        for idx, patch in enumerate(ax.patches):
            ratio = counts.iloc[idx+1]/counts.sum()
            x, y = patch.get_xy()
            height = patch.get_height()
            ax.text(x-xmax/6, y+height/4, f'{ratio:.2%}', rotation=45)
    remark = counts.index[0]+':  {:.1%}'.format(counts.iloc[0]/counts.sum())
    ax.text(0.45, 0.75, remark, transform=ax.transAxes)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.yaxis.set_visible(False)
    # ax.set_xlabel('Qty')
    ax.set_ylim(-1.5, len(labels)-1.5)
    ax.set_facecolor('white')
    ax.set_title(title) if title != None else None
    return ax


def _cat_counts(df, item, qty_limit=10, code_dict=None):
    """
    Faciliate the tranformation of the categorical variable to numerals for plotting
    """
    if code_dict:
        df[item] = df[item].replace(code_dict)
    counts = df[item].dropna().value_counts()
    unique_qty = len(counts)
    labels = list(counts.index)
    nums = list(range(unique_qty))
    cat2num = dict(zip(counts.index, nums))
    if unique_qty <= qty_limit:
        return counts, labels, cat2num
    else:
        other_qty = 0
        for i in range(unique_qty-qty_limit):
            other_qty += counts.iloc[-i-1]
            cat2num[labels[-i-1]] = qty_limit-1
        counts = counts[:qty_limit -
                        1].append(pd.Series(data=[other_qty], index=['Others']))
        return counts, list(counts.index), cat2num


def create_incmap(df, vsigmas={'ELG_RES': 0.2, 'WELG_RES': 0.2, 'MR': 10, 'PCM': 5, 'OSR': 1}, title=None):
    """Create Combined Wafermaps with Incoming Data

    Args:
        df (pd.DataFrame): Wafer Data
        sigmas (dict, optional): {'item': float} Preset sigmas for vrange estimation
        title (str, optional): Title

    Returns:
        fig (matplotlib.figure.Figure):  Figure
    """
    qty = len(vsigmas)
    fig = plt.figure(figsize=(4*qty+2, 3.5))
    gs = fig.add_gridspec(1, qty*2, width_ratios=[10, 2]*qty)
    idx = 0
    for item in vsigmas:
        ax1 = plt.subplot(gs[idx])
        ax2 = plt.subplot(gs[idx+1])
        if df[item].notnull().sum() > 0:
            num_heatmap(df, item, ax=ax1, title=item, vsigma=vsigmas[item])
            _color_distplot(df, item, vlim=auto_vlim(
                df[item], vsigma=vsigmas[item]), ax=ax2)
        else:
            ax1.set_title(item)
        idx += 2
    plt.tight_layout()
    if title:
        plt.suptitle(title, x=0.36, fontsize=18)
        plt.subplots_adjust(top=0.90)
    return fig


def wafermap(df, value, row='MAP_ROW', col='MAP_COL', title=None, vrange=None, vsigma=None, wftype=None):
    """Create Wafer Heatmap

    Args:
        df (pd.DataFrame): Wafer Data
        value (str): Column name of the numeric variable
        row (str, optional): Wafer Map Row (Y Coordinate)
        col (str, optional): Wafer Map Col (X Coordinate)
        title (str, optional): Title
        vrange (float, optional):  Range of Y-axis
        vsigma (float, optional): color bar range is median±3*vsigma if vsigma is provided
        wftype (str, optional): _Wafer Layout Type_, Plot additional trend chart if provided

    Returns:
        fig (matplotlib.figure.Figure):  Figure
    """
    fig = plt.figure(figsize=(14, 10))
    gs = fig.add_gridspec(2, 4, width_ratios=[
                          2, 8, 1.9, 2.1], height_ratios=[8, 2])
    hmap = plt.subplot(gs[0, 1:3])
    vbar = plt.subplot(gs[0, 3])
    vlim = auto_vlim(df[value], vrange=vrange, vsigma=vsigma)
    num_heatmap(df, value, ax=hmap, vlim=vlim)
    _color_distplot(df, value, ax=vbar, vlim=vlim)
    if wftype:
        vtrend = plt.subplot(gs[0, 0])
        htrend = plt.subplot(gs[1, 1])
        row_m = df.groupby(row).agg('median').reset_index()
        col_m = df.groupby(col).agg('median').reset_index()
        sb.scatterplot(data=row_m, x=value, y=row, ax=vtrend)
        sb.scatterplot(data=col_m, x=col, y=value, ax=htrend)
        htrend.set_xlim(df[col].min(), df[col].max())
        htrend.yaxis.set_label_position("right")
        htrend.yaxis.tick_right()
        vtrend.set_ylim(df[row].max(), df[row].min())
        h_boundary, v_boundary = FF_BOUNDARY.get(wftype)
        htrend.set_xticks(h_boundary)
        vtrend.set_yticks(v_boundary)
        htrend.set_ylim(vlim)
        vtrend.set_xlim(vlim)
        htrend.grid(axis='x', linestyle='--')
        vtrend.grid(axis='y', linestyle='--')
    plt.subplots_adjust(hspace=0.01, wspace=0.02, top=0.95)
    if title:
        plt.suptitle(title, fontsize=18)
    return fig


def defectmap(df, defect_col, ok_codes=['OK', 'BINA'], row='MAP_ROW', col='MAP_COL', qty_limit=10, colors=DEFECT_COLORS, title=None):
    """Create Wafer DefectMap

    Args:
        df (pd.DataFrame): Wafer Data
        defect_col (str): Column name of the defect code
        ok_codes (list, optional): list of code being treated as 'OK'
        row (str, optional): Wafer Map Row (Y Coordinate)
        col (str, optional): Wafer Map Col (X Coordinate)
        qty_limit (int, optional): add restrictions on the total unique variables to show in the plot
        colors (list, optional): ['lightgreen', 'red', 'orange', 'blue', 'purple', 'cyan', 'pink', 'yellow', 'lightblue', 'gold', 'darkblue', 'gray', 'darkred', 'black']
        title (str, optional): Title

    Returns:
        fig (matplotlib.figure.Figure):  Figure
    """
    df[defect_col] = df[defect_col].astype(str)
    code_dict = {code: 'OK' for code in ok_codes}

    fig = plt.figure(figsize=(10, 8))
    gs = fig.add_gridspec(1, 2, width_ratios=[10, 2])
    ax1 = plt.subplot(gs[0])
    ax2 = plt.subplot(gs[1])

    _, counts, labels, _ = cat_heatmap(
        df, defect_col, qty_limit=qty_limit, code_dict=code_dict, ax=ax1, verbose=True)
    _color_barplot(counts, colors[:len(labels)], ax=ax2)

    plt.tight_layout()
    title = defect_col if not title else title
    plt.suptitle(title, x=0.52, fontsize=18)
    plt.subplots_adjust(top=0.92, wspace=0)
    return fig


def _new_wafer_fig(wftype, ff_shape={'UP': (6, 8), 'UP2': (8, 8), 'UP3': (8, 8), 'UP2E': (12, 10), 'UP3E': (12, 10)}):
    """
    Create Figure and Gridspec
    """
    fig = plt.figure(figsize=(7, 7))
    row, col = ff_shape.get(wftype, (8, 8))
    gs = fig.add_gridspec(row, col)
    return fig, gs


def _base_trend(df, y, fig, gs, ty=None, color=None, tcolor=None,
                x='WIF_COL', xn='FF_COL', yn='FF_ROW', method='median', style='.'):
    """
    Create Trend Charts by Flash Field
    """
    axes = {}
    for (row, col), ff in df.groupby([yn, xn]):
        ax = plt.subplot(gs[int(row-1), int(col-1)])
        # ax.text(0.05,0.85,f'FF{int(row)}{int(col)}',transform=ax.transAxes,fontsize=7) #optional
        if len(ff.dropna(subset=[y])) > 2:
            ytrend = ff.groupby(x).agg(method)[y]
            ytrend.plot(ax=ax, style=style, color=color, label=y, legend=None)
        else:
            ax.plot()
        if ty:
            axt = ax.twinx()
            tytrend = ff.groupby(x).agg(method)[ty]
            if abs(tytrend.mean()) >= 0:
                tytrend.plot(ax=axt, style=style, color=tcolor,
                             label=ty, legend=None)
            axes[(row, col)] = (ax, axt)
        else:
            axes[(row, col)] = (ax, None)
    return axes


def _tweak_trend(axes, n=2, x='WIF_COL', yn='FF_ROW', xn='FF_COL', xlim=(0, 24),
                 xticks=[8, 16], ylim=None, tylim=None, twin=False, title=None):
    """
    Tweak Subplots for Trend Charts
    """
    max_row = sorted(axes, key=lambda x: x[0])[-1][0]
    max_col = sorted(axes, key=lambda x: x[1])[-1][-1]
    for (row, col), (ax, axt) in axes.items():
        ax.set_xlim(xlim)
        ax.set_xlabel(None)
        if ylim:
            ax.set_ylim(ylim)
        if col != 1:
            ax.yaxis.set_visible(False)
        else:
            _ = [tick.set_rotation(0)for tick in ax.get_yticklabels()]
        if row != max_row:
            ax.xaxis.set_visible(False)
        else:
            ax.set_xticks(xticks)
        if twin:
            if col != max_col:
                axt.yaxis.set_visible(False)
            else:
                _ = [tick.set_rotation(0)for tick in axt.get_yticklabels()]
            if tylim:
                axt.set_ylim(tylim)
            axt.grid(False)
        ax.grid(False)
    plt.tight_layout()
    ax = axes[(max_row, max_col//2)][0]
    ax.text(0.5, -0.5, x, transform=ax.transAxes)
    ax = axes[(1, max_col-2)][0]
    handles, labels = _get_legend(axes)
    ax.legend(handles, labels, bbox_to_anchor=(1, 1), facecolor='white',
              loc=2, borderaxespad=0., fontsize=12)
    plt.suptitle(title) if title != None else None
    plt.subplots_adjust(hspace=0, wspace=0, top=0.95, bottom=0.08)


def _get_legend(axes):
    """
    Processing handles and labels for new legend
    """
    n_label = 0
    n_tlabel = 0
    for _, (ax, axt) in axes.items():
        h, l = ax.get_legend_handles_labels()
        if len(l) > n_label:
            handles, labels = h, l
            n_label = len(labels)
        if axt != None:
            th, tl = axt.get_legend_handles_labels()
            if len(tl) > n_tlabel:
                t_handles, t_labels = th, tl
                n_tlabel = len(t_labels)
    if n_tlabel > 0:
        handles += t_handles
        labels = [f'Y: {l}' for l in labels]+[f't-Y: {l}' for l in t_labels]
    return handles, labels


def wif_trend(df, y, x='WIF_COL', yn='FF_ROW', xn='FF_COL', wftype='UP2',
              method='median', title=None, ylim=None, yrange=None, color='b', style='.'):
    """Create Wafer Trend Chart by Flash Field

    Args:
        df (pd.DataFrame): Wafer Data
        y (str): Column name of the numeric variable to plot
        x (str, optional): Column name(and x_label) of x-axis
        yn (str, optional): Y Coordinate of Flash Field/Subplot
        xn (str, optional): X Coordinate of Flash Field/Subplot
        wftype (str, optional): _Wafer Layout Type_  ['UP'|'UP2'|'UP3'|'UP2E'|'UP3E']       
        method (str, optional): 'mean' or 'median' Trend
        title (str, optional): Title
        ylim (tuple, optional): (ymin:float,ymax:float)        
        yrange (float, optional):  Range of Y-axis, ignored if ylim is provided
        color (str, optional): Color of the trend line
        style (str, optional): Style of the trend line

    Returns:
        fig (matplotlib.figure.Figure):  Figure
    """
    fig, gs = _new_wafer_fig(wftype)
    if ylim == None:
        ylim = auto_vlim(df[y], vrange=yrange)
    axes = _base_trend(df, y, fig, gs, method=method,
                       color=color, style=style)

    def quantile(df, y, quantile=0.5):
        return np.quantile(df[y].dropna(), quantile) if len(df[y].dropna()) >= 1 else np.nan

    for (row, col), (ax, _) in axes.items():
        # df.query(f'{xn}=={col} and {yn}=={row}')
        ff = df[(df[xn] == col) & (df[yn] == row)]
        if len(ff.dropna(subset=[y])) > 2:
            q1 = ff.groupby(x).apply(quantile, y, 0.25)
            q3 = ff.groupby(x).apply(quantile, y, 0.75)
            quantiles = pd.concat([q1, q3], axis=1).reset_index()
            ax.fill_between(quantiles.iloc[:, 0],
                            quantiles.iloc[:, 1],
                            quantiles.iloc[:, 2],
                            color='orange', alpha=0.5)

    _tweak_trend(axes, ylim=ylim, title=title)
    return fig


def wif_trends(df, ys, x='WIF_COL', yn='FF_ROW', xn='FF_COL', wftype='UP2',
               method='median', title=None, ylim=None, yrange=None):
    """Create Wafer Trend Charts by Flash Field (when numerical variables share similar ranges)
    Args:
        df (pd.DataFrame): Wafer Data
        ys (list): List of column names to plot
        x (str, optional): Column name(and x_label) of x-axis
        yn (str, optional): Y Coordinate of Flash Field/Subplot
        xn (str, optional): X Coordinate of Flash Field/Subplot
        wftype (str, optional): _Wafer Layout Type_  ['UP'|'UP2'|'UP3'|'UP2E'|'UP3E']        
        method (str, optional): 'mean' or 'median' Trend
        title (str, optional): Title
        ylim (tuple, optional): (ymin:float,ymax:float)        
        yrange (float, optional):  Range of Y-axis, ignored if ylim is provided

    Returns:
        fig (matplotlib.figure.Figure):  Figure
    """
    fig, gs = _new_wafer_fig(wftype)
    for i, y in enumerate(ys):
        axes = _base_trend(df, y, fig, gs,
                           color=TAB10_COLOR[i], method=method)
    if ylim == None:
        ylim = auto_vlim(df[ys].stack(), vrange=yrange)
    _tweak_trend(axes, ylim=ylim, title=title)
    return fig


def twin_trends(df, y, ty, x='WIF_COL', yn='FF_ROW', xn='FF_COL', wftype='UP2',
                method='median', title=None, yrange=None, tyrange=None, keep_rng=True):
    """Create Wafer Trend Charts by Flash Field (when two variables have very different ranges)

    Args:
        df (pd.DataFrame): Wafer Data
        y (str):  Column name of the variable to plot on the primary axis
        ty (str): Column name of the variable to plot on the secondary axis
        x (str, optional): Column name(and x_label) of x-axis
        yn (str, optional): Y Coordinate of Flash Field/Subplot
        xn (str, optional): X Coordinate of Flash Field/Subplot
        wftype (str, optional): _Wafer Layout Type_  ['UP'|'UP2'|'UP3'|'UP2E'|'UP3E']    
        method (str, optional): 'mean' or 'median' Trend
        title (str, optional): Title
        yrange (float, optional):  Range of Y-axis
        tyrange (float, optional): Range of 2nd Y-axis
        keep_rng (bool, optional):  Keep the same range or Not

    Returns:
        fig (matplotlib.figure.Figure):  Figure
    """
    fig, gs = _new_wafer_fig(wftype)
    ymin, ymax = auto_vlim(df[y], vrange=yrange)
    tymin, tymax = auto_vlim(df[ty], vrange=tyrange)
    if keep_rng and not all([yrange, tyrange]):
        range_delta = (ymax-ymin)-(tymax-tymin)
        if range_delta >= 0:
            tymin -= range_delta/2
            tymax += range_delta/2
        else:
            ymin += range_delta/2
            ymax -= range_delta/2
    axes = _base_trend(df, y, fig, gs, ty=ty,
                       color=TAB10_COLOR[0], tcolor=TAB10_COLOR[1], method=method)
    _tweak_trend(axes, ylim=(ymin, ymax), tylim=(
        tymin, tymax), twin=True, title=title)
    return fig
