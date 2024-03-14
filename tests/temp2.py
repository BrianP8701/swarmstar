from swarmstar import Swarmstar
from swarmstar.models import SwarmConfig


swarm_config = SwarmConfig.get_swarm_config("temp")
print(swarm_config)
Swarmstar.delete_swarmstar_space(swarm_config.id)