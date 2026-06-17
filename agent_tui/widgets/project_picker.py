from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Button, Input
from textual.widget import Widget
from textual.message import Message
from textual.reactive import reactive

from agent_tui.data import PROJECTS
from agent_tui.theme import render_css

OPTION_CONTENT_GUTTER = 2  # safety margin
_MORE_LABELS = ["Show more...", "Add new project", "Don't work in a project"]
PROJECT_OPTIONS_WIDTH = (
    max(len(label) for label in list(PROJECTS) + _MORE_LABELS) + OPTION_CONTENT_GUTTER
)


class ProjectPicker(Widget):
    """Project selector dropdown (overlay style, matches model/thinking dropdowns)."""

    DEFAULT_CSS = render_css(
        """
    ProjectPicker {
        width: auto;
        height: 1;
    }

    #project-drop {
        width: auto;
        height: 1;
        min-width: 0;
        margin: 0;
    }

    #project-trigger {
        width: auto;
        height: 1;
        background: transparent;
        border: none;
        color: $TEXT_PRIMARY;
        margin: 0;
        padding: 0 0;
        text-align: left;
        content-align: left middle;
    }

    #project-options {
        display: none;
        width: auto;
        min-width: 0;
        height: auto;
        background: $SURFACE_BACKGROUND;
        border: none;
        padding: 0;
        overlay: screen;
        align-horizontal: left;
    }
    #project-options.open {
        display: block;
    }

    #project-search-input {
        width: 100%;
        height: 1;
        background: transparent;
        border: none;
        color: $TEXT_PRIMARY;
        padding: 0 1;
    }

    #project-list {
        width: 100%;
        height: auto;
        padding: 0;
    }

    #project-options Button {
        width: 100%;
        height: 1;
        background: transparent;
        background-tint: transparent;
        tint: transparent;
        border: none;
        color: $TEXT_PRIMARY;
        text-align: left;
        content-align: left middle;
        padding: 0 0;
        margin: 0;
    }
    #project-options Button:hover,
    #project-options Button:focus,
    #project-options Button.-active {
        border: none;
        border-top: none;
        border-bottom: none;
        background: $TEXT_PRIMARY;
        background-tint: transparent;
        tint: transparent;
        color: $PAGE_BACKGROUND;
    }

    #project-options #more-trigger {
        width: 100%;
        height: 1;
        background: transparent;
        border: none;
        color: $TEXT_MUTED;
        text-align: left;
        content-align: left middle;
        padding: 0 0;
        margin: 0;
    }
    #project-options #more-trigger:hover {
        background: $TEXT_PRIMARY;
        color: $PAGE_BACKGROUND;
    }

    #more-options {
        display: none;
        height: auto;
        padding: 0;
    }
    #more-options.open {
        display: block;
    }
    #more-options Button {
        width: 100%;
        height: 1;
        background: transparent;
        border: none;
        color: $TEXT_PRIMARY;
        text-align: left;
        content-align: left middle;
        padding: 0 0;
        margin: 0;
    }
    #more-options Button:hover {
        background: $TEXT_PRIMARY;
        color: $PAGE_BACKGROUND;
    }
    """
    )

    current_project = reactive("")
    _all_projects: list[str] = PROJECTS.copy()

    class ProjectSelected(Message):
        def __init__(self, project: str) -> None:
            super().__init__()
            self.project = project

    class NoProject(Message):
        pass

    class AddProject(Message):
        pass

    def on_mount(self) -> None:
        options = self.query_one("#project-options", Container)
        options.styles.width = PROJECT_OPTIONS_WIDTH
        options.styles.min_width = PROJECT_OPTIONS_WIDTH
        self._fit_trigger()

    def compose(self) -> ComposeResult:
        with Container(id="project-drop"):
            yield Button("Work in a project", id="project-trigger")
            with Container(id="project-options"):
                yield Input(placeholder="Search Project...", id="project-search-input")
                with Container(id="project-list"):
                    for proj in self._all_projects:
                        yield Button(proj, classes="project-item")
                yield Button("Show more...", id="more-trigger")
                with Container(id="more-options"):
                    yield Button("Add new project", id="add-project-btn")
                    yield Button("Don't work in a project", id="no-project-btn")

    def _fit_trigger(self) -> None:
        drop = self.query_one("#project-drop", Container)
        trigger = self.query_one("#project-trigger", Button)
        label_width = len(str(trigger.label)) + 2
        drop.styles.width = label_width
        trigger.styles.width = label_width

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn_id = event.button.id

        if btn_id == "project-trigger":
            self._toggle_dropdown()
            event.stop()
            return

        if btn_id == "more-trigger":
            self._toggle_more()
            event.stop()
            return

        project_buttons = self.query("#project-list Button")
        for btn in project_buttons:
            if btn.id == event.button.id:
                proj_name = str(event.button.label)
                self.current_project = proj_name
                trigger = self.query_one("#project-trigger", Button)
                trigger.label = proj_name
                self._fit_trigger()
                self._close_dropdown()
                self.post_message(self.ProjectSelected(proj_name))
                event.stop()
                return

        if btn_id == "add-project-btn":
            self._close_dropdown()
            self.post_message(self.AddProject())
            event.stop()
        elif btn_id == "no-project-btn":
            self._close_dropdown()
            self.current_project = ""
            trigger = self.query_one("#project-trigger", Button)
            trigger.label = "Work in a project"
            self._fit_trigger()
            self.post_message(self.NoProject())
            event.stop()

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "project-search-input":
            query = event.value.lower()
            project_items = self.query("#project-list Button")
            for item in project_items:
                label = str(item.label).lower()
                item.display = query in label if query else True

    def _toggle_dropdown(self) -> None:
        options = self.query_one("#project-options", Container)
        if options.has_class("open"):
            options.remove_class("open")
        else:
            self._close_chat_input_dropdowns()
            options.add_class("open")

    def _close_chat_input_dropdowns(self) -> None:
        try:
            chat_input = self.app.query_one("#chat-input")
            chat_input._close_all_dropdowns()
        except Exception:
            pass

    def _toggle_more(self) -> None:
        more = self.query_one("#more-options", Container)
        if more.has_class("open"):
            more.remove_class("open")
        else:
            more.add_class("open")

    def _close_dropdown(self) -> None:
        options = self.query_one("#project-options", Container)
        options.remove_class("open")
        try:
            more = self.query_one("#more-options", Container)
            more.remove_class("open")
        except Exception:
            pass
