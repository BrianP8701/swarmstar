"""
Decompose a directive into actionable subdirectives.

The agent will ask questions if it needs more information before decomposing the directive.
"""
from typing import List, Optional

from pydantic import BaseModel, Field

from swarmstar.swarm.types import BlockingOperation, NodeEmbryo, SpawnOperation
from swarmstar.swarm.types.base_action import BaseAction


class DecomposeDirectiveModel(BaseModel):
    scrap_paper: Optional[str] = Field(
        None,
        description="Scrap paper for notes, planning etc. Use this space to think step by step. (optional)",
    )
    questions: Optional[List[str]] = Field(
        ..., description="Questions you need answered before decomposition."
    )
    subdirectives: Optional[List[str]] = Field(
        ...,
        description="List of subdirectives to be executed in parallel, if you have no questions.",
    )


DECOMPOSE_DIRECTIVE_INSTRUCTIONS = (
    "You are given a directive. You have 2 options:\n"
    "1. Ask questions to get more information or clarification of requirements and intentions.\n"
    "2. Decompose the directive into actionable subdirectives that will be executed independently and in parallel. "
    "After those are done, youll generate the next set of subdirectives. I stress that the subdirectives "
    "must be independent and parallel.\n\nChoose one of the options and proceed. Do not ask questions and decompose the directive at the same time."
)


class DecomposeDirective(BaseAction):
    def main(self) -> BlockingOperation:
        messages = [
            {"role": "system", "content": DECOMPOSE_DIRECTIVE_INSTRUCTIONS},
            {
                "role": "user",
                "content": f"Directive to decompose: \n`{self.node.message}`",
            },
        ]

        self.add_journal_entry(
            {
                "header": "Directive to decompose",
                "content": self.node.message,
            }
        )

        return BlockingOperation(
            node_id=self.node.node_id,
            blocking_type="instructor_completion",
            args={
                "messages": messages,
                "instructor_model_name": "DecomposeDirectiveModel",
            },
            context={},
            next_function_to_call="analyze_output",
        )

    def analyze_output(self, completion: DecomposeDirectiveModel) -> SpawnOperation:
        '''
        Depending on the completion, we will either ask questions
        or spawn child nodes for each subdirective.
        '''
        if completion.questions and len(completion.questions) > 0:
            message = f"An agent was tasked with decomposing the directive: \n`{self.node.message}`\n\nBefore decomposing, the agent decided it needs the following questions answered first:\n"
            message += "\n".join(completion.questions)

            self.add_journal_entry(
                {
                    "header": "Question Requested",
                    "content": message
                }
            )
            
            spawn_operation = SpawnOperation(
                node_id=self.node.node_id,
                node_embryo=NodeEmbryo(
                    action_id="swarmstar/actions/communication/ask_user_questions",
                    message=message,
                ),
            )
            return spawn_operation
        else:
            subdirectives = completion.subdirectives
            spawn_operations = []
            for subdirective in subdirectives:
                spawn_operation = SpawnOperation(
                    node_id=self.node.node_id,
                    node_embryo=NodeEmbryo(
                        action_id="swarmstar/actions/reasoning/route_action",
                        message=subdirective,
                    ),
                )
                spawn_operations.append(spawn_operation)
            subdirectives_str = "\n".join(subdirectives)
            self.add_journal_entry(
                {
                    "header": "Successfully Decomposed Directives",
                    "content": subdirectives_str,
                }
            )

            return spawn_operations
