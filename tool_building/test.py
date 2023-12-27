# Test run the swarm
import asyncio
from swarm.swarm import Swarm

async def main():
    snapshot_path = 'tool_building/past_runs/v0/snapshot.json'
    history_path = 'tool_building/past_runs/v0/history.json'

    swarm = Swarm(snapshot_path, history_path)
    goal = 'Create a class called GithubWrapper that has all the necessary functions to interact with and modify a Github repository.'
    context = ''
    swarm.load_goal(goal)

    await swarm.run()  # Use await here

# Run the async main function
asyncio.run(main())
