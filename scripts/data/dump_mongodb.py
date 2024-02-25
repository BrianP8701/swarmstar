import subprocess

def dump_database(mongodb_uri: str, db_name: str, dump_folder_path: str):
    """
    Dump a MongoDB database to a specified folder.

    :param mongodb_uri: MongoDB URI for connecting to the source instance.
    :param db_name: Name of the database to dump.
    :param dump_folder_path: Path to the folder where the dump files will be stored.
    """
    # Construct the mongodump command
    dump_command = [
        "mongodump",
        "--uri", mongodb_uri,
        "--db", db_name,
        "--out", dump_folder_path
    ]

    try:
        # Execute the mongodump command
        subprocess.run(dump_command, check=True)
        print("Database dumped successfully.")
    except subprocess.CalledProcessError as e:
        raise ValueError(f"Failed to dump database: {e}")

