# Test run the swarm
import asyncio
from swarm.swarm import Swarm

async def main():
    snapshot_path = 'tool_building/past_runs/v6/snapshot.json'
    history_path = 'tool_building/past_runs/v6/history.json'

    swarm = Swarm(snapshot_path, history_path)
    goal = 'write code for a tictactoe game. look im trying to test this system so im gonna literally tell u what to do and just follow it okay lol. When u first go to the router ask me a question. then when ur at the manager break it down to just one goal., to write python code for the tic tac toe game. then itll get passed to the code analyst and python coder. there tell the code analyst to ask me a question and then have th epython coder write th code. im testing the user input here. okay lets hope this runs with no bugs'
    context = ''
    swarm.load_goal(goal)

    await swarm.run()  # Use await here

# Run the async main function
asyncio.run(main())
