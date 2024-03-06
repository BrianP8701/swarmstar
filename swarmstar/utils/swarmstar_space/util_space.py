from swarmstar.utils.data import get_internal_util_metadata, get_kv
from swarmstar.types import UtilMetadata, SwarmConfig

def get_util_metadata(swarm: SwarmConfig, util_id: str) -> UtilMetadata:
    try:
        util_metadata = get_kv(swarm, "util_space", util_id)
        if util_metadata is None:
            raise ValueError(
                f"This util id: `{util_id}` does not exist in external util space."
            )
    except Exception as e1:
        try:
            util_metadata = get_internal_util_metadata(util_id)
            if util_metadata is None:
                raise ValueError(
                    f"This util id: `{util_id}` does not exist in internal util space."
                ) from e1
        except Exception as e2:
            raise ValueError(
                f"This util id: `{util_id}` does not exist in both internal and external util spaces."
            ) from e2

    type_mapping = {

    }
    util_type = util_metadata["type"]
    if util_type in type_mapping:
        return type_mapping[util_type](**util_metadata)
    return UtilMetadata(**util_metadata)
