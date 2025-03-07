# screens.py

import pathlib

from textual import on
from textual.app import ComposeResult
from textual.containers import Grid, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, DirectoryTree, Footer, Label, Header


class WarningScreen(ModalScreen):
    """
    Creates a pop-up Screen that displays a warning message to the user
    """

    def __init__(self, warning_message: str) -> None:
        super().__init__()
        self.warning_message = warning_message

    def compose(self) -> ComposeResult:
        """
        Create the UI in the Warning Screen
        """
        yield Grid(
            Label(self.warning_message, id="warning_msg"),
            Button("OK", variant="primary", id="ok_warning"),
            id="warning_dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Event handler for when the OK button - dismisses the screen
        """
        self.dismiss()
        event.stop()


class FileBrowser(ModalScreen):
    BINDINGS = [("escape", "exit_screen", "Exit")]

    def __init__(self) -> None:
        super().__init__()
        self.selected_file = pathlib.Path("bad")
        self.title = "Load SQLite Database"

    def compose(self) -> ComposeResult:
        yield Header()
        yield DirectoryTree("/")
        yield Horizontal(
            Button("Open Database", variant="primary", id="load_db_file"),
            Button("Cancel", variant="error", id="cancel_db_file"),
        )
        yield Footer()

    @on(DirectoryTree.FileSelected)
    def on_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        """
        Called when the FileSelected Message is emitted from the DirectoryTree
        """
        self.selected_file = event.path

    def action_exit_screen(self) -> None:
        self.dismiss("bad")

    @on(Button.Pressed, "#cancel_db_file")
    def cancel_dialog(self) -> None:
        self.dismiss("bad")

    @on(Button.Pressed, "#load_db_file")
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Event handler for when the load file button is pressed
        """
        event.stop()

        if (
            self.selected_file.suffix.lower() not in [".db", ".sqlite"]
            and self.selected_file.is_file()
        ):
            self.app.push_screen(WarningScreen("ERROR: You must choose a *.db file!"))
            return

        self.dismiss(self.selected_file)
