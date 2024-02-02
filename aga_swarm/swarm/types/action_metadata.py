from pydantic import BaseModel, Field, RootModel
from typing import Dict, List, Optional, Union, Literal

class Property(BaseModel):
    type: str                                                       # the type of the property
    description: str                                                # the description of the property
    enum: Optional[List[str]] = None                                # optional list of possible values of the property

class ActionMetadata(BaseModel):
    type: Literal['action'] = Field('action', Literal=True)         # this is always 'action'
    name: str                                                       # the human readable name of the action
    description: str                                                # concise & comprehensive description of the action
    input_schema: BaseModel                                         # the input schema of the action
    output_schema: BaseModel                                        # the output schema of the action
    dependencies: List[str] = []                                    # the list of packages that this action depends on
    parent: str = None                                              # the parent folder of the action
    script_path: str = None                                         # the path to the script that the action runs
    language: str = None                                            # the language that the action is written in
    internal: bool = False                                          # whether the action is inside the package or custom
    content_path: str = None                                        # the path to the content of the action
    
class ActionFolderMetadata(BaseModel):
    type: Literal['folder'] = Field('folder', Literal=True)         # this is always 'folder'
    name: str                                                       # the human readable name of the folder
    description: str                                                # the description of the folder
    children: List[str] = []                                        # the list of children of the folder
    parent: Optional[str] = None                                    # the parent folder of the folder
    folder_path: str = None                                         # the path to the folder
    internal: bool = False                                          # whether the folder is inside the package or custom

class ActionSpaceMetadata(RootModel):
    root: Dict[str, Union[ActionMetadata, ActionFolderMetadata]]
    
    def get_action_type(self, action_id: str) -> str:
        action_metadata = self.root[action_id]
        if action_metadata is None:
            raise ValueError(f"This action id {action_id} does not exist.")
        return action_metadata.type

    def get_action_name(self, action_id: str) -> str:
        action_metadata = self.root[action_id]
        if action_metadata is None:
            raise ValueError(f"This action id {action_id} does not exist.")
        return action_metadata.name
