'''
The swarms job is to do stuff. this typically means creating 
stuff, writing code, writing docs, making plans etc. 

The stage is like the buffer that holds the stuff that the 
swarm creates before it gets routed to its appropriate 
destination in the memory space.
'''
import os
import json
from old_swarm.utils.uuid import generate_uuid

def stage_content(content, metadata, name):
    id = generate_uuid(name)
    try:
        file_extension = metadata['file_extension'] 
    except KeyError:
        raise KeyError("Metadata must contain a 'file_extension' key.")
    
    dir_path = 'swarm/stage'
    if not os.path.exists(dir_path):
        raise FileNotFoundError(f"Directory {dir_path} does not exist.")

    file_name = os.path.join(dir_path, f'{id}.{file_extension}') 
    metadata_file_name = os.path.join(dir_path, f'_meta_{id}.json')
    
    try:
        with open(file_name, 'w') as file:
            file.write(content)
        with open(metadata_file_name, 'w') as file:
            json.dump(metadata, file)
    except IOError as e:
        print(f"File I/O error: {e}")
    except TypeError as e:
        print(f"JSON serialization error: {e}")

    return id