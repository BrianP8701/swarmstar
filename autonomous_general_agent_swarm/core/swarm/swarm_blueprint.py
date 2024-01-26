from pydantic import BaseModel, Field, validate_arguments
import importlib
from typing import Callable, BinaryIO
from core.swarm.default_swarm_operations import get_default_action_space, get_default_memory_space, setup_swarm_space



def build_swarm_blueprint(swarm_name: str, openai_key: str, frontend_url: str, platform: str, root_path: str):
    '''
    Create and configure your swarm with your environment and data. 
    
    Parameters:
        - swarm_name (str)
        - openai_key (str)
        - frontend_url (str): The URL for the frontend interface of the swarm.
        - platform (str): Choose between: ['mac', 'windows', 'linux', 'azure', 'gcp', 'aws']
        - root_path (str): The root path for this swarm blueprint and it's instances to be stored.
    '''
    swarm_blueprint = {
        'swarm_name': swarm_name,
        'action_space': get_default_action_space(),
        'memory_space': get_default_memory_space(),
        'configs': {
            openai_key: openai_key,
            frontend_url: frontend_url,
            platform: platform,
            'root_path': root_path
        },
        'nodes': {},
        'history': []
    }
    # Set the default actions in action space
    setup_swarm_space(swarm_blueprint)
    



