from sklearn.datasets import fetch_openml

from rich_dataframe import prettify

if __name__ == "__main__":
    speed_dating = fetch_openml(name="SpeedDating", version=1, parser="auto")[
        "frame"
    ]
    table = prettify(
        speed_dating,
        row_limit=20,
        first_rows=True,
        col_limit=10,
        first_cols=False,
    )
