from __future__ import annotations

from textual.app import ComposeResult
from textual.widgets import Button, Label, Tree
from textual.containers import Vertical, Container

from agent_tui.data import PROJECTS, SAMPLE_CHATS, ORPHAN_CHATS
from agent_tui.theme import render_css


class Sidebar(Vertical):
    """Left sidebar with New Chat, Projects tree, Chats tree, and Settings."""

    DEFAULT_CSS = render_css(
        """
    Sidebar {
        width: 32;
        height: 1fr;
        dock: left;
        background: $SURFACE_BACKGROUND;
        border-right: none;
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
        padding: 1;
    }

    Sidebar Button {
        width: 100%;
        text-align: left;
        border: none;
        background: transparent;
        color: $TEXT_PRIMARY;
        padding: 0 1;
    }
    Sidebar Button:hover {
        background: $PAGE_BACKGROUND;
    }

    #side-new-chat {
        height: 3;
        text-align: left;
        margin-bottom: 1;
        background: transparent;
        color: $TEXT_PRIMARY;
    }

    Sidebar Tree {
        background: transparent;
        padding: 0;
        margin: 0;
    }

    Sidebar > #sidebar-bottom-spacer {
        height: 1fr;
    }

    #side-settings {
        height: 3;
        margin-top: 1;
    }
    """
    )

    def compose(self) -> ComposeResult:
        with Vertical(id="sidebar-content"):
            yield Button("+  New Chat", id="side-new-chat")

            yield Tree("Projects", id="projects-tree")

            yield Tree("Chats", id="chats-tree")

            yield Container(id="sidebar-bottom-spacer")

            yield Button("\u2699  Settings", id="side-settings")

    def on_mount(self) -> None:
        self._populate_trees()

    def _populate_trees(self) -> None:
        projects_tree = self.query_one("#projects-tree", Tree)

        for proj in PROJECTS:
            proj_node = projects_tree.root.add(proj, expand=False)
            chats = SAMPLE_CHATS.get(proj, [])
            for chat in reversed(chats):
                proj_node.add_leaf(f"  {chat}")

        chats_tree = self.query_one("#chats-tree", Tree)
        for chat in ORPHAN_CHATS:
            chats_tree.root.add_leaf(chat)

        projects_tree.root.expand()
        chats_tree.root.expand()
