import json
from pymongo import MongoClient, errors

def upload_json_to_mongodb(mongodb_uri: str, db_name: str, collection_name: str, json_path: str) -> None:
    # Load JSON data from the given path
    with open(json_path, 'r') as file:
        data = json.load(file)
    
    # Connect to MongoDB
    client = MongoClient(mongodb_uri)
    db = client[db_name]
    collection = db[collection_name]
    
    # Ensure the 'key' field is a unique index
    try:
        collection.create_index([('key', 1)], unique=True)
    except errors.OperationFailure:
        print("Index already exists.")
    
    # Loop through each key-value pair in the JSON data and upload
    for key, value in data.items():
        try:
            collection.update_one({'key': key}, {'$set': value}, upsert=True)
            print(f"Uploaded {key} to MongoDB.")
        except Exception as e:
            print(f"Failed to upload {key}: {str(e)}")


upload_json_to_mongodb('mongodb://localhost:27017', 'internal_metadata', 'action_space', 'swarmstar/actions/action_space.json')