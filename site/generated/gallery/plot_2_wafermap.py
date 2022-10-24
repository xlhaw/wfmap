"""
WaferMap `wafermap`
=================================
> WaferMap with Distribution & Median Trend Subplots

WaferMap add additional color distribution plot and trend charts by row/col around basic NumHeatmap.Color distribution plot shares the same limit as colorbar from heatmap. And vertical and horizonal trend charts is only diplayed when `wftype` is provided, since the grid line are using the pre-defined flash field boundary by `wftype`.

"""

from wfmap.data import load_data
from wfmap import wafermap

data = load_data()
fig = wafermap(data, 'MR', wftype='UP3')
