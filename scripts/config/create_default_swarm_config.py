import os
from dotenv import load_dotenv

from swarmstar.models import SwarmConfig

load_dotenv()
openai_key = os.getenv("OPENAI_KEY")
mongodb_uri = os.getenv("MONGODB_URI")
mongodb_db_name = os.getenv("MONGODB_DB_NAME")

def create_default_swarm_config():
    swarm_config = SwarmConfig(
        id="default_config",
        openai_key=openai_key,
        platform="mac",
        mongodb_uri=mongodb_uri,
        mongodb_db_name=mongodb_db_name,
    )
    
    SwarmConfig.add_swarm_config(swarm_config)

create_default_swarm_config()
    