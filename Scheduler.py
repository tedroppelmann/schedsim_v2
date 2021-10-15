from abc import *
import SchedEvent
import SchedIO


class Scheduler:

    def __init__(self):
        self.name = 'GenericScheduler'
        self.tasks = []
        self.start = None
        self.end = None

        self.executing = None

        self.arrival_events = []
        self.finish_events = []
        self.deadline_events = []
        self.start_events = []

        self.output_file = SchedIO.SchedulerEventWriter()

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def is_feasible(self, tasks):
        return NotImplementedError

    def get_all_arrivals(self):
        arrival_events = []
        for task in self.tasks:
            if task.type == 'periodic':
                i = self.start
                j = 1
                while i < self.end:
                    event = SchedEvent.ScheduleEvent(i, task, SchedEvent.EventType.activation.value)
                    event.job = j
                    arrival_events.append(event)
                    i += i + task.period
                    j += 1
            elif task.type == 'sporadic':
                event = SchedEvent.ScheduleEvent(task.activation, task, SchedEvent.EventType.activation.value)
                arrival_events.append(event)
        arrival_events.sort(key=lambda x: x.timestamp)
        return arrival_events

    def find_finish_events(self, time):
        helper_list = []
        for event in self.finish_events:
            if event.timestamp == time:
                self.output_file.add_scheduler_event(event)
                self.executing = None
            elif event.timestamp > time:
                helper_list.append(event)
        self.finish_events = helper_list

    def find_deadline_events(self, time):
        helper_list = []
        for event in self.deadline_events:
            if event.timestamp == time:
                self.output_file.add_scheduler_event(event)
            elif event.timestamp > time:
                helper_list.append(event)
        self.deadline_events = helper_list

    def find_arrival_event(self, time):
        helper_list = []
        for event in self.arrival_events:
            if event.timestamp == time:
                self.output_file.add_scheduler_event(event)
                start_event = SchedEvent.ScheduleEvent(
                    event.timestamp, event.task, SchedEvent.EventType.start.value)
                start_event.job = event.job
                self.start_events.append(start_event)
            elif event.timestamp > time:
                helper_list.append(event)
        self.arrival_events = helper_list


class NonPreemptive(Scheduler):

    def __init__(self):
        super().__init__()
        self.name = 'GenericNonPreemptiveScheduler'

    def execute(self):
        pass

    def is_feasible(self, tasks):
        pass

    def find_start_events(self, time):
        helper_list = []
        for event in self.start_events:
            if event.timestamp == time and self.executing is None:
                self.output_file.add_scheduler_event(event)
                self.executing = event
                # Create finish event:
                finish_timestamp = event.timestamp + event.task.wcet
                finish_event = SchedEvent.ScheduleEvent(
                    finish_timestamp, event.task, SchedEvent.EventType.finish.value)
                finish_event.job = event.job
                self.finish_events.append(finish_event)
                # Create deadline event:
                if event.task.real_time:
                    deadline_timestamp = event.timestamp + event.task.deadline
                    deadline_event = SchedEvent.ScheduleEvent(
                        deadline_timestamp, event.task, SchedEvent.EventType.deadline.value)
                    deadline_event.job = event.job
                    self.deadline_events.append(deadline_event)
            elif event.timestamp == time and self.executing:
                event.timestamp += (self.executing.timestamp + self.executing.task.wcet - event.timestamp)
            if event.timestamp > time:
                helper_list.append(event)
        self.start_events = helper_list


class FIFO(NonPreemptive):

    def __init__(self):
        super().__init__()
        self.name = 'FIFO'

    def execute(self):
        self.arrival_events = self.get_all_arrivals()

        time = self.start
        while time <= self.end:
            self.find_finish_events(time)
            self.find_deadline_events(time)
            self.find_arrival_event(time)
            self.find_start_events(time)
            time += 1

        self.output_file.terminate_write()

    def is_feasible(self, tasks):
        pass


class SJF(NonPreemptive):

    def __init__(self):
        super().__init__()
        self.name = 'SJF'

    def execute(self):
        self.arrival_events = self.get_all_arrivals()

        time = self.start
        while time <= self.end:
            self.find_finish_events(time)
            self.find_deadline_events(time)
            self.find_arrival_event(time)
            self.start_events.sort(key=lambda x: x.task.wcet)
            self.find_start_events(time)
            time += 1

    def is_feasible(self, tasks):
        pass


class HRRN(NonPreemptive):

    def __init__(self):
        super().__init__()
        self.name = 'HRRN'

    def execute(self):
        self.arrival_events = self.get_all_arrivals()

        time = self.start
        while time <= self.end:
            self.calculate_responsive_ratio(time)
            self.find_finish_events(time)
            self.find_deadline_events(time)
            self.find_arrival_event(time)
            self.start_events.sort(key=lambda x: x.response_ratio, reverse=True)
            self.find_start_events(time)
            time += 1

    def calculate_responsive_ratio(self, time):
        for event in self.arrival_events:
            if event.timestamp <= time:
                event.response_ratio += 1/event.task.wcet

    def is_feasible(self, tasks):
        pass


class RoundRobin(Scheduler):

    def __init__(self, quantum):
        super().__init__()
        self.name = 'RoundRobin'
        self.deadlineNeeded = False
        self.quantum = quantum

    def execute(self):
        pass

    def is_feasible(self, tasks):
        pass
