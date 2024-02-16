from enum import Enum
from pydantic import BaseModel
from typing import Dict, List, Optional, Union

class UtilType(Enum):
    INTERNAL_FOLDER = 'internal_folder'
    INTERNAL_FUNCTION = 'internal_function'

class Test(BaseModel):
    idk: str
    idk2: int

class UtilFolder(BaseModel):
    type: UtilType
    name: str
    description: str
    parent: Optional[str] = None
    children: List[str] = []
    metadata: Optional[Dict[str, str]] = None 
    idk: Test
    
example = UtilFolder(
    type=UtilType.INTERNAL_FOLDER,
    name='folder_name',
    description='folder_description',
    parent='parent_id',
    children=['child_id_1', 'child_id_2'],
    metadata={'key': 'value'},
    idk=Test(idk='idk', idk2=1)
)

print(example)

print(example.model_dump())

