from tim.constants import PROJECT_TABLE_LOCATION

from dataclasses import dataclass, field
import pickle
import os

"""
Could have separate task and project tables so it mimics more closely the sql database structure,
but will likely never interact with the tasks independently of the project it is associated with so it makes the
separation not as useful.

Could always split them later if there is a good reason

Also worth noting that since this is mimicing the existing data it is just populating values which changes a
bit of the interface.
"""


@dataclass
class Task:
    id: int
    name: str


@dataclass
class Project:
    id: int
    name: str
    tasks: dict = field(default_factory=dict)

    def add_task(self, task: Task):
        self.tasks[task.id] = task

    def remove_task(self, task_id: int):
        return self.tasks.pop(task_id)

    def find_task(self, name: str) -> Task | None:
        for key, val in self.tasks:
            if val.name == name:
                return key
        return None

    def get_task(self, task_id: int) -> Task | None:
        return self.tasks.get(task_id)

    def list_tasks(self):
        return self.tasks.items()


@dataclass
class ProjectTable:
    table: dict = field(default_factory=dict)

    def add_project(self, project: Project):
        self.table[project.id] = project

    def remove_project(self, project_id: int):
        return self.table.pop(project_id)

    def find_project(self, name: str):
        for key, val in self.table.items():
            if val.name == name:
                return key
        return None

    def find_task(self, project_id: int, name: str):
        project = self.table.get(project_id)
        if project is None:
            return None
        else:
            return project.find_task(name)

    def get_project(self, project_id: int):
        return self.table.get(project_id)

    def get_task(self, project_id: int, task_id: int):
        project = self.get_project(project_id)
        if project is None:
            return None
        else:
            return project.get_task(task_id)

    def list_projects(self):
        return self.table.items()

    @classmethod
    def load(cls, file=PROJECT_TABLE_LOCATION):
        with open(file, "rb") as f:
            return pickle.load(f)

    def save(self, file=PROJECT_TABLE_LOCATION):
        os.makedirs(os.path.dirname(file), exist_ok=True)
        with open(file, "wb") as f:
            pickle.dump(self, f)
