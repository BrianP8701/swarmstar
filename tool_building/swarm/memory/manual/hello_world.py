from swarm.utils import update_python_script_test_success

print('Hello World')

success = {
    'input': {'ooget': 'boogey'},
    'output': {'ooga': 'booga'}
}

update_python_script_test_success('hello_world', False, success)