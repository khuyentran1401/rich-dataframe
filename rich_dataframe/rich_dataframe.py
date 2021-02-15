from rich.table import Table
from rich import print 
from rich.console import Console
from rich.columns import Columns
from rich.table import Table
from rich.measure import Measurement
from rich.box import SQUARE, MINIMAL, SIMPLE_HEAD, SIMPLE
from rich.live import Live
from argparse import ArgumentParser

from contextlib import contextmanager
import time

import pandas as pd
from sklearn.datasets import fetch_openml

console = Console()

BEAT_TIME = 0.004

COLORS = ["cyan", "magenta", 'red', 'green', 'blue', 'purple']
@contextmanager
def beat(length: int = 1) -> None:
    with console:
        yield
    time.sleep(length * BEAT_TIME)


class DataFramePrettify:

    def __init__(self, df: pd.DataFrame, row_limit: int=20, col_limit: int=10, first_rows:bool=True, first_cols: bool=True, delay_time: int=5) -> None:
        self.df = df 
        self.table = Table(show_footer=False)
        self.table_centered = Columns((self.table,), align="center", expand=True)
        self.num_colors = len(COLORS)
        self.delay_time = delay_time
        self.row_limit = row_limit
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

    def add_columns(self):
        for col in self.columns:
            with beat(self.delay_time):
                self.table.add_column(col)

    def add_rows(self):
        for row in self.rows:
            with beat(self.delay_time):

                if self.first_cols:
                    row = row[:self.col_limit]
                else:
                    row = row[-self.col_limit:]
                
                row =  [str(item) for item in row] 
                self.table.add_row(*list(row))

    def move_text_to_right(self):
        for i in range(len(self.table.columns)): 
            with beat(self.delay_time):
                self.table.columns[i].justify = "right"

    def add_random_color(self):
        for i in range(len(self.table.columns)):
            with beat(self.delay_time):
                self.table.columns[i].header_style = COLORS[i%self.num_colors]
    
    def add_style(self):
        for i in range(len(self.table.columns)):
            with beat(self.delay_time):
                self.table.columns[i].style = "bold " + COLORS[i%self.num_colors]

    def adjust_box(self):
        for box in [MINIMAL, SIMPLE, SIMPLE_HEAD, SQUARE]:
            with beat(self.delay_time):
                self.table.box = box

    def dim_row(self):
        with beat(self.delay_time):
            self.table.row_styles = ["none", "dim"]

    def adjust_border_color(self):
        self.table.border_style = "bright_yellow"

    def change_width(self):
        original_width = Measurement.get(console, self.table).maximum
        width_ranges = [[original_width, console.width, 2], 
                      [console.width, original_width, -2],
                      [original_width, 90, -2],
                      [90, original_width + 1, 2]]

        for width_range in width_ranges:
            for width in range(*width_range):
                with beat(1):
                    self.table.width = width

            with beat(1):
                self.table.width = None

    def add_caption(self):
        with beat(self.delay_time):
            self.table.caption = f"Only {self.row_limit} rows and {self.col_limit} columns is shown here."
        with beat(self.delay_time):
            self.table.caption = f"Only [bold green] {self.row_limit} rows[/bold green] and [bold red]{self.col_limit} columns[/bold red] is shown here."
        with beat(self.delay_time):
            self.table.caption = f"Only [bold magenta not dim] {self.row_limit} rows[/bold magenta not dim] and [bold green not dim]{self.col_limit} columns[/bold green not dim] are shown here."
        
    def prettify(self):
        with Live(self.table_centered, console=console, refresh_per_second=self.delay_time, vertical_overflow="ellipsis"
        ):
            self.add_columns()
            self.add_rows()
            self.move_text_to_right()
            self.add_random_color()
            self.add_style()
            self.adjust_box()
            # self.dim_row()
            self.adjust_border_color()
            self.change_width()
            self.add_caption()
            # pass

        return self.table



if __name__=='__main__':

    parser = ArgumentParser("Prettify Pandas DataFrame")
    parser.add_argument('-n', '--NumRows', help="Number of rows to show. Default is 20 rows.", 
                        type=int, default=20)
    parser.add_argument('-f', '--ShowFirst', 
                        help="Whether to show first rows or last rows. Default is True. Type False if you want to show the last rows",
                        type=bool, default=True)
    parser.add_argument('-t', '--DelayTime', 
                        help="How fast it is to run the animation. Default is 5",
                        type=int, default=5)

    args = parser.parse_args()

    speed_dating = fetch_openml(name='SpeedDating', version=1)['frame']
    
    table = DataFramePrettify(speed_dating, row_limit=args.NumRows, first_rows=args.ShowFirst, delay_time=args.DelayTime).prettify()
    