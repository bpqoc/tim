from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalScroll
from textual.reactive import reactive
from textual.widgets import (
    Footer,
    Header,
    Button,
    Digits,
    Welcome,
    Select,
    TextArea,
    Input,
)
from textual import on

from tim import event, project

PROJECTS = project.ProjectTable.load()
EVENTS = event.EventTable.load()


class ProjectSelect(Select):
    project_list = reactive([])

    def watch_project_list(self, project_list):
        self.from_values(project_list)


class TaskSelect(Select):
    task_list = reactive([])

    def watch_task_list(self, task_list):
        self.from_values(task_list)


class EventDef(HorizontalGroup):
    def compose(self):
        yield ProjectSelect(
            [(project.name, project.id) for (_, project) in PROJECTS.list_projects()],
            id="project",
        )
        yield TaskSelect([], id="task")
        yield Input()
        yield Button("Save", id="save")

    @on(Select.Changed, "#project")
    def project_select(self):
        project_id = self.query_one("#project").value
        task_list = [
            (task.name, task.id)
            for (_, task) in PROJECTS.get_project(project_id).list_tasks()
        ]
        self.query_one("#task").set_options(task_list)

class EventDisplay(HorizontalGroup):
    def compose(self):
        yield 

# class EventDefinition(HorizontalGroup):
#     project_list = reactive(PROJECTS.list_projects)
#     task_list = reactive([])

#     def compose(self) -> ComposeResult:
#         yield Select(
#             [(project.name, project.id) for (_, project) in self.project_list],
#             id="project",
#         )
#         yield Select(self.task_list, id="task")
#         yield Input()

#     @on(Select.Changed, "#project")
#     def select_project(self):
#         project_id = self.query_one("#project").value
#         self.task_list = [
#             (task.name, task.id)
#             for (_, task) in PROJECTS.get_project(project_id).list_tasks()
#         ]
#         self.task_list = [
#             (task.name, task.id)
#             for (_, task) in PROJECTS.get_project(project_id).list_tasks()
#         ]

#     def watch_task_list(self, task_list):

#         self.query_one("#task").update(task_list)


class TimApp(App):
    CSS_PATH = "static/css/app.tcss"

    def compose(self):
        yield Header()
        yield Footer()
        yield EventDef()


def main():
    """
    Textual app
    """
    app = TimApp()
    app.run()
