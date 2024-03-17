"""
This agent is called when all the children of a "Decompose Directive" node have terminated.

The "DecomposeDirective" node breaks a directive into a set of,
    "immediate actionable subdirectives to be independently executed in parallel"
    
Following the execution of these subdirectives, this node is called to make a decision.

1. Review child branch subdirective completion:
    The first step is to review the completion of each branch's subdirective.

    Every node in swarmstar finishes execution of their action by producing a conclusive
    report detailing what they've done. We are to trust these reports, as it is each node's
    responsibility to produce an accurate report. Note, non-leaf nodes are typically managerial
    nodes that make decisions like routing actions or decomposing directives. Leaf nodes are 
    typically more actionable and the ones that actually do the work. 
    
    So what we'll do is collect the reports from every leaf node from every branch. In addition, 
    we don't want to overflood the context window so we don't want to traverse all the way down the 
    tree. Instead, if we reach a child decompose directive node, we'll stop and collect it's 
    "consolidated reports", from the node's context. This contains a condensed report of that 
    decompose directive's children.
    
    Now given this context on what this branch has performed, we'll ask the AI to make a decision
    on whether the branch has completed it's assigned subdirective. The AI may also choose to ask
    questions, which will spawn a question router node to handle and return answers. Once the AI has 
    finished making a decision for each branch, we'll move to the next phase.

2. Review overarching directive completion:
    Now that we've reviewed each branch, we'll collect all the reports and answers to any questions
    we've gathered along the way. We'll use this information to ask the AI to make a final decision
    on whether the overarching directive has been completed. The AI may also choose to ask questions,
    which will spawn a question router node to handle and return answers. Once the AI has finished
    making a decision, we'll move to the next phase.

3. Create summary of entire branch:
    Now that we've gathered enough information to make a decision on whether the overarching directive
    has been completed, we'll create a summary of what the entire branch has done from all the branch
    reports and question answers we've gathered along the way. This will be saved to the decompose 
    directive node's context as "consolidated reports". Based on the decision made in the previous phase,
    we have two options:
    
    a. If the AI has determined the directive is complete, we'll terminate and signal the parent node to
        terminate as well.
    b. If the AI has determined the directive is not complete, we'll spawn a new decompose directive node
        to continue the process, generating the next sequential set of subdirectives. This new decompose
        directive node will be given an updated directive, that takes the overarching directive, subdirectives
        and consolidated reports into account.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

from swarmstar.models import BlockingOperation, TerminationOperation, SpawnOperation, NodeEmbryo, SwarmNode
from swarmstar.actions.base_action import BaseAction


class ConfirmDirectiveModel(BaseModel):
    is_complete: bool = Field(
        ..., description="Whether the directive is complete or not."
    )
    questions: Optional[str] = Field(
        None, description="Ask questions to determine if the directive has been completed."
    )

confirm_directive_completion_INSTRUCTIONS = (
    "Your purpose is to review and determine if the directive has been completed. "
    "You'll be given the directive and reports detailing what has been done. You are "
    "to trust these reports, as it is each node's responsibility to produce an accurate report. "
    "In addition you may be given answers to questions you've previously asked when you were "
    "unsure in a previous attempt."
    "You have 3 choices:\n"
    "1. If the directive is complete, mark is_complete as True, and leave questions empty.\n"
    "2. If the directive is not complete, mark is_complete as False, and leave questions empty.\n"
    "3. If you need more information to determine if the directive is complete, mark is_complete as False, "
    "and ask for the information you need in the questions field."
)

CONSOLIDATE_REPORTS_INSTRUCTIONS = (
    "A node has been given a directive and decomposed it into a set of immediate actionable subdirectives "
    "to be executed independently in parallel. These branches have terminated, and you have just reviewed each "
    "branch, to first confirm the completion of each subdirective and then that of the overarching directive, "
    "asking questions along the way if necessary. Now you'll be given all those reports and question answers and "
    "have a new task: You must create a concise, yet comprehensive consolidated report covering everything this "
    "branch has done. Be certain to be concise, yet comprehensive."
)

UPDATE_DIRECTIVE_INSTRUCTIONS = (
    "A node has been given a directive and decomposed it into a set of immediate actionable subdirectives "
    "to be executed independently in parallel. These branches have terminated, but the overarching directive "
    "has not been completed. You have just reviewed each branch, to first confirm the completion of each subdirective "
    "and then that of the overarching directive, asking questions along the way if necessary. Now you'll be given "
    "a consolidated report of this branch and it's subdirectives. You must use all of this information to update the "
    "directive that will be passed to the next decompose directive node, who will generate another set of subdirectives "
    "to be executed independently in parallel. Be certain to be concise, yet comprehensive."
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
        return self.review_branches()
            
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

        decompose_directive_node = SwarmNode.get(self.node.parent_id)
        branch_head_node_ids = decompose_directive_node.children_ids
        branch_head_node_ids.remove(self.node.id)
        self.add_value_to_execution_memory("branch_head_node_ids_under_review", branch_head_node_ids)

        branch_reports = self._get_branch_reports(branch_head_node_ids)
        self.add_value_to_execution_memory("branch_reports", branch_reports)

        confirm_completion_operations = []
        for node_id in branch_head_node_ids:
            this_branch_reports_str = "\n".join(branch_reports[node_id])
            this_branch_directive = SwarmNode.get(node_id).message
            
            system_message = (
                f"{confirm_directive_completion_INSTRUCTIONS}"
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
                    node_id=self.node.id,
                    blocking_type="instructor_completion",
                    args={"messages": messages},
                    context={
                        "branch_head_node_id": node_id,
                        "log_index_key": this_branch_log_index_key,
                        "instructor_model_name": "ConfirmDirectiveModel"
                    },
                    next_function_to_call="analyze_branch_review"
                )
            )        
        return confirm_completion_operations

    @BaseAction.receive_completion_handler
    def analyze_branch_review(self, completion: ConfirmDirectiveModel, branch_head_node_id: str, log_index_key: List[int]):
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
                parent_node_id=self.node.id,
                node_embryo=NodeEmbryo(
                    action_id="communication/ask_user_questions",
                    message=completion.questions,
                    context={
                        "branch_head_node_id": branch_head_node_id,
                        "log_index_key": log_index_key
                    }
                )
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
            execution_memory["branch_head_node_ids_under_review"].remove(branch_head_node_id)
            self.update_execution_memory(execution_memory)
            if not execution_memory["branch_head_node_ids_under_review"]:
                log_index_key.pop()
                self.log({
                    "role": "swarmstar",
                    "content": "All branches have been reviewed. Moving on to confirm completion of overarching directive."
                }, log_index_key
                )
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
        branch_head_node = SwarmNode.get(branch_head_node_id)
        branch_directive = branch_head_node.message
        reports = self.node.execution_memory["branch_reports"][branch_head_node_id]
        terminator_node = SwarmNode.get(terminator_node_id)
        question_answers = terminator_node.report
        
        self.log({
            "role": "swarmstar",
            "content": f"Received answers to questions:\n{question_answers}"
        }, log_index_key)

        reports += f"\n\n{question_answers}"
        self.node.execution_memory["branch_reports"][branch_head_node_id] = reports

        system_message = (
            f"{ConfirmDirectiveModel}"
            f"\n\nBranch directive:\n{branch_directive}"
            f"\n\nBranch reports:\n{reports}"
        )
        messages = [{"role": "system", "content": system_message}]

        self.log({
            "role": "system",
            "content": system_message
        }, log_index_key)
        
        return BlockingOperation(
            node_id=self.node.id,
            blocking_type="instructor_completion",
            args={"messages": messages},
            context={
                "branch_head_node_id": branch_head_node_id,
                "instructor_model_name": "ConfirmDirectiveModel"
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
            branch_directive = SwarmNode.get(branch_head_node_id).message
            all_branch_reports.append(f"Branch directive: {branch_directive}\n\nBranch reports:\n{reports_str}\n\n")
            
        reports_str = "\n\n".join(all_branch_reports)
        overarching_directive = SwarmNode.get(self.node.parent_id).message
        system_message = (
            f"{confirm_directive_completion_INSTRUCTIONS}"
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
            node_id=self.node.id,
            blocking_type="instructor_completion",
            args={"messages": messages},
            context={"instructor_model_name": "ConfirmDirectiveModel"},
            next_function_to_call="analyze_overarching_directive_review"
        )

    @BaseAction.receive_completion_handler
    def analyze_overarching_directive_review(self, completion: ConfirmDirectiveModel):
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
                parent_node_id=self.node.id,
                node_embryo=NodeEmbryo(
                    action_id="communication/ask_user_questions",
                    message=completion.questions
                )
            )
        else:
            is_complete = completion.is_complete

            if is_complete is None:
                raise ValueError("The ai returned None for both params, questions and is_complete in the ReviewDirectiveModel.")
            
            self.add_value_to_execution_memory("is_overarching_directive_complete", is_complete)
            is_complete_message = "The overarching directive has been completed." if is_complete else "The overarching directive has not been completed."
            self.log({
                "role": "swarmstar",
                "content": is_complete_message
            })
            
            return self.consolidate_reports()

    @BaseAction.termination_handler
    def review_overarching_directive_with_questions_answered(self, terminator_node_id: str, context: Dict[str, Any]):
        """
            This function is called when the communication node spawned to answer 
            questions about the overarching directive has terminated. The AI will then repeat the 
            analysis of the overarching directive with the answers to the questions, potentially 
            asking more questions or making a final decision on the overarching directive's 
            completion.
        """
        terminator_node = SwarmNode.get(terminator_node_id)
        question_answers = terminator_node.report
        execution_memory = self.get_node().execution_memory
        overarching_directive_question_answers = (
            execution_memory.get("overarching_directive_question_answers", "") +
            f"\n\n{question_answers}"
        )
        execution_memory["overarching_directive_question_answers"] = overarching_directive_question_answers
        self.update_execution_memory(execution_memory)        
        self.update_termination_policy("simple")

        self.log({
            "role": "swarmstar",
            "content": f"Received answers to questions:\n{question_answers}"
        })
        
        all_branch_reports = []
        for branch_head_node_id, reports in self.node.execution_memory["branch_reports"].items():
            reports_str = "\n".join(reports)
            branch_directive = SwarmNode.get(branch_head_node_id).message
            all_branch_reports.append(f"Branch directive: {branch_directive}\n\nBranch reports:\n{reports_str}\n\n")
        reports_str = "\n\n".join(all_branch_reports)
        
        system_message = (
            f"{ConfirmDirectiveModel}"
            f"\n\nOverarching directive:\n{SwarmNode.get(self.node.parent_id).message}"
            f"\n\nFollowing reports are from branches which pursued subdirectives derived from the overarching directive."
            f"\n\nBranch reports:\n{reports_str}"
            f"\n\nAnswers to questions:\n{overarching_directive_question_answers}"
        )
        messages = [{"role": "system", "content": system_message}]
        
        self.log({
            "role": "system",
            "content": system_message
        })
        return BlockingOperation(
            node_id=self.node.id,
            blocking_type="instructor_completion",
            args={"messages": messages},
            context={"instructor_model_name": "ConfirmDirectiveModel"},
            next_function_to_call="analyze_overarching_directive_review"
        )

    def consolidate_reports(self):
        overarching_directive_question_answers = (
            self.node.execution_memory.get("overarching_directive_question_answers", "")
        )
        all_branch_reports = []
        for branch_head_node_id, reports in self.node.execution_memory["branch_reports"].items():
            reports_str = "\n".join(reports)
            branch_directive = SwarmNode.get(branch_head_node_id).message
            all_branch_reports.append(f"Branch directive: {branch_directive}\n\nBranch reports:\n{reports_str}\n\n")
        reports_str = "\n\n".join(all_branch_reports)
        reports_str += f"\n\n{overarching_directive_question_answers}"
        
        decompose_directive_node = SwarmNode.get(self.node.parent_id)
        subdirectives = decompose_directive_node.report
        
        system_message = (
            f"{CONSOLIDATE_REPORTS_INSTRUCTIONS}"
            f"\n\nOverarching directive:\n{decompose_directive_node.message}"
            f"\n\nSubdirectives:\n{subdirectives}"
            f"\n\nBranch reports:\n{reports_str}"
        )
        messages = [{"role": "system", "content": system_message}]

        self.log({
            "role": "system",
            "content": system_message
        })
        
        return BlockingOperation(
            node_id=self.node.id,
            blocking_type="openai_completion",
            args={"messages": messages},
            context={},
            next_function_to_call="close_review"
        )

    @BaseAction.receive_completion_handler
    def close_review(self, completion: str):
        self.log({
            "role": "ai",
            "content": completion.content
        })
        decompose_directive_node = SwarmNode.get(self.node.parent_id)
        if decompose_directive_node.context:
            decompose_directive_node.context["consolidated_reports"] = completion
        else:
            decompose_directive_node.context = {"consolidated_reports": completion}
        SwarmNode.replace(decompose_directive_node)
        
        is_complete = self.node.execution_memory["is_overarching_directive_complete"]
        if is_complete:
            self.log({
                "role": "swarmstar",
                "content": "The overarching directive has been completed. Terminating self and signaling parent to terminate."
            })
            self.report(
                "Reviewed decompose directive node's directive and all it's subdirectives. "
                "The overarching directive has been completed. Terminating self and signaling parent to terminate."
            )
            self.clear_execution_memory()
            return TerminationOperation(
                node_id=self.node.id,
                terminator_node_id=self.node.id,
            )
        else:
            self.log({
                "role": "swarmstar",
                "content": "The overarching directive has not been completed. Updating directive with information from this review."
            })

            system_message = (
                f"{UPDATE_DIRECTIVE_INSTRUCTIONS}"
                f"\n\nOverarching directive:\n{decompose_directive_node.message}"
                f"\n\nSubdirectives:\n{decompose_directive_node.report}"
                f"\n\nConsolidated reports:\n{completion}"
            )
            messages = [{"role": "system", "content": system_message}]
            
            self.log({
                "role": "system",
                "content": system_message
            })
            
            return BlockingOperation(
                node_id=self.node.id,
                blocking_type="openai_completion",
                args={"messages": messages},
                context={},
                next_function_to_call="spawn_new_decompose_directive_node"
            )
            
    @BaseAction.receive_completion_handler
    def spawn_new_decompose_directive_node(self, completion: str):
        self.log({
            "role": "ai",
            "content": completion
        })
        
        self.log({
            "role": "swarmstar",
            "content": "Spawning a new decompose directive node to continue the process."
        })
        self.report(
            "Reviewed decompose directive node's directive and all it's subdirectives. "
            "The overarching directive has not been completed. Spawning a new decompose "
            "directive node to continue pursuing the goal."
        )
        
        self.clear_execution_memory()
        return SpawnOperation(
            parent_node_id=self.node.id,
            node_embryo=NodeEmbryo(
                action_id="general/decompose_directive",
                message=completion
            )
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
            
            node = SwarmNode.get(node_id)
            if node.action_id == "general/decompose_directive":
                branch_reports[head_node_id].append(node.context["consolidated_reports"])
            elif not node.children_ids:
                branch_reports[head_node_id].append(node.report)
            else:
                for child_id in node.children_ids:
                    recursive_helper(head_node_id, child_id)

        for branch_head_node_id in branch_head_node_ids:
            branch_reports[branch_head_node_id] = []
            recursive_helper(branch_head_node_id, branch_head_node_id)
        
        return branch_reports
