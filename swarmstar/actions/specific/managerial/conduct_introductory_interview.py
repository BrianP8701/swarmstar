from typing import Any, Dict

from swarmstar.models import (
    BlockingOperation,
    NodeEmbryo,
    SpawnOperation,
    SwarmNode,
    Memory,
    MemoryMetadata
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

GENERATE_USER_PREFERENCES_PROMPT = (
    "Craft a concise user profile based on their preferences for involvement in the project. "
    "The profile should guide when and how to engage the user, particularly around technical "
    "discussions and decision-making. Consider these refined examples:\n\n"
    "Non-Technical, Minimal Involvement: Prefers to stay uninvolved in technical matters and "
    "decision-making processes. Avoid technical discussions.\n"
    "Non-Technical, Strategic Involvement: Though lacking a technical background, the user "
    "wishes to outline core workflows and approve key designs, offering feedback on presented "
    "options rather than contributing to the creative process.\n"
    "Technical, Architectural Focus: Interested in making architectural decisions and naming "
    "key components. Prefers to oversee major decisions without delving into the minutiae of "
    "implementation or deployment.\n"
    "Repository Expert, Open Communication: The user is the original creator of the SwarmStar "
    "repository and possesses deep expertise in its workings. They encourage open queries regarding "
    "any aspects of the code or documentation that are unclear. Always consult the user for "
    "clarifications to ensure fidelity to the project's original vision and standards.\n"
    "Technical, Comprehensive Oversight: Desires updates on all significant system decisions "
    "for  approval. Seeks no role in frontend development but insists on approving and providing "
    "feedback on the design.\n\n"
    "Post-interview, distill the user's preferences into a succinct profile to guide their project "
    "involvement. This task may present unique scenarios beyond these examples; aim for clarity and "
    "brevity."
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
    def generate_user_preferences(self, terminator_node_id: str, context: Dict[str, Any]):
        terminator_node = SwarmNode.get(terminator_node_id)
        post_interview_report = terminator_node.report
        self.add_value_to_execution_memory("post_interview_report", post_interview_report)

        self.log({
            "role": "swarmstar",
            "content": f"Received report on user's background after initial interview:\n{post_interview_report}"
        })

        system_message = (
            f"{GENERATE_USER_PREFERENCES_PROMPT}"
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
    def save_user_preferences(self, completion: str):
        user_preferences = completion
        memory_metadata = MemoryMetadata(
            is_folder=False,
            type="string",
            name="User Preferences",
            description="User preferences for project involvement",
            parent="user/"
        )
        Memory.save(memory_metadata, user_preferences)
    # TODO

