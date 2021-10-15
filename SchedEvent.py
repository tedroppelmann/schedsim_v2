from enum import Enum


class EventType(Enum):
    activation = 'A'
    deadline = 'D'
    worst_case_finish_time = 'W'
    start = 'S'
    finish = 'F'
    deadline_miss = 'M'
    preemption = 'P'


class ScheduleEvent:

    def __init__(self, timestamp, task, _type):
        self.timestamp = timestamp
        self.task = task
        self.job = 0
        self.processor = 0
        self.type = _type
        self.extra = 0
        self.response_ratio = 1
