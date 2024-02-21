from functools import wraps
import traceback

from swarmstar.swarm.types import FailureOperation, SwarmState

def swarmstar_operation_decorator(func):
    '''
    The swarmstar decorator is a wrapper for all functions that work directly with/on swarm operations.
    These functions have params of:
        - swarm: SwarmConfig
        - swarm_operation: SwarmOperation
    
    It will catch any exceptions and return a FailureOperation with a report of the error.
    It will also provide journaling and logging capabilities for the function.
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result, journal_entry = func(*args, **kwargs)
            swarm_state = SwarmState(swarm=args[0])
            node = swarm_state.get_node(args[1].node_id)
            if journal_entry:
                node.append_journal_entry(journal_entry)
                swarm_state.update_node(node)
            return result
        except Exception as e:
            tb_str = traceback.format_exc()
            swarm_operation = args[1]
            node_id = swarm_operation.node_id
            
            params_str = f"node_id: {node_id}\nParams: {kwargs}"
            report = f"Error in {func.__name__}:\n{str(e)}\n\n{tb_str}\n\n{params_str}"
            return FailureOperation(
                node_id=node_id,
                report=report,
            )
    return wrapper
