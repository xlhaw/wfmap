"""
IncomingMap 
=================================
> Combined WaferMap for Wafer Incoming Data

IncomingMap is an horizontal concatenation of multiple WaferMap for wafer incoming data. `vsigmas` is a `dict` which collects the estimated value sigma for heatmap/colorbar range determination. Items which only lists in the `vsigmas` will be plotted. You can adjust the `vsigmas` &  `title` to customize your own wafermap combination.

Below is a simple IncomingMap which contains two variables `MR` & `HDI` only.

"""

from wfmap.data import load_data
from wfmap import create_incmap

data = load_data()
fig = create_incmap(data, vsigmas={'MR': 10, 'HDI': 1})
