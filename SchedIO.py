import xml.etree.ElementTree as ET
import Task
import Scheduler


# The idea of this function was based on SchedSim v1:
# https://github.com/HEAPLab/schedsim/blob/master/SchedIo.py
def import_file(file_path, output_file):
    scheduler = None
    root_node = ET.parse(file_path).getroot()
    if root_node.tag == 'simulation':
        if root_node[1][1].tag == 'scheduler':
            _scheduler = root_node[1][1]
            if _scheduler.attrib['algorithm'] == 'RR':
                if 'quantum' in _scheduler.attrib:
                    quantum = _scheduler.attrib['quantum']
                    scheduler = Scheduler.RoundRobin(output_file, quantum)
                else:
                    raise Exception(
                        'non "quantum" attribute are defined in the file')
            if _scheduler.attrib['algorithm'] == 'FIFO':
                scheduler = Scheduler.FIFO(output_file)
            if _scheduler.attrib['algorithm'] == 'SJF':
                scheduler = Scheduler.SJF(output_file)
            if _scheduler.attrib['algorithm'] == 'HRRN':
                scheduler = Scheduler.HRRN(output_file)
            if _scheduler.attrib['algorithm'] == 'SRTF':
                scheduler = Scheduler.SRTF(output_file)
        else:
            raise Exception(
                'non scheduler are defined in the file')

        if root_node[1].tag == 'software':
            if scheduler:
                task_root = root_node[1][0]
                for task_leaf in task_root:
                    _real_time = False
                    if task_leaf.attrib['real-time'] == 'true':
                        _real_time = True
                    _type = task_leaf.attrib['type']
                    _id = int(task_leaf.attrib['id'])
                    _period = -1
                    _activation = -1
                    _deadline = -1
                    _wcet = int(task_leaf.attrib['wcet'])
                    if task_leaf.attrib['type'] == 'periodic':
                        _period = int(task_leaf.attrib['period'])
                    if task_leaf.attrib['type'] == 'sporadic':
                        _activation = int(task_leaf.attrib['activation'])
                    if task_leaf.attrib['real-time'] == 'true':
                        _deadline = int(task_leaf.attrib['deadline'])

                    if _id < 0 or _wcet <= 0 or _period <= 0 and (_deadline <= 0 and not _deadline == -1):
                        raise Exception(
                            'non positive values are saved in the file')
                    if (_wcet > _period != -1) or (_deadline != -1 and _deadline < _wcet):
                        raise Exception(
                            'inconsistent values saved in the file')

                    task = Task.Task(_real_time, _type, _id, _period, _activation, _deadline, _wcet)
                    scheduler.tasks.append(task)
            else:
                raise Exception(
                    'non scheduler recognized in the file')

        if root_node[0].tag == 'time':
            time = root_node[0].attrib
            scheduler.start = int(time['start'])
            scheduler.end = int(time['end'])

    return scheduler


# This class was based on SchedSim v1:
# https://github.com/HEAPLab/schedsim/blob/master/SchedIo.py
class SchedulerEventWriter:
    def __init__(self, output_file):
        self.out = open(output_file, 'w')

    def add_scheduler_event(self, scheduler_event):
        self.out.write(
            str(scheduler_event.timestamp) + ',' + str(scheduler_event.task.id) + ',' +
            str(scheduler_event.job) + ',' + str(scheduler_event.processor) + ',' +
            str(scheduler_event.type) + ',' + str(scheduler_event.extra) + '\n')

    def terminate_write(self):
        self.out.close()
