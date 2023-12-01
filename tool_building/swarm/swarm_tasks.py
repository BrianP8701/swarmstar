

task_handlers = {
    'initialize_swarm': initialize_swarm,
    # Add more task type handlers here
}

async def handle_task(task):
    handler = task_handlers.get(task.task_type)
    if handler:
        return await handler(task)
    else:
        raise ValueError(f"Unknown task type: {task.task_type}")