import json
from pymongo import MongoClient, errors

def upload_json_to_mongodb(mongodb_uri: str, db_name: str, collection_name: str, json_path: str) -> None:
    """
    Uploads JSON data to a MongoDB collection. If the database already exists, it will be deleted before proceeding.
    
    :param mongodb_uri: MongoDB URI for connecting to the instance.
    :param db_name: Name of the database. If it exists, it will be deleted.
    :param collection_name: Name of the collection to upload data to.
    :param json_path: Path to the JSON file containing data to upload.
    """
    # Load JSON data from the given path
    with open(json_path, 'r') as file:
        data = json.load(file)
    
    # Connect to MongoDB
    client = MongoClient(mongodb_uri)
    
    # Check if the database exists and delete it if it does
    if db_name in client.list_database_names():
        client.drop_database(db_name)
        print(f"Database {db_name} already exists. Deleting and creating a new one.")
    
    db = client[db_name]
    collection = db[collection_name]
    
    # Loop through each _id-value pair in the JSON data and upload
    for _id, value in data.items():
        try:
            collection.update_one({'_id': _id}, {'$set': value}, upsert=True)
            print(f"Uploaded {_id} to MongoDB.")
        except Exception as e:
            print(f"Failed to upload {_id}: {str(e)}")


