from sklearn.datasets import fetch_openml

from rich_dataframe import DataFramePrettify

if __name__ == "__main__":

    speed_dating = fetch_openml(name="SpeedDating", version=1)["frame"]

    table = DataFramePrettify(
        speed_dating, row_limit=20, first_rows=True, delay_time=5
    ).prettify()
