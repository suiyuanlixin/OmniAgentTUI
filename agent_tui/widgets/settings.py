from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Button, Label, Static
from textual.screen import ModalScreen


class SettingsModal(ModalScreen[None]):
    """Settings modal window centered on screen."""

    DEFAULT_CSS = """
    SettingsModal {
        align: center middle;
        background: rgba(0, 0, 0, 0.6);
    }

    SettingsModal > Container {
        width: 50;
        height: 20;
        background: $surface;
        border: solid $primary;
    }

    #settings-header {
        width: 100%;
        height: 1;
        background: $primary;
        color: $text;
    }

    #settings-title {
        text-align: center;
        text-style: bold;
        padding: 0 1;
    }

    #settings-close-btn {
        width: 3;
        height: 1;
        background: transparent;
        border: none;
        color: $text;
        dock: right;
    }
    #settings-close-btn:hover {
        background: $primary-lighten-1;
    }

    #settings-body {
        width: 100%;
        height: 1fr;
        padding: 2;
        align: center middle;
    }
    """

    BINDINGS = [
        ("escape", "dismiss_result(None)", "Close"),
    ]

    def compose(self) -> ComposeResult:
        with Container():
            with Horizontal(id="settings-header"):
                yield Static("Settings", id="settings-title")
                yield Button("X", id="settings-close-btn")
            with Vertical(id="settings-body"):
                yield Label("Settings panel", id="settings-placeholder")
                yield Label("(Configuration options coming soon)")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "settings-close-btn":
            self.dismiss(None)

    def action_dismiss_result(self, result: None = None) -> None:
        self.dismiss(result)
