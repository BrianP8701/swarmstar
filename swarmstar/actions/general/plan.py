from pydantic import BaseModel, Field
from typing import List, Dict, Any

from swarmstar.models import BlockingOperation, SpawnOperation
from swarmstar.actions.base_action import BaseAction

class ActionPlan(BaseModel):
    plan: List[str] = Field(..., description="The plan to be executed. Each element in this list is an action to be pursued immediately, in parallel, without dependencies.")

class ReviewPlan(BaseModel):
    confirmation: bool = Field(..., description="Whether the plan is valid or not.")
    revised_plan: List[str] = Field(None, description="If the plan is not valid, the revised plan to be executed.")

PLAN_INSTRUCTIONS = (
    "You need to decide on a plan of action. Output a list of actions to take. "
    "Actions should be specific, actionable and concise. Ensure that the actions "
    "are independent and can be executed in parallel. Pursuing multiple actions at "
    "the same time is efficient, but only viable if they are entirely independent. "
    "It's okay to only output one action if we need it to be done before we can proceed "
    "with the next action. Your an actual AGI system trying to solve a problem, so think "
    "like one."
)

REVIEW_PLAN_INSTRUCTIONS = (
    "Please review the plan of action carefully. Your task is to determine if each action in the plan "
    "is truly independent and can be executed in parallel by separate teams without any dependencies or communication."
    "\n\nOutput a boolean value for the 'confirmation' field:"
    "\n- If all actions in the plan are independent and can be pursued immediately in parallel, output 'true'."
    "\n- If any action in the plan depends on the completion of another action or requires information from another action, output 'false'."
    "\n\nIf you output 'false', please provide a 'revised_plan' as a list of actions, where each action is independent and can be "
    "executed in parallel. Ensure that the revised plan maintains the original intent and goals, but with actions that can be "
    "pursued independently."
    "\n\nRemember, as an AGI system, your goal is to create an efficient and effective plan of action. Parallel execution is "
    "desirable, but only if the actions are truly independent. If dependencies exist, it's better to revise the plan and "
    "ensure each action can be executed independently."
)

class Action(BaseAction):
    def main(self):
        message = (
            f"{PLAN_INSTRUCTIONS}"
            f"\n\nDirective: \n`{self.node.message}`"
        )
        return self.generate_plan(message=message)

    @BaseAction.oracle_access
    def generate_plan(self, message: str) -> BlockingOperation:
        return BlockingOperation(
            node_id=self.node.id,
            blocking_type="instructor_completion",
            args={"message": message, "instructor_model_name": "ActionPlan"},
            context={},
            next_function_to_call="review_plan"
        )

    @BaseAction.receive_instructor_completion_handler
    def review_plan(self, completion: ActionPlan) -> None:
        plan = completion.plan
        return BlockingOperation(
            node_id=self.node.id,
            blocking_type="instructor_completion",
            args={"message": f"{REVIEW_PLAN_INSTRUCTIONS}\n\n{plan}", "instructor_model_name": "ReviewPlan"},
            context={"plan": plan},
            next_function_to_call="confirm_plan"
        )

    @BaseAction.receive_instructor_completion_handler
    def confirm_plan(self, completion: ReviewPlan, context: Dict[str, Any]) -> None:
        confirmation = completion.confirmation
        if confirmation:
            spawn_operations = []
            for action in context["plan"]:
                spawn_operations.append(
                    SpawnOperation(
                        parent_id=self.node.id,
                        action_id="routers/route_action",
                        message=action,
                    )
                )
            return spawn_operations
        else:
            revised_plan = completion.revised_plan
            return BlockingOperation(
                node_id=self.node.id,
                blocking_type="instructor_completion",
                args={"message": f"{REVIEW_PLAN_INSTRUCTIONS}\n\n{revised_plan}", "instructor_model_name": "ReviewPlan"},
                context={"plan": revised_plan},
                next_function_to_call="confirm_plan"
            )
