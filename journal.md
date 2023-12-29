Okay lol this is a preface i added later. this is just like a place for me to jot down my thoughts as i code the swarm. there is no cohesiveness, this is not meant to be read by anyone. but i like keeping it up

Okay so often i copy and paste the whole of this file into chatgpt when im stuck and have it help me pick up with my thoughts where i left off. so im gonna include the main doc page in between these underscored lines for that purpose:

____________________________________________________________________________________________
# Agent_Swarm_Experiments
Making experiments locally to contribute to AGI. Documenting my journey on YouTube @ [AI Agent Swarm Playlist](https://youtube.com/playlist?list=PLO8gVow6df_Rh7DEJ10_WAdnkGnIRCh-K&si=eYdyBu7NShKckilS)

# Principles
    1. Make everything as simple as possible
    2. Make swarm universally applicable/infinitely scalable to any goal
    3. Strategically build to take advantage of SOTA models
    4. Prepare for new modalities and robotics

## Usage
First, configure the .env file. Each subfolder contains an idea or experiment (RAG/agent swarm related). Each experiment contains a plan.md file for my personal use (likely not of any use to you), and a docs.md which you should read. The docs.md will contain usage instructions, architecture details etc.

In the rest of this file I will describe the motivation and takeaways of each experiment.

## Experiments

In theory - or my imagination at least - there ought to be an inflection point where the swarm becomes self sufficient. 

The swarm needs to be self aware that it is a swarm. The top agents need to know about the system they operate in. They need sufficient context. Lower agents who gain more and more specific tasks will need less context.



### Tool Building Experiment
Goal: Have agents autonomously make new python functions that can be used by the swarm
____________________________________________________________________________________________



We want functions that can:
    Take text describing a function
    Return a function

In addition we need the option to:
    Generate test cases for the function
    Make the function executable
    Run the function with the test cases
    Save the function
save the function, test the function

We want an agent that can:
    Take a function and a set of arguments
    Return the result of the function

## Agents


## Functions Config
json file with:
    function name
    function description
    function arguments
    function return type
    function test cases
    function code
    function dependencies

### Who can call functions?
there is one global entrypoint to functions: exec_function()
It checks if the 

### Initial Functions:
- create_assistant()
- create_function() 
- create_test_cases()
- test_function()
- save_function()



All of the above initialization will happen in what is called a 'toolkit'



okay fuck scrap the toolkit.

## Swarm flow in my head 1
Create head agent
Pass goal to head agent through chat()
Take output of chat(). Spawn a new standard agent with the output of chat() as the instructions

In order to write functions that interact with other functions, an agent needs to:
    1. be aware of the other functions
    2. be able to call the other functions

To be aware of other functions we need to include in the context all the function names, descriptions and parameters

There are some flows that are concrete, like the one aforementioned. But how can the swarm autonomously create and access new flows?

# Tool creation... were finally actually at the point where i can do it
okay.. okay...
so i now have the route subtasks down. the current flow is 

1. pass goal to swarm
2. swarm breaks goal down to smaller goals
3. swarm routes each goal to next task 

Now the "next task" could be anything like retrieve information from the web, github, some other api. Write or perform some action. Either way, the point is we might not have the capability to perform this next task. So we might have to 



One key thing is we dont want to break down tasks too much. Id rather opt for a swarm that tries to accomplish a task too early and realizes it has to break down more than one that frequently breaks down tasks too small.



having an agent write test cases for a piece of generated python code is challenging cuz depending on the code we might need an object that involves other shit... and the output is not a clear cut type, its dynamic... so first we need an agent to produce a tool schema for that code.




_________________________________________________________________

Ive made the agent that breaks down goals and the one that routes goals.... but now im confused. Im trying to write the "write_python" function:


from swarm.swarm import Swarm
from swarm.agent import Agent
import json
async def write_python(goal):
    swarm = Swarm()
    task_handler = swarm.task_handler
    python_agent: Agent = swarm.agents['write_python_agent']
    python_test_cases_agent: Agent = swarm.agents['python_test_cases_agent']
    
    tool_output = await python_agent.chat(goal)
    python_code = tool_output['arguments']['python_code']
    
    test_cases = 
    
    # Create test cases for function
    with open('tool_building/config/test_cases.json', 'r') as file:
        test_cases = json.load(file)


okay. calm down. recollect.
The assumption im making is that if the problem has been broken down enough, and we gather all the relevant context and information to solve the problem chatgpt should be able to solve it.

"Solving it." Ultimately, tasks get broken down into one of the following: [Write code, retrieval, run code] (for now)

First lets focus on the task of "writing code"

When writing code we need to gather all relevant context. Here's some examples:
    - If the code works with some class we previously made, we need that class in context to see how it works
    - If the code is a piece of a bigger project or process we need a comprehensive description of the architecture the code being written now will be put into
    - If the code is using some library we'll need to have the relvant documentation or actual code from that library in context potentially.

In doing this little exercise above... I realize one thing. Part of me previously believed what would happen is we break down the task into smaller pieces, and then at the bottom that agent will do a retrieval of whats relevant. But now part of me sees that in breaking down the task we might need context along the way to break down the task correctly.


so now i talked to myself a bit more. i kinda ranted abt my concerns.... whats the solution? Remember we want simple.... it needs to be simple.

theres rlly quite a lot of things the swarm needs to be capable of doing before becoming self sufficient. And it can become sel sufficient but be extremely sub optimal. I reckon... we gotta hack shit and optimize as we go. ahh back to the same old adage.

so we start simple. just write the python and save it. we'll assume the code will get written correctly. for now, dont worry about making test cases, debugging or complex retrieval. we'll start with a simple goal that wont need that then scale up.

_________________________________________________________________________________________________________

so first we try to have the swarm build a github class. 
then have it save and make it available to itself.

Add web scraping tools, pdf scrapers
save data locally and to database. Have a global VIEW of all data, and function describing how to get it if its local or on cloud
Add all of the above as functions

have the swarm create new functions to write code in different languages.
try to find ways to make the system more robust when it makes wrong decisions or errors in code
create a better user interface to allow the user to provide input while the swarm is running
Then try to have the swarm construct a web app (real estate autogen CMA's, chat, leads, zapier routing etc)
Try to have the swarm go over its own code and generate documentation describing itself, upgrade itself, add typing hints etc

As our database for the swarm grows we're going to need to create multiple different rag implementaions. one with embeddings-chunking strat, one with knowledge graph/folders, and more etc.


_________________________________________________________________________________________________________

# Tree structure
There are 3 concerns i have now:

1. Should i do the tree spawn-terminate method? Is that all encompassing? Is it too rigid and introducess too much complexity?
2. There needs to be places for user input. I have a temporary answer to this. Now initially, i can make it so that we have user input and verification at every step. I know, the point is that i want to automate the process, but initially this will make it easier, and it will also be easy to take this away later
3. This current task is very easy for a human. Im spending more effort getting the swarm to do it than itd take me alone. but - the key is that im automating this whole level of difficulty and type of task

The question is first and foremost how do we implement tree architecture?

Tasks are nodes. Tasks can spawn other tasks. 

TaskNode - we'll call them tasknodes. 

TaskNodes:
    - type (str)
    - children (List[TaskNode])
    - parent (TaskNode)

    - spawn new TaskNodes
    - terminate themselves and report to parent


Now, before we introduce these changes, lets review the current abstractions in place for tasks

We have a task type which holds the function name to be called in functions config and the corresponding parameters to be passed. Its a one time use thing.
Then we have the TaskHandler object which takes a task and runs it. very simple rn.

What i see now is that the forward pass and backwards pass through that Node will likely require us to call different functions. On the way down, we'll need to perform and decide what to do next. On the way up we'll be reviewing reports and seeing if our task is done and if we can terminate, or if we need to try again.

So the question is, at each Node is it as simple as having two functions, one for forward and one for backwards pass? Remember the age old adage - we want it to be as simple as possible to avoid complexity, but the swarm needs to be universally applicable and infinitely scalable.


________________



# Tree Implementation for Swarm

Fundamental unit is the node which consists of:
- TaskType
- Unique data
- Parent
- Children

What this means for simplicities sake is that each node cannot do internal review, rather it must spawn a new node to do so

Additionally the swarm must now maintain two more things:
- The curresnt state of the tree
- The history of the tree

Schema for swarm history (JSON):

create node
run node
delete node

[
    {
        action: "create_node",
        node: Node
    },
    {
        action: "run_node",
        node: Node
    },
    {
        action: "delete_node",
        node: Node
    },
    ...
]


When the swarm ends its run we must save a snapshot of the current state of the swamrm that is recreatable

Schema for swarm snapshot (JSON):
{
    population: x,
    nodes: {0: root_node, 1: node1, 2: node2...},
    task_queue: [(task, queue), (task, queue)...]
}

Now one challenge with taking the snapshot is at the time of deletion the task being performed at that moment will not be included in the snapshot


So now, when we implement this we'll be able to pick up where we left off with snapshot and get a good visualization with history


each node must now:
perform their task
save their output within themselves
save state and history
create children or terminate

OKAY I GOT IT. The functions in functions.py should not contain the logic related to nodes at all. 
Where does the loop go? What does the loop handle? Execution of tasks? Creation, deletion and activation of nodes?
Now the thing is functionally it doesent matter. Why does this decision matter? Because it affects the way we think about the swarm. 
If we think about the swarm as a loop that executes tasks, then we have to think about the swarm as a loop that executes tasks.
If we think about the swarm as a loop that creates, deletes and activates nodes, then we have to think about the swarm as a loop that creates, deletes and activates nodes.
The second way of thinking about it is more general. The first way of thinking about it is more specific.
The loop defines the level of granularity that will be easy for us to visualize and 
Oh shit i got it. At what granularity do we want to save state? Thats what matters for the swarm. 

To save state we need:
All the nodes

The reason we have history and state is because the current state of the swarm doesent show us how we got there as the swarm will delete nodes. So for history, to see how we got to the current state we need more.
We need all instances of node creation, execution and deletion

So that answers our question. We will have a queue in the swarm responsible for three tasks creation, execution and termination of nodes. this queue shall be called: node_lifecycle_queue
# Swarm coding Challenge

Okay I've identified a big challenge in the RAG portion of this project. When i have the swarm write code its going to need to write code to interact with the rest of the swarm and *squeeze* itself in. Okay lol i just thought of the solution.

Create an internal swarm api. And make good documentation on usage and functionality and just pass that to thw swarm whenever it is necessary. 

Now, when the swarm then needs to interact with other libraries or apis, its going to need to retrieve that documentation or code. in fact, we need to somehow do retrieval over the docs to find the relevant portion of the docs/code to add to context. Effective autonomous RAG is crucial for self sufficient swarm capabilities.

# Refactor structure plan for the future #TODO
So now i kinda have better thoughts.... ima need a big refactor but ima push features for a little longer because the complexity rn is still managable for my brain. But when I do refactor heres a rough structure:

- Swarm (Tree structure, nodes, state, history)
- TaskMaster is responsible for execution of all functions (task_queue)
- Internal Swarm API (minimal functionality for self sufficiency. This is some theoretical bound)
- Memory (Storing data, documentation and also code, classes etc to be used by the swarm)
- Human Interface (Terminal for now, but later a web app including visualization with easy access to communicate and interact with the swarm as it works)

Okay. so this actually helped clear up my head a lot. We get the swarm and taskmaster done once and for all, and then there should be no further iteration added there.

The internal swarm api will take time and lots of iteration to get right. But once its right, the swarm will be able to do anything.

The memory will be iterated on for all eternity. 

The key thing is that the internal swarm api needs to contain the rag functionally to effectively navigate the memory. thats what it all comes down to.



# Theoretical non rigorous thinking abt the internal swarm api

Okay... so what do we need to include in the internal swarm api for self sufficiency? specific fucntions:

- break down goal
- route goal
- write code/text
- save code/text so it can be used
- execute code
- retrieve context from memory




_____________________________________________________________________________________________

create node -> execute node -> create node, create node, create node -> execute node, execute node, execute node -> ... -> terminate node, terminate node, terminate node

okay the crucial thing is when a node terminates, it terminates itself and signals its parent to execute. a parent cant execute unless all of its children have given it the go. then it terminates itself and the process continues.

When we spawn a node, we spawn it and execute the node. That node is responsible for internally deciding whether to terminate or spawn children. 

so if we have the lifecycle queue in the swarm be responsible for two things:

- spawning nodes
- terminating nodes




## Creating/spawning nodes

This is my thought process writing the _create_node() function in swarm:

Well the node is actually already created. it has the task type, data and a pointer to its parent.
Now you need to save to history the fact that this node was created.
Save to state the node prior to execution
Then execute the task
Then save to state the node after execution
And save to history the fact that the node was executed

Now the question is, do we create/terminate nodes inside the task run, or seperate but inside the node?

Will every node use an LLM? Or will some just execute code?
Okay, not all nodes will use an LLM. Some will just execute code.

So lets clear up.... we need the node to be very general. lets think of all the things we want a node to be able to do:

- break down goals
- route goals to appropriate next tasks
- write text
- write code
- execute code
- read terminal output
- go back up and retrieve outputs from previous nodes
- browse the web
- interact with internal swarm api
... and many more

now that im looking at this... i take back what i said earlier. it does seem every node task is coupled with an llm interaction. cuz we can combine write & execute code, and etc.... Hmmmm.... lets see can i think of a node that would not involve the use of an llm...

okay so i talked to chatgpt... he complimented me and i let it feed my ego for how "complex" my project is. but anyway i came to the conclusion that i want each node to call an llm with this reasoning:

"I mean i think for my feel the swarm will take predefined routes and paths of logic, and the llm reasoning engine helps you know... automate my knowledge work and that should be what defines the granularity of a node. every node is one llm call."

So now we decided every node has:
type, data, parent, children, output

Each node will execute its predefined logic, and do an LLM call to automate a piece of knowledge work, and will then either execute some more logic then create a new node or just create a new node. So this means every node is associated with an agent + predefined logic. Now, how should we implement the flow of the node?

So the node has its type attribute which should link us to the logic and agent used in this node. It could be:

-> agent ->
-> logic -> agent ->
-> agen -> logic
-> logic -> agent -> logic

Okay each node is associated with a script. The script is stored as a string in one of the configuration files. executing the node is just executing the script. output is simply the output of that script. Included in the output is all the data needed to spawn the next set of nodes or to terminate self. We want to decouple swarm interaction from the script for simplicity purposes

all scripts will be run from the same place so import statements wont fuck up. all scripts are seperate and meant to run on their own

now the question is, actually 3 questions:
- are all scripts in python?
- where should i store the scripts?
- what metadata should i store alongside each script?

well lets just put language as metadata
store the scripts as strings in json file in config folder... but potentially in new folder later. thing is we'll probably have thousands and just more and more scripts in the future. this is where rag file system/tree comes in to organize navigation 


node_scripts.json:

{
    node_type: {
        language: str,
        description: str,
        script: str
    },
    ...
}

can add more metadata later as needed
most importantly, later on we're going to have to find better ways to organize and navigate the scripts and tools available to the swarm as it grows bigger



# Router

A question im saving for later, is rn the router has the choices:
['break_down_goal', 'write_text', 'write_python', 'retrieve_info', 'ask_user_for_help']

But how do we 'route' when we have many hundreds of options to route to?




Remember when we terminate a node we dont just go up to the most recent fork in the tree. some managers didnt do inparralel at break but had a plan with steps so u need to pass back to them



# Incorrect abstraction

Some abstraction is wrong. specifically, a naming issue. It doesent seem intuitive.

Primarily, the part where we "spawn" a node in the main loop, when it is already spawned and we really are just executing it.

So here is the actual flow of what is going on:

1. We have a node blueprint without output data
2. We then instantiate the node object and add it to the lifecycle queue
3. The lifecycle queue will receive the node and execute it.
4. Based off the output of the node we will either:
    - receive node blueprints for children and go back to step 1
    - begin termination process for node

Here are the current naming conventions i have for each step:
1. 
2. create_node()
3. spawn, terminate
4. 
    - create children
    - terminate

i think better naming is just one small change:
1. 
2. spawn_node()
3. execute, terminate
4. 
    - spawn
    - terminate