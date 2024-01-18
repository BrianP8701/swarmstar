import asyncio
import os
import json

async def execute_node(node):
    """
    Executes a node as a subprocess and returns the result
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

async def execute_script(script_path, args_dict):
    """
    Executes a node as a subprocess and returns the result
    """
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