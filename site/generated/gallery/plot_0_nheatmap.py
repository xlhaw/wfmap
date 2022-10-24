"""
Numerical Heatmap `num_heatmap`
=================================
> WaferMap for Numerical Variable

`num_heatmap` uses the colormap `jet` which present high value with hot color(red) and low value with cold value(blue). This example demonstrates how to use the sample data to create simple WaferMap at ease.  `MAP_ROW` & `MAP_COL` are the default value for wafer `row` & `col`, need be replaced if it's different from your data.

"""

import numpy as np
from wfmap.data import load_data
from wfmap import num_heatmap
import matplotlib.pyplot as plt

data = load_data()
ax = num_heatmap(data, 'MR')
plt.tight_layout()


# %%
# Usually, the range of colorbar is auto inferred by majority of center population, which suggests the range might not be consistent for the same parameter by different wafers. If you want to have more subtle colorbar control, you can provide the est.sigma of value `vsigma` or value range `vrange` to keep the colorbar to have a fixed range.


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
