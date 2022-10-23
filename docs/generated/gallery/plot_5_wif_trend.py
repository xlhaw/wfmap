"""
WIF Trend
=================================
> Wafer Trend Charts by Flash Field For Single Variables

This example demonstrates how to import a local module and how images are
stacked when two plots are created in one code block. The variable ``N`` from
the example 'Local module' (file ``local_module.py``) is imported in the code
below. Further, note that when there is only one code block in an example, the
output appears before the code block.



# mkdocs_gallery_thumbnail_number = 2

# WIF Trend

Flash Field to flash field variation,

The Flash to flash variation is based

API All Input
"""

from wfmap.data import load_data
from wfmap import wif_trend

data = load_data()
fig = wif_trend(data, 'MR')
