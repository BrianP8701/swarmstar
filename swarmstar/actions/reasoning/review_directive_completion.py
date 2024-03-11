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


class ReviewDirectiveCompletionModel(BaseModel):
    is_complete: bool = Field(
        ..., description="Whether the directive is complete or not."
    )
    questions: Optional[str] = Field(
        None, description="Ask questions to determine if the directive has been completed."
    )

REVIEW_DIRECTIVE_COMPLETION_INSTRUCTIONS = (
    "Your purpose is to review and determine if the directive has been completed. "
    "You'll be given the directive and reports detailing what has been done. "
    "You have 3 choices:\n"
    "1. If the directive is complete, mark is_complete as True, and leave questions empty.\n"
    "2. If the directive is not complete, mark is_complete as False, and leave questions empty.\n"
    "3. If you need more information to determine if the directive is complete, mark is_complete as False, "
    "and ask for the information you need in the questions field."
)


class Action(BaseAction):
    """
    execution_memory:
        branch_head_node_ids_under_review: List[str]
            In the first phase of this action, we'll be reviewing each branch. This list
            will contain the ids of the branch head nodes under review. When done reviewing
            a branch, we'll remove it from this list. When the list is empty, we'll move
            to the next phase.
        branch_reports: Dict[str, List[str]]
            A dictionary of branch head node ids to a list of their respective reports.
            Each branch will have a list of reports from all its leaf nodes and immediate
            child decompose directive nodes. In addition to the reports, we'll also add
            answers to any questions the reviewer asks to this list.
    """
    def main(self) -> List[BlockingOperation]:
        return self.review_branches(self)
            
    def review_branches(self) -> List[BlockingOperation]:
        """
            For each branch, collect reports of all leaf nodes and immediate child decompose 
            directive nodes. Use an LLM to determine if each branch has completed it's assigned
            subdirective. It also may choose to ask questions to make a better decision.
        """
        log_index_key = self.log({
            "role": "swarmstar",
            "content": ("Reviewing if parent's directive has been completed. Reviewing each branch "
                        "in parallel and determining if it's subdirective is complete.")
        })

        decompose_directive_node = get_swarm_node(self.swarm_config, self.node.parent_id)
        branch_head_node_ids = decompose_directive_node.children_ids
        self.add_value_to_execution_memory("branch_head_node_ids_under_review", branch_head_node_ids)

        branch_reports = self._get_branch_reports(branch_head_node_ids)
        self.add_value_to_execution_memory("branch_reports", branch_reports)

        confirm_completion_operations = []
        for node_id in branch_head_node_ids:
            this_branch_reports_str = "\n".join(branch_reports[node_id])
            this_branch_directive = get_swarm_node(self.swarm_config, node_id).message
            
            system_message = (
                f"{REVIEW_DIRECTIVE_COMPLETION_INSTRUCTIONS}"
                f"\n\nBranch directive:\n{this_branch_directive}"
                f"\n\nBranch reports:\n{this_branch_reports_str}"
            )
            messages = [{"role": "system", "content": system_message}]

            this_branch_log_index_key = self.log({
                "role": "system",
                "content": system_message
            }, log_index_key)
            
            confirm_completion_operations.append(
                BlockingOperation(
                    node_id=self.node_id,
                    blocking_type="instructor_completion",
                    args={
                        "messages": messages,
                        "instructor_model": "ReviewDirectiveCompletionModel",
                    },
                    context={
                        "branch_head_node_id": node_id,
                        "log_index_key": this_branch_log_index_key
                    },
                    next_function_to_call="analyze_branch_review"
                )
            )        
        return confirm_completion_operations

    def analyze_branch_review(self, completion: ReviewDirectiveCompletionModel, branch_head_node_id: str, log_index_key: List[int]):
        """
            Analyzes the completion model returned by the AI. If the AI has questions, we'll 
            spawn a communication node to get answers. If the AI has determined the branch
            has completed it's directive, we'll remove it from the list of branches under review.
            
            Once all branches have been reviewed, we'll move to the next phase.
        """
        self.log({
            "role": "ai",
            "content": (
                f"Is the directive complete: {completion.is_complete if completion.is_complete is not None else 'None'}\n\n"
                f"Questions: {completion.questions if completion.questions is not None else 'None'}"
            )
        }, log_index_key)
        
        if completion.questions:
            self.log({
                "role": "swarmstar",
                "content": "Spawning a communication node to ask questions about the branch."
            }, log_index_key)

            self.add_value_to_execution_memory("__termination_handler__", "review_branch_with_questions_answered")
            self.update_termination_policy("custom_action_termination")
            return SpawnOperation(
                node_id=self.node.id,
                node_embryo=NodeEmbryo(
                    action_id="swarmstar/actions/communication/route_questions",
                    message=completion.questions
                ),
                context={
                    "branch_head_node_id": branch_head_node_id,
                    "log_index_key": log_index_key
                }
            )
        else:
            is_complete = completion.is_complete
            if is_complete is None:
                raise ValueError("The ai returned None for both params, questions and is_complete in the ReviewDirectiveModel.")
            elif is_complete:
                self.log({
                    "role": "swarmstar",
                    "content": "This branch has completed it's directive."
                }, log_index_key)
            else:
                self.log({
                    "role": "swarmstar",
                    "content": "This branch has not completed it's directive."
                }, log_index_key)

            execution_memory = self.node.execution_memory
            execution_memory["branch_head_node_ids_under_review"].pop(branch_head_node_id)
            self.update_execution_memory(execution_memory)
            if not execution_memory["branch_head_node_ids_under_review"]:
                log_index_key.pop()
                self.log({
                    "role": "swarmstar",
                    "content": "All branches have been reviewed. Moving on to confirm completion of overarching directive."
                }, log_index_key
                )
                self.node.execution_memory.pop("__termination_handler__", None)
                self.remove_value_from_execution_memory("branch_head_node_ids_under_review")
                self.update_termination_policy("simple")
                return self.confirm_completion_of_overarching_directive()

    @BaseAction.termination_handler
    def review_branch_with_questions_answered(self, terminator_node_id: str, context: Dict[str, Any]):
        """
            This function is called when the communication node spawned to answer 
            questions about the branch has terminated. The AI will then repeat the 
            analysis of the branch with the answers to the questions, potentially 
            asking more questions or making a final decision on this branch's 
            completion.
        """
        branch_head_node_id = context["branch_head_node_id"]
        log_index_key = context["log_index_key"]
        branch_head_node = get_swarm_node(self.swarm_config, branch_head_node_id)
        branch_directive = branch_head_node.message
        reports = self.node.execution_memory["branch_reports"][branch_head_node_id]
        terminator_node = get_swarm_node(self.swarm_config, terminator_node_id)
        question_answers = terminator_node.report
        
        self.log({
            "role": "swarmstar",
            "content": f"Received answers to questions:\n{question_answers}"
        }, log_index_key)

        reports += f"\n\n{question_answers}"
        self.node.execution_memory["branch_reports"][branch_head_node_id] = reports

        system_message = (
            f"{ReviewDirectiveCompletionModel}"
            f"\n\nBranch directive:\n{branch_directive}"
            f"\n\nBranch reports:\n{reports}"
        )
        messages = [{"role": "system", "content": system_message}]

        self.log({
            "role": "system",
            "content": system_message
        }, log_index_key)
        
        return BlockingOperation(
            node_id=self.node_id,
            blocking_type="instructor_completion",
            args={
                "messages": messages,
                "instructor_model": "ReviewDirectiveCompletionModel",
            },
            context={
                "branch_head_node_id": branch_head_node_id
            },
            next_function_to_call="analyze_branch_review"
        )

    def confirm_completion_of_overarching_directive(self) -> List[BlockingOperation]:
        """
            This is the final step in the review process. Given reports of all branches,
            and answers to any questions which we gathered in execution memory along the 
            way, we'll ask the AI to make a final decision on whether the overarching
            directive has been completed. It may also ask questions to make a better decision.
            
            If the AI determines the directive is complete, it will terminate and signal the parent
            node to terminate as well. If the AI determines the directive is not complete, it will
            spawn a new decompose directive node to continue the process, generating the next 
            sequential set of subdirectives.
        """

        all_branch_reports = []
        for branch_head_node_id, reports in self.node.execution_memory["branch_reports"].items():
            reports_str = "\n".join(reports)
            branch_directive = get_swarm_node(self.swarm_config, branch_head_node_id).message
            all_branch_reports.append(f"Branch directive: {branch_directive}\n\nBranch reports:\n{reports_str}\n\n")
            
        reports_str = "\n\n".join(all_branch_reports)
        overarching_directive = get_swarm_node(self.swarm_config, self.node.parent_id).message
        system_message = (
            f"{REVIEW_DIRECTIVE_COMPLETION_INSTRUCTIONS}"
            f"\n\nOverarching directive:\n{overarching_directive}"
            f"\n\nFollowing reports are from branches which pursued subdirectives derived from the overarching directive."
            f"\n\nBranch reports:\n{reports_str}"
        )
        messages = [{"role": "system", "content": system_message}]

        self.log({
            "role": "system",
            "content": system_message
        })

        return BlockingOperation(
            node_id=self.node_id,
            blocking_type="instructor_completion",
            args={
                "messages": messages,
                "instructor_model": "ReviewDirectiveCompletionModel",
            },
            next_function_to_call="analyze_overarching_directive_review"
        )

    def analyze_overarching_directive_review(self, completion: ReviewDirectiveCompletionModel):
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
                "content": "Spawning a communication node to ask questions."
            })
            self.add_value_to_execution_memory("__termination_handler__", "review_overarching_directive_with_questions_answered")
            self.update_termination_policy("custom_action_termination")
            return SpawnOperation(
                node_id=self.node.id,
                node_embryo=NodeEmbryo(
                    action_id="swarmstar/actions/communication/route_questions",
                    message=completion.questions
                )
            )
        else:
            is_complete = completion.is_complete

            if is_complete is None:
                raise ValueError("The ai returned None for both params, questions and is_complete in the ReviewDirectiveModel.")
            
            all_reports = "\n\n".join(self.node.execution_memory["branch_reports"].values())
            all_reports += self.node.execution_memory["overarching_directive_questions_answers"] if \
            "overarching_directive_questions_answers" in self.node.execution_memory else ""
            self.clear_execution_memory()
            self.report(all_reports)
            
            if is_complete:
                self.log({
                    "role": "swarmstar",
                    "content": "The overarching directive has been completed."
                })

                return TerminationOperation(
                    node_id=self.node.id,
                    terminator_node_id=self.node.id,
                    target_node_id=self.node.id
                )
            else:
                self.log({
                    "role": "swarmstar",
                    "content": "The overarching directive has not been completed."
                })
                return SpawnOperation(
                    node_id=self.node.id,
                    node_embryo=NodeEmbryo(
                        action_id="swarmstar/actions/reasoning/decompose_directive",
                        message=all_reports
                    )
                )

    @BaseAction.termination_handler
    def review_overarching_directive_with_questions_answered(self, terminator_node_id: str, context: Dict[str, Any]):
        """
            This function is called when the communication node spawned to answer 
            questions about the overarching directive has terminated. The AI will then repeat the 
            analysis of the overarching directive with the answers to the questions, potentially 
            asking more questions or making a final decision on the overarching directive's 
            completion.
        """
        terminator_node = get_swarm_node(self.swarm_config, terminator_node_id)
        question_answers = terminator_node.report
        execution_memory = self.get_node().execution_memory
        overarching_directive_questions_answers = execution_memory.get("overarching_directive_questions_answers", "")
        overarching_directive_questions_answers += f"\n\n{question_answers}"
        execution_memory["overarching_directive_questions_answers"] = overarching_directive_questions_answers
        self.update_execution_memory(execution_memory)        
        self.update_termination_policy("simple")
        self.remove_value_from_execution_memory("__termination_handler__")

        self.log({
            "role": "swarmstar",
            "content": f"Received answers to questions:\n{question_answers}"
        })
        
        all_branch_reports = []
        for branch_head_node_id, reports in self.node.execution_memory["branch_reports"].items():
            reports_str = "\n".join(reports)
            branch_directive = get_swarm_node(self.swarm_config, branch_head_node_id).message
            all_branch_reports.append(f"Branch directive: {branch_directive}\n\nBranch reports:\n{reports_str}\n\n")
        reports_str = "\n\n".join(all_branch_reports)
        
        system_message = (
            f"{ReviewDirectiveCompletionModel}"
            f"\n\nOverarching directive:\n{get_swarm_node(self.swarm_config, self.node.parent_id).message}"
            f"\n\nFollowing reports are from branches which pursued subdirectives derived from the overarching directive."
            f"\n\nBranch reports:\n{reports_str}"
            f"\n\nAnswers to questions:\n{overarching_directive_questions_answers}"
        )
        messages = [{"role": "system", "content": system_message}]
        
        self.log({
            "role": "system",
            "content": system_message
        })
        return BlockingOperation(
            node_id=self.node_id,
            blocking_type="instructor_completion",
            args={
                "messages": messages,
                "instructor_model": "ReviewDirectiveCompletionModel",
            },
            next_function_to_call="analyze_overarching_directive_review"
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
