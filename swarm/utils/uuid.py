import uuid
from datetime import datetime

def generate_uuid(identifier):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = uuid.uuid4()
    return f"{identifier}_{timestamp}_{unique_id}"
