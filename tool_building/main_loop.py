import asyncio
from types import Task
from toolkit.agent_handler import create_agent

# This function loops forever, processing tasks as they come in.
async def main_loop(task_queue):
    while True:
        task = await task_queue.get()
        try:
            # Process the task (API call, database operation, etc.)
            result = await handle_task(task)
            # Handle the result (save to database, further processing, etc.)
        except Exception as error:
            # Handle errors
            print(error)
        finally:
            task_queue.task_done()


# Dispatch table
task_handlers = {
    'create_agent': create_agent,
    # Add more task type handlers here
}

async def handle_task(task):
    handler = task_handlers.get(task.task_type)
    if handler:
        return await handler(task)
    else:
        raise ValueError(f"Unknown task type: {task.task_type}")


async def main():
    task_queue = asyncio.Queue()
    spawn_conversation_with_initial_head_agent = Task("spawn_conversation_with_initial_head_agent", {})
    # Add tasks to the queue
    task_queue.put_nowait(task1)
    task_queue.put_nowait(task2)
    # More tasks can be added over time

    # Start the main loop
    await main_loop(task_queue)

if __name__ == "__main__":
    asyncio.run(main())


# the first task i want to do..... is spawn my conversation with the initial head agent
# Task 1: Spawn conversation with initial head agent