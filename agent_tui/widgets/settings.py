from __future__ import annotations

from textual import events
from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Input, Static
from textual.screen import ModalScreen

from agent_tui.theme import render_css


from agent_tui.widgets.chat_input import HalfRowSpacer


class SettingsModal(ModalScreen[None]):
    """Settings modal window centered on screen."""

    DEFAULT_CSS = render_css(
        """
    SettingsModal {
        align: center middle;
        background: $OVERLAY_BACKGROUND;
    }

    #settings-wrapper {
        width: 100%;
        min-width: 44;
        max-width: 78;
        height: auto;
        padding: 0;
        margin: 0;
        background: transparent;
    }

    #settings-dialog {
        width: 100%;
        height: auto;
        min-height: 14;
        background: $SURFACE_BACKGROUND;
        border: none;
    }

    #settings-top-edge {
        color: $PAGE_BACKGROUND;
        background: $SURFACE_BACKGROUND;
    }

    #settings-bottom-edge {
        color: $SURFACE_BACKGROUND;
        background: $PAGE_BACKGROUND;
    }

    #settings-header {
        width: 100%;
        height: 1;
        background: $SURFACE_BACKGROUND;
        color: $TEXT_PRIMARY;
        padding: 0 2;
    }

    #settings-title {
        width: 1fr;
        text-align: left;
        text-style: bold;
        padding: 0;
    }

    #settings-close-btn {
        width: auto;
        height: 1;
        background: transparent;
        color: $TEXT_PRIMARY;
        padding: 0;
        text-align: right;
        content-align: right middle;
    }

    #settings-body {
        width: 100%;
        height: auto;
        padding: 0 2;
    }

    #settings-search-row,
    #settings-list,
    .settings-row {
        width: 100%;
        height: auto;
    }

    .settings-gap {
        width: 100%;
        height: 1;
        background: $SURFACE_BACKGROUND;
    }

    #settings-search {
        width: 100%;
        height: 1;
        border: none;
        background: transparent;
        color: $TEXT_PRIMARY;
        padding: 0;
    }

    .settings-row {
        height: 1;
        color: $TEXT_PRIMARY;
        margin: 0;
    }

    .settings-name {
        width: 1fr;
        text-align: left;
        color: $TEXT_PRIMARY;
    }

    .settings-value {
        width: auto;
        color: $TEXT_MUTED;
        text-align: right;
    }
    """
    )

    BINDINGS = [
        ("escape", "dismiss_result(None)", "Close"),
    ]

    def compose(self) -> ComposeResult:
        with Container(id="settings-wrapper"):
            yield HalfRowSpacer(id="settings-top-edge")
            with Vertical(id="settings-dialog"):
                with Horizontal(id="settings-header"):
                    yield Static("Settings", id="settings-title")
                    yield Static("esc", id="settings-close-btn")
                with Vertical(id="settings-body"):
                    yield Static(classes="settings-gap")
                    with Horizontal(id="settings-search-row"):
                        yield Input(placeholder="Search settings...", id="settings-search")
                    yield Static(classes="settings-gap")
                    with Vertical(id="settings-list"):
                        with Horizontal(classes="settings-row"):
                            yield Static("Theme", classes="settings-name")
                            yield Static("Dark", classes="settings-value")
                        with Horizontal(classes="settings-row"):
                            yield Static("Model", classes="settings-name")
                            yield Static("GPT 5.5 Instant", classes="settings-value")
                        with Horizontal(classes="settings-row"):
                            yield Static("Approval", classes="settings-name")
                            yield Static("Ask for approval", classes="settings-value")
            yield HalfRowSpacer(id="settings-bottom-edge")

    def on_click(self, event: events.Click) -> None:
        if not event.control:
            return
        if event.control.id == "settings-close-btn":
            self.dismiss(None)

    def action_dismiss_result(self, result: None = None) -> None:
        self.dismiss(result)
