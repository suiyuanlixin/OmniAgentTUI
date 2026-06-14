from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, Container
from textual.widgets import Button, Input, Static
from textual.widget import Widget
from textual.message import Message
from textual.reactive import reactive

from agent_tui.data import MODELS, THINKING_LEVELS, APPROVAL_LEVELS


class ChatInput(Widget):
    """Chat input bar with [+] Plan/Build Approval [text input] Model Thinking [Send]."""

    DEFAULT_CSS = """
    ChatInput {
        width: 75;
        height: auto;
        padding: 1 0;
        background: #0a0a0a;
    }
    ChatInput.stretch {
        width: 100%;
    }

    ChatInput > #input-area {
        width: 100%;
        height: auto;
        background: #1e1e1e;
        border-left: tall #fab283;
        padding: 1;
    }

    #message-row {
        width: 100%;
        height: auto;
        padding-bottom: 1;
    }

    #controls-row {
        width: 100%;
        height: auto;
        align-horizontal: left;
        overflow: hidden;
    }

    #message-input {
        width: 100%;
        height: 1;
        border: none;
        background: transparent;
        color: #eeeeee;
    }

    #input-area Button {
        min-width: 1;
        height: 1;
        margin: 0 1 0 0;
        border: none;
        background: transparent;
        color: #808080;
        padding: 0;
    }
    #input-area Button:focus {
        border: none;
    }
    #input-area Button:hover {
        border: none;
        border-top: none;
        border-bottom: none;
        background: #2a2a2a;
        color: #eeeeee;
    }

    #attach-btn {
        width: 1;
        min-width: 1;
        background: transparent;
        border: none;
        color: #808080;
        margin: 0 1 0 0;
        padding: 0;
        content-align: center middle;
    }
    #attach-btn:focus {
        border: none;
    }
    #attach-btn:hover {
        border: none;
        border-top: none;
        border-bottom: none;
        background: transparent;
        color: #eeeeee;
    }

    /* dropdown wrappers */
    #plan-drop, #approval-drop, #model-drop, #thinking-drop {
        width: auto;
        height: 1;
        margin: 0 1 0 0;
    }
    #approval-drop.hidden {
        display: none;
    }

    /* dropdown triggers */
    #plan-trigger, #approval-trigger, #model-trigger, #thinking-trigger {
        width: auto;
        height: 1;
        background: transparent;
        border: none;
        color: #808080;
        margin: 0;
        padding: 0;
    }

    /* dropdown option panels */
    #plan-options, #approval-options, #model-options, #thinking-options {
        display: none;
        width: auto;
        min-width: 16;
        height: auto;
        background: #141414;
        border: none;
        padding: 0;
        overlay: screen;
        constrain: none inside;
    }
    #plan-options.open, #approval-options.open, #model-options.open, #thinking-options.open {
        display: block;
    }

    #plan-options Button, #approval-options Button, #model-options Button, #thinking-options Button {
        width: 100%;
        height: 1;
        background: transparent;
        border: none;
        color: #eeeeee;
        text-align: left;
        padding: 0 3;
        margin: 0;
    }
    #plan-options Button:hover, #approval-options Button:hover, #model-options Button:hover, #thinking-options Button:hover {
        border: none;
        border-top: none;
        border-bottom: none;
        background: #fab283;
        color: #0a0a0a;
    }

    #attached-files {
        width: 100%;
        height: auto;
        padding: 0 0 0 4;
        color: #808080;
        background: #0a0a0a;
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
        with Vertical(id="input-area"):
            with Horizontal(id="message-row"):
                yield Input(
                    placeholder="Type a message...",
                    id="message-input",
                )

            with Horizontal(id="controls-row"):
                yield Button("+", id="attach-btn")

                # Plan/Build toggle dropdown
                with Container(id="plan-drop"):
                    yield Button("Plan", id="plan-trigger")
                    with Container(id="plan-options"):
                        yield Button("Plan", id="plan-opt-plan")
                        yield Button("Build", id="plan-opt-build")

                # Approval dropdown
                with Container(id="approval-drop"):
                    yield Button("Ask for approval", id="approval-trigger")
                    with Container(id="approval-options"):
                        for label, value in APPROVAL_LEVELS:
                            yield Button(label, id=f"approval-{value}")

                # Model dropdown
                with Container(id="model-drop"):
                    yield Button("Claude 3.5 Sonnet", id="model-trigger")
                    with Container(id="model-options"):
                        for label, value in MODELS:
                            sid = value.replace(".", "-")
                            yield Button(label, id=f"model-{sid}")

                # Thinking dropdown
                with Container(id="thinking-drop"):
                    yield Button("Medium", id="thinking-trigger")
                    with Container(id="thinking-options"):
                        for label, value in THINKING_LEVELS:
                            yield Button(label, id=f"thinking-{value}")

        with Container(id="attached-files", classes="hidden"):
            yield Static("", id="attached-files-label")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn_id = event.button.id
        if btn_id == "attach-btn":
            self.post_message(self.FileAttached(""))
        elif btn_id == "plan-opt-plan":
            self._set_plan_mode(True)
        elif btn_id == "plan-opt-build":
            self._set_plan_mode(False)

        elif btn_id == "plan-trigger":
            self._toggle_dropdown("plan-options")
        elif btn_id == "approval-trigger":
            self._toggle_dropdown("approval-options")
        elif btn_id == "model-trigger":
            self._toggle_dropdown("model-options")
        elif btn_id == "thinking-trigger":
            self._toggle_dropdown("thinking-options")

        elif btn_id and btn_id.startswith("approval-"):
            self._select_dropdown_option("approval", btn_id, event.button.label)
        elif btn_id and btn_id.startswith("model-"):
            self._select_dropdown_option("model", btn_id, event.button.label)
        elif btn_id and btn_id.startswith("thinking-"):
            self._select_dropdown_option("thinking", btn_id, event.button.label)

    def _set_plan_mode(self, plan: bool) -> None:
        self.plan_mode = plan
        trigger = self.query_one("#plan-trigger", Button)
        trigger.label = "Plan" if plan else "Build"
        self._close_all_dropdowns()

    def _toggle_dropdown(self, options_id: str) -> None:
        options = self.query_one(f"#{options_id}", Container)
        if options.has_class("open"):
            options.remove_class("open")
        else:
            self._close_all_dropdowns()
            options.add_class("open")

    def _close_all_dropdowns(self) -> None:
        for oid in ("plan-options", "approval-options", "model-options", "thinking-options"):
            try:
                opt = self.query_one(f"#{oid}", Container)
                opt.remove_class("open")
            except Exception:
                pass

    def _select_dropdown_option(self, prefix: str, btn_id: str, label: str) -> None:
        trigger_id = f"{prefix}-trigger"
        trigger = self.query_one(f"#{trigger_id}", Button)
        trigger.label = str(label)
        self._close_all_dropdowns()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "message-input":
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
            trigger = self.query_one("#plan-trigger", Button)
            approval = self.query_one("#approval-drop", Container)
            if self.plan_mode:
                trigger.label = "Plan"
                approval.remove_class("hidden")
            else:
                trigger.label = "Build"
                approval.add_class("hidden")
        except Exception:
            pass
