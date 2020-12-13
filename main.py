matrix = [[None for _ in range(16)] for _ in range(16)]
matrix[0][4] = 4
matrix[1][4] = 1
matrix[1][5] = 2
matrix[2][6] = 3
matrix[3][7] = 1
matrix[3][11] = 4
matrix[4][8] = 3
matrix[5][9] = 1
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
        self._child_tasks.append({'task': task, 'weight': weight})
        if both:
            task.add_parent(self, weight)
    
    def add_parent(self, task, weight):
        self._parent_tasks.append({'task': task, 'weight': weight})
    
    def add_proc(self, proc):
        assert self._proc is None, 'Proc exists'
        self._proc = proc
    
    @property
    def is_start_task(self):
        return not self._parent_tasks
    
    def __repr__(self):
        return f'{self.id}|{[i["task"].id for i in self._child_tasks]}|{[i["task"].id for i in self._parent_tasks]}'


class Processor:
    def __init__(self, slowness):
        self.tact = 0
        self.slowness = slowness


tasks = [Task(j, i) for i, j in enumerate(weights)]
for i in range(len(matrix)):
    for j in range(len(matrix)):
        if matrix[i][j] is not None:
            tasks[i].add_child(tasks[j], matrix[i][j])


for task in tasks:
    print(task)


