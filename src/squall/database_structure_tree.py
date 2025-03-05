# database_structure.py

from squall import db_utility

from pathlib import Path
from textual.app import ComposeResult
from textual.widgets import TabPane, Tree


class DatabaseStructurePane(TabPane):

    def __init__(self, db_path: Path, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.db_path = db_path
        if self.db_path.exists():
            self.db_schema = db_utility.get_schema(self.db_path)

    def compose(self) -> ComposeResult:
        tree: Tree[str] = Tree(f"Tables ({len(self.db_schema.keys())})")
        tree.root.expand()
        table_names = sorted(list(self.db_schema.keys()))
        for table_name in table_names:
            table = tree.root.add(table_name)
            columns = self.db_schema[table_name]["Columns"]
            for column in columns:
                table.add_leaf(f"{column}  [green]{columns[column]['Type']}[/]")
        yield tree
