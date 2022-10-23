"""
WaferMap
=================================
> Wafer Trend Charts by Flash Field For Very Different Two Variables

WaferMap uses hot color(red) presents high value and cold value(blue) presents low value.

uses hot/cold colors to the distribution and uniformity of

nstrates how to import a local module and how images are
stacked when two plots are created in one code block. The variable ``N`` from
the example 'Local module' (file ``local_module.py``) is imported in the code
below. Further, note that when there is only one code block in an example, the
output appears before the code block.
"""

from wfmap.data import load_data
from wfmap import wafermap

data = load_data()
fig = wafermap(data, 'MR', wftype='UP3')
