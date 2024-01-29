import json
import sys
import asyncio
sys.path.insert(0, '/Users/brianprzezdziecki/Code/Agent_Swarm_Experiments')

from old_swarm.utils.actions.validate_action_args import validate_action_args
from old_swarm.utils.memory.save_to_stage import stage_content
from old_swarm.core.oai_agent import OAI_Agent

async def python_coder(directive):
    with open('swarm/actions/code/python_coder/tools.json') as f:
        tools = json.load(f)

    # Gather all relevant context
    # code_analyst = OAI_Agent(tools['code_analyst']['instructions'], tools['code_analyst']['tools'], 'ask_questions')
    # while True:
    #     questions = await code_analyst.chat(directive)
    #     analyst_has_questions = questions['arguments']['do_you_have_questions']
        
    #     if analyst_has_questions:
    #         questions = questions['arguments']['questions']
    #         user_input = input(f"\n\nGoal: {directive}\n\nQuestions: {questions}\n")
    #         directive = f'{directive}\n\nQuestions: {questions} \n\nUser answer: {user_input}'
    #     else: 
    #         break

    # Write code
    python_coder = OAI_Agent(tools['python_coder']['instructions'], tools['python_coder']['tools'], 'write_python')
    python_coder_output = await python_coder.chat(directive)
    code = python_coder_output['arguments']['python_code']

    # Get metadata for code
    python_metadata_extractor = OAI_Agent(tools['python_metadata_extractor']['instructions'], tools['python_metadata_extractor']['tools'], 'extract_metadata')
    metadata_extractor_output = await python_metadata_extractor.chat(code)
    name = metadata_extractor_output['arguments']['name']
    code_type = ['function', 'class', 'script', 'other']
    metadata = {
        'language': 'python',
        'name': name,
        'code_type': code_type[metadata_extractor_output['arguments']['code_type']],
        'description': metadata_extractor_output['arguments']['description'],
        'dependencies': metadata_extractor_output['arguments'].get('dependencies', []),
        'file_extension': 'py'
    }

    # Save code to staging area and pass to memory router
    data_id = stage_content(code, metadata, name)
    node_blueprints = [{'type': 'memory/memory_router', 'data': {'data_id': data_id}}]
    lifecycle_command = {'action': 'spawn', 'node_blueprints': node_blueprints}
    report = {
        'message': f'Given the directive "{directive}", the python coder wrote the code "{data_id}"',
        'data_id': data_id
    }
    return {'report': report, 'lifecycle_command': lifecycle_command} 

def main(args):
    try:
        results = asyncio.run(python_coder(args['directive']))
        print(json.dumps(results))  # Convert dict to JSON and print
    except Exception as e:
        raise RuntimeError(f"Script execution failed: {str(e)}")

if __name__ == "__main__":
    schema = {
        "directive": str
    }
    args_dict = validate_action_args(schema)
    main(args_dict)