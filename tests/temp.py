import pymongo
from pymongo import MongoClient
from typing import Any, Dict, List, Tuple

from swarmstar.types import SwarmConfig, SwarmNode
from swarmstar.utils.swarmstar_space import get_swarm_node, get_action_metadata
from swarmstar.utils.data import get_kv, get_internal_action_metadata

developer_logs = [{"role": "system", "content": "Log 0.0"}]

def log(log_dict: Dict[str, Any], index_key: List[int] = None):
        if index_key is None:
            developer_logs.append(log_dict)
            return_index_key = [len(developer_logs) - 1]
        else:
            nested_list = developer_logs
            for i, index in enumerate(index_key):
                if index > len(nested_list):
                    raise IndexError(f"Index {index} is out of range for the current list. {nested_list}")
                if i == len(index_key) - 1:
                    if len(nested_list) == index:
                        nested_list.append([log_dict])
                        return_index_key = index_key + [0]
                    elif isinstance(nested_list[index], list):
                        nested_list[index].append(log_dict)
                        return_index_key = index_key + [len(nested_list[index]) - 1]
                    else:
                        nested_list[index] = [nested_list[index], log_dict]
                        return_index_key = index_key + [1]
                else:
                    if isinstance(nested_list[index], list):
                        nested_list = nested_list[index]
                    else:
                        raise ValueError("Invalid index_key. Cannot traverse non-list elements.")
        return return_index_key

def test_log_function():
    global developer_logs
    developer_logs = [{"role": "system", "content": "Log 0.0"}]

    try:
        # Test appending a log to the main list
        index_key = log({"role": "user", "content": "Log 1.0"})
        assert developer_logs == [
            {"role": "system", "content": "Log 0.0"},
            {"role": "user", "content": "Log 1.0"}
        ]
        assert index_key == [1]

        # Test appending a log at an index out of range
        try:
            log({"role": "system", "content": "Log 3.0"}, [4])
            assert False, "Expected ValueError for appending a log out of range"
        except IndexError:
            pass

        # Test appending a log to the main list
        index_key = log({"role": "ai", "content": "Log 2.0"})
        assert developer_logs == [
            {"role": "system", "content": "Log 0.0"},
            {"role": "user", "content": "Log 1.0"},
            {"role": "ai", "content": "Log 2.0"}
        ]
        assert index_key == [2]

        # Test appending a log to an existing nested list
        index_key = log({"role": "ai", "content": "Log 2.1"}, [2])
        assert developer_logs == [
            {"role": "system", "content": "Log 0.0"},
            {"role": "user", "content": "Log 1.0"},
            [
                {"role": "ai", "content": "Log 2.0"},
                {"role": "ai", "content": "Log 2.1"}
            ]
        ]
        assert index_key == [2, 1]

        # Test appending a log to a new nested list
        index_key = log({"role": "system", "content": "Log 3.0"}, [3])
        assert developer_logs == [
            {"role": "system", "content": "Log 0.0"},
            {"role": "user", "content": "Log 1.0"},
            [
                {"role": "ai", "content": "Log 2.0"},
                {"role": "ai", "content": "Log 2.1"}    
            ],
            [{"role": "system", "content": "Log 3.0"}]
        ]
        assert index_key == [3, 0]

        # Test appending a log to a non-list element within a nested list
        index_key = log({"role": "user", "content": "Log 2.1.0"}, [2, 1])
        assert developer_logs == [
            {"role": "system", "content": "Log 0.0"},
            {"role": "user", "content": "Log 1.0"},
            [
                {"role": "ai", "content": "Log 2.0"},
                [{"role": "ai", "content": "Log 2.1"}, {"role": "user", "content": "Log 2.1.0"}]
            ],
            [{"role": "system", "content": "Log 3.0"}]
        ]
        assert index_key == [2, 1, 1]

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