import asyncio

from swarmstar import Swarmstar
from swarmstar.models import SwarmConfig

from swarmstar.utils.ai.openai import OpenAI
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
print(project_root_memory.id)
get = MemoryMetadata.get('project_root')

print(get)

MemoryMetadata.delete('project_root')