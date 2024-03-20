import uuid
from datetime import datetime

def generate_uuid(identifier: str) -> str:
    id = str(uuid.uuid4())
    return f"{identifier}_{id}"

# This is overkill. Lol imagine one day i reach the scale of needing to use this. HA
def generate_uuid_with_timestamp(identifier: str) -> str:
    if not isinstance(identifier, str):
        raise TypeError("Identifier must be a string")

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    unique_id = uuid.uuid4()
    return f"{identifier}_{timestamp}_{unique_id}"
