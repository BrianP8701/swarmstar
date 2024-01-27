1 this is a temporary file for me to define schemas for objects, config files etc

 # Memory Space Schema

 {
    "navigation_type": "folder, vector_index, sql_table, sql_row, sql_column, blob_storage, file_system...",    -for Uploader
    "retrieval_type": "none, sql, router, vector_similarity, choice",     -for Retriever
    "name": "",
    "id": "",
    "description": "",
    "children": [ids of children]
}


# Action Space Schema

{
    id: {
        "type": "folder",
        "name": "",
        "id": "",
        "description": "",
        "children": [ids of children]
    },
    ...
}
Action:
{
    id: {
        "type": "action",
        "name": "",
        "id": "",
        "description": "",
        "input_schema": "",
        "output_schema": "",
        "dependencies": [],
        "configs": []
    },
    ...
}


# Input to Lifecycle Executor

{
    "lifecycle_command": "spawn or terminate",
    "action" : {
        "id": "",
        "args": {}
    },
    "swarm_blueprint": {
        "memory_space": {},
        "action_space": {}
    }
}



# Swarm
{
    "nodes": {
        node_id: Node,
        ...
    },
    "action_space": {
        # check action space schema above
    },
    "memory_space": {
        # check memory space schema above
    },
    "history": [
        {
            "lifecycle_command": "terminate" or "spawn",
            # this rlly just depends on how we want to visualize it. as a bare minimum just passing id and args of action is all thats needed
        }
    ],
    configs: {
        "platform": ""
        "root_path": "",
        "openai_key": "",
        ...
    }
}
## Node
