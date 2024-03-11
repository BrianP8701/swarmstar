"""
This agent is called when all the children of a "Decompose Directive" node have terminated.

The "DecomposeDirective" node breaks a directive into a set of,
    "immediate actionable subdirectives to be executed independently and in parallel."
    
Following the execution of these subdirectives, this node is called to make a decision.

    1. If the directive is complete, it will terminate and signal the parent node to terminate as well.
    2. If the directive is not complete, it will spawn a new decompose directive node to continue 
        the process, generating the next sequential set of subdirectives.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

from swarmstar.utils.swarmstar_space import get_swarm_node
from swarmstar.types import BlockingOperation, TerminationOperation, SpawnOperation, NodeEmbryo
from swarmstar.types.base_action import BaseAction


class ReviewDirectiveModel(BaseModel):
    is_complete: bool = Field(
        ..., description="Whether the directive is complete or not."
    )
    questions: Optional[str] = Field(
        None, description="Ask questions to determine if the directive has been completed."
    )

REVIEW_DIRECTIVE_INSTRUCTIONS = (
    "Your purpose is to review and determine if the directive has been completed. "
    "You'll be given the directive and reports detailing what has been done. "
    "You have 3 choices:\n"
    "1. If the directive is complete, mark is_complete as True, and leave questions empty.\n"
    "2. If the directive is not complete, mark is_complete as False, and leave questions empty.\n"
    "3. If you need more information to determine if the directive is complete, mark is_complete as False, "
    "and ask for the information you need in the questions field."
)




class Action(BaseAction):
    def main(self) -> List[BlockingOperation]:
        return self.confirm_completion_of_branches(self)
            
    def confirm_completion_of_branches(self) -> List[BlockingOperation]:
        self.log({
            "role": "swarmstar",
            "content": ("Reviewing if parent's directive has been completed. First, reviewing  "
                        "each branch and determining if it's subdirective is complete.")
        })

        decompose_directive_node = get_swarm_node(self.swarm_config, self.node.parent_id)
        branch_head_node_ids = decompose_directive_node.children_ids
        self.node.execution_memory["branch_head_node_ids_under_review"] = branch_head_node_ids
        
        branch_reports = self._get_branch_reports()
        self.node.execution_memory["branch_reports"] = {}
        for branch_head_node_id in branch_head_node_ids:
            self.node.execution_memory["branch_reports"][branch_head_node_id] = branch_reports[branch_head_node_id]

        confirm_completion_operations = []
        for node_id in branch_head_node_ids:
            branch_reports_str = "\n".join(branch_reports[node_id])
            branch_directive = get_swarm_node(self.swarm_config, node_id).message
            
            system_message = (
                f"{REVIEW_DIRECTIVE_INSTRUCTIONS}"
                f"\n\nBranch directive:\n{branch_directive}"
                f"\n\nBranch reports:\n{branch_reports_str}"
            )
            messages = [{"role": "system", "content": system_message}]

            self.log({
                "role": "system",
                "content": system_message
            })
            
            confirm_completion_operations.append(
                BlockingOperation(
                    node_id=self.node_id,
                    blocking_type="instructor_completion",
                    args={
                        "messages": messages,
                        "instructor_model": "ReviewDirectiveModel",
                    },
                    context={
                        "branch_head_node_id": node_id
                    },
                    next_function_to_call="analyze_branch_review"
                )
            )        
        return confirm_completion_operations

    def analyze_branch_review(self, completion: ReviewDirectiveModel, branch_head_node_id: str):
        self.log({
            "role": "ai",
            "content": (
                f"Is the directive complete: {completion.is_complete if completion.is_complete is not None else 'None'}\n\n"
                f"Questions: {completion.questions if completion.questions is not None else 'None'}"
            )
        })
        
        if completion.questions:
            self.log({
                "role": "swarmstar",
                "content": "Asking questions to determine if this branch completed it's directive."
            })
            self.node.execution_memory["__termination_handler__"] = "analyze_branch_question_answers"
            return SpawnOperation(
                node_id=self.node.id,
                node_embryo=NodeEmbryo(
                    action_id="swarmstar/actions/communication/route_questions",
                    message=completion.questions
                ),
                termination_policy_change="custom_action_termination",
                context={
                    "branch_head_node_id": branch_head_node_id
                }
            )
            
    def analyze_branch_question_answers(self, terminator_node_id: str, context: Dict[str, Any]):
        branch_head_node_id = context["branch_head_node_id"]
        branch_head_node = get_swarm_node(self.swarm_config, branch_head_node_id)
        branch_directive = branch_head_node.message
        reports = self.node.execution_memory["branch_reports"][branch_head_node_id]
        
        self.log({
            "role": "swarmstar",
            "content": "Received answers to questions."
        })
        
        terminator_node = get_swarm_node(self.swarm_config, terminator_node_id)
        question_answers = terminator_node.report
        
        reports += f"\n\n{question_answers}"
        
        system_message = (
            f"{REVIEW_DIRECTIVE_INSTRUCTIONS}"
            f"\n\nBranch directive:\n{branch_directive}"
            f"\n\nBranch reports:\n{reports}"
        )
        messages = [{"role": "system", "content": system_message}]
        
        return BlockingOperation(
            node_id=self.node_id,
            blocking_type="instructor_completion",
            args={
                "messages": messages,
                "instructor_model": "ReviewDirectiveModel",
            },
            context={
                "branch_head_node_id": branch_head_node_id
            },
            next_function_to_call="analyze_branch_review"
        )
    
    
    
    
    
    

    def _get_branch_reports(self, branch_head_node_ids: List[str]) -> Dict[str, List[str]]:
        """
            Returns a dictionary of branch head node ids to a list of their respective reports.
            
            Each branch will have a list of reports from all its leaf nodes and immediate
            child decompose directive nodes.
        """
        branch_reports = {}
        
        def recursive_helper(head_node_id: str, node_id: str):
            """
                Recursively traverses down a branch to retrieve reports of 
                all leaf nodes. Also stops at decompose directive nodes.
            """
            
            node = get_swarm_node(self.swarm_config, node_id)
            if node.action_id == "swarmstar/actions/reasoning/decompose_directive":
                branch_reports[head_node_id].append(node.report)
            elif not node.children_ids:
                branch_reports[head_node_id].append(node.report)
            else:
                for child_id in node.children_ids:
                    recursive_helper(head_node_id, child_id)
                    
        
        for branch_head_node_id in branch_head_node_ids:
            branch_reports[branch_head_node_id] = []
            recursive_helper(branch_head_node_id, branch_head_node_id)
            self.node.execution_memory["branch_reports"][branch_head_node_id] = branch_reports[branch_head_node_id]