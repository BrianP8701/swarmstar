import os

from swarmstar.utils.containers import DockerContainerManager
from swarmstar.models import Memory, MemoryMetadata, MemoryFolder, MemoryNode


project_root_memory = MemoryFolder(
    id='project_root',
    type='project_root_folder',
    name='project_root',
    children_ids=[
        'child1',
        'child2'
    ],
    description="This is the root folder of the project.",
)
MemoryMetadata.save(project_root_memory)
child1_memory = MemoryNode(
    id='child1',
    type='project_file_bytes',
    name='child1',
    description="This is a file in the project.",
    parent='project_root',
    context={'file_path': 'child1.py'}
)
MemoryMetadata.save(child1_memory)
child2_memory = MemoryNode(
    id='child2',
    type='project_file_bytes',
    name='child2',
    description="This is a file in the project.",
    parent='project_root',
    context={'file_path': 'folder2/child2.py'}
)
MemoryMetadata.save(child2_memory)



file_name = "child1.py"
file_content = '''print("Hello, World!")'''
with open(file_name, 'w') as file:
    file.write(file_content)

file_name = "child2.py"
file_content = '''x = 10/0
print(x)'''
with open(file_name, 'w') as file:
    file.write(file_content)

child1_file_bytes = open('child1.py', 'rb').read()
child2_file_bytes = open('child2.py', 'rb').read()
Memory.save('child1', child1_file_bytes)
Memory.save('child2', child2_file_bytes)



container_manager = DockerContainerManager()
container_id = container_manager.start_terminal_session('python:3.12', project_root_memory.id)
try:
    container_manager.transfer_file_to_container(container_id, 'child1.py', child1_file_bytes)
    container_manager.transfer_file_to_container(container_id, 'folder2/child2.py', child2_file_bytes)
    output = container_manager.send_command(container_id, 'python child1.py')
    print(output)
    output = container_manager.send_command(container_id, 'python folder2/child2.py')
    print(output)
    print('what')
    print(type(output))
    print('huh')
except Exception as e:
    print(e)
finally:
    os.remove('child1.py')
    os.remove('child2.py')
    Memory.delete('child1')
    Memory.delete('child2')
    MemoryMetadata.delete('project_root')
    MemoryMetadata.delete('child1')
    MemoryMetadata.delete('child2')
    container_manager.close_terminal_session(container_id)
