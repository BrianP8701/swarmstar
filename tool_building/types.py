class Task:
    def __init__(self, task_type, data):
        self.task_type = task_type
        self.data = data
        
    ''' 
    task_types:
    
    - create_agent
        > {instructions, name, tools}
    '''