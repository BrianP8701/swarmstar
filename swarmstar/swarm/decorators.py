from functools import wraps
import traceback

from swarmstar.swarm.types import FailureOperation, SwarmState


def swarmstar_decorator(func):
    """
    Functions wrapped with this decorator need to take the following arguments:
        swarm: SwarmConfig
        swarm_operation: Union[SwarmOperation, TerminationOperation]

    They should output a SwarmOperation, with an optional journal_entry, which this decorator will handle.
        return SwarmOperation, journal_entry

    If an exception is raised, the decorator will catch it and return a FailureOperation.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result, journal_entry = func(*args, **kwargs)
            swarm_state = SwarmState(swarm=args[0])
            node = swarm_state[args[1].node_id]
            if journal_entry:
                node.journal.append(journal_entry)
                swarm_state.update_state(node)
            return result
        except Exception as e:
            tb_str = traceback.format_exc()
            swarm_operation = args[1]
            node_id = swarm_operation.node_id

            params_str = f"node_id: {node_id}\nParams: {kwargs}"
            error_message = (
                f"Error in {func.__name__}:\n{str(e)}\n\n{tb_str}\n\n{params_str}"
            )
            raise Exception(error_message)
        # TODO Later change back to returning FailureOperation
        # return FailureOperation(
        #     node_id=node_id,
        #     report=report,
        # )

    return wrapper
