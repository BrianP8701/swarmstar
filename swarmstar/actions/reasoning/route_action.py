"""
Given a directive, the router agent uses an LLM to navigate the action space 
through its metadata to decide what action to take. If there is no good action
path to take, the router agent will describe what type of action is needed in detail.
"""
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from swarmstar.types import (
    ActionFolder,
    BlockingOperation,
    NodeEmbryo,
    SpawnOperation,
    SwarmOperation,
    ActionMetadata
)
from swarmstar.types.base_action import BaseAction
from swarmstar.utils.swarmstar_space import get_action_metadata

class NextActionPath(BaseModel):
    index: Optional[int] = Field(
        None, description="Index of the best action path to take"
    )
    failure_message: Optional[str] = Field(
        None,
        description="There's no good action path to take. Describe what type of action is needed in detail.",
    )


ROUTE_ACTION_INSTRUCTIONS = (
    "Decide what action path to take based on the directive and the available actions. "
    "If there is no good action path to take, describe what type of action is needed "
    "in detail in the failure message, and leave index empty."
)


class Action(BaseAction):
    def main(self) -> BlockingOperation:
        root: ActionFolder = get_action_metadata(self.swarm_config, "swarmstar/actions")
        root_children = self.get_children_action_metadata(root)
        children_action_ids = [child.id for child in root_children]
        root_children_descriptions = self.get_children_descriptions(root_children)
        messages = self.build_route_messages(
            self.node.message, root_children_descriptions
        )

        self.log({
                "role": "swarmstar",
                "content": "Deciding what action to take given a directive."  
        })
        self.log({
            "role": "system",
            "content": messages[0]["content"]
        })

        return BlockingOperation(
            node_id=self.node.id,
            blocking_type="instructor_completion",
            args={"messages": messages},
            context={"instructor_model_name": "NextActionPath", "children_action_ids": children_action_ids},
            next_function_to_call="route_goal",
        )

    @BaseAction.receive_completion_handler
    def route_goal(
        self, completion: NextActionPath, children_action_ids: List[str]
    ) -> SwarmOperation:
        """
        This function gets called over and over again 
        until we reach a leaf node, aka an action.
        """
        current_action_id = children_action_ids[completion.index]
        current_action = get_action_metadata(self.swarm_config, current_action_id)

        self.log({
            "role": "ai",
            "content": (
                f"Index: {completion.index if completion.index is not None else 'None'}\n\n "
                f"Failure message: {completion.failure_message if completion.failure_message is not None else 'None'}"
            )
        })
        
        if completion.index is not None:
            if current_action.is_folder:
                
                self.log({
                    "role": "swarmstar",
                    "content": f"The router navigated to the {current_action.name} folder."
                })
                
                children = self.get_children_action_metadata(current_action)
                current_children_action_ids = [child.id for child in children]
                children_descriptions = self.get_children_descriptions(children)
                messages = self.build_route_messages(
                    self.node.message, children_descriptions
                )
                
                self.log({
                    "role": "system",
                    "content": messages[0]["content"]
                })
                
                return BlockingOperation(
                    node_id=self.node.id,
                    blocking_type="instructor_completion",
                    args={"messages": messages},
                    context={
                        "children_action_ids": current_children_action_ids,
                        "instructor_model_name": "NextActionPath"    
                    },
                    next_function_to_call="route_goal",
                )
            else: # We've reached an action
                self.log({
                    "role": "swarmstar",
                    "content": f"The router decided to take the {current_action.name} action for this directive."
                })
                self.report(
                    f"The router agent chose an action to take given a directive.\n\nDirective: {self.node.message}"
                    f"\n\nChosen action: {current_action.name}\n\nAction description: {current_action.description}"
                )
                
                return SpawnOperation(
                    parent_node_id=self.node.id,
                    node_embryo=NodeEmbryo(
                        action_id=current_action_id, message=self.node.message
                    )
                )
        else: # There's no good action path to take
            failure_message = completion.failure_message
            
            self.log({
                "role": "swarmstar",
                "content": "The router failed to find a good action path to take."
            })
            self.report(
                f"Tried to find a good action path to take given a directive, but failed.\n\n"
                f"Directive: {self.node.message}\n\nFailure message: {failure_message}"
            )
            
            raise ValueError(
                f"The router agent failed to find a good action path to take. We need to implement something here to handle this. For example we could pass this to the action creator or talk to the user.\n\nThe agent's failure message: {failure_message}"
            )
            # TODO Handle failure message. Pass to action creator or user for review

    def build_route_messages(self, goal: str, children_descriptions: List[str]) -> List[Dict[str, str]]:
        goal_and_action_path_options = (
            f"Directive: {goal}\n\n"
            f"Options:\n"
        )
        for i, description in enumerate(children_descriptions):
            goal_and_action_path_options += f"{i}. {description}\n"

        messages = [
            {"role": "system", "content": f"{ROUTE_ACTION_INSTRUCTIONS}\n\n{goal_and_action_path_options}"},
        ]
        return messages

    def get_children_descriptions(self, children_action_metadata: List[ActionMetadata]) -> List[str]:
        children_descriptions = []
        for child in children_action_metadata:
            children_descriptions.append(child.name + ": " + child.description)
        return children_descriptions

    def get_children_action_metadata(self, action_folder: ActionFolder) -> List[ActionMetadata]:
        children_metadata = []
        for child_id in action_folder.children_ids:
            child_metadata = get_action_metadata(self.swarm_config, child_id)
            if child_metadata.routable:
                children_metadata.append(child_metadata)
        return children_metadata