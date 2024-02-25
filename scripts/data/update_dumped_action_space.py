from scripts.data.json_to_mongodb import upload_json_to_mongodb
from scripts.data.dump_mongodb import dump_database

def update_dumped_action_space() -> None:
    """
    Update the action space in MongoDB with the given file path.
    """
    upload_json_to_mongodb('mongodb://localhost:27017', 'internal_metadata', 'action_space', 'swarmstar/actions/action_space.json')
    dump_database('mongodb://localhost:27017', 'internal_metadata', 'swarmstar')

update_dumped_action_space()
