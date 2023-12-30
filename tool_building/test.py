# Test run the swarm
import asyncio
from swarm.swarm import Swarm

async def main():
    snapshot_path = 'tool_building/past_runs/v1/snapshot.json'
    history_path = 'tool_building/past_runs/v1/history.json'

    swarm = Swarm(snapshot_path, history_path)
    goal = 'Write a disk-backed, log structure merge tree KV stroe with RESTFUL API, figure out the root causes of aging and genuinely pursue and solve aging for humanity'
    context = ''
    swarm.load_goal(goal)

    await swarm.run()  # Use await here

# Run the async main function
asyncio.run(main())
