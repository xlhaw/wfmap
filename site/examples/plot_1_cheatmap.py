"""
Categorical Heatmap `cat_heatmap`
=================================
> WaferMap for Categorical Variable

`cat_heatmap` is essentially a variant of `num_heatmap`. Internally, the categorical variable is  first transformed to integers according to the rank of each unique count. And then plot the heatmap using the intermediate numbers.

Below example demonstrates the simplest case of creating a categorical heatmap. You can have more customization by providing `code_dict` if you want to have some transformation before the plotting, eg. merge some items or change perticular item name. You can also set the `qty_limit` to control the max items will be presented in the plot, categories which are beyond the `qty_limit` will be counted together as `Others`.

"""

from wfmap.data import load_data
from wfmap import cat_heatmap

data = load_data()
fig = cat_heatmap(data, 'DEFECT')
