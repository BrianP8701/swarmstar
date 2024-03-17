from typing import Any, Dict

from swarmstar.models import (
    BlockingOperation,
    NodeEmbryo,
    SpawnOperation,
    SwarmNode
)
from swarmstar.actions.base_action import BaseAction

UNDERSTAND_USER_BACKGROUND_PROMPT = (
    "The following is a general prompt for understanding the user's background. "
    "It is not specific to any particular directive.\n\n"
    "The user has assigned a directive to the swarm. Before the swarm can proceed, "
    "we must understand the user's background. Some things we must ask:\n"
    "1. Does the user have any experience with this type of task? (If this is a "
    "technical/software directive, is the user technical? Do they know how to code?)\n"
    "2. How involved does the user want to be? Does the user want to come up with "
    "every feature, or do they want to be bothered as little as possible?\n\n"
    "If, and only if the user is technical:\n"
    "1. Does the user want to be involved in the technical decisions?\n"
    "2. If so, what type of decisions? Does the user want to be involved in "
    "creating the DSL, choosing the stack and architecture (Idk what the exact "
    "directive is, but im just making examples).\n"
    "3. Does the user want to confirm all decisions? What type of decisions can "
    "be made without the user's confirmation?\n\n"
    "I'm just a software engineer (The person writing this prompt), but if the user is "
    "asking for a directive in some field outside software, ask them what level of "
    "involvement they want to have in decision making, things similar to what I wrote "
    "above."
)

ANALYZE_USER_BACKGROUND_PROMPT = (
    "We have gotten more information about the user's background and how they want "
    "to be involved. Now we must make a decision:\n"
    "1. If the user wants to come up with every feature, we must ask them what they want.\n"
)

GENERATE_USER_DESCRIPTION_PROMPT = (
    "Now you need to generate a description of the user that will be used to decide if "
    "and when to get the user involved. The description should be concise. Examples:\n"
    "1. The user does not have a technical background and wants to be involved as little as "
    "possible. Do not discuss any technical details with the user.\n"
    "2. The user is a lawyer and has no technical background. He doesn't want to be involved "
    "in any technical decisions. He wants to come up with the main workflows and usage details "
    "and approve the frontend design, although he says you can come up with the frontend design "
    "and he'll just comment.\n"
    "3. The user is technical and wants to make architectural choices. He wants to be involved "
    "in naming important components, and wants to confirm high level decisions. He doesn't want "
    "to be involved in small details of the implementation or deployment details.\n"
    "4. The user is technical and wants to be updated about every high level system decision. "
    "He wants to confirm every decision. However, he doesn't want any involvement in the "
    "building the frontend, but does want to confirm and comment on the frontend design. "
    "He wants you to create the frontend and iterate on it until he's happy.\n\n"
    "Now given a report post interview with the user, generate a concise description of the "
    "user that will be used to decide if and when to get the user involved like the examples above. "
    "I'm sure there'll be lots of edge cases I didnt think of, but you get the idea."
)

class Action(BaseAction):
    def main(self) -> BlockingOperation:
        self.update_termination_policy("custom_action_termination")
        self.add_value_to_execution_memory("__termination_handler__", "")
        self.log({
            "role": "swarmstar",
            "content": "Spawning node to understand the user's background."
        })
        return SpawnOperation(
            node_id=self.node.id,
            node_embryo=NodeEmbryo(
                message=UNDERSTAND_USER_BACKGROUND_PROMPT,
                action_id="specific/managerial/ask_user_questions",
            ),
            next_function_to_call="understand_user_background",
        )

    @BaseAction.termination_handler
    def analyze_user_background(self, terminator_node_id: str, context: Dict[str, Any]):
        terminator_node = SwarmNode.get(terminator_node_id)
        post_interview_report = terminator_node.report
        self.add_value_to_execution_memory("post_interview_report", post_interview_report)
        
        self.log({
            "role": "swarmstar",
            "content": f"Received report on user's background after initial interview:\n{post_interview_report}"
        })
        
        system_message = (
            f"{GENERATE_USER_DESCRIPTION_PROMPT}"
            "\n\nPost interview report with the user:\n"
            f"{post_interview_report}"
        )
        
        self.log({
            "role": "system",
            "content": system_message
        })

        return BlockingOperation(
            node_id=self.node.id,
            blocking_type="instructor_completion",
            args={"messages": [{"role": "system", "content": system_message}]},
            context={"instructor_model_name": "UserDescriptionModel"},
            next_function_to_call="analyze_user_description",
        )

    @BaseAction.receive_completion_handler
    def save_user_description(self, completion: str):
        pass
    # TODO