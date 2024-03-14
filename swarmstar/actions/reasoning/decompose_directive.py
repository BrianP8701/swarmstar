"""
Decompose a directive into immediate actionable subdirectives to be independently executed in parallel.

The agent will ask questions if it needs more information before decomposing the directive.
"""
from typing import List, Optional

from pydantic import BaseModel, Field

from swarmstar.models import BlockingOperation, NodeEmbryo, SpawnOperation
from swarmstar.actions.base_action import BaseAction


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
    "must be independent and parallel.\n\nChoose one of the options and proceed. Do not ask questions and "
    "decompose the directive at the same time."
)


class Action(BaseAction):
    def main(self) -> BlockingOperation:
        self.log({
            "role": "swarmstar",
            "content": "Decomposing directive into actionable subdirectives.",
        })
        
        system_message = (
            f"{DECOMPOSE_DIRECTIVE_INSTRUCTIONS}"
            f"\n\nDirective to decompose: \n`{self.node.message}`"
        )
        messages = [
            {"role": "system", "content": system_message}
        ]

        self.log({
            "role": "system",
            "content": system_message
        })

        return BlockingOperation(
            node_id=self.node.id,
            blocking_type="instructor_completion",
            args={"messages": messages},
            context={"instructor_model_name": "DecomposeDirectiveModel"},
            next_function_to_call="analyze_output",
        )

    @BaseAction.receive_completion_handler
    def analyze_output(self, completion: DecomposeDirectiveModel) -> SpawnOperation:
        '''
        Depending on the completion, we will either ask questions
        or spawn child nodes for each subdirective.
        '''
        self.log({
            "role": "ai",
            "content": (
                f"Scrap paper: {completion.scrap_paper if completion.scrap_paper is not None else 'None'}\n\n"
                f"Questions: {completion.questions if completion.questions is not None else 'None'}\n\n"
                f"Subdirectives: {completion.subdirectives if completion.subdirectives is not None else 'None'}"
            )
        })
        
        if completion.questions and len(completion.questions) > 0:
            message = (
                f"An agent was tasked with decomposing the directive: \n`{self.node.message}`"
                "\n\nBefore decomposing, the agent decided it needs the following questions answered first:\n"
                )
            message += "\n".join(completion.questions)

            self.log({
                "role": "swarmstar",
                "content": "Asking questions before decomposing directive."
            })
            
            spawn_operation = SpawnOperation(
                parent_node_id=self.node.id,
                node_embryo=NodeEmbryo(
                    action_id="swarmstar/actions/communication/ask_user_questions",
                    message=message,
                )
            )
            self.report(
                f"Tried to decompose directive but decided to ask questions first.\n\n"
                f"Directive:\n{self.node.message}\n\nQuestions:\n{completion.questions}"
            )

            return spawn_operation
        else:
            subdirectives = completion.subdirectives
            spawn_operations = []
            for subdirective in subdirectives:
                
                spawn_operation = SpawnOperation(
                    parent_node_id=self.node.id,
                    node_embryo=NodeEmbryo(
                        action_id="swarmstar/actions/reasoning/route_action",
                        message=subdirective,
                    )
                )
                
                spawn_operations.append(spawn_operation)

            self.log({
                "role": "swarmstar",
                "content": (
                    "Decomposed directive into subdirectives. Spawning action router "
                    "nodes to decide what action to take given the subdirectives."
                    )
            })
            self.report(
                f"Decomposed directive into immediate actionable subdirective to be independently "
                f"executed in parallel.\n\nDirective:\n{self.node.message}\n\nSubdirectives:\n{subdirectives}"
            )

            return spawn_operations
