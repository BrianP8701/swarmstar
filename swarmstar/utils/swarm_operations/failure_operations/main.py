from typing import List, Union

from swarmstar.models import FailureOperation, SwarmConfig, SwarmOperation


def failure(node_failure_operation: FailureOperation) -> Union[SwarmOperation, List[SwarmOperation]]:
    raise (node_failure_operation.report)
    # TODO Handle failure operation
