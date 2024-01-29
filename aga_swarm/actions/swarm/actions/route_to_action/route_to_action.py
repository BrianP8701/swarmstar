import json
import copy
import sys
import asyncio
import os
sys.path.insert(0, '/Users/brianprzezdziecki/Code/Agent_Swarm_Experiments')

# from old_swarm.core.oai_agent import OAI_Agent
# from old_swarm.settings import Settings
# from old_swarm.utils.user_input import get_user_input
# from old_swarm.utils.actions.validate_action_args import validate_action_args

# settings = Settings()

# async def action_router(directive: str):
#     '''
#     The action router decides what action to take next given a string, the "directive"
#     '''
#     with open('swarm/actions/action_router/tool.json') as f:
#         router_schema = json.load(f)
#     tool_blueprint = router_schema['action_router']['tools'][0]
#     instructions = router_schema['action_router']['instructions']

#     action_space_path = 'swarm/actions'
        
#     searching_action_space = True
#     options = _extract_options(action_space_path)
#     path = ['swarm', 'actions']

#     while searching_action_space:
#         # Let LLM choose where to go in the action_space
#         tool_blueprint_copy = copy.deepcopy(tool_blueprint)
#         action_router = _update_router(options, tool_blueprint_copy, instructions)
#         action_router_output = await action_router.chat(directive)
#         action_index = action_router_output['arguments'].get('action_index', None)

#         # Continue to traverse action space if you are in a folder. Exit if you are in an action.
#         path.append(options[action_index]['name'])
        
#         node_info_path = os.path.join(*path, '_node_info.json')
#         try:
#             with open(node_info_path, 'r') as json_file:
#                 node_info = json.load(json_file)
#         except FileNotFoundError:
#             print(f"File {node_info_path} does not exist.")
#             node_info = None

#         if node_info['type'] == 'folder':
#             options = _extract_options(os.path.join(*path))
#         elif node_info['type'] == 'action':
#             searching_action_space = False
#         else:
#             raise ValueError(f"Invalid type in action space. Expected 'folder' or 'action'.\n\nPath: {path}\n\n")
    
#     path = '/'.join(path[2:])
#     report = {
#         'message': f'Given the directive "{directive}", the action router chose the action "{path}"',
#         'action_path': path
#     }
#     node_blueprints = [{'type': path, 'data': {'directive': directive}}]
#     lifecycle_command = {'action': 'spawn', 'node_blueprints': node_blueprints}
#     return {'report': report, 'lifecycle_command': lifecycle_command}

# def _update_router(options, tool, instructions):
#     tool['function']['parameters']['properties']['action_index']['description'] += str(options)
#     tool['function']['parameters']['properties']['action_index']['enum'] = list(range(len(options)))

#     tool_choice = {"type": "function", "function": {"name": "action_router"}}
    
#     return OAI_Agent(instructions, [tool], tool_choice)

# def _extract_options(base_folder):
#     """
#     Scans the subfolders in the base_folder for _node_info.json files,
#     and returns a dict with incrementing indices as keys and the content
#     of these json files as values.

#     :param base_folder: The path of the folder to scan.
#     :return: Dict of indices to json content.
#     """
#     node_info_dict = {}
#     index = 0

#     for folder in os.listdir(base_folder):
#         json_path = os.path.join(base_folder, folder, '_node_info.json')
#         if os.path.isfile(json_path):
#             with open(json_path, 'r') as json_file:
#                 node_info_dict[index] = json.load(json_file)
#                 index += 1

#     return node_info_dict

# def main(args):
#     try:
#         results = asyncio.run(action_router(args['directive']))
#         print(json.dumps(results))  # Convert dict to JSON and print
#     except Exception as e:
#         raise RuntimeError(f"Script execution failed: {str(e)}")

# if __name__ == "__main__":
#     schema = {
#         "directive": str
#     }
#     args_dict = validate_action_args(schema)
#     main(args_dict)