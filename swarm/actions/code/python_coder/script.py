from swarm.core.swarm import Swarm
from settings import Settings
import json
settings = Settings() # For config paths

async def python_coder(goal):
    swarm = Swarm()
    
    # Gather all relevant context
    code_analyst = swarm.agents['code_analyst']
    while True:
        questions = await code_analyst.chat(goal)
        analyst_has_questions = questions['arguments']['do_you_have_questions']
        
        if analyst_has_questions:
            questions = questions['arguments']['questions']
            user_input = input(f"\n\nGoal: {goal}\n\nQuestions: {questions}\n")
            goal = f'{goal}\n\nQuestions: {questions} \n\nUser answer: {user_input}'
        else: 
            break

    # Write code
    python_coder = swarm.agents['python_coder']
    code = await python_coder.chat(goal)
    code = code['arguments']['python_code']
    python_metadata_extractor = swarm.agents['python_metadata_extractor']
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