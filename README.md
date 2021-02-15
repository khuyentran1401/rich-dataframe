[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![License: Apache-2.0](https://img.shields.io/badge/Apache-2.0%20v3-blue.svg)](https://github.com/khuyentran1401/rich-dataframe/blob/master/LICENSE)

# Rich DataFrame

Create animated and pretty Pandas Dataframe, as shown below:

![image](prettify_table.gif)

# Installation
```bash
pip install rich-dataframe
```
# Usage
## Minimal example
```python
from sklearn.datasets import fetch_openml
from rich_dataframe import DataFramePrettify

if __name__=='__main__':
   
    speed_dating = fetch_openml(name='SpeedDating', version=1)['frame']
    
    table = DataFramePrettify(speed_dating, row_limit=20, first_rows=True, delay_time=5).prettify()
    
```
## Parameters
* **df: pd.DataFrame**
The data you want to prettify
* **row_limit : int, optional**
    Number of rows to show, by default `20`
* **col_limit : int, optional**
    Number of columns to show, by default `10`
* **first_rows : bool, optional**
    Whether to show first n rows or last n rows, by default `True`. If this is set to False, show last n rows.
* **first_cols : bool, optional**
    Whether to show first n columns or last n columns, by default True. If this is set to `False`, show last n rows.
* **delay_time : int, optional**
    How fast is the animation, by default `5`. Increase this to have slower animation.

