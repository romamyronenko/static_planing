def get_html(arr):
    res = '<table>'
    for i in arr:
        res += '<tr>'
        for j in i:
            res += f'<td>{j}</td>'
        res += '</tr>'
    res += '</table>'

    template = f"<html><head><link rel='stylesheet' type='text/css' href='style.css'></head><body>{res}</body></html>"
    with open('index.html', 'w+') as f:
        f.write(template)


matrix = [[None for _ in range(16)] for _ in range(16)]
matrix[0][4] = 4
matrix[1][4] = 1
matrix[1][5] = 2
matrix[2][6] = 3
matrix[3][7] = 1
matrix[3][11] = 4
matrix[4][8] = 3
matrix[5][9] = 3
matrix[6][10] = 1
matrix[7][10] = 2
matrix[8][12] = 7
matrix[9][12] = 2
matrix[10][13] = 3
matrix[11][14] = 2
matrix[12][15] = 2
matrix[13][15] = 2
matrix[14][15] = 3

weights = [1, 4, 3, 2, 4, 8, 1, 3, 2, 1, 4, 3, 7, 2, 3, 4]


class Task:
    def __init__(self, time, task_id):
        self.id = task_id
        self.time = time
        self._parent_tasks = []
        self._child_tasks = []
        self._proc = None

    def add_child(self, task, weight, both=True):
        self._child_tasks.append({'task': task, 'weight': weight, 'finished_time': None})
        if both:
            task.add_parent(self, weight)

    def add_parent(self, task, weight):
        self._parent_tasks.append({'task': task, 'weight': weight, 'finished_time': None})

    def add_proc(self, proc):
        assert self._proc is None, 'Proc exists'
        self.time *= proc.slowness
        self._proc = proc

    def send_data(self):
        for i, task in enumerate(self._child_tasks):
            if task['weight']:
                self._child_tasks[i]['weight'] -= 1
                task['task'].get_data(self)
                if not self._child_tasks[i]['weight']:
                    self._child_tasks[i]['finished_time'] = self.proc.tact

                return task['task']

    def same_proc(self, task):
        print('ewf')
        for i, t in enumerate(self._parent_tasks):
            if task.proc.id == t['task'].proc.id:
                print('dadwqdwadwqad')
                self._parent_tasks[i]['weight'] = 0
                self._parent_tasks[i]['finished_time'] = 0

    def get_data(self, task):
        for i, t in enumerate(self._parent_tasks):
            if t['task'] is task and self._parent_tasks[i]['weight']:
                self._parent_tasks[i]['weight'] -= 1
                if not self._parent_tasks[i]['weight']:
                    self._parent_tasks[i]['finished_time'] = task.proc.tact
                

    def step(self):
        self.time -= 1

        if self.is_done:
            for i, task in enumerate(self._child_tasks):
                if task['task'].proc.id == self.proc.id:
                    self._child_tasks[i]['weight'] = 0
                    task['task'].same_proc(self)

    @property
    def proc_added(self):
        return self._proc is not None

    @property
    def is_start_task(self):
        return not self._parent_tasks

    @property
    def is_ready(self):
        return self.is_start_task or all([i['weight'] == 0 and (i['finished_time'] is not None and i['finished_time'] < self.proc.tact) for i in self._parent_tasks])

    @property
    def is_done(self):
        return not self.time

    @property
    def is_finished(self):
        return self.is_done and all([i['weight'] == 0 for i in self._child_tasks])

    @property
    def proc(self):
        return self._proc

    def __repr__(self):
        return f'{self.id}|{[i["task"].id for i in self._child_tasks]}|{[i["task"].id for i in self._parent_tasks]}|{self.time}'


class Processor:
    def __init__(self, slowness, proc_id):
        self.id = proc_id
        self.tact = 0
        self.slowness = slowness
        self._tray = []
        self._tasks = []
        self.task_to_do = None

    def step(self):
        if self._tasks and any([task.is_done and not task.is_finished for task in self._tasks]):
            task = tuple(filter(lambda task: task.is_done and not task.is_finished, self._tasks))[0]
            task_to = self.send(task)
            self._tray.append(f'({task.id})>{task_to.proc.id}({task_to.id})')
        elif self._tasks and any([task.is_ready and not task.is_done for task in self._tasks]):
            for i, task in enumerate(self._tasks):
                if task.is_ready and not task.is_done:
                    self._tasks[i].step()
                    self._tray.append(str(task.id))
                    break
        else:
            self._tray.append('')
        self.tact += 1

    def add_task(self, task):
        self._tasks.append(task)
        task.add_proc(self)

    def send(self, task):
        """Return task send to"""
        return task.send_data()

    def get_tray(self):
        return self._tray


proc_slownesses = [1, 2, 3, 1]
procs = [Processor(i, j + 1) for j, i in enumerate(proc_slownesses)]

tasks = [Task(j, i + 1) for i, j in enumerate(weights)]
for i in range(len(matrix)):
    for j in range(len(matrix)):
        if matrix[i][j] is not None:
            tasks[i].add_child(tasks[j], matrix[i][j])

for task in tasks:
    print(task)

procs[0].add_task(tasks[1])
procs[0].add_task(tasks[5])
procs[0].add_task(tasks[7])
procs[0].add_task(tasks[10])
procs[0].add_task(tasks[13])
procs[1].add_task(tasks[3])
procs[1].add_task(tasks[11])
procs[1].add_task(tasks[14])
procs[1].add_task(tasks[9])
procs[2].add_task(tasks[0])
procs[2].add_task(tasks[6])
procs[3].add_task(tasks[2])
procs[3].add_task(tasks[4])
procs[3].add_task(tasks[8])
procs[3].add_task(tasks[12])
procs[3].add_task(tasks[15])
del proc_slownesses
del weights
del i
del j
del matrix
while not all([task.is_finished for task in tasks]):
    for proc in procs:
        proc.step()
    ...

for proc in procs:
    print(f'{proc.id}:' + '|'.join(proc.get_tray()))
get_html([i.get_tray() for i in procs])

