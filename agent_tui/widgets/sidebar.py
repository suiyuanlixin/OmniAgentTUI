from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Static
from textual import events

from agent_tui.data import PROJECTS, SAMPLE_CHATS, ORPHAN_CHATS
from agent_tui.theme import render_css


class SidebarActionButton(Button, can_focus=False):
    """Flat sidebar button without Textual's focus/press visuals."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.active_effect_duration = 0


class Sidebar(Vertical):
    """Left sidebar with flat project/chat lists and action buttons."""

    DEFAULT_CSS = render_css(
        """
    Sidebar {
        width: 100%;
        height: 1fr;
        background: $SURFACE_BACKGROUND;
        padding: 0;
        display: none;
    }
    Sidebar.sidebar-visible {
        display: block;
    }
    Sidebar.sidebar-hidden {
        display: none;
    }

    Sidebar > #sidebar-content {
        height: 1fr;
        background: $SURFACE_BACKGROUND;
        padding: 0;
        overflow-y: auto;
        scrollbar-size: 0 0;
    }

    Sidebar Button.sidebar-action {
        width: 100%;
        min-width: 1;
        height: 1;
        margin: 0;
        border: none;
        background: transparent;
        background-tint: transparent;
        tint: transparent;
        color: $TEXT_PRIMARY;
        padding: 0;
        text-align: left;
        content-align: left middle;
    }
    Sidebar Button.sidebar-action:hover,
    Sidebar Button.sidebar-action:focus,
    Sidebar Button.sidebar-action.-active {
        border: none;
        border-top: none;
        border-bottom: none;
        background: transparent;
        background-tint: transparent;
        tint: transparent;
        color: $TEXT_PRIMARY;
    }

    #side-new-chat {
        width: 100%;
        margin: 1 1 1 1;
        background: $SURFACE_BACKGROUND;
        background-tint: transparent;
        tint: transparent;
        color: $TEXT_PRIMARY;
    }
    #side-new-chat:hover,
    #side-new-chat:focus,
    #side-new-chat.-active,
    #side-new-chat:focus-within {
        background: $SURFACE_BACKGROUND;
        background-tint: transparent;
        tint: transparent;
        color: $TEXT_PRIMARY;
    }

    .sidebar-section-title {
        width: 100%;
        height: 1;
        color: $TEXT_MUTED;
        background: transparent;
        padding: 0 0 0 2;
        margin: 0;
        content-align: left middle;
    }
    .sidebar-section-title:hover {
        color: $TEXT_PRIMARY;
    }
    #chats-title {
        margin-top: 1;
    }

    .sidebar-list {
        width: 100%;
        height: auto;
        padding: 0;
        margin: 0;
    }
    .sidebar-list.hidden {
        display: none;
    }

    .sidebar-item {
        width: 100%;
        height: 1;
        color: $TEXT_PRIMARY;
        background: transparent;
        padding: 0 0 0 2;
        margin: 0;
        content-align: left middle;
    }
    .sidebar-item:hover {
        background: $TEXT_PRIMARY;
        color: $PAGE_BACKGROUND;
    }
    .sidebar-chat-item {
        padding: 0 0 0 4;
    }
    .sidebar-empty-item {
        color: $TEXT_MUTED;
    }
    .sidebar-empty-item:hover {
        background: transparent;
        color: $TEXT_MUTED;
    }

    #side-settings {
        dock: bottom;
        width: 100%;
        height: 1;
        margin: 0;
        padding: 0;
        border: none;
        background: $SURFACE_BACKGROUND;
        background-tint: transparent;
        tint: transparent;
        color: $TEXT_PRIMARY;
        text-style: bold;
    }
    #side-settings:hover,
    #side-settings:focus,
    #side-settings.-active {
        border: none;
        background: $SURFACE_BACKGROUND;
        background-tint: transparent;
        tint: transparent;
        color: $TEXT_PRIMARY;
        text-style: bold;
    }
    """
    )

    def compose(self) -> ComposeResult:
        new_chat = SidebarActionButton(
            "New Chat", id="side-new-chat", classes="sidebar-action"
        )
        yield new_chat
        with Vertical(id="sidebar-content"):
            yield Static(
                "Projects", id="projects-title", classes="sidebar-section-title"
            )
            with Vertical(id="projects-list", classes="sidebar-list"):
                for index, project in enumerate(PROJECTS):
                    yield Static(project, id=f"project-{index}", classes="sidebar-item")
                    with Vertical(
                        id=f"project-chats-{index}",
                        classes="sidebar-list project-chat-list hidden",
                    ):
                        chats = list(reversed(SAMPLE_CHATS.get(project, [])))
                        if chats:
                            for chat in chats:
                                yield Static(
                                    chat,
                                    classes="sidebar-item sidebar-chat-item",
                                )
                        else:
                            yield Static(
                                "No chats",
                                classes="sidebar-item sidebar-chat-item sidebar-empty-item",
                            )
            yield Static("Chats", id="chats-title", classes="sidebar-section-title")
            with Vertical(id="chats-list", classes="sidebar-list"):
                for chat in ORPHAN_CHATS:
                    yield Static(chat, classes="sidebar-item")
                yield Static("", classes="sidebar-item")

        settings = SidebarActionButton(
            "= Settings", id="side-settings", classes="sidebar-action"
        )
        yield settings

    def on_click(self, event: events.Click) -> None:
        if not event.control or not event.control.id:
            return

        if event.control.id == "projects-title":
            lst = self.query_one("#projects-list", Vertical)
            if lst.has_class("hidden"):
                lst.remove_class("hidden")
            else:
                lst.add_class("hidden")
        elif event.control.id == "chats-title":
            lst = self.query_one("#chats-list", Vertical)
            if lst.has_class("hidden"):
                lst.remove_class("hidden")
            else:
                lst.add_class("hidden")
        elif event.control.id.startswith(
            "project-"
        ) and not event.control.id.startswith("project-chats-"):
            index = event.control.id.removeprefix("project-")
            lst = self.query_one(f"#project-chats-{index}", Vertical)
            if lst.has_class("hidden"):
                lst.remove_class("hidden")
            else:
                lst.add_class("hidden")
