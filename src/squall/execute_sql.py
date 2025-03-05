# execute_sql.py

import sqlite3
import time

try:
    import db_utility
except ModuleNotFoundError:
    from . import db_utility
    
from pathlib import Path
from rich.text import Text
from textual import on
from textual.app import ComposeResult
from textual.widgets import Button, DataTable, TextArea, RichLog
from textual.widgets import TabPane


class ExecuteSQLPane(TabPane):

    def __init__(self, db_path: Path, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.db_path = db_path

    def compose(self) -> ComposeResult:
        text = TextArea(id="sql_commands")
        text.border_title = "SQL"
        results = DataTable(id="sql_results_table", zebra_stripes=True)
        results.border_title = "SQL Results"
        sql_command_output = RichLog(id="sql_log")
        sql_command_output.border_title = "SQL Output / Status"
        yield text
        yield Button("Run SQL", id="run_sql_btn", variant="primary")
        yield results
        yield sql_command_output

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        data = [("No", "Data", "Loaded"), ("", "", "")]
        table.add_columns(*data[0])
        table.add_rows(data[1:])
        table.cursor_type = "row"


    @on(Button.Pressed, "#run_sql_btn")
    def run_sql(self) -> None:
        sql = self.query_one("#sql_commands", TextArea).text
        start = time.time()
        error_msg = None
        result = None

        try:
            result = db_utility.run_sql(self.db_path, sql)
        except sqlite3.OperationalError as e:
            error_msg = str(e)
        end = time.time()
        row_count = 0
        total_runtime = end - start

        if result:
            if len(result) > 1:
                row_count = len(result) - 1

            self.update_sqlite_table(result)

        self.update_log(total_runtime, row_count, error_msg)

    def update_sqlite_table(self, data: list[tuple]) -> None:
        table = self.query_one(DataTable)
        table.clear(columns=True)
        table.add_columns(*data[0])
        if len(data[1:]):
            table.add_rows(data[1:])
        else:
            table.add_rows([tuple(["" for x in data[0]])])

        table.cursor_type = "row"

    def update_log(self, seconds: float, row_count: int, error_msg: str | None) -> None:
        rich_log = self.query_one("#sql_log", RichLog)
        rich_log.clear()

        if error_msg is None:
            rich_log.write(Text("SQL execution finished with no errors", style="green"))
        else:
            rich_log.write(Text("SQL execution failed!"))
            rich_log.write(Text(f"ERROR: {error_msg}", style="red"))

        if row_count > 0:
            rich_log.write(f"Result: {row_count} rows returned in {seconds: .4f}s")
