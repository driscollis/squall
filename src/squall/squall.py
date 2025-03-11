# squall.py

from argparse import ArgumentParser, Namespace
from pathlib import Path
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Center
from textual.widgets import Button, Footer, Header, Input
from textual.widgets import Label, TabbedContent, TabPane

from squall.database_structure_tree import DatabaseStructurePane
from squall.execute_sql import ExecuteSQLPane
from squall.screens import FileBrowser
from squall.table_viewer import TableViewerPane


class SQLiteClientApp(App):
    BINDINGS = [
        ("o", "open_database", "Open Database"),
        ("q", "quit", "Exit the program"),
        ("f5", "run_sql", "Run SQL"),
    ]

    CSS_PATH = "squall.tcss"

    def __init__(self, cli_args: Namespace, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.args = cli_args
        self.title = "Squall"

    def compose(self) -> ComposeResult:
        db_path = Input(id="db_path_input")
        db_path.border_title = "Database Path"
        yield Header()
        yield Center(
            Button("Open Database", id="open_db_btn", variant="primary"), id="center"
        )
        with TabbedContent("Database", id="tabbed_ui"):
            with TabPane("Database Structure"):
                yield Label("No data loaded")
            with TabPane("Table Viewer"):
                yield Label("No data loaded")
            with TabPane("Execute SQL"):
                yield Label("No data loaded")
        yield Footer()

    async def on_mount(self) -> None:
        path = Path(self.args.filepath) if self.args.filepath else Path("BAD")
        if path and path.exists():
            db_path = path.absolute()
            await self.update_ui(db_path)

    @on(Button.Pressed, "#open_db_btn")
    async def action_open_database(self) -> None:
        self.push_screen(FileBrowser(), self.update_ui)  # type: ignore

    def action_run_sql(self) -> None:
        """
        Runs when F5 is pressed and executes the user's SQL when on the "Run SQL" tab
        """
        tabbed_content = self.query_one("#tabbed_ui", TabbedContent)
        active_tab = tabbed_content.active
        if active_tab == "run_sql":
            self.execute_sql_pane.run_sql()

    async def update_ui(self, db_file_path: Path) -> None:
        if not Path(db_file_path).exists():
            self.notify("BAD PATH")
            return

        tabbed_content = self.query_one("#tabbed_ui", TabbedContent)
        self.execute_sql_pane = ExecuteSQLPane(
            db_file_path, title="Execute SQL", id="run_sql"
        )
        await tabbed_content.clear_panes()

        await tabbed_content.add_pane(
            DatabaseStructurePane(
                db_file_path, title="Database Structure", id="db_structure"
            )
        )
        await tabbed_content.add_pane(
            TableViewerPane(db_file_path, title="Table Viewer", id="table_viewer")
        )
        await tabbed_content.add_pane(self.execute_sql_pane)
        tabbed_content.active = "db_structure"
        self.title = f"Squall - {db_file_path}"


def get_args() -> Namespace:
    """
    Get the arguments the user passed to the application
    """
    parser = ArgumentParser()
    parser.add_argument("-f", "--filepath", help="Path to a SQLite database")
    return parser.parse_args()


def main() -> None:
    cli_args = get_args()
    app = SQLiteClientApp(cli_args)
    app.run()


if __name__ == "__main__":
    main()
