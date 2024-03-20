from pydantic import BaseModel, Field
from typing import List, Dict, Any

from swarmstar.models import BlockingOperation
from swarmstar.actions.base_action import BaseAction

class ActionPlan(BaseModel):
    plan: List[str] = Field(..., description="The plan to be executed. Each element in this list is an action to be pursued immediately, in parallel, without dependencies.")

PLAN_INSTRUCTIONS = (
    "You need to decide on a plan of action. Output a list of actions to take. "
    "Actions should be specific, actionable and concise. Ensure that the actions are independent and can be executed in parallel. Pursuing multiple actions at the same time is efficient, but only viable if they are entirely independent. It's okay to only output one action if we need it to be done before we can proceed with the next action. Your an actual AGI system trying to solve a problem, so think like one."
)

class Action(BaseAction):
    def main(self):
        message = (
            f"{PLAN_INSTRUCTIONS}"
            f"\n\nDirective: \n`{self.node.message}`"
        )
        self.generate_plan(message)

    @BaseAction.oracle_access
    def generate_plan(self, message: str) -> BlockingOperation:
        return BlockingOperation(
            node_id=self.node.id,
            blocking_type="instructor_completion",
            args={"message": message, "instructor_model_name": "ActionPlan"},
            context={},
            next_function_to_call="review_plan"
        )

    @BaseAction.receive_completion_handler
    def review_plan(self, completion: ActionPlan, context: Dict[str, Any]) -> None:
        pass

