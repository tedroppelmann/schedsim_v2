class Task:

    def __init__(self, real_time, _type, _id, period, activation, deadline, wcet):
        self.real_time = real_time
        self.type = _type
        self.id = _id
        self.period = period
        self.activation = activation
        self.deadline = deadline
        self.wcet = wcet
