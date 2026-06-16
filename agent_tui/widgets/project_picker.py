from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Input, Static
from textual.widget import Widget
from textual.message import Message
from textual.reactive import reactive

from agent_tui.data import PROJECTS
from agent_tui.theme import render_css


class ProjectPicker(Widget):
    """Project selector dropdown at bottom-left."""

    DEFAULT_CSS = render_css(
        """
    ProjectPicker {
        width: auto;
        height: auto;
    }

    #picker-vertical {
        width: auto;
        height: auto;
    }

    #project-trigger {
        width: 28;
        height: 1;
        background: transparent;
        border: none;
        color: $TEXT_PRIMARY;
        text-align: left;
        padding: 0 1;
    }
    #project-trigger:hover {
        background: $SURFACE_BACKGROUND;
    }

    #project-dropdown {
        width: 40;
        height: auto;
        display: none;
        background: $PAGE_BACKGROUND;
        border: none;
        padding: 0;
    }
    #project-dropdown.open {
        display: block;
    }

    #project-search-input {
        width: 100%;
        height: 3;
        background: $SURFACE_BACKGROUND;
        border: none;
        border-bottom: solid $TEXT_MUTED;
        color: $TEXT_PRIMARY;
        padding: 0 1;
    }

    #project-list-scroll {
        max-height: 5;
        overflow-y: auto;
        width: 100%;
        padding: 0;
    }

    #project-list-scroll Button {
        width: 100%;
        height: 1;
        background: transparent;
        border: none;
        color: $TEXT_PRIMARY;
        text-align: left;
        padding: 0 1;
    }
    #project-list-scroll Button:hover {
        background: $SURFACE_BACKGROUND;
    }

    #project-dropdown-divider {
        width: 100%;
        height: 1;
        border-top: solid $TEXT_MUTED;
    }

    #project-bottom-actions {
        width: 100%;
        height: auto;
    }
    #project-bottom-actions Button {
        width: 100%;
        height: 1;
        background: transparent;
        border: none;
        color: $TEXT_MUTED;
        text-align: left;
        padding: 0 1;
    }
    #project-bottom-actions Button:hover {
        background: $SURFACE_BACKGROUND;
        color: $TEXT_PRIMARY;
    }
    """
    )

    current_project = reactive("")
    dropdown_open = reactive(False)
    _all_projects: list[str] = PROJECTS.copy()

    class ProjectSelected(Message):
        def __init__(self, project: str) -> None:
            super().__init__()
            self.project = project

    class NoProject(Message):
        pass

    class AddProject(Message):
        pass

    def compose(self) -> ComposeResult:
        with Vertical(id="picker-vertical"):
            yield Button("Select Project \u25bc", id="project-trigger")

            with Container(id="project-dropdown"):
                yield Input(placeholder="Search Project...", id="project-search-input")

                with Container(id="project-list-scroll"):
                    for proj in self._all_projects:
                        yield Button(proj, classes="project-item")

                yield Static(id="project-dropdown-divider")

                with Horizontal(id="project-bottom-actions"):
                    yield Button("+ Add new project", id="add-project-btn")
                    yield Button("Don't work in a project", id="no-project-btn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn_id = event.button.id

        if btn_id == "project-trigger":
            self.dropdown_open = not self.dropdown_open
            event.stop()
            return

        project_buttons = self.query("#project-list-scroll Button")
        for btn in project_buttons:
            if btn.id == event.button.id:
                proj_name = str(event.button.label)
                self.current_project = proj_name
                self.dropdown_open = False
                trigger = self.query_one("#project-trigger", Button)
                trigger.label = f"{proj_name} \u25bc"
                self.post_message(self.ProjectSelected(proj_name))
                event.stop()
                return

        if btn_id == "add-project-btn":
            self.dropdown_open = False
            self.post_message(self.AddProject())
            event.stop()
        elif btn_id == "no-project-btn":
            self.dropdown_open = False
            self.current_project = ""
            trigger = self.query_one("#project-trigger", Button)
            trigger.label = "Select Project \u25bc"
            self.post_message(self.NoProject())
            event.stop()

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "project-search-input":
            query = event.value.lower()
            project_items = self.query("#project-list-scroll Button")
            for item in project_items:
                label = str(item.label).lower()
                item.display = query in label if query else True

    def watch_dropdown_open(self, open_val: bool) -> None:
        dropdown = self.query_one("#project-dropdown", Container)
        if open_val:
            dropdown.add_class("open")
            search = self.query_one("#project-search-input", Input)
            search.focus()
        else:
            dropdown.remove_class("open")
