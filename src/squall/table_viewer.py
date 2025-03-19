# table_viewer.py

import logging
import sqlite3

from squall import db_utility
from squall.edit_row import EditRowScreen

from pathlib import Path
from textual import on
from textual.app import ComposeResult
from textual.widgets import Button, DataTable, Select
from textual.widgets import TabPane

logger = logging.getLogger("squall")


class TableViewerPane(TabPane):
    def __init__(self, db_path: Path, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.db_path = db_path
        self.tables = db_utility.get_table_names(self.db_path)
        self.tables.sort()
        self.selected_row_key = None
        self.columns: tuple = tuple()

    def compose(self) -> ComposeResult:
        yield Select.from_values(
            self.tables, id="table_names_select", value=self.tables[0]
        )
        yield Button("Edit Row", id="edit_row_btn", variant="primary")
        yield DataTable(id="sqlite_table_data")

    def on_mount(self) -> None:
        self.update_sqlite_table_view()

    @on(Select.Changed, "#table_names_select")
    def update_sqlite_table_view(self) -> None:
        current_table = str(self.app.query_one("#table_names_select", Select).value)

        try:
            data = db_utility.get_data_from_table(self.db_path, current_table)
        except sqlite3.OperationalError:
            return

        data = db_utility.get_data_from_table(self.db_path, current_table)
        self.columns = data[0]
        table = self.query_one(DataTable)
        table.clear(columns=True)
        table.add_columns(*self.columns)
        if len(data[1:]):
            table.add_rows(data[1:])
        else:
            table.add_rows([tuple(["" for x in data[0]])])

        table.cursor_type = "row"

    @on(DataTable.RowSelected)
    @on(DataTable.RowHighlighted)
    def on_row_clisked(self, event: DataTable.RowSelected) -> None:
        self.selected_row_key = event.row_key  # type: ignore

    @on(Button.Pressed, "#edit_row_btn")
    def on_edit_row(self) -> None:
        table = self.app.query_one("#sqlite_table_data", DataTable)
        current_table = self.app.query_one("#table_names_select", Select).value
        primary_keys = db_utility.get_primary_keys(self.db_path, current_table)  # type: ignore
        if self.selected_row_key is not None and self.columns is not None:
            logger.info(self.columns)
            row_data = table.get_row(self.selected_row_key)
            data = dict(zip(self.columns, row_data))
            logger.info(primary_keys)
            logger.info(data)
            self.app.push_screen(
                EditRowScreen(self.db_path, data, current_table, primary_keys)
            )
