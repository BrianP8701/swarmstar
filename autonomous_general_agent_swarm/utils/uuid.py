import uuid
from datetime import datetime

def generate_uuid(identifier):
    if not isinstance(identifier, str):
        raise TypeError("Identifier must be a string")

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f") 
    unique_id = uuid.uuid4()
    return f"{identifier}_{timestamp}_{unique_id}"
