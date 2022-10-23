"""
TwinY Trends
=================================
> Wafer Trend Charts by Flash Field For Very Different Two Variables

This example demonstrates how to import a local module and how images are
stacked when two plots are created in one code block. The variable ``N`` from
the example 'Local module' (file ``local_module.py``) is imported in the code
below. Further, note that when there is only one code block in an example, the
output appears before the code block.

_R can see the correlation between two variables more clear

"""

from wfmap.data import load_data
from wfmap import twin_trends

data = load_data()
fig = twin_trends(data, 'MR', 'HDI', keep_rng=False)


"""
# Twin Trends

Some time it's . It's slightly different than put, it put the in secondary axis, some the two variables are have bigger gap or b.

Take the Resistance of STO for example, before the OSR Wafer level rest is and while the STO_R(STO Resistance After Lapping)

Comparat to or put ba in the same y-axis, more,

With Different Hw and HDI_R can see the correlation between two variables more clear

"""
