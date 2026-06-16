from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Button, Label, Static
from textual.screen import ModalScreen

from agent_tui.theme import render_css


class SettingsModal(ModalScreen[None]):
    """Settings modal window centered on screen."""

    DEFAULT_CSS = render_css(
        """
    SettingsModal {
        align: center middle;
        background: $OVERLAY_BACKGROUND;
    }

    SettingsModal > Container {
        width: 50;
        height: 20;
        background: $SURFACE_BACKGROUND;
        border: none;
    }

    #settings-header {
        width: 100%;
        height: 1;
        background: $SURFACE_BACKGROUND;
        color: $TEXT_PRIMARY;
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
        color: $TEXT_PRIMARY;
        dock: right;
    }
    #settings-close-btn:hover {
        background: $PAGE_BACKGROUND;
    }

    #settings-body {
        width: 100%;
        height: 1fr;
        padding: 2;
        align: center middle;
    }
    """
    )

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
