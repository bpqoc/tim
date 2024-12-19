from tim.constants import EVENT_TABLE_LOCATION
from tim.project import ProjectTable

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import pickle
import os


class Event(ABC):
    pass


@dataclass
class EventID(Event):
    id: int

    def show(self, projects, events):
        event_def = events.get_event(self.id)
        return event_def.show(projects)

    def is_empty(self):
        return False


@dataclass
class EventEmpty(Event):

    def set_id(self, id):
        return EventID(id)

    def show(self, projects, events):
        return "Nothing"

    def is_empty(self):
        return True


@dataclass
class EventDefinition:
    project_id: int
    task_id: int
    description: str

    def show(self, projects: ProjectTable):
        project = projects.get_project(self.project_id)
        task = project.get_task(self.task_id)
        return f"{project.name} - {task.name} | {self.description}"


# NOTE: using a dict since I don't want to have to deal with when deleting an event all the ID's after it shift
# this could be avoided by just markings things inactive, but not going to bother
@dataclass
class EventTable:
    table: dict = field(default_factory=dict)
    last_key: int = field(init=False, default=0)

    def add_event(self, event: EventDefinition):
        self.last_key += 1
        self.table[self.last_key] = event
        return self.last_key

    def delete_event(self, event_id: int):
        if event_id in self.table:
            return self.table.pop(event_id)
        else:
            return None

    def list_events(self):
        return self.table.items()

    def get_event(self, event_id: int):
        return self.table.get(event_id)

    @classmethod
    def load(cls, file=EVENT_TABLE_LOCATION):
        with open(file, "rb") as f:
            return pickle.load(f)

    def save(self, file=EVENT_TABLE_LOCATION):
        os.makedirs(os.path.dirname(file), exist_ok=True)
        with open(file, "wb") as f:
            # print(f"Saving to {file}")
            pickle.dump(self, f)
