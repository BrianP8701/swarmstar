# Test run the swarm
import asyncio
from swarm.swarm import Swarm

async def main():
    snapshot_path = 'tool_building/past_runs/v6/snapshot.json'
    history_path = 'tool_building/past_runs/v6/history.json'

    swarm = Swarm(snapshot_path, history_path)
    goal = 'Just generate a script that prints hello world. dont ask questions. pass it straight to the coder and finish it fast'
    context = ''
    swarm.load_goal(goal)

    await swarm.run()  # Use await here

# Run the async main function
asyncio.run(main())
