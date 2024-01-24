from core.swarm.configuration_utils import get_default_action_tree

def test_get_default_action_tree():
    action_tree = get_default_action_tree()
    assert isinstance(action_tree, dict), "The returned action tree is not a dictionary"
    print("Test passed!")

if __name__ == "__main__":
    test_get_default_action_tree()
    
