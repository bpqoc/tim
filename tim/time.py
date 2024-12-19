from abc import ABC, abstractmethod
from datetime import datetime, timezone
from dataclasses import dataclass, field
from dateutil import tz


class Time(ABC):
    @abstractmethod
    def get_time(self) -> datetime:
        pass

    def show(self):
        return f"{self.get_time().strftime("%Y-%m-%d %H:%M")}"


@dataclass
class TimeSet(Time):
    time: datetime = field(
        default_factory=lambda: datetime.now(tz.tzlocal()).replace(second=0)
    )

    def get_time(self):
        return self.time.replace(second=0)

    def update(self, year=None, month=None, day=None, hour=None, minute=None):
        print(f"update {year} {month} {day} {hour} {minute}")
        if year is not None:
            self.time = self.time.replace(year=year)
        if month is not None:
            self.time = self.time.replace(month=month)
        if day is not None:
            self.time = self.time.replace(day=day)
        if hour is not None:
            self.time = self.time.replace(hour=hour)
        if minute is not None:
            self.time = self.time.replace(minute=minute)

    def set(self):
        return self


@dataclass
class TimeFloat(Time):
    def get_time(self):
        return datetime.now(tz.tzlocal()).replace(second=0)

    def update(self, **kwargs):
        pass

    def set(self):
        # convert to a set time using the current time
        return TimeSet()
