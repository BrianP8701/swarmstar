from typing import Dict, Any, Literal, Optional, List
from pydantic import BaseModel, Field
from swarmstar.utils.retrieval.get_code_as_string import get_class_as_string
class NodeEmbryo(BaseModel):
    action_id: str
    message: str
    
class SwarmOperation(BaseModel):
    operation_type: Literal['spawn', 'terminate', 'node_failure', 'blocking']
    node_id: str

class BlockingOperation(SwarmOperation):
    operation_type: Literal['blocking']
    node_id: str
    blocking_type: str  
    args: Dict[str, Any] = {}
    context: Dict[str, Any] = {}
    next_function_to_call: str 

class SpawnOperation(SwarmOperation):
    operation_type: Literal['spawn']
    node_embryo: NodeEmbryo
    termination_policy_change: Literal[
        'simple',
        'parallel_review', 
        'clone_with_reports'
    ] = None
    node_id: str = None
    report: str = None
    
model = get_class_as_string('swarmstar/actions/reasoning/decompose_directive.py', 'DecomposeDirectiveModel')


exec(model)

something = DecomposeDirectiveModel(
    questions = ['What is the meaning of life?'],
    subdirectives = ['Go to the store', 'Buy some milk'],
    scrap_paper = 'I need to buy some milk'
)

print(something)

