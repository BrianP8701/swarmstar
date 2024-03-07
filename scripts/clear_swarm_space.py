from pymongo import MongoClient

from swarmstar.utils.data.kv_operations.mongodb import mongodb_set_kv

def clear_swarm_space(db_name: str, mongodb_uri: str) -> None:
    """
    Goes through every collection in a MongoDB except for the one named 'config',
    and deletes all documents in those collections.

    :param mongodb_uri: MongoDB URI for connecting to the instance.
    """
    client = MongoClient(mongodb_uri)

    db = client[db_name]
    collection_names = db.list_collection_names()

    for collection_name in collection_names:
        if collection_name == 'admin':
            pass
        elif collection_name != 'config':
            db[collection_name].delete_many({})
        else:
            db[collection_name].delete_many({"_id": {"$ne": "default_config"}})
    
    empty_admin = {"data": []}
    mongodb_set_kv(mongodb_uri, db_name, "admin", "swarms", empty_admin)

    print("Cleared all documents from all collections except 'config'.")

clear_swarm_space('swarmstar_tests', 'mongodb://localhost:27017/')