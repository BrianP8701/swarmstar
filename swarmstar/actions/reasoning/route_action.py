from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from swarmstar.swarm.types import (
    ActionFolder,
    ActionSpace,
    BlockingOperation,
    NodeEmbryo,
    SpawnOperation,
    SwarmOperation,
)
from swarmstar.swarm.types.base_action import BaseAction


class NextActionPath(BaseModel):
    index: Optional[int] = Field(
        None, description="Index of the best action path to take"
    )
    failure_message: Optional[str] = Field(
        None,
        description="There's no good action path to take. Describe what type of action is needed in detail.",
    )


ROUTE_ACTION_INSTRUCTIONS = (
    "Decide what action path to take based on the goal and the available actions. "
    "If there is no good action path to take, describe what type of action is needed "
    "in detail in the failure message, and leave index empty."
)


class RouteAction(BaseAction):
    def main(self) -> BlockingOperation:
        action_space = ActionSpace(swarm=self.swarm)
        root: ActionFolder = action_space["swarmstar/actions"]
        root_children_descriptions = self.get_children_descriptions(action_space, root)
        messages = self.build_route_messages(
            self.node.message, root_children_descriptions
        )

        self.add_journal_entry(
            {
                "header": "Decideing what action to take given directive",
                "content": self.node.message
            }
        )

        return BlockingOperation(
            node_id=self.node.node_id,
            blocking_type="instructor_completion",
            args={"messages": messages, "instructor_model_name": "NextActionPath"},
            context={"parent_action_id": "swarmstar/actions"},
            next_function_to_call="route_goal",
        )

    def route_goal(
        self, completion: NextActionPath, parent_action_id: str
    ) -> SwarmOperation:
        """
        This function gets called over and over again 
        until we reach a leaf node, aka an action.
        """
        
        if completion.index is not None:
            action_space = ActionSpace(swarm=self.swarm)
            parent_action = action_space[parent_action_id]
            next_action_id = parent_action.children_ids[completion.index]
            current_action = action_space[next_action_id]

            if current_action.is_folder:
                children_descriptions = self.get_children_descriptions(
                    action_space, current_action
                )
                messages = self.build_route_messages(
                    self.node.message, children_descriptions
                )
                return BlockingOperation(
                    node_id=self.node.node_id,
                    blocking_type="instructor_completion",
                    args={
                        "messages": messages,
                        "instructor_model_name": "NextActionPath",
                    },
                    context={"parent_action_id": next_action_id},
                    next_function_to_call="route_goal",
                )
            else:
                self.add_journal_entry({
                    "header": "Successfully routed action",
                    "content": f"Routed goal: {self.node.message} to {next_action_id}"
                })
                return SpawnOperation(
                    node_id=self.node.node_id,
                    node_embryo=NodeEmbryo(
                        action_id=next_action_id, message=self.node.message
                    )
                )
        else:
            failure_message = completion.failure_message
            raise ValueError(
                f"The router agent failed to find a good action path to take. We need to implement something here to handle this. For example we could pass this to the action creator or talk to the user.\n\nThe agent's failure message: {failure_message}"
            )
            # TODO Handle failure message. Pass to action creator or user for review

    def build_route_messages(
        self, goal: str, children_descriptions: List[str]
    ) -> List[Dict[str, str]]:
        goal_and_action_path_options = (
            f"Decide what action path is best to take to accomplish this goal: {goal}\n\n"
            f"Options:\n"
        )
        for i, description in enumerate(children_descriptions):
            goal_and_action_path_options += f"{i}. {description}\n"

        messages = [
            {"role": "system", "content": ROUTE_ACTION_INSTRUCTIONS},
            {"role": "system", "content": goal_and_action_path_options},
        ]
        return messages

    def get_children_descriptions(
        self, action_space: ActionSpace, action_folder: ActionFolder
    ) -> List[str]:
        children_descriptions = []
        for child_id in action_folder.children_ids:
            child_metadata = action_space[child_id]
            children_descriptions.append(child_metadata.description)
        return children_descriptions
