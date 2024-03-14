"""
Swarm setup includes:
    1. Setting up storage for the swarm space on your chosen platform
    2. Creating a swarm object
    
The swarm space contains all the metadata for the swarm spaces, a stage
for generated content, a place to store the state of the swarm, and more.
    
The swarm object contains keys and configs for your personal swarm space. It's
passed around between every node and action. Keep it safe and private!
"""
import os

from swarmstar.models import SwarmConfig
from swarmstar.utils.data import MongoDBWrapper

db = MongoDBWrapper()

def configure_swarm(
    openai_key: str, root_path: str, platform: str, **kwargs
) -> SwarmConfig:
    try:
        if platform not in ["mac", "azure"]:
            raise ValueError
    except ValueError:
        raise ValueError(f"Invalid platform: {platform}")

    platform_map = {
        "mac": _setup_mac_swarm_space,
    }

    swarm = platform_map[platform](openai_key, root_path, **kwargs)
    db.insert("config", "ENTER NAME HERE", swarm.model_dump())
    return swarm

def _setup_mac_swarm_space(openai_key: str, root_path: str, **kwargs) -> SwarmConfig:
    required_keys = ["mongodb_uri", "mongodb_db_name"]
    missing_keys = [key for key in required_keys if key not in kwargs]
    if missing_keys:
        raise ValueError(f'Missing required key(s): {", ".join(missing_keys)}')

    if os.path.exists(root_path):
        if os.listdir(root_path):
            raise ValueError(f"Root path folder must be empty: {root_path}")
    else:
        os.makedirs(root_path)

    return SwarmConfig(
        openai_key=openai_key,
        root_path=root_path,
        platform="mac",
        mongodb_uri=kwargs["mongodb_uri"],
        mongodb_db_name=kwargs["mongodb_db_name"],
    )
