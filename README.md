# Wafer Heatmap by Matplotlib & Seaborn

Heatmap could be extremely useful when find 

heatmap is implemented using seaborn and add add more feature(eg, inset, historgram, pra) and finetune the graphics using 

This package use to 

the module support both numerical and categorical data, No need to special, but you need to tran into pandas DataFrame object.




## Installation


To install the latest release via PyPI using pip::

    pip install wfmap


Locally install



## Basic Usages

For demonstration, I generate some dummy data under the `/data` folder. Let's load the data first and explore the usage of this package.

```python
import pandas as pd
from wfmap import wafermap
data=pd.read_csv('/data/demo.csv')
```

One row is one die data, 'MAP_ROW' and 'MAP_COL'  and 'CODE' column stands for the _Defect Code_  and 'DATA' stand for __ individual die.



**Numerical Data**

'MAP_ROW' and 'MAP_COL' are the default column name for wafer mapping.  If you have preprocessed your data as the same format as I did above. The command required could be as simple as follows:

```python
wafermap(data,value='DATA')
```

![DATA](/img/Figure_2.png)

On the but the fine-tune Parameter(eg. bins, cmap) not provided so far.



**Categorical Data **

Similar to above numerical/continuous data, categorical data such as _Defect Code_ `CODE` can also be visualized as below.

```python
wafermap(data,value='CODE')
```

![CODE](/img/Figure_1.png)



Considering that add limit to focus on the top



See the `documentation <https://pythonhosted.org/wfmap>`.


