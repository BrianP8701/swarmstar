import asyncio
import os
import json

async def execute(node):
    """
    Executes a script located in the given folder path as an asyncio subprocess
    and returns its result.

    :param folder_path: Path to the folder containing the script.
    :param args_dict: Dictionary of arguments to pass to the script.
    :return: The output of the script.
    """
    path_prefix = 'swarm/actions/'
    folder_path = node.type
    args_dict = node.data

    action_path = os.path.join(path_prefix, folder_path)

    # Append script.py to the folder path
    script_path = os.path.join(action_path, 'script.py')

    # Check if the script exists
    if not os.path.exists(script_path):
        raise FileNotFoundError(f"No script found at path: {script_path}")

    # Prepare the command
    command = ['python', script_path] + [json.dumps(args_dict)]

    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        raise RuntimeError(f"Script execution failed: {stderr.decode()}")

    # Parse the JSON output
    try:
        result_dict = json.loads(stdout.decode())
    except json.JSONDecodeError:
        raise ValueError(f"Failed to parse script output as JSON: {stdout.decode()}")

    return result_dict
