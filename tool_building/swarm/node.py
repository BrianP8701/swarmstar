from settings import Settings
from task import Task
settings = Settings() # For config paths

class Node:
    def __init__(self, id: int, task_type: str, data: dict, parent):
        self.id = id
        self.task_type = task_type
        self.parent = parent
        self.children = []
        self.data = data
        self.output = None
        
    def execute(self):
        task = Task(self.forward_task_name, self.data)
        self.swarm.task_queue.put_nowait(self, task)
        
    def jsonify(self):
        return {
            "task_type": self.task_type,
            "parent": self.parent,
            "children": self.children,
            "input_data": self.input_data,
            "output_data": self.output_data
        }