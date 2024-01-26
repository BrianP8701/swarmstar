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
        "keys": []
    },
    ...
}