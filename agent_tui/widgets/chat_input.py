from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Horizontal, Container
from textual.widgets import Button, Input, Static, Select
from textual.widget import Widget
from textual.message import Message
from textual.reactive import reactive

from agent_tui.data import MODELS, THINKING_LEVELS, APPROVAL_LEVELS


class ChatInput(Widget):
    """Chat input bar with [+] Plan/Build Approval [text input] Model Thinking [Send]."""

    DEFAULT_CSS = """
    ChatInput {
        width: 100%;
        height: auto;
        padding: 1;
        background: $surface;
        border-top: solid $panel;
    }

    ChatInput > #input-row {
        width: 100%;
        height: auto;
        align-horizontal: center;
        align-vertical: middle;
    }

    ChatInput Button {
        min-width: 3;
        height: 3;
        margin: 0 1 0 0;
        border: none;
        background: transparent;
        color: $text;
    }
    ChatInput Button:hover {
        background: $surface-lighten-1;
    }

    #attach-btn {
        width: 6;
        background: $surface-darken-1;
        border: solid $primary;
        color: $primary;
    }
    #attach-btn:hover {
        background: $surface-lighten-1;
        color: $text;
    }

    #plan-build-group {
        width: auto;
        height: 3;
        border: solid $primary;
        margin: 0 1 0 0;
    }
    #plan-build-group Button {
        width: 8;
        height: 3;
        border: none;
        background: transparent;
        color: $text-muted;
        margin: 0;
    }
    #plan-build-group Button.active {
        background: $primary;
        color: $text;
    }

    #approval-select {
        width: 22;
        height: 3;
        margin: 0 1 0 0;
    }
    #approval-select.hidden {
        display: none;
    }

    #message-input {
        width: 1fr;
        min-width: 10;
        height: 3;
        margin: 0 1 0 0;
        border: solid $primary;
        background: $surface-darken-1;
        color: $text;
        padding: 0 1;
    }

    #model-select {
        width: 24;
        height: 3;
        margin: 0 1 0 0;
    }

    #thinking-select {
        width: 12;
        height: 3;
        margin: 0 1 0 0;
    }

    #send-btn {
        width: 6;
        height: 3;
        margin: 0;
        background: $primary;
        color: $text;
        border: none;
    }
    #send-btn:hover {
        background: $primary-lighten-1;
    }

    #attached-files {
        width: 100%;
        height: auto;
        padding: 0 0 1 0;
        color: $text-muted;
    }
    #attached-files.hidden {
        display: none;
    }
    """

    plan_mode = reactive(True)
    chat_active = reactive(False)

    class FileAttached(Message):
        def __init__(self, path: str) -> None:
            super().__init__()
            self.path = path

    class Send(Message):
        def __init__(self, content: str) -> None:
            super().__init__()
            self.content = content

    def compose(self) -> ComposeResult:
        with Horizontal(id="input-row"):
            yield Button("+", id="attach-btn")

            with Horizontal(id="plan-build-group"):
                yield Button("Plan", id="plan-btn", classes="active")
                yield Button("Build", id="build-btn")

            yield Select(
                APPROVAL_LEVELS,
                id="approval-select",
                prompt="Ask for approval",
                value="ask",
                allow_blank=False,
            )

            yield Input(
                placeholder="Type a message...",
                id="message-input",
            )

            yield Select(
                MODELS,
                id="model-select",
                prompt="Model",
                value="claude-3.5-sonnet",
                allow_blank=False,
            )

            yield Select(
                THINKING_LEVELS,
                id="thinking-select",
                prompt="Thinking",
                value="medium",
                allow_blank=False,
            )

            yield Button("\u2192", id="send-btn")

        with Container(id="attached-files", classes="hidden"):
            yield Static("", id="attached-files-label")

    def add_attached_file(self, path: str) -> None:
        container = self.query_one("#attached-files", Container)
        label = self.query_one("#attached-files-label", Static)
        container.remove_class("hidden")
        label.update(f"  Attached: {path}")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn_id = event.button.id
        if btn_id == "attach-btn":
            self.post_message(self.FileAttached(""))
        elif btn_id == "plan-btn":
            self.plan_mode = True
        elif btn_id == "build-btn":
            self.plan_mode = False
        elif btn_id == "send-btn":
            self._do_send()

    def _do_send(self) -> None:
        msg_input = self.query_one("#message-input", Input)
        content = msg_input.value.strip()
        if content:
            self.post_message(self.Send(content))
            msg_input.value = ""

    def watch_plan_mode(self, value: bool) -> None:
        self._update_plan_build()

    def _update_plan_build(self) -> None:
        try:
            plan_btn = self.query_one("#plan-btn", Button)
            build_btn = self.query_one("#build-btn", Button)
            approval = self.query_one("#approval-select", Select)
            if self.plan_mode:
                plan_btn.add_class("active")
                build_btn.remove_class("active")
                approval.remove_class("hidden")
            else:
                plan_btn.remove_class("active")
                build_btn.add_class("active")
                approval.add_class("hidden")
        except Exception:
            pass
