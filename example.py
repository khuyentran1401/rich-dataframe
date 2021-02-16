from sklearn.datasets import fetch_openml

from rich_dataframe import prettify

if __name__ == "__main__":

    speed_dating = fetch_openml(name="SpeedDating", version=1)["frame"]
    speed_dating = speed_dating.iloc[:, 0].rename(0)
    print(speed_dating)
    table = prettify(speed_dating, row_limit=20, first_rows=True, delay_time=5)
