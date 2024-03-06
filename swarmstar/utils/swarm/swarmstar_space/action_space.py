from swarmstar.utils.data import get_internal_action_metadata, get_kv
from swarmstar.swarm.types import SwarmConfig, ActionMetadata, InternalAction, InternalFolder

def get_action_metadata(swarm: SwarmConfig, action_id: str) -> ActionMetadata:
    try:
        action_metadata = get_kv(swarm, "action_space", action_id)
        if action_metadata is None:
            raise ValueError(
                f"This action id: `{action_id}` does not exist in external action space."
            )
    except Exception as e1:
        try:
            action_metadata = get_internal_action_metadata(action_id)
            if action_metadata is None:
                raise ValueError(
                    f"This action id: `{action_id}` does not exist in internal action space."
                ) from e1
        except Exception as e2:
            raise ValueError(
                f"This action id: `{action_id}` does not exist in both internal and external action spaces."
            ) from e2

    type_mapping = {
        "internal_action": InternalAction,
        "internal_folder": InternalFolder,
    }
    action_type = action_metadata["type"]
    if action_type in type_mapping:
        return type_mapping[action_type](**action_metadata)
    return ActionMetadata(**action_metadata)
