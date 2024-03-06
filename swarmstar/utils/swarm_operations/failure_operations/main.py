from typing import List, Union

from swarmstar.types import FailureOperation, SwarmConfig, SwarmOperation


def failure(
    swarm: SwarmConfig, node_failure_operation: FailureOperation
) -> Union[SwarmOperation, List[SwarmOperation]]:
    raise (node_failure_operation.report)
    # TODO Handle failure operation
