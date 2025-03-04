# edit_row.py

import db_utility
import sqlite3

from screens import WarningScreen

from textual import on
from textual.app import ComposeResult, App
from textual.containers import Center, Horizontal, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, Input


class EditRowScreen(App):
    """
    Edit a row of data shown in the Table Viewer in the database
    """

    def __init__(self, data: dict[str, str], table_name: str, primary_keys: tuple[str], db_path: str,
                 *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.data = data
        self.table_name = table_name
        self.primary_keys = primary_keys
        self.db_path = db_path
        self.title = f"Editing {table_name}"

    def compose(self) -> ComposeResult:
        children = []
        for field_name in self.data:
            disabled = True if field_name in self.primary_keys else False
            field = Input(str(self.data[field_name]), id=f"{field_name}", disabled=disabled)
            field.border_title = f"{field_name} (Primary Key)" if disabled else f"{field_name}"
            field.styles.border = ("round", "gold")
            children.append(field)

        h_container = Horizontal(
            Button("Save Changes", variant="primary", id="edit_save_btn"),
            Button("Cancel", variant="error", id="edit_cancel_btn"),
            id="h_buttons_container"
            )

        children.append(h_container)
        yield VerticalScroll(*children, id="edit_vertical_scroll")

    @on(Button.Pressed, "#edit_cancel_btn")
    def on_cancel_edit(self) -> None:
        self.dismiss()

    @on(Button.Pressed, "#edit_save_btn")
    def on_save_changes(self) -> None:
        column_types = db_utility.get_column_types(self.db_path, self.table_name)
        primary_keys = db_utility.get_primary_keys(self.db_path, self.table_name)
        print(f"{primary_keys  =  }")
        column_values = [self.query_one(f"#{column}", Input).value
                         for column in self.data
                         if column not in primary_keys[0]]
        # Create loop over keys in data to grab Input values
        # May need some way of casting the input values to the correct type
        # Maybe use field schema?
        set_clause = ", ".join([f"{column} = ?" for column in self.data
                                if column not in primary_keys[0]])
        if len(primary_keys[0]) == 1:
            primary_key = primary_keys[0][0]
            primary_key_value = self.query_one(f"#{primary_key}", Input).value
            sql =  f"UPDATE {table_name} SET {set_clause} WHERE {primary_key} = ?"
            print(sql, (*column_values, primary_key_value))

        try:
            db_utility.run_row_update(self.db_path, sql, column_values, primary_key_value)
        except sqlite3.OperationalError as e:
            self.app.push_screen(WarningScreen(f"[red]ERROR Committing data:[/] {e}"))


data =  dict(zip(('AlbumId', 'Title', 'ArtistId'), [1, 'For Those About To Rock We Salute You', 1]))
table_name = "Album"
primary_keys = ('AlbumId',)
app = EditRowScreen(data, table_name, primary_keys, r"C:\Chinook_Sqlite.sqlite")
app.run()
