from __future__ import annotations

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Label, Tree, Static

from agent_tui.data import PROJECT_NAME, PROJECT_LOGO
from agent_tui.theme import render_css
from agent_tui.widgets.sidebar import Sidebar
from agent_tui.widgets.chat_input import ChatInput
from agent_tui.widgets.chat_view import ChatView
from agent_tui.widgets.project_picker import ProjectPicker
from agent_tui.widgets.settings import SettingsModal


class AgentTUIApp(App):
    """Main Agent TUI application."""

    CSS = render_css(
        """
    Screen {
        background: $PAGE_BACKGROUND;
        color: $TEXT_PRIMARY;
        overflow: hidden;
    }

    #top-bar {
        height: 1;
        dock: top;
        background: $PAGE_BACKGROUND;
        padding: 0 1;
    }

    #sidebar-toggle {
        width: 3;
        min-width: 3;
        height: 1;
        border: none;
        background: transparent;
        color: $TEXT_PRIMARY;
        padding: 0;
        content-align: center middle;
    }
    #sidebar-toggle:hover {
        background: $SURFACE_BACKGROUND;
    }

    #main-area {
        width: 1fr;
        height: 1fr;
    }

    #project-title-wrap {
        width: 100%;
        height: auto;
        align-horizontal: center;
    }

    #chat-input-wrap {
        width: 100%;
        height: auto;
        align-horizontal: center;
    }
    #chat-input-wrap > #chat-input {
        margin: 0;
    }

    #project-title {
        width: auto;
        height: 3;
        text-align: left;
        margin-bottom: 2;
        padding: 0;
    }
    #project-title.hidden {
        display: none;
    }

    #messages-view {
        display: none;
        height: 1fr;
        background: $PAGE_BACKGROUND;
    }
    #messages-view.visible {
        display: block;
    }

    #input-wrapper {
        width: 100%;
        height: auto;
    }
    #input-wrapper.welcome {
        height: 1fr;
        align-vertical: middle;
    }
    #input-wrapper.welcome #chat-input {
        padding: 0;
    }

    #bottom-area {
        dock: bottom;
        height: auto;
        background: $PAGE_BACKGROUND;
        padding: 0 1;
    }

    #bottom-bar {
        height: auto;
    }

    #context-label {
        text-align: right;
        color: $TEXT_MUTED;
        padding-right: 1;
        height: 1;
    }
    """
    )

    BINDINGS = [
        ("escape", "dismiss", "Dismiss"),
    ]

    sidebar_visible: bool = False

    def compose(self) -> ComposeResult:
        yield Sidebar(id="sidebar", classes="sidebar-hidden")

        with Vertical(id="main-area"):
            with Horizontal(id="top-bar"):
                yield Button("\u2630", id="sidebar-toggle")

            yield ChatView(id="messages-view")

            with Vertical(id="input-wrapper", classes="welcome"):
                with Container(id="project-title-wrap"):
                    yield Static(PROJECT_LOGO, id="project-title")
                with Container(id="chat-input-wrap"):
                    yield ChatInput(id="chat-input")

            with Container(id="bottom-area"):
                with Horizontal(id="bottom-bar"):
                    yield ProjectPicker(id="project-picker")
                    yield Label("Context: 0.0k (0%)", id="context-label")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn_id = event.button.id
        if btn_id == "sidebar-toggle":
            self.toggle_sidebar()
        elif btn_id == "side-new-chat":
            self.new_chat()
        elif btn_id == "side-settings":
            self.push_screen(SettingsModal())

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        pass

    def on_chat_input_send(self, event: ChatInput.Send) -> None:
        chat_input = self.query_one("#chat-input", ChatInput)
        if not chat_input.chat_active:
            self.start_chat()
            chat_input.chat_active = True
        chat_view = self.query_one("#messages-view", ChatView)
        chat_view.add_message("user", event.content)

    def toggle_sidebar(self) -> None:
        self.sidebar_visible = not self.sidebar_visible
        sidebar = self.query_one("#sidebar", Sidebar)
        if self.sidebar_visible:
            sidebar.remove_class("sidebar-hidden")
            sidebar.add_class("sidebar-visible")
        else:
            sidebar.remove_class("sidebar-visible")
            sidebar.add_class("sidebar-hidden")

    def action_dismiss(self) -> None:
        if self.sidebar_visible:
            self.toggle_sidebar()
        elif self.is_modal_open:
            self.pop_screen()

    @property
    def is_modal_open(self) -> bool:
        return len(self.screen_stack) > 1

    def new_chat(self) -> None:
        if self.sidebar_visible:
            self.toggle_sidebar()
        messages = self.query_one("#messages-view", ChatView)
        chat_input = self.query_one("#chat-input", ChatInput)
        input_wrapper = self.query_one("#input-wrapper", Vertical)
        project_title = self.query_one("#project-title", Static)
        chat_input.chat_active = False
        chat_input.remove_class("stretch")
        project_title.remove_class("hidden")
        messages.remove_class("visible")
        messages.clear()
        input_wrapper.add_class("welcome")

    def start_chat(self) -> None:
        messages = self.query_one("#messages-view", ChatView)
        input_wrapper = self.query_one("#input-wrapper", Vertical)
        chat_input = self.query_one("#chat-input", ChatInput)
        project_title = self.query_one("#project-title", Static)
        project_title.add_class("hidden")
        messages.add_class("visible")
        input_wrapper.remove_class("welcome")
        chat_input.add_class("stretch")
