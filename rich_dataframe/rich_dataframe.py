import time
from contextlib import contextmanager

import pandas as pd
from rich import print
from rich.box import MINIMAL, SIMPLE, SIMPLE_HEAD, SQUARE
from rich.columns import Columns
from rich.console import Console
from rich.live import Live
from rich.measure import Measurement
from rich.table import Table

console = Console()

BEAT_TIME = 0.008

COLORS = ["cyan", "magenta", "red", "green", "blue", "purple"]


@contextmanager
def beat(length: int = 1) -> None:
    with console:
        yield
    time.sleep(length * BEAT_TIME)


# TODO: Add error message when not using this with pandas


class DataFramePrettify:
    """Create animated and pretty Pandas DataFrame

    Parameters
    ----------
    df : pd.DataFrame
        The data you want to prettify
    row_limit : int, optional
        Number of rows to show, by default 20
    col_limit : int, optional
        Number of columns to show, by default 10
    first_rows : bool, optional
        Whether to show first n rows or last n rows, by default True. If this is set to False, show last n rows.
    first_cols : bool, optional
        Whether to show first n columns or last n columns, by default True. If this is set to False, show last n rows.
    delay_time : int, optional
        How fast is the animation, by default 5. Increase this to have slower animation.
    """

    def __init__(
        self,
        df: pd.DataFrame,
        row_limit: int = 20,
        col_limit: int = 10,
        first_rows: bool = True,
        first_cols: bool = True,
        delay_time: int = 5,
    ) -> None:
        self.df = df.reset_index().rename(columns={"index": ""})
        self.table = Table(show_footer=False)
        self.table_centered = Columns(
            (self.table,), align="center", expand=True
        )
        self.num_colors = len(COLORS)
        self.delay_time = delay_time
        self.row_limit = row_limit
        self.first_rows = first_rows
        self.col_limit = col_limit
        self.first_cols = first_cols

        if first_cols:
            self.columns = self.df.columns[:col_limit]
        else:
            self.columns = self.df.columns[-col_limit:]

        if first_rows:
            self.rows = self.df.values[:row_limit]
        else:
            self.rows = self.df.values[-row_limit:]

        print(self.columns)

        console.clear()

    def _add_columns(self):
        for col in self.columns:
            with beat(self.delay_time):
                self.table.add_column(str(col))

    def _add_rows(self):
        for row in self.rows:
            with beat(self.delay_time):

                if self.first_cols:
                    row = row[: self.col_limit]
                else:
                    row = row[-self.col_limit :]

                row = [str(item) for item in row]
                self.table.add_row(*list(row))

    def _move_text_to_right(self):
        for i in range(len(self.table.columns)):
            with beat(self.delay_time):
                self.table.columns[i].justify = "right"

    def _add_random_color(self):
        for i in range(len(self.table.columns)):
            with beat(self.delay_time):
                self.table.columns[i].header_style = COLORS[
                    i % self.num_colors
                ]

    def _add_style(self):
        for i in range(len(self.table.columns)):
            with beat(self.delay_time):
                self.table.columns[i].style = (
                    "bold " + COLORS[i % self.num_colors]
                )

    def _adjust_box(self):
        for box in [SIMPLE_HEAD, SIMPLE, MINIMAL, SQUARE]:
            with beat(self.delay_time):
                self.table.box = box

    def _dim_row(self):
        with beat(self.delay_time):
            self.table.row_styles = ["none", "dim"]

    def _adjust_border_color(self):
        with beat(self.delay_time):
            self.table.border_style = "bright_yellow"

    def _change_width(self):
        original_width = Measurement.get(console, self.table).maximum
        width_ranges = [
            [original_width, console.width, 2],
            [console.width, original_width, -2],
            [original_width, 90, -2],
            [90, original_width + 1, 2],
        ]

        for width_range in width_ranges:
            for width in range(*width_range):
                with beat(self.delay_time):
                    self.table.width = width

            with beat(self.delay_time):
                self.table.width = None

    def _add_caption(self):
        if self.first_rows:
            row_text = "first"
        else:
            row_text = "last"
        if self.first_cols:
            col_text = "first"
        else:
            col_text = "last"

        with beat(self.delay_time):
            self.table.caption = f"Only the {row_text} {self.row_limit} rows and the {col_text} {self.col_limit} columns is shown here."
        with beat(self.delay_time):
            self.table.caption = f"Only the [bold green] {row_text} {self.row_limit} rows[/bold green] and the [bold red]{self.col_limit} {col_text} columns[/bold red] is shown here."
        with beat(self.delay_time):
            self.table.caption = f"Only the [bold magenta not dim] {row_text} {self.row_limit} rows[/bold magenta not dim] and the [bold green not dim]{col_text} {self.col_limit} columns[/bold green not dim] are shown here."

    def prettify(self):
        with Live(
            self.table_centered,
            console=console,
            refresh_per_second=self.delay_time,
            vertical_overflow="ellipsis",
        ):
            self._add_columns()
            self._add_rows()
            self._move_text_to_right()
            self._add_random_color()
            self._add_style()
            # self._adjust_box()
            self._adjust_border_color()
            # self._change_width()
            self._add_caption()

        return self.table


def prettify(
    df: pd.DataFrame,
    row_limit: int = 20,
    col_limit: int = 10,
    first_rows: bool = True,
    first_cols: bool = True,
    delay_time: int = 5,
):
    """Create animated and pretty Pandas DataFrame

    Parameters
    ----------
    df : pd.DataFrame
        The data you want to prettify
    row_limit : int, optional
        Number of rows to show, by default 20
    col_limit : int, optional
        Number of columns to show, by default 10
    first_rows : bool, optional
        Whether to show first n rows or last n rows, by default True. If this is set to False, show last n rows.
    first_cols : bool, optional
        Whether to show first n columns or last n columns, by default True. If this is set to False, show last n rows.
    delay_time : int, optional
        How fast is the animation, by default 5. Increase this to have slower animation.
    """
    if isinstance(df, pd.DataFrame) or isinstance(df, pd.DataFrame):
        DataFramePrettify(
            df, row_limit, col_limit, first_rows, first_cols, delay_time
        ).prettify()

    else:
        # In case users accidentally pass a non-datafame input, use rich's print instead
        print(df)
