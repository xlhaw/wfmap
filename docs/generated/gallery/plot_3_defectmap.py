"""
DefectMap `defectmap`
=================================
> Wafer DefectMap with Pareto Subplot

DefectMap is aimed for defect analysis, beside the defect distribution by `cat_heatmap`, yield summary and top defect statistics are also applied by using inset pie chart and bar chart subplot.

Unlike in the `cat_heatmap`, categories are ordered by unique count in default. `defectmap` use the 'OK' as the top category and set it with `lightgreen` color. You can UAI other codes eg. 'BINA','BINB' as `OK` by update the `ok_codes`.

"""

import random
from wfmap.data import load_data
from wfmap import defectmap

data = load_data()
fig = defectmap(data, 'DEFECT')

# %%
# Above example used the default defect code from sample data, you change it to more reader-friendly and meaningful remark by modify the `code_dict` as below.

code_dict = {}
for code in data['DEFECT'].unique():
    if code.startswith('S'):
        code_dict[code] = random.choice(
            ['QST Rej', 'HDD Rej', 'DP Rej', 'VM Rej'])

fig2 = defectmap(data, 'DEFECT', code_dict=code_dict)
