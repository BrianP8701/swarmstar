from swarm.core.swarm import Swarm
from swarm.core.oai_agent import OAI_Agent
from settings import Settings
import json
settings = Settings() # For config paths

async def python_coder(directive):
    swarm = Swarm()

    with open(settings.TOOLS_PATH) as f:
        tools = json.load(f)
    
    # Gather all relevant context
    code_analyst = OAI_Agent(tools['code_analyst']['instructions'], tools['code_analyst']['tools'], 'ask_questions')
    while True:
        questions = await code_analyst.chat(directive)
        analyst_has_questions = questions['arguments']['do_you_have_questions']
        
        if analyst_has_questions:
            questions = questions['arguments']['questions']
            user_input = input(f"\n\nGoal: {directive}\n\nQuestions: {questions}\n")
            directive = f'{directive}\n\nQuestions: {questions} \n\nUser answer: {user_input}'
        else: 
            break

    # Write code
    python_coder = OAI_Agent(tools['python_coder']['instructions'], tools['python_coder']['tools'], 'write_python')
    code = await python_coder.chat(directive)
    code = code['arguments']['python_code']
    python_metadata_extractor = OAI_Agent(tools['python_metadata_extractor']['instructions'], tools['python_metadata_extractor']['tools'], 'extract_metadata')
    metadata = await python_metadata_extractor.chat(code)
    name = metadata['arguments']['name']
    code_type = ['function', 'class', 'script', 'other']
    packet = {
        'language': 'python',
        'code_type': code_type[metadata['arguments']['code_type']],
        'code': code,
        'description': metadata['arguments']['description'],
        'dependencies': metadata['arguments'].get('dependencies', [])
    }

    file_name = settings.SYNTHETIC_CODE_PATH
    with open(file_name, 'r') as file:
        data = json.load(file)
    data[name] = packet
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)

    node_blueprints = [{'type': 'python_script_tester', 'data': {'code_key': name}}]
    return {'action': 'spawn', 'node_blueprints': node_blueprints}  