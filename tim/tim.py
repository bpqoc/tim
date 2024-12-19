from tim.time import Time, TimeSet, TimeFloat
from tim.event import Event, EventID, EventEmpty
from dataclasses import dataclass, field
from datetime import datetime, date
from tim.constants import LOG_LOCATION
import os
import pickle


@dataclass
class Tim:
    """
    The object that maintains the list of times and event ids.
    The main interface to interact with.
    """

    times: list[Time]
    events: list[Event]
    start_date: datetime = field(default_factory=datetime.now)

    @classmethod
    def start(cls, id=None):
        """Standard starting configuration for a day"""
        if id is None:
            return cls([TimeSet(), TimeFloat()], [EventEmpty()])
        else:
            return cls([TimeSet(), TimeFloat()], [EventID(id)])

    def stop(self):
        final_time = self.times[-1].set()
        self.times[-1] = final_time

    def add(self, event_id):
        self.times[-1] = self.times[-1].set()
        self.times.append(TimeFloat())
        self.events.append(EventID(event_id))

    def update_time(self, index, **kwargs):
        print(f"update time {kwargs}")
        self.times[index].update(**kwargs)

    def update_event(self, index, id):
        event = self.events[index]
        if event.is_empty():
            self.events[index] = event.set_id(id)
        else:
            event.id = id

    @classmethod
    def load(cls, path):
        with open(path, "rb") as f:
            return pickle.load(f)

    def save(self, dir=LOG_LOCATION):
        os.makedirs(dir, exist_ok=True)
        path = os.path.join(dir, self.start_date.strftime("%Y-%m-%d"))
        path = f"{path}.pkl"
        with open(path, "wb") as f:
            pickle.dump(self, f)

    def delete(self, dir=LOG_LOCATION):
        path = os.path.join(dir, self.start_date.strftime("%Y-%m-%d"))
        path = f"{path}.pkl"
        os.remove(path)

    def show(self, projects, events):
        """
        A pretty printed version of the log
        """
        lines = []
        for i, event in enumerate(self.events):
            time = self.times[i]
            next_time = self.times[i + 1]
            lines.append(f"{i}) {time.show()}")

            # add spacing in 15 minute chunks
            diff = next_time.get_time() - time.get_time()
            minutes = diff.seconds // 60
            increments = ["  |"] * max((minutes - 1) // 15 + 1, 1)
            increments[len(increments) // 2] += f" {i}) {event.show(projects, events)}"

            lines.extend(increments)

        final_time = self.times[-1]
        lines.append(f"{len(self.times) - 1} ) {final_time.show()}")
        print("\n".join(lines))

    def export(self, events):
        lines = ["Date,Project/Database ID,Task/Database ID,Description,Quantity"]
        for i, event_id in enumerate(self.events):

            if event_id.is_empty():
                continue
            else:
                time = self.times[i]
                next_time = self.times[i + 1]
                event = events.get_event(event_id.id)
                date = time.get_time().strftime("%m/%d/%Y")
                project_id = event.project_id
                task_id = event.task_id
                description = event.description
                quantity = (next_time.get_time() - time.get_time()).seconds / 3600
                lines.append(
                    f'{date},{project_id},{task_id},"{description}",{quantity}'
                )
        return "\n".join(lines)


class TimManager:
    """
    Manage multiple days of time logging
    For now identifying by start date and storing all in a separate
    """

    def __init__(self, logs=None):
        if logs is None:
            self.logs = {}
        else:
            self.logs = logs

    @classmethod
    def load(cls, dir=LOG_LOCATION):
        logs = {}
        os.makedirs(dir, exist_ok=True)
        for path in os.listdir(dir):
            filename = os.path.basename(path)

            vals = filename.split(".")
            if len(vals) > 1 and vals[-1] == "pkl":
                try:
                    d = datetime.strptime(vals[0], "%Y-%m-%d")
                except ValueError as e:
                    print(
                        f"Expect files to have the format %Y-%m-%d.pkl, unrecognized {filename}."
                    )
                    continue
            else:
                print(
                    f"Expect files to have the format %Y-%m-%d.pkl, unrecognized {filename}."
                )
                continue
            logs[vals[0]] = Tim.load(os.path.join(dir, path))
        return cls(logs)

    def save(self, dir=LOG_LOCATION):
        # probably never called since you'll want to save the working file
        for name, content in self.logs().items():
            content.save(dir)

    def latest(self):
        if len(self.logs) == 0:
            return None
        items = iter(self.logs.items())
        first = next(items)
        max_date = first[0]
        latest_log = first[1]
        for d, log in items:
            if d > max_date:
                max_date = d
                latest_log = log
        return latest_log

    def get_log(self, key):
        return self.logs.get(key)

    def list_logs(self):
        return self.logs.items()

    def start(self):
        log = Tim.start()
        self.logs[log.start_date.strftime("%Y-%m-%d")] = log
        return log

    def delete(self, key):
        log = self.get_log(key)
        if log is not None:
            log.delete()
