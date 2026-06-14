from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal, Container
from textual.widgets import Button, Label, Static, RichLog
from textual.widget import Widget
from textual.reactive import reactive
from datetime import datetime


class ChatView(Widget):
    """Chat messages display area."""

    DEFAULT_CSS = """
    ChatView {
        width: 100%;
        height: 1fr;
        background: #0a0a0a;
    }

    ChatView #chat-log {
        width: 100%;
        height: 1fr;
        background: #0a0a0a;
        border: none;
        padding: 0 1;
    }
    """

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
