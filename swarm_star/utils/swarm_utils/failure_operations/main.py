from swarm_star.swarm.types import FailureOperation, SwarmConfig, SwarmOperation

def execute_failure_operation(swarm: SwarmConfig, node_failure_operation: FailureOperation) -> SwarmOperation:
    raise NotImplementedError('Havent implemented failure handling for nodes yet.')

