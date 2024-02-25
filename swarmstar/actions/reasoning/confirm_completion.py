"""
This agent is called when all the children of a "DecomposeDirective" node have terminated.

It is crucial to note, the "DecomposeDirective" node breaks a directive into parallel 
subdirectives to be executed independently. There may still be further steps that need to be
taken following the completion of this set of subdirectives.

This agent will confirm the completion of the directive. If complete, it will terminate
and signal the parent node to terminate as well. Otherwise, it will spawn a new deompose
directive node to continue the process.
"""
from typing import List, Optional
from pydantic import BaseModel, Field

from swarmstar.swarm.types import BlockingOperation, SwarmState, TerminationOperation, SpawnOperation
from swarmstar.swarm.types.base_action import BaseAction


class ConfirmCompletionModel(BaseModel):
    is_complete: bool = Field(
        ..., description="Whether the directive is complete or not."
    )
    message: Optional[str] = Field(
        None, description="If the directive is not complete, this message will be sent back to the decompose directive node."
    )


CONFIRM_COMPLETION_INSTRUCTIONS = (
    "Your purpose is to review and determine if the directive has been completed. "
    "The node above you was given a directive, which it decomposed into subdirectives "
    "which were executed independently and in parallel. However, there may still be further "
    "steps that need to be taken following the completion of this set of subdirectives. "
    "You are given the directive and reports of all the child branches. Determine if the "
    "directive is complete or not. If it is not complete, generate a comprehensive message "
    "to send back to the decompose directive node, with all the information it might need to "
    "continue the process, to generate the next sequential set of subdirectives. The message "
    "you generate is all the node will see, so make sure it is comprehensive and actionable. "
)

class ConfirmCompletion(BaseAction):
    def main(self) -> BlockingOperation:
        '''
        Get reports of all child branches
        '''
        swarm_state = SwarmState(swarm=self.swarm)
        parent_node = swarm_state[self.node.parent_id]
        subdirectives = parent_node.journal[-1]["content"]
        initial_directive = parent_node.message
        child_branch_reports, branch_subdirectives = self.get_child_branch_reports()
        stringified_reports = ""
        for branch_report, branch_subdirective in zip(child_branch_reports, branch_subdirectives):
            joined_branch_reports = "\n".join(branch_report)
            stringified_reports += f"This branch's overarching directive is: {branch_subdirective}\n\n" \
                                   f"Here is the last journal entry of every node in this branch, stopping at a stop or leaf node:\n" \
                                   f"{joined_branch_reports}\n\n"
        
        messages = [
            {
                "role": "system", 
                "content": CONFIRM_COMPLETION_INSTRUCTIONS
            },
            {
                "role": "system",
                "content": (
                    f"The parent decomposed the directive: \n`{initial_directive}`\n\n",
                    f"Into subdirectives: {subdirectives}\n\n",
                    "Here are the reports of all the child branches:\n",
                    stringified_reports
                ),
            },
        ]
        
        self.add_journal_entry({
            "header": "Confirming Completion of Directive",
            "content": parent_node.message
        })
        
        return BlockingOperation(
            node_id=self.node.node_id,
            blocking_type="instructor_completion",
            args={
                "messages": messages,
                "instructor_model_name": "ConfirmCompletionModel",
            },
            context={},
            next_function_to_call="analyze_output",
        )


    def analyze_output(self, completion: ConfirmCompletionModel) -> BlockingOperation:
        '''
        Depending on the completion, we will either terminate or spawn a new decompose directive node.
        '''
        if completion.is_complete:
            self.add_journal_entry({
                "header": "Directive Complete",
                "content": "The directive has been completed."
            })
            return TerminationOperation(
                node_id=self.node.node_id,
            )
        else:
            self.add_journal_entry({
                "header": "Directive Incomplete",
                "content": f"The directive is incomplete. The message to send back to the decompose directive node is: {completion.message}"
            })
            return SpawnOperation(
                node_id=self.node.node_id,
                node_embryo={
                    "action_id": "swarmstar/actions/reasoning/decompose_directive",
                    "message": completion.message
                }
            )

    def get_child_branch_reports(self) -> List[List[str]]:
        '''
        This function will return a list of list of strings (all_branch_reports) 
        and a list of strings (branch_subdirectives)
        
        Each string in all_branch_reports contains the last journal entry of 
        a node in a branch.
        Each sublist in all_branch_reports represents a branch of the tree.
        
        Each string in branch_subdirectives contains the overarching directive
        of that entire branch.
        '''
        # When descending a branch, stop at these nodes
        # This should contain any nodes that have multiple children
        stop_action_ids = ["swarmstar/actions/reasoning/decompose_directive"]

        swarm_state = SwarmState(swarm=self.swarm)
        parent_node = swarm_state[self.node.parent_id]
        all_branch_reports = []
        branch_subdirectives = []
        for child_id in parent_node.children_ids: # Loop through all children of decompose directive node
            if child_id == self.node.node_id: # Skip this node (the confirm completion node)
                continue
            child_node = swarm_state[child_id]
            branch_subdirectives.append(child_node.message)
            this_branches_reports = []
            while True: # Descend down the branch, attaching the last journal entry of each node
                last_journal_entry = child_node.journal[-1]
                this_branches_reports.append(f"{last_journal_entry['header']}: {last_journal_entry['content']}")
                if child_node.action_id in stop_action_ids:  
                    break
                if child_node.children_ids:
                    child_id = child_node.children_ids[0]
                else:
                    break
            all_branch_reports.append(this_branches_reports)
        return all_branch_reports, branch_subdirectives
