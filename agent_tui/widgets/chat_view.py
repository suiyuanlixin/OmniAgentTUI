from __future__ import annotations

from datetime import datetime

import json
import urllib.request
from rich.style import Style
from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Static
from textual.widget import Widget

from agent_tui.theme import PAGE_BACKGROUND, SURFACE_BACKGROUND, render_css


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
        padding: 0;
        scrollbar-size: 0 0;
    }
    .message-row {
        width: 100%;
        height: auto;
        margin: 0;
        padding: 0;
    }
    .message-row-user {
        align-horizontal: right;
    }
    .message-row-assistant {
        align-horizontal: left;
    }

    .message-bubble {
        width: auto;
        max-width: 100%;
        height: auto;
        margin: 0;
    }
    .message-half {
        width: 100%;
        height: 1;
        background: $PAGE_BACKGROUND;
    }
    .message-half-user {
        color: $SURFACE_BACKGROUND;
    }
    .message-half-assistant {
        color: $PAGE_BACKGROUND;
    }

    .message-bubble-content {
        width: auto;
        max-width: 100%;
        height: auto;
        min-width: 1;
        min-height: 1;
        padding: 0 1;
        margin: 0;
    }
    .message-bubble-user {
        background: $SURFACE_BACKGROUND;
        color: $TEXT_PRIMARY;
    }
    .message-bubble-assistant {
        background: transparent;
        color: $TEXT_PRIMARY;
    }
    """
    )

    messages: list[tuple[str, str, str]] = []

    def compose(self) -> ComposeResult:
        yield VerticalScroll(id="chat-log")

    # #region debug-point A:report-event
    def _debug_report(self, hypothesis_id: str, msg: str, data: dict) -> None:
        _p = ".dbg/chat-message-hidden.env"
        _u, _s = "http://127.0.0.1:7777/event", "chat-message-hidden"
        try:
            with open(_p, encoding="utf-8") as f:
                c = f.read()
            _u = next(
                (
                    l.split("=", 1)[1]
                    for l in c.splitlines()
                    if l.startswith("DEBUG_SERVER_URL=")
                ),
                _u,
            )
            _s = next(
                (
                    l.split("=", 1)[1]
                    for l in c.splitlines()
                    if l.startswith("DEBUG_SESSION_ID=")
                ),
                _s,
            )
        except Exception:
            pass
        try:
            urllib.request.urlopen(
                urllib.request.Request(
                    _u,
                    data=json.dumps({
                        "sessionId": _s,
                        "runId": "post-fix",
                        "hypothesisId": hypothesis_id,
                        "location": "agent_tui/widgets/chat_view.py",
                        "msg": msg,
                        "data": data,
                    }).encode(),
                    headers={"Content-Type": "application/json"},
                )
            ).read()
        except Exception:
            pass

    # #endregion

    def add_message(self, role: str, content: str) -> None:
        log = self.query_one("#chat-log", VerticalScroll)
        row_classes = "message-row"
        bubble_classes = "message-bubble"
        content_classes = "message-bubble-content"
        half_classes = "message-half"
        if role == "user":
            row_classes += " message-row-user"
            bubble_classes += " message-bubble-user"
            content_classes += " message-bubble-user"
            half_classes += " message-half-user"
        else:
            row_classes += " message-row-assistant"
            bubble_classes += " message-bubble-assistant"
            content_classes += " message-bubble-assistant"
            half_classes += " message-half-assistant"
        bubble = Vertical(
            TopHalfSpacer(classes=half_classes),
            Static(
                content,
                classes=content_classes,
                markup=False,
                expand=False,
            ),
            BottomHalfSpacer(classes=half_classes),
            classes=bubble_classes,
        )
        row = Horizontal(bubble, classes=row_classes)
        # #region debug-point B:add-message-before-mount
        self._debug_report(
            "B",
            "[DEBUG] add_message before mount",
            {
                "role": role,
                "content_len": len(content),
                "row_classes": row.classes,
                "bubble_classes": bubble.classes,
                "content_classes": content_classes,
                "half_classes": half_classes,
            },
        )
        # #endregion
        log.mount(row)
        # #region debug-point C:add-message-after-refresh
        self.call_after_refresh(
            self._debug_capture_layout, log, row, bubble, role, content
        )
        # #endregion
        self.call_after_refresh(log.scroll_end, animate=False)
        self.messages.append((role, content, datetime.now().isoformat()))

    def clear(self) -> None:
        log = self.query_one("#chat-log", VerticalScroll)
        log.remove_children()
        self.messages.clear()

    # #region debug-point D:capture-layout
    def _debug_capture_layout(
        self,
        log: VerticalScroll,
        row: Horizontal,
        bubble: Vertical,
        role: str,
        content: str,
    ) -> None:
        try:
            content_widget = bubble.query_one(".message-bubble-content", Static)
        except Exception:
            content_widget = None
        half_widgets = bubble.query(".message-half").results(Static)
        self._debug_report(
            "D",
            "[DEBUG] layout after refresh",
            {
                "role": role,
                "content_len": len(content),
                "log_size": tuple(log.size),
                "row_size": tuple(row.size),
                "bubble_size": tuple(bubble.size),
                "content_size": tuple(content_widget.size) if content_widget else None,
                "half_sizes": [tuple(widget.size) for widget in half_widgets],
                "children_count": len(list(log.children)),
            },
        )

    # #endregion


class TopHalfSpacer(Static):
    """A 1-cell-high spacer that paints the lower half of the row."""

    def render(self):
        width = self.size.width
        if width <= 0:
            return ""
        colour = self.styles.color
        bg = self.styles.background
        return Text(
            "\u2584" * width,
            style=Style(
                color=colour.hex if colour else SURFACE_BACKGROUND,
                bgcolor=bg.hex if bg else PAGE_BACKGROUND,
            ),
        )


class BottomHalfSpacer(Static):
    """A 1-cell-high spacer that paints the upper half of the row."""

    def render(self):
        width = self.size.width
        if width <= 0:
            return ""
        colour = self.styles.color
        bg = self.styles.background
        return Text(
            "\u2580" * width,
            style=Style(
                color=colour.hex if colour else SURFACE_BACKGROUND,
                bgcolor=bg.hex if bg else PAGE_BACKGROUND,
            ),
        )
