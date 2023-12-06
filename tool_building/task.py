class Task:
    def __init__(self, task_type: str, data: dict):
        self.task_type = task_type
        self.data = data
        
    def __str__(self):
        return f"\n\n{self.task_type}\n{self.data}\n\n"