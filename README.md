# WaferMap Visualization with Heatmap and Trend Charts

This package heavily depends upon **_matplotlib_** & **_seaborn_**. It provides simple wafer heatmap for numerical & categorical variables, as well as highly customized trend charts regarding to different wafer shot map definitions. You can built your own wafermap on the top of the API provided.

> This package only tested under Windows, the aesthetics of charts might be slightly different under Mac/Linux.

## Example Gallery

This gallery contains a selection of examples of the plots _**wfmap**_ can create. _Advanced Usages_ and _API Reference_ please refer to the [Online Docs](https://wfmap.ml) (WIP)

<img src="https://raw.githubusercontent.com/xlhaw/wfmap/master/docs/img/DefectMap.png" width="50%"></img> <img src="https://raw.githubusercontent.com/xlhaw/wfmap/master/docs/img/WaferMap.png" width="50%"></img> <img src="https://raw.githubusercontent.com/xlhaw/wfmap/master/docs/img/WIF_Trend.png" width="50%"></img> <img src="https://raw.githubusercontent.com/xlhaw/wfmap/master/docs/img/Twin_Trends.png" width="50%"></img> 

<img src="https://raw.githubusercontent.com/xlhaw/wfmap/master/docs/img/IncomingMap.png"></img> 


## Installation
To install _**wfmap**_ via PyPI using pip:

```bash
pip install wfmap
```

or build the latest release from Github:

```bash
git clone https://github.com/xlhaw/wfmap.git
cd wfmap
python setup.py install
```

## Basic Usage

Before you get started, please have a look at the definition used in this package for wafer mapping. You can modify the configuration to meet your requirement.

<img src="https://raw.githubusercontent.com/xlhaw/wfmap/master/docs/img/definition.png"></img>

Sample data is shipped with this packages, you can load it with the following snippet.
```python
from wfmap.data import load_data
data=load_data()
```


**BasePlot**

`num_heatmap` and `cat_heatmap` are core functions used to generate `matplotlib.axes`, dealing with numerical & categorical variables respectively. Remain functions provides in packages return `matplotlib.figure.Figure` instead.

```python
from wfmap import num_heatmap,cat_heatmap
fig,axs=plt.subplots(1,2,figsize=(8,3))
_=num_heatmap(data,'MRR',ax=axs[0])
_=cat_heatmap(data,'DEFECT',ax=axs[1])
#fig.savefig('BasePlot.png',dpi=200)
```

<img src="https://raw.githubusercontent.com/xlhaw/wfmap/master/docs/img/BasePlot.png"></img>

**WaferMap**
WaferMap is a customized plot for numerical variables built with `num_heatmap`, beside the basic heatmap, an horizontal distribution plot sits along with the colorbar. For full details please refer to the `API Reference`.
```python
from wfmap import wafermap
fig=wafermap(data,'HDI_R',wtype='UP3')
```

<img src="https://raw.githubusercontent.com/xlhaw/wfmap/master/docs/img/WaferMap.png"></img>


**DefectMap**
DefectMap is a customized plot for categorical variables using `cat_heatmap`, which put additional pareto histogram and pie chart aside. For full details please refer to the `API Reference`.
```python
from wfmap import defectmap
fig=defectmap(data,'DEFECT')
```
<img src="https://raw.githubusercontent.com/xlhaw/wfmap/master/docs/img/DefectMap.png"></img>




## License

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fxlhaw%2Fwfmap.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fxlhaw%2Fwfmap?ref=badge_large)