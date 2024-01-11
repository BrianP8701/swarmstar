# action_tree.json
This file defines the space of possible actions that the swarm can take. The action router helps navigate this space. 

The action name must correspond to a node. !PROBLEM! Nodes with the same name problems in namespace.. should it be the path? I reckon yeah.

{
    "type": "folder",
    "description": "This is the root of the action tree",
    "folder": {
        "type": "folder",
        "description": "[Description of the folder]",
        "contents": {
            "action1": {
                "type": "action",
                "description": "[Description of action 1]"
            },
            "subfolder": {
                "type": "folder",
                "description": "[Description of subfolder]",
                "contents": {
                    "action2": {
                        "type": "action",
                        "description": "[Description of action 2]"
                    }
                    // ... more actions or subfolders
                }
            }
            // ... more actions or subfolders
        }
    }
    // ... more folders at the root level
}


# memory_tree.json