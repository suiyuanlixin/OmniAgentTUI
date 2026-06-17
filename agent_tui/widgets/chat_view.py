from __future__ import annotations

from textual.app import ComposeResult
from textual.widgets import RichLog
from textual.widget import Widget
from datetime import datetime

from agent_tui.theme import render_css


class ChatView(Widget):
    """Chat messages display area."""

    DEFAULT_CSS = render_css(
        """
    ChatView {
        width: 100%;
        height: 1fr;
        background: $PAGE_BACKGROUND;
    }

    ChatView #chat-log {
        width: 100%;
        height: 1fr;
        background: $PAGE_BACKGROUND;
        border: none;
        padding: 0 1;
    }
    """
    )

    messages: list[tuple[str, str, str]] = []

    def compose(self) -> ComposeResult:
        yield RichLog(id="chat-log", highlight=True, markup=True)

    def add_message(self, role: str, content: str) -> None:
        log = self.query_one("#chat-log", RichLog)
        if role == "user":
            prefix = "[bold cyan]You:[/]"
        elif role == "assistant":
            prefix = "[bold green]Assistant:[/]"
        else:
            prefix = f"[bold]{role}:[/]"
        log.write(f"\n{prefix} {content}")
        self.messages.append((role, content, datetime.now().isoformat()))

    def clear(self) -> None:
        log = self.query_one("#chat-log", RichLog)
        log.clear()
        self.messages.clear()
