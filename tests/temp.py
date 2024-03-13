"""file for quick tests. nothing to see here."""
import pymongo
from pymongo import MongoClient
from typing import Any, Dict, List, Tuple, get_origin, get_args
from tests.test_config import SWARMSTAR_UNIT_TESTS_MONGODB_DB_NAME, MONGODB_URI

from swarmstar.types import SwarmConfig, SwarmNode, SpawnOperation, BlockingOperation, TerminationOperation, ActionOperation, UserCommunicationOperation, FailureOperation
from swarmstar.utils.swarmstar_space import get_swarm_node, get_action_metadata, get_swarm_config
from swarmstar.utils.data import get_kv, get_internal_action_metadata

import traceback
from abc import ABCMeta, abstractmethod
from functools import wraps
from typing import Any, Dict, List, Callable, get_type_hints
from inspect import signature

from swarmstar.utils.swarmstar_space import update_swarm_node
from swarmstar.types.swarm_config import SwarmConfig
from swarmstar.types.swarm_node import SwarmNode
from swarmstar.types.swarm_operations import SwarmOperation


test_termination_operation = TerminationOperation(
    terminator_node_id="node_id",
    node_id="node_id",
    context={"context": "context"}
)

dum = test_termination_operation.model_dump()

ddd = SwarmOperation.model_validate(dum)

print(ddd)
print(type(ddd))