from openai import OpenAI

client = OpenAI(api_key='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')

'''
Create assistant with no tools
'''
# assistant = client.beta.assistants.create(
#     instructions='Render the input as a distilled list of succinct statements, assertions, associations, concepts, analogies, and metaphors. The idea is to capture as much, conceptually, as possible but with as few words as possible. Write it in a way that makes sense to you, as the future audience will be another language model, not a human. Use complete sentences.',
#     name='Test_Agent',
#     tools=[],
#     model='gpt-4-1106-preview'
# )


'''
    OpenAI Official Function Tool Schema
'''
valid_tool_example = {
    'type': 'function',
    'function': {
        'name': 'add',
        'description': 'Sum up a list of numbers',
        'parameters': {
            'type': 'object',
            'properties': {
                'numbers': {
                    'type': 'array',
                    'items': {
                        'type': 'number',
                        'description': 'Number to sum up'
                    },
                    'description': 'List of numbers to sum up'
                }
            }
        }
    }
}


'''
    Create assistant with a tool
'''
# assistant = client.beta.assistants.create(
#     instructions='Render the input as a distilled list of succinct statements, assertions, associations, concepts, analogies, and metaphors. The idea is to capture as much, conceptually, as possible but with as few words as possible. Write it in a way that makes sense to you, as the future audience will be another language model, not a human. Use complete sentences.',
#     name='Test_Agent',
#     tools=[valid_tool_example],
#     model='gpt-4-1106-preview'
# )


'''
    List all assistants
'''
# my_assistants = client.beta.assistants.list(
#     order="desc",
#     limit="20",
# )
# print(my_assistants.data)


'''
    Modify assistant tools
'''
# from openai import OpenAI
# client = OpenAI()

# my_updated_assistant = client.beta.assistants.update(
#   "asst_l9tUmlor4UUFzWeQBJ5oOEqm",
#   tools=[valid_tool_example]
# )

# print(my_updated_assistant)


'''
    Modify assistant
'''
# my_updated_assistant = client.beta.assistants.update(
#   "asst_l9tUmlor4UUFzWeQBJ5oOEqm",
#   instructions="You are an HR bot, and you have access to files to answer employee questions about company policies. Always response with info from either of the files.",
#   name="HR Helper",
#   tools=[{"type": "retrieval"}],
#   model="gpt-4",
#   file_ids=["file-abc123", "file-abc456"],
# )

# print(my_updated_assistant)


'''
    Delete assistant by ID
'''
# response = client.beta.assistants.delete("asst_jOGFhaPALF8QpxpyuZjPSYqe")
# print(response)


'''
    Retrieve assistant by ID
'''
# my_assistant = client.beta.assistants.retrieve("asst_yfhdfCycSwUpTXaxgHA9m6A2")
# print(my_assistant)


'''
    Create thread
'''
# empty_thread = client.beta.threads.create(
#     metadata={
#         'name': 'Test Thread'
#     }
#     )
# print(empty_thread)


'''
    Delete thread by ID
'''
# response = client.beta.threads.delete("thread_kPMYHnc4PQgEuqF0ieJLlMhE")
# print(response)


'''
    Retrieve thread by ID
'''
# my_thread = client.beta.threads.retrieve("thread_B6vqqVGLRQxmBP5QAwyr1ylT")
# print(my_thread)


'''
    Create message
'''
# thread_message = client.beta.threads.messages.create(
#   "thread_kPMYHnc4PQgEuqF0ieJLlMhE",
#   role="user",
#   content="How does AI work? Explain it in simple terms.",
#   file_ids=[],
#   metadata={}
# )
# print(thread_message)


'''
    Retrieve message by ID
'''
# message = client.beta.threads.messages.retrieve(
#   message_id="msg_mNH5iZRTe6R8cjppeX6c3Q4L",
#   thread_id="thread_kPMYHnc4PQgEuqF0ieJLlMhE",
# )
# print(message)


'''
    List messages
'''
# thread_messages = client.beta.threads.messages.list("thread_B6vqqVGLRQxmBP5QAwyr1ylT")
# print(thread_messages.data)

'''
    Create a run
'''
# run = client.beta.threads.runs.create(
#   thread_id="thread_B6vqqVGLRQxmBP5QAwyr1ylT",
#   assistant_id="asst_l9tUmlor4UUFzWeQBJ5oOEqm"
# )
# print(run)


'''
    Retrieve a run
'''
# run = client.beta.threads.runs.retrieve(
#   thread_id="thread_3frcw3OSaQ7s9gnYyaGROYmu",
#   run_id="run_Vd3VV97mzv2VCec0WkcfXi8x"
# )
# print(run)


'''
    List runs
'''
# runs = client.beta.threads.runs.list(
#   "thread_Ty2TeHZjnmh38AZJUoPmRZ3t"
# )
# print(runs.data)
# print(runs.data[0].required_action.submit_tool_outputs.tool_calls[0].function.arguments)


'''
    Check if we need to call tools
'''
# run = client.beta.threads.runs.retrieve(
#   thread_id="thread_3frcw3OSaQ7s9gnYyaGROYmu",
#   run_id="run_Vd3VV97mzv2VCec0WkcfXi8x"
# )
# if(run.required_action):
#     tool_calls = run.required_action.submit_tool_outputs.tool_calls 
'''
    [{
        'id': '', 
        'type': 'function', 
        'function': {
            'name': '', 
            'description': '', 
            'arguments': {}
        }
    }]
'''


'''
Submit tool outputs to run
'''
# run = client.beta.threads.runs.submit_tool_outputs(
#   thread_id="thread_abc123",
#   run_id="run_abc123",
#   tool_outputs=[
#     {
#       "tool_call_id": "call_abc123",
#       "output": "28C"
#     }
#   ]
# )
# print(run)


'''
    Create thread and run in one request
'''
# run = client.beta.threads.create_and_run(
#   assistant_id="asst_l9tUmlor4UUFzWeQBJ5oOEqm",
#   thread={
#     "messages": [
#       {"role": "user", "content": "what is 7 + 5 + 4 + 30 + 2"}
#     ]
#   }
# )
# print(run)
