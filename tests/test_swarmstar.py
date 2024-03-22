import asyncio
 
from swarmstar import Swarmstar

def test_swarmstar():
    swarm_id = "test"
    swarm = Swarmstar(swarm_id)
    goal = (
        "Create a google sheet of all people I've ever met, their name, LinkedIn, "
        "company, role, twitter, where they are based, last time I met them, skills, "
        "priority, and notes. Information gathered by scraping my email/cal. For each "
        "row, imaginably there will be pieces of information that can't be gathered. "
        "For these, an email is sent to me highlighting the individual, which info we "
        "have, and which info is missing. I can reply to the email with some of the "
        "missing info and that is input into the google sheet. Every time I email someone "
        "new or meet someone new, this list is updated and an email is sent to me."
    )
    operations = [swarm.instantiate(goal)]
    try:
        next_operations = []
        while True:
            for operation in operations:
                print(f"Executing operation: {operation}")
                result = asyncio.run(swarm.execute(operation))
                print(f"Result: {result}")
                if isinstance(result, list):
                    next_operations.extend(result)
                elif result is not None:
                    next_operations.append(result)
            input("Press enter to continue...")
            operations = next_operations
            next_operations = []
    except Exception as e:
        raise e from None
    finally:
        swarm.delete()

test_swarmstar()