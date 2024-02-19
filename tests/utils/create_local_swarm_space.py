import os

def find_next_available_swarm_folder():
    base_path = "tests/my_swarms/swarm_"
    x = 0
    while True:
        folder_path = f"{base_path}{x}"
        if not os.path.exists(folder_path):
            return folder_path
        x += 1
