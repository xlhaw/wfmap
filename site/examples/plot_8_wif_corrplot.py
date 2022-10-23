"""
WIF Corrrelation Plot `wif_corrplot`
=================================
> Corrrelation Plot by Flash Field Between Two Variables

`wif_corrplot` is created to further investigate relationship between two variables. Beside the basic scatterplot, regression fitting line and R_squared annotation are both included.

"""

from wfmap.data import load_data
from wfmap import wif_corrplot
import scipy.stats.distributions as dist

data = load_data().query('80<MR<180')
norm = dist.norm_gen()

data['Fit'] = data['MR'] + \
    norm.rvs(data['MR'].median(), data['MR'].std(), size=len(data['MR']))
fig = wif_corrplot(data, 'MR', 'Fit')
# %%
# Linear regression is applied by default, while polynomial fit is also supported, modify the `fit_deg` to see the outcome.


data['Fit2'] = (data['MR']-data['MR'].median())**2 + data['MR'] * \
    norm.rvs(data['MR'].median(), data['MR'].std(), size=len(data['MR']))
fig2 = wif_corrplot(data, 'MR', 'Fit2', fit_deg=2)
