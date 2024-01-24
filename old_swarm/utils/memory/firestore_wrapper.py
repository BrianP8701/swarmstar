from google.cloud import datastore
import os
import sys
sys.path.insert(0, '/Users/brianprzezdziecki/Code/Agent_Swarm_Experiments')
from old_swarm.settings import Settings

settings = Settings()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.FIRESTORE_CREDENTIALS

# Initialize a datastore client
client = datastore.Client()

def save_dict_to_firestore(datastore_entity, key, data_dict):
    """
    Save a dictionary to the specified datastore entity with the given key.
    """
    key = client.key(datastore_entity, key)
    entity = datastore.Entity(key=key)
    entity.update(data_dict)
    client.put(entity)

def get_dict_from_firestore(datastore_entity, key):
    """
    Retrieve a dictionary from the specified datastore entity using the given key.
    """
    key = client.key(datastore_entity, key)
    entity = client.get(key)
    return entity if entity else None
