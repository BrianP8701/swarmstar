# Test run the swarm
import asyncio
from swarm.swarm import Swarm

async def main():
    snapshot_path = 'tool_building/past_runs/v4/snapshot.json'
    history_path = 'tool_building/past_runs/v4/history.json'

    swarm = Swarm(snapshot_path, history_path)
    goal = 'Create a class called GithubWrapper that has all the necessary functions to interact with and modify a Github repository. Just write the code in one go. Write code to interact with and retrieve info on existing repos, push and add code to existing repos, make new repos, and much more. implement everything in full, and make sure to write the code in one go.'
    context = ''
    swarm.load_goal(goal)

    await swarm.run()  # Use await here

# Run the async main function
asyncio.run(main())
