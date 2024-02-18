'''
Throughout the conversation we maintain a "Conversation State" which is a data structure that contains the following:
    - A list of questions that need to be answered.
    - A concise and compact representation of only the necessary information to persist through the conversation.
    - A list of reports that is built up throughout the conversation. This report is what will be sent back when the conversation ends.
'''

from pydantic import BaseModel, Field
from typing import List
from swarm_star.swarm.types import BlockingOperation, TerminationOperation



class ConversationState(BaseModel):
    questions: List[str] = Field(..., description="List of questions we need answered")
    persisted_context: str = Field(..., description="A concise and compact representation of the necessary information to persist through the conversation.")
    report: str = Field(..., description="Concise and comprehensive report of answers to our questions and supporting context.")
    
class AgentMessage(BaseModel):
    content: str = Field(..., description="The message to send to the user.")
    
class FinalReport(BaseModel):
    report: str = Field(..., description="Concise and comprehensive report of answers to our questions and supporting context.")
    
generate_initial_conversation_state_instructions = (
    'Steps:\n\n'
    '1. Identify the questions that need to be answered.\n'
    '2. Persist critical context that is needed for the conversation from the goal. This '
    'context should be minimal and directly support the agent in maintaining the conversation.\n'
    '3. Craft an initial message to the user that is concise and clear to avoid confusion.\n\n'
    'Leave the report field empty. You are initializing the conversation state\n\n'
    'The reports aren\'t used as context throughout the conversation, so make sure all necessary context is in the persisted context.'
).replace("\n", "\\n")

update_conversation_state_instructions = (
    'Refine the conversation state based on the user\'s latest response.\n\n'

    'Steps:\n'
    '1. Update Questions: Rewrite the list of questions by removing resolved items and adding new ones as needed.\n'
    '2. Update Context: Rewrite the persisted context based off the most recent message. Keep it focused on essential ' 
    'information required for ongoing dialogue.\n'
    '3. Add to Reports: Add answers and relevant information to the reports given the users message. This report is what '
    'will be sent back when the conversation ends. Keep it brief and actionable yet comprehensive. What you say will be '
    'added to the current reports.\n\n'
    'The reports aren\'t used as context throughout the conversation, so make sure all necessary context is in the persisted context.'
).replace("\n", "\\n")

generate_message_instructions = (
    'Generate a message to send to the user based on the current conversation state and the user\'s most recent message.\n'
    'You are given a list of questions that need to be answered. Don\'t stray off topic and aim to get answers to the questions.'
).replace("\n", "\\n")

finalize_report_instructions = (
    'Consolidate the list of reports into a final report.'
).replace("\n", "\\n")



def main(node_id: str, message: str, **kwargs):
    generate_initial_conversation_state(node_id, message)
    
def generate_initial_conversation_state(node_id: str, message: str):
    messages = [
        { 
            "role": "system",
            "content": generate_initial_conversation_state_instructions
        },
        {
            "role": "user",
            "content": f'Extract questions from this message:\n`{message}`'
        }
    ]
    return BlockingOperation(
        operation_type='blocking',
        node_id=node_id,
        blocking_type="openai_instructor_completion",
        args={
            "messages": messages,
            "instructor_model": ConversationState
        },
        context = {
            "node_id": node_id    
        },
        next_function_to_call="generate_first_message"
    )
    
def generate_first_message(node_id: str, completion: ConversationState):
    messages = [
        {
            "role": "system",
            "content": generate_message_instructions
        },
        {
            "role": "system",
            "content": f"Questions: {completion.questions}\n\nContext: {completion.persisted_context}"
        }
    ]
    return BlockingOperation(
        operation_type='blocking',
        node_id=node_id,
        blocking_type="openai_instructor_completion",
        args={
            "messages": messages,
            "instructor_model": AgentMessage
        },
        context = {
            "node_id": node_id,
            "questions": completion.questions,
            "persisted_context": completion.persisted_context, 
        },
        next_function_to_call="create_chat"
    )
    
def create_chat(node_id: str, completion: AgentMessage, questions: List[str], persisted_context: str):
    return BlockingOperation(
        operation_type='blocking_operation',
        node_id=node_id,
        blocking_type="create_chat",
        args={
            "ai_message": completion.message,
            "node_id": node_id
        },
        context = {
            "node_id": node_id,
            "questions": questions,
            "persisted_context": persisted_context,
            "reports": []
        },
        next_function_to_call="update_conversation_state"
    )
    
def update_conversation_state(node_id: str, questions: List[str], persisted_context: str, reports: List[str], user_response: str,):
    messages = [
        { 
            "role": "system",
            "content": update_conversation_state_instructions
        },
        {
            "role": "user",
            "content": user_response
        },
        {
            "role": "system",
            "content": f"Update Questions: {questions}\n\nUpdate Context: {persisted_context}\n\nAdd to Reports: {reports}"
        }
    ]
    return BlockingOperation(
        operation_type='blocking_operation',
        node_id=node_id,
        blocking_type="openai_instructor_completion",
        args={
            "messages": messages,
            "instructor_model": ConversationState
        },
        context = {
            "node_id": node_id,
            "reports": reports,

        },
        next_function_to_call="update_conversation_state"
    )
    
def decide_to_continue_or_end_conversation(node_id: str, reports: List[str], completion: ConversationState):
    reports.append(completion.report)
    if (not completion.questions) or (len(completion.questions) > 0):
        finalize_report(node_id, reports)
    else:
        questions = completion.questions
        persisted_context = completion.persisted_context
        
        messages = [
            { 
                "role": "system",
                "content": generate_message_instructions
            },
            {
                "role": "system",
                "content": f"Questions: {questions}\n\nContext: {persisted_context}"
            }
        ]
        
        return BlockingOperation(
            operation_type='blocking_operation',
            node_id=node_id,
            blocking_type="openai_instructor_completion",
            args={
                "messages": messages,
                "instructor_model": AgentMessage
            },
            context = {
                "node_id": node_id,
                "questions": questions,
                "persisted_context": persisted_context,
                "reports": reports,
            },
            next_function_to_call="generate_message"
        )
    
def send_message(node_id: str, questions: List[str], persisted_context: str, reports: List[str], completion: AgentMessage):
    return BlockingOperation(
        operation_type='blocking_operation',
        node_id=node_id,
        blocking_type="send_message",
        args={
            "ai_message": completion.content,
            "node_id": node_id
        },
        context = {
            "node_id": node_id,
            "questions": questions,
            "persisted_context": persisted_context,
            "reports": reports
        },
        next_function_to_call="update_conversation_state"
    )
    
def finalize_report(node_id: str, reports: List[str]):
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
        operation_type='blocking_operation',
        node_id=node_id,
        blocking_type="openai_instructor_completion",
        args={
            "message": messages,
            "instructor_model": FinalReport
        },
        context = {
            "node_id": node_id   
        },
        next_function_to_call="terminate_conversation"
    )
    
def terminate_conversation(node_id: str, completion: AgentMessage):
    return TerminationOperation(
        node_id=node_id,
        operation_type='terminate',
        report=completion.content
    )
