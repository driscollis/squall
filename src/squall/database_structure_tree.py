# database_structure.py

from textual.app import ComposeResult
from textual.widgets import TabPane, Tree


class DatabaseStructurePane(TabPane):
    def __init__(self, db_schema: dict[str, dict], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.db_schema = db_schema

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
