"""
WIF Trend `wif_trend`
=================================
> Wafer Trend Charts by Flash Field For Single Variable

WIF Trend gives you a clear view of within flash field & field to field tendency and distribution. Anormal waving or mountain shape pattern and shot-jump pattern could be easily spotted with this chart.
Blue line is median trend by default which is less impacted by outliers, and orange area indicates the major distribution at the same `WIF_COL`.

"""

from wfmap.data import load_data
from wfmap import wif_trend

data = load_data()
fig = wif_trend(data, 'MR')

# %%
# The size of orange area is determined by `majority`, which means the center percentage of the whole distribution. To achieve similar quantile as boxplot could set `majority=50`.


fig2 = wif_trend(data, 'MR', majority=50)
