"""
WIF Trends `wif_trends`
=================================
> Wafer Trend Charts by Flash Field For Multiple Variables

Slightly different from `wif_trend`, WIF Trends removes the orange area highlight for major distribution and focus on the median trend comparison between different variables. Further, for the sake of brevity and aesthetics, max number of variables to plot is limited to 4.

Below is an example trend chart of the wafer level MR Resistence for both R1 & R2. Please be noted this chart is only recommended for variables which share similar range. When the mean or sigma is much different, please consider using the `twin_trends` instead.

"""

from wfmap.data import load_data
from wfmap import wif_trends

data = load_data()
fig = wif_trends(data, ['MR', 'MR2'])
