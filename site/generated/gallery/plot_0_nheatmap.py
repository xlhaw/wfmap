"""
NumHeatmap
=================================
> WaferMap for Numerical Variables
This example demonstrates how to import a local module and how images are
stacked when two plots are created in one code block. The variable ``N`` from
the example 'Local module' (file ``local_module.py``) is imported in the code
below. Further, note that when there is only one code block in an example, the
output appears before the code block.
"""

from wfmap.data import load_data
from wfmap import num_heatmap
import matplotlib.pyplot as plt

data = load_data()
ax = num_heatmap(data, 'MR')
plt.tight_layout()
