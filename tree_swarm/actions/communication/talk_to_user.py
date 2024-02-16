from pydantic import BaseModel, Field
from typing import List
from tree_swarm.swarm.types import Swarm, BlockingOperation, LifecycleCommand, NodeOutput

# TODO we need to handle cases where the persisted context or report gets too large


'''
    Instructor models and instructions
'''

# The conversation state is used by the model to generate messages and keep track of the conversation.
class ConversationState(BaseModel):
    questions: List[str] = Field(..., description="List of questions we need answered")
    persisted_context: str = Field(..., description="A very concise and compact representation of only the necessary information to persist through the conversation.")
    report: str = Field(..., description="Concise and comprehensive report of answers to our questions and supporting context.")
    message: str = Field(..., description="Message to send to user")
    
class AgentMessage(BaseModel):
    content: str = Field(..., description="The content of the message")
    

generate_initial_conversation_state_instructions = '''
Identify and clarify any unspecified information ("primary questions") from the goal.

Steps:
1. Review the goal and compile a list of information that needs clarification ("primary questions"). This list should be brief and focused.
2. Persist critical context that is needed for the conversation from the goal. This context should be minimal and directly support the agent in maintaining the conversation.
3. Craft an initial message to the user that is concise and clear to avoid confusion.

Leave the report field empty. You are initializing the conversation state'''.replace("\n", "\\n")

update_conversation_state_instructions = '''
Refine the conversation state based on the user's latest response.

Steps:
1. Update Questions: Review the user's latest message. Adjust the list of questions by removing resolved items and adding new ones as needed.
2. Update Context: Add relevant new details to the persisted context based off the most recent message. Keep it focused on essential information required for ongoing dialogue. Don't repeat anything already mentioned, what you say will be added to the current persisted context.
3. Update Reports: Add answers and relevant information to the reports given the users message. This report is what will be sent back when the conversation ends. Keep it brief and actionable yet comprehensive. Don't repeat anything already mentioned, what you say will be added to the current reports.'''.replace("\n", "\\n")

generate_message_instructions = '''
Generate a message to send to the user based on the current conversation state.

You are given a list of questions that need to be answered. In addition you have context that has been stored throughout the question. Do not stray off topic and only aim to get answers to the questions.'''.replace("\n", "\\n")

finalize_report_instructions = '''Given the list of reports, consolidate it into a single comprehensive yet concise report to return.'''.replace("\n", "\\n")


'''
    Action functions
'''


def main(swarm: Swarm, node_id: str, message: str):
    analyze_goal(node_id, message)
    
def analyze_goal(node_id: str, goal: str):
    '''
    The goal analysis step generates the initial conversation state.
    - It extracts a list of questions that need to be answered.
    - It extracts a concise and compact representation of only the necessary information to persist through the conversation.
    - It generates the first message to send to the user.
    
    Throughout the conversation:
    - It will update the list of questions by removing ones that have been answered and adding new questions that arise throughout the conversation.
    - It will update the persisted context be adding relevant details that the agent needs to keep in mind during the conversation.
    - It will update the report with answers and relevant information to the original questions.
    '''
    messages = [
        { 
            "role": "system",
            "content": generate_initial_conversation_state_instructions
        },
        {
            "role": "user",
            "content": f'Goal:\n{goal}'
        }
    ]
    
    return BlockingOperation(
        lifecycle_command=LifecycleCommand.BLOCKING_OPERATION,
        node_id=node_id,
        type="openai_instructor_completion",
        args={
            "messages": messages,
            "instructor_model": ConversationState
        },
        context = {},
        next_function_to_call="make_first_user_input_request"
    )
    
def make_first_user_input_request(node_id: str, completion: ConversationState):
    '''
    The first message gets sent to the user and we await the response.
    '''
    return BlockingOperation(
        lifecycle_command=LifecycleCommand.BLOCKING_OPERATION,
        node_id=node_id,
        type="initiate_conversation_with_user",
        args={
            "message": completion.message,
            "node_id": node_id
        },
        context = {
            "questions": completion.questions,
            "persisted_context": [completion.persisted_context],
            "reports": []
        },
        next_function_to_call="analyze_user_input"
    )
    
def analyze_user_input(node_id: str, conversation_id: str, user_input: str, questions: List[str], persisted_context: List[str], reports: List[str]):
    '''
    This step will analyze the user's input.
    '''
    messages = [
        { 
            "role": "system",
            "content": update_conversation_state_instructions
        },
        {
            "role": "user",
            "content": user_input
        },
        {
            "role": "system",
            "content": f"Update Questions: {questions}\n\nUpdate Context: {persisted_context}\n\nUpdate Report: {reports}"
        }
    ]
    return BlockingOperation(
        lifecycle_command=LifecycleCommand.BLOCKING_OPERATION,
        node_id=node_id,
        type="openai_instructor_completion",
        args={
            "messages": messages,
            "instructor_model": ConversationState
        },
        context = {
            "persisted_context": persisted_context,
            "reports": reports,
            "conversation_id": conversation_id
        },
        next_function_to_call="update_conversation_state"
    )
    
def update_conversation_state(node_id: str, conversation_id: str, completion: ConversationState, persisted_context: List[str], reports: List[str]):
    '''
    This step updates the conversation state given the analysis.
    '''
    if len(completion.questions) > 0:
        reports.append(completion.report)
        finalize_report(node_id, conversation_id, reports)
    else:
        persisted_context.append(completion.persisted_context)
        reports.append(completion.report)
        messages = [
            { 
                "role": "system",
                "content": generate_message_instructions
            },
            {
                "role": "system",
                "content": f"Questions: {completion.questions}\n\nContext: {persisted_context}"
            }
        ]
        return BlockingOperation(
            lifecycle_command=LifecycleCommand.BLOCKING_OPERATION,
            node_id=node_id,
            type="openai_instructor_completion",
            args={
                "messages": messages,
                "instructor_model": AgentMessage
            },
            context = {
                "persisted_context": persisted_context,
                "reports": reports,
                "conversation_id": conversation_id,
                "questions": completion.questions
            },
            next_function_to_call="make_user_input_request"
        )
    
def make_user_input_request(node_id: str, conversation_id: str, completion: AgentMessage, questions: List[str], persisted_context: List[str], reports: List[str]):
    return BlockingOperation(
        lifecycle_command=LifecycleCommand.BLOCKING_OPERATION,
        node_id=node_id,
        type="request_user_input",
        args={
            "message": completion.content,
            "conversation_id": conversation_id
        },
        context = {
            "conversation_id": conversation_id,
            "questions": questions,
            "persisted_context": persisted_context,
            "reports": reports
        },
        next_function_to_call="analyze_user_input"
    )

def finalize_report(node_id: str, reports: List[str]):
    '''
    This step finalizes the report and terminates the conversation.
    '''
    messages = [
        { 
            "role": "system",
            "content": finalize_report_instructions
        },
        {
            "role": "system",
            "content": f"Reports: {reports}"
        }
    ]
    return BlockingOperation(
        lifecycle_command=LifecycleCommand.BLOCKING_OPERATION,
        node_id=node_id,
        type="openai_instructor_completion",
        args={
            "messages": messages,
            "instructor_model": AgentMessage
        },
        context = {},
        next_function_to_call="terminate_conversation"
    )
    
def terminate_conversation(node_id: str, completion: AgentMessage):
    return NodeOutput(
        lifecycle_command=LifecycleCommand.TERMINATE,
        swarm_commands = [],
        report=completion.content
    )
