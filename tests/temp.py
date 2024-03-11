import pymongo
from pymongo import MongoClient
from typing import Any, Dict, List, Tuple

from swarmstar.types import SwarmConfig, SwarmNode
from swarmstar.utils.swarmstar_space import get_swarm_node, get_action_metadata
from swarmstar.utils.data import get_kv, get_internal_action_metadata

developer_logs = [{"role": "system", "content": "Log 0.0"}]

def log(log_dict: Dict[str, Any], index_key: List[int] = None):
    """
    This function appends a log to the developer_logs list or a nested list within developer_logs.

    The log_dict should have the following format:
    {
        "role": (swarmstar, system, ai or user),
        "content": "..."
    }

    Node developer_logs contains a list of logs in time order.
    Developer logs can also contain nested lists.
    Logs inside a nested list means those were performed in parallel. For example:

    [log0, log1, log2, [log3.0, log3.1, log3.2], log4]
        log3.0, log3.1, log3.2 were performed in parallel.

    or even,

    [log0, log1, [[log2.0.0, log2.0.1, log2.0.2], [log2.1.0, log2.1.1]], log3]
        log2.0.1, log2.0.2, log2.0.3 were performed in parallel.
        log2.1.1, log2.1.2 were performed in parallel.
        log2.0 and log2.1 were performed in parallel.

    If index_key is None, the log will be appended to the developer_logs list.
    If an index_key is provided, the log will be appended to the nested list at the index_key.

    The function can create a new empty list and add the log if the list doesn't exist,
    but it can only create one list at a time. If an attempt is made to create more than one list
    at a time, an error will be raised.

    :param log_dict: A dictionary representing the log to be added.
    :param index_key: A list of integers representing the index path to the nested list where the log should be added.
    :raises ValueError: If an attempt is made to create more than one list at a time.
    """
    if index_key is None:
        developer_logs.append(log_dict)
    else:
        nested_list = developer_logs
        for i, index in enumerate(index_key):
            if index > len(nested_list):
                raise IndexError(f"Index {index} is out of range for the current list. {nested_list}")
            if i == len(index_key) - 1:
                if len(nested_list) == index:
                    nested_list.append([log_dict])
                elif isinstance(nested_list[index], list):
                    nested_list[index].append(log_dict)
                else:
                    nested_list[index] = [nested_list[index], log_dict]
            else:
                if isinstance(nested_list[index], list):
                    nested_list = nested_list[index]
                else:
                    raise ValueError("Invalid index_key. Cannot traverse non-list elements.")

def test_log_function():
    global developer_logs
    developer_logs = [{"role": "system", "content": "Log 0.0"}]

    try:
        # Test appending a log to the main list
        log({"role": "user", "content": "Log 1.0"})
        assert developer_logs == [
            {"role": "system", "content": "Log 0.0"},
            {"role": "user", "content": "Log 1.0"}
        ]

        # Test appending a log at an index out of range
        try:
            log({"role": "system", "content": "Log 3.0"}, [4])
            assert False, "Expected ValueError for appending a log out of range"
        except IndexError:
            pass

        # Test appending a log to the main list
        log({"role": "ai", "content": "Log 2.0"})
        assert developer_logs == [
            {"role": "system", "content": "Log 0.0"},
            {"role": "user", "content": "Log 1.0"},
            {"role": "ai", "content": "Log 2.0"}
        ]

        # Test appending a log to an existing nested list
        log({"role": "ai", "content": "Log 2.1"}, [2])
        assert developer_logs == [
            {"role": "system", "content": "Log 0.0"},
            {"role": "user", "content": "Log 1.0"},
            [
                {"role": "ai", "content": "Log 2.0"},
                {"role": "ai", "content": "Log 2.1"}
            ]
        ]

        # Test appending a log to a new nested list
        log({"role": "system", "content": "Log 3.0"}, [3])
        assert developer_logs == [
            {"role": "system", "content": "Log 0.0"},
            {"role": "user", "content": "Log 1.0"},
            [
                {"role": "ai", "content": "Log 2.0"},
                {"role": "ai", "content": "Log 2.1"}    
            ],
            [{"role": "system", "content": "Log 3.0"}]
        ]

        # Test appending a log to a non-list element within a nested list
        log({"role": "user", "content": "Log 2.1.0"}, [2, 1])
        assert developer_logs == [
            {"role": "system", "content": "Log 0.0"},
            {"role": "user", "content": "Log 1.0"},
            [
                {"role": "ai", "content": "Log 2.0"},
                [{"role": "ai", "content": "Log 2.1"}, {"role": "user", "content": "Log 2.1.0"}]
            ],
            [{"role": "system", "content": "Log 3.0"}]
        ]

        # Test creating more than one list at a time (should raise an error)
        try:
            log({"role": "system", "content": "Log 4.0"}, [4, 0])
            assert False, "Expected ValueError for creating more than one list at a time"
        except IndexError:
            pass
    except Exception as e:
        print('\n\n')
        print(developer_logs)
        print('\n\n')
        raise(e)

test_log_function()