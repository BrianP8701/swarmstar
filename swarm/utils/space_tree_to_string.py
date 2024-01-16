import json

def build_tree(data, indent=''):
    tree_str = ''
    for key, value in data.items():
        # Check if the value is a dictionary and has a 'type' key
        if isinstance(value, dict) and 'type' in value:
            tree_str += indent + key + '\n'
            # Recursively build the tree for nested dictionaries (folders)
            if value['type'] == 'folder':
                tree_str += build_tree(value, indent + '    ')
    return tree_str

def create_tree_from_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
        return build_tree(data)