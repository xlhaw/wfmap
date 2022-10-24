
<!--
 DO NOT EDIT.
 THIS FILE WAS AUTOMATICALLY GENERATED BY mkdocs-gallery.
 TO MAKE CHANGES, EDIT THE SOURCE PYTHON FILE:
 "docs/examples/plot_4_incmap.py"
 LINE NUMBERS ARE GIVEN BELOW.
-->

!!! note

    Click [here](#download_links)
    to download the full example code


IncomingMap 
=================================
> Combined WaferMap for Wafer Incoming Data

IncomingMap is an horizontal concatenation of multiple WaferMap for wafer incoming data. `vsigmas` is a `dict` which collects the estimated value sigma for heatmap/colorbar range determination. Items which only lists in the `vsigmas` will be plotted. You can adjust the `vsigmas` &  `title` to customize your own wafermap combination.

Below is a simple IncomingMap which contains two variables `MR` & `HDI` only.

<!-- GENERATED FROM PYTHON SOURCE LINES 11-17 -->


![MR, HDI](./images/mkd_glr_plot_4_incmap_001.png){: .mkd-glr-single-img srcset="../images/mkd_glr_plot_4_incmap_001.png"}

Out:
{: .mkd-glr-script-out }

```{.shell .mkd-glr-script-out-disp }
E:\zwPython\py37\python-3.7.4.amd64\lib\site-packages\seaborn\matrix.py:70: DeprecationWarning: `np.bool` is a deprecated alias for the builtin `bool`. To silence this warning, use `bool` by itself. Doing this will not modify any behavior and is safe. If you specifically wanted the numpy scalar type, use `np.bool_` here.
Deprecated in NumPy 1.20; for more details and guidance: https://numpy.org/devdocs/release/1.20.0-notes.html#deprecations
  mask = np.zeros(data.shape, np.bool)

```







<br />

```{.python }

from wfmap.data import load_data
from wfmap import create_incmap

data = load_data()
fig = create_incmap(data, vsigmas={'MR': 10, 'HDI': 1})
```


**Total running time of the script:** ( 0 minutes  0.955 seconds)

<div id="download_links"></div>



[:fontawesome-solid-download: Download Python source code: plot_4_incmap.py](./plot_4_incmap.py){ .md-button .center}

[:fontawesome-solid-download: Download Jupyter notebook: plot_4_incmap.ipynb](./plot_4_incmap.ipynb){ .md-button .center}


[Gallery generated by mkdocs-gallery](https://mkdocs-gallery.github.io){: .mkd-glr-signature }