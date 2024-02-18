# Action Space
## What is the action space?
The action space contains all of the swarm's actions. Each node is designated a single action from this space. Action are predefined code, that have varying levels of dynamism sprinkled in from ai or human input. Some examples of actions:

    - decompose directive
    - route action
    - consolidate reports
    - write python
    - ask questions
    - ask user questions
    - browse internet
    - search swarm memory
    - create action
    - ...

Dynamism and intelligence is sprinkled into these actions from ais or talking to the human. The "create action" action allows the swarm to dynamically generate and create a new action on it's own if the action it needs doesen't exist in the action space. 

## Organization of the action space
The action space is organized as a tree, and each action has metadata that describes what it is and how to handle it. This is called the Action Metadata Space and is used to find what action to take.

## Navigating the action space
The action space is navigated by the "route_action" action. This node takes a goal and decides what is the best action to take. It starts from the root node of the action space. Given the goal, it looks at descriptons of the immediate children of the root action node. From this it decides what node to move to. It then repeats this process, traversing the action space until it reaches a leaf node, or an action.
