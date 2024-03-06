import json
import os

from swarmstar.swarm.types import SwarmOperation
from swarmstar.utils.swarm.swarmstar_space import get_swarm_node

def save_dict_to_json_file(file_path: str, data: dict) -> None:
    """
    Saves a given dictionary to a JSON file in a readable format.

    :param file_path: The path to the JSON file where the data will be saved.
    :param data: The dictionary to save.
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def save_swarm_operation_info(swarm, swarm_operation: SwarmOperation, file_path: str) -> None:
    """
    Extracts relevant information from a SwarmOperation object based on its type,
    and appends it to a list in a JSON file. If the file is empty, creates an empty list first.

    :param swarm_operation: The SwarmOperation object to extract information from.
    """
    info_to_save = {
        "node_id": swarm_operation.node_id,
        "operation_type": swarm_operation.operation_type
    }


    node_id = swarm_operation.node_id
    if node_id is not None:
        node = get_swarm_node(swarm, node_id)
        info_to_save["node"] = node.model_dump()
    
    if swarm_operation.operation_type == "spawn":
        info_to_save["action_id"] = swarm_operation.node_embryo.action_id
        info_to_save["message"] = swarm_operation.node_embryo.message

    if hasattr(swarm_operation, 'report') and swarm_operation.report:
        info_to_save["report"] = swarm_operation.report

    # Check if the file exists and is not empty, then read the existing data
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, 'r', encoding='utf-8') as file:
            existing_data = json.load(file)
            if not isinstance(existing_data, list):
                existing_data = []
    else:
        existing_data = []

    existing_data.append(info_to_save)

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(existing_data, file, ensure_ascii=False, indent=4)


def find_next_available_results_file(folder_path: str) -> str:
    """
    Searches inside the specified folder path and returns the path, including the folder path, 
    to the next available results file.

    :param folder_path: The path to the folder where the results files are stored.
    :return: The path to the next available results file, including the folder path.
    """
    x = 0
    while True:
        file_name = f"results_{x}.json"
        file_path = os.path.join(folder_path, file_name)
        if not os.path.exists(file_path):
            return file_path
        x += 1
