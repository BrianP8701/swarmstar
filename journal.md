this file is not meant to be read but i like keeping it up 

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
-> agent -> logic
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



# Testing offline

So i am currently on a plane and have no internet so im gonna add testing without api calls to test the terminate spawning flows of the tree.

So to do offline testing i essentially need to mimic and make up the openai output as thats the only use of network, everything else is offline local

So lets just make up our own fake scenario:

goal: determine the root cause of aging
routed to : break_down_goal
parralel -> retrieve_info, write text

We will need to retrieve: Most recent and well peer reviewed research on causes and solutions to aging and what are the primary unanswered questions/ bottlenecks

We will need to write text detailing a plan to do x


goal > router
goal > manager > retrieval, write_text
retrieval
write_text

so an offline_test method in swarm





# THinking about when we have more tools

Okay fukc it lets just listy off all the potential tools we might add:

router
manager
write_python, write_java, write_javascript, write_english...
browse_web
save_code
run_code (return output of code in terminal, error or any print statement)
retrieval (Links u to the option of browse_web, search through swarm database)


Fundamentally this becomes a retrieval and memory management problem





# Swarm

Fundamentally what is the purpose of the swarm? Specifically, i mean the way im building this out, this architecture with a tree? Why do i have asynchronous stuff? What im doing could easily be done synchronously, sequentially.

Im doing this for efficiency and dare i say scalability? Efficiency obviously because we'll have llm calls running in parralel, more and more the deeper we go down the tree. And scalability.... well tbh we already discussed this part. so far our 'swarm' system we are building locally is very fast and efficient with the only bottleneck being the llm calls.

bruh, okay but this could be horizontally distributed need be. idk i just wanted to think about how this might grow with scale now but i guess thats a problem for another time. I just finished reading alex xu's system design interview book a couple days ago in iceland.




# Github api class

goal: create a class that has all the functionality to interact with github repositories
mapped to write_python
got the code, the class string
save the code
generate test cases for the code and run it
take the output




# logging

Well the thing ise we definitely want to integrate python logging into the swarm, not only for the purposes of debugging the swarm, but also for the purposes of debugging the code that the swarm writes.

The question, as always is how do i implement this? One of the clear problems that arise now is that im noticing that im spending lots of time overthinking how to implement this stuff, what is the best way, trying to predict into the future... i should just move faster and aim for action and code writing.

Okay so how i ought to implement logging?

We already have the functionality written to save state and history in json format. this allows us to resume running the swarm from where it left off previously and to retrace the swarms every step. thats good. tbh the only place to add python logging in the swarm is for debugging when it fucks up

The second place i need logging is to test the code that the swarm writes. I need to be able to see the output of the code and the output of the test cases. Now these definitely do ought to be seperate. 

Now here is the question. i dont want the code written by the swarm to contain logging... but i might have no other choice. What i might have to do is have the swarm write the code 

# Potential conflicts with the swarm writing code 

- Testing
    Testing can vary very widely. It might be a singular unit. Or it might be more tightly coupled with the rest of the system. It might require further user input, like a key or url. How do we actually test it, see the errors or if it did well? We might need to use logging, we might need to save output to somewhere else and check if it did whatr it was supposed to afterwards. We might have to generate test cases. Essentially, we'll have to after writing the code pass the code to a tester who will consider all these possibilities and act accordingly.
- Naming conflicts. As the scale of the swarm grows we might reach a point where we have naming conflicts.
- Saving the code. As scale grows and we have lots of code we will need to organize everything in a file system/tree that the swarm can navigate to find the code it needs to work.   



____________________________________________________________________________________________________________________________

# On where to add user input, retrieval etc

we can add an option to every agent to opt out of performing its task and to ask for user input or more context, and to not just check a box asking for it but to output a string asking its actual question. This way we can have a more dynamic system where the swarm can ask for more context or user input when it needs it.

OOOHHH another cool detail while writing a much more in depth prompt for the agents and adding a place for user input, i can have the agents in the swarm identify inefficienciues or improvements in the swarm if i give each of them enough detail abt the swarm and what role they play/where they are. for example at the bottom of the managers prompt i say: "Your insights and further questions are welcome as we refine and optimize this swarm system. Let’s discuss any aspect of the plan where you think improvements or clarifications are needed."


Okay im adjusting my agent prompts and changing them to give them options to retrieve context or ask for user input and im reaching a few questions. So ive already concluded that each agent should be able to ask the user or retrieval agent questions. Im confused about:

- Do i give the manager agent an is_parrallel choice or just have it output a list of immediate goals?
    This depends. In the code do we come back to this agent to review and make the next decision or does it get terminated and another agent does review and next decision? Where does review happen is the question? Do we have a seperate review agent or have review happen within the agent? review within the agent fosho. review within the agent fosho. SOoooo like... hmm. Itll be aware of what it wanted accomplished. And then its children will pass it a report. and then it will decide to terminate or create new children. so no in parralel. just output immediate goals to be done now.



Okay this is 2 days later still working on where to have the agents stop and ask questions. What type of questions might arise?
- Question might need to be directed to user
- Question might require searching the web
- Question might requiring searching through the swarm internally

So questions can get mapped to many different places. For now let's not concern ourselves with that. Just where do we have the agents ask questions and how? 

For some reason im having a really big problem now. My first instance of the model failing to output my defined json schema. The python coder is outputting all parameters expect the python_code, despite the fact that its in the required section. I wanted to have one api call giving it the option to either: ask question output no code OR output code and ask no questions. But the model failed to ask questions or output code. So i thought, okay maybe this is to much for the model to handle.... maybe i need to break it up so now i have an agent to ask questions and one to write code, but now no code is getting written!!!! wtf!!

router - no questions, just ask user to choose it if cant decide
manager - ask questions
code analyst - ask questions

# JSON Mode Issues
well this is good news and bad news. What we see is that json mode is not reliable. i tried looking online but cant find anything in particular to help increase reliability. Obv there are methods like finetuning and giving examples but that for later down the line. (btw fine tuning is not abt fine tuning. SOTA model will always change its abt having data for my system. then i can just refinetune whatever SOTA model is on that) So what are some things i can do to increase reliability? THere is no science to this, just intuition but here i go:
- Less complex requirements
- Smaller tasks
- Use enums
- set required json mode 

The thing is i wanted to pass my data in one time 
Data -> questions or answer
but this might be too much for the model to handle. it might be better to:
data -> questions -> data -> ... until no more questions
data -> answer
This is more costly.... but might be more reliable? Should be more reliable. dumbass ai cant do shit(im joking i was just mad spent hours yesterday fucking with this problem)

okay. well now why is this good? Cuz everyone else is dealing with this problem... and while this problem exists theres no way u can have huge autonomous ai systems... which is the reason we dont see them today. 

Bro lmao this thing man. it.... nvrm.. this llm just did some shit that was dumb but smart at the same time. like its breaking the rules but in a good way 


# what next... ??
okay... um so ive kind of passed the first border. weird i dont feel any bit of satisfaction. well now its time to upgrade to a harder goal. lets choose a goal that will require ideally:

More user back and forth
Actually multiple pieces of code the system will write that will have to interact together
web scraping maybe?

oooh boyyy!!!!! This means were gonna start implementing some RAG methods!!! ABt goddamn time.

oh shit wait. i forgot. i need to implement the terminate functionality first. oh yeah lets do that and THEN were done with the simple goal. The swarm needs to self terminate once the goal is accomplished. 

sooo terminaton huh. So we have this simple goal of create a tictactoe game.

router -> python_coder
very simple. We can force it to go through the manager by just telling it so we can make sure all the pieces are working:
router -> manager -> router -> python_coder

we might as well add some testing here. this is a really easy place to start. in the future we could have a seperate contrainer to do testing. but here we could just have the python tester run the tic tac toe script.

so after the python coder finishes writing the code, we can pass the code name to the python tester... who will have to decide how to test it. it can output a plan to test the code

python tester planner


BRUHHHH FUCKING FUCKS SAKE. so the python coder didnt output fucking tic tac toe code the second the time, im almost sure it did the first time. Okay i think i have a solution to this. split it into another two steps, one where its SOLE TASK is to just output the python code, and then a second time where it is to generate the other parameters. the metadata for the code. so we have a new agent synthetic_python_metadata_extractor


# Autonomous script testing
so ima be honest with myself - i might be pushing the limits of the model with trying to implement autonomous testing. But i still want to have it in there and just have a catch where i can step in if it fails rather just giving up and just dooming it to user input. so here is the flow with script testing: (im starting with testing standalone scripts cuz thats easiest)

- we start with a script and its description generated by the python coder
- we pass it to the Python Script Test Planner Agent to determine a few things:
    - is the script executable as is?
    - can the llm generate synthetic input data?
    - does the user need to provide input parameters?
- If the script isn't executable as is gather input params from user if the planner says so and pass all this info with the code to the Python Script Test Generator Agent who will return an executable script. this is what im assuming will be a major failpoint. The agent will also have to add logic to save the relevant outputs to the right place in a given json path if the script succeeds
- Then download dependencies from the dependency list provided by the python coder
- Run the script and if there are errors save them to the same place where we would have saved success messages
- If at any point in this process we fail, we save the script to a .py file in the testing grounds, and let the user go in their himself and prepare the script, and the user will signal to the system when he is done by saying something in the terminal, and the system will pick up from there. 



# Namespaces




# Reorganizing repo
okay so im reorganizing the structure of the repo massively. let me share where im at now, and lets plan:

.
├── LICENSE
├── README.md
├── journal.md
├── past_runs
├── reference
│   ├── autogen_reference.py
│   ├── openai_config.py
│   ├── openaiapi_reference.py
│   ├── settings.py
│   └── utils.py
├── scripts
│   ├── helper_script.py
│   └── manual_write.py
├── swarm
│   ├── config
│   │   ├── agents.json
│   │   ├── agents.md
│   │   ├── config_docs.md
│   │   ├── node_scripts.json
│   │   ├── node_scripts.py
│   │   └── synthetic_code.json
│   ├── core
│   │   ├── agent.py
│   │   ├── memory
│   │   │   ├── manual
│   │   │   │   └── hello_world.py
│   │   │   ├── testing_ground
│   │   │   │   └── python_scripts
│   │   │   │       ├── schema.py
│   │   │   │       └── test_results.json
│   │   ├── node.py
│   │   ├── swarm.py
│   │   ├── task_handler.py
│   │   └── utils.py
│   ├── openai_config.py
│   └── settings.py
├── testing
│   ├── temp_unit_testing.py
│   └── test.py
└── todo.md

i removed some of the pycache files and the runs inside the past_runs folder. So let me explain the current state

past_runs folder contains history and snapshots of the swarm while im testing. a temporary folder for now. one day this will all be on cloud and a web app/gui
reference contains reference code, just pieces of code i might use. this is gitignored
scripts contain standalone scripts for the swarm. important and will forever be a thing
swarm is the main folder
    config contains stuff the swarm needs like agents and functions for nodes. its also a place for the swarm to save code its written
    core contains core classes for agents, nodes, handling tasks and utils for the swarm.
        the memory folder contains a place for the swarm to test its written code
testing is for testing obv.

okay so what things do i want to change now? 
1. I want to break up the config folder
2. I want to fix the mess that is the memory folder... nothing feels right there.

well. one of the big realizations ive made... 

bruh okay im back i just broke the whole config folder up. its way better now whew. now theres a folder dedicated for agents, where each agent has its own folder with a folder for their tool, prompt and script.

now next... the synthetic code generated by the swarm, and its testing. where do these get saved? Lets list out all the stuff we have

- generated synthetic code
if the swarm is creating a project itll be saved and tested in some seperate folder and ran in a seperate enviroment. if the swarm is creating some wrapper class or script it thinks it will itself use it can be saved somewhere within its memory. this code that ***might*** be used should be seperated from the core functionality that is necessary for the swarm to be self sufficient, which is called the "internal swarm api".
so what about things like the swarms terminate spawn methods, task handlers? those are internal swarm api things. the actual CORE of the system. 
the rest of the code will need to go in memory and be dynamically managed. so should the memory folder go in the swarm folder or at the root? the root cuz itll get BIG.
also quick note... this is so obvious but theres no need to always have to store code as strings. 



# Reading 2023 RAG survey paper
Interesting quote: "Additionally, it is suggested that LLMs may have a preference for focusing on readable rather than information-rich documents."
One thing to note, is that in my swarm most of my rag will be over structured data, data structured as dicts. but just for a layer, under that we get to unstructured text and code etc

searching over documentation requires common rag, like embedding nearest k.
searching in a codebase requires structured rag

potential tools for rag agents:
recursive retrieval
iterative retrieval
small to big chunking
reranking k results
rewriting query
compressing and verifying retrieved hits
multiple indexes for same document
indexing raw text, metadata, summaries, extracted info, different combos etc


# Debugging swarm with new organization

Essentially we should have a detailed description of the tree/file structure of our project to allow the swarm to autonomously navigate it to find what it wants. in addition to allow it to reorganize the file structure and write code to interact with different pieces on its own.

like i have a couple pieces now i already talked abt above yesterday: testing, synthetic code, manual place for user to prepare scripts for testing, documentation for the swarm. so i suppose how will context retrieval really work? some agent will have task X and will require context which may be code, documentation, results of some other agent or test etc. the retrieval agent will be like a router agent but to navigate over memory:

- structured code search
- rag query
- web search

so yeah. i guess we have the one memory folder to hold it all. and a memory router or retrieval router to navigate it

retrieval router, action router. when the quantity of options grow to large we need to break it down into sections and layers, a tree with clone nodes allowed. the routers navigate the action and memory tree. the swarm can create new actions and memories of its own. oh yeah baby now we're onto something.

all the actions are agents
any history, state, synthetic code, docs is memory

okay i guess here is whats bothering me. i want one place for memory, which ive done now. lets say i want to save something like a new python script that was generated

i want to make examples of the memory and action trees. just so u can see what i mean. These need to be autonomously configured - in the future. not yet. dont overwhelm myself yet. for now i can organize the action and memory space.


                            ------- memory router      ----- script
                            |                          |
                            |   -------- python ------------ class   
                            |   |                      |
            retrieve info ---   |------- java ----     ----- function
            code ---------------|                      
action ---- write
            test
            break down goal
            user interaction


actually the initial layer can be more abstract


             write
action ----- code
             test

whatever im not doing this its taking too long to type out.
okay so i get the action space is a tree. and the memory space is a tree. now one thing i gotta implement now is namespaces

okay i need to make a dynamic router... meaning a router agent where i can pass a list of options along with an optional further description of each option to the router.
the only problem is my whole architecture as of now has it so that the tools and prompts for agents are static. i need to make them dynamic.

ah god do i need to make a unique object for the router agent? i wanted all agents to follow the same pattern but it cant.... approaches i can take:

- have router, manager, optimizer, coder, writer agent in internal swarm and rest be in external memory? well ultimately.... fuck like writing code is something that can be done 

Memory Router (list of options)
Action Router (list of options)

Manager (goal/action statement)

Coder(goal/action statement)

Writer(goal/action statement)

not every llm call has to be called an agent right? fuckk my abstractions were wrong. bro im lost now. fuck fuck fuck. cuz the router needs dynamic input. ahhhhhhhhh

what do i do bro fuck there does need to be a standard pattern for each agent or no? I guess.... no? each agent just needs clear documentation describing how to interact with it. each agent needs an api for itself. 


should there be a single router for memory and actions or one for each? Whats the difference between both? 


okay so ive created a schema for the action space. the action router recursively navigates the space to find the appropriate action. 

now we need a way to pass this action back to the swarms action loop. 

currently the way this works is the action loop takes a node blueprint which it will create and execute. so each action in the action space corresponds to a node which corresponds to a script is that correct? i guess it is...

the node blueprint contains a path to the corresponding action in the action space.

This action... could be an agent we've defined and made ourselves. 

nah okay it cant just be an agent. it has to be more dynamic then that. what i reckon is the action space is replicated as an actual file system in the actions folder and each leaf node is a folder which is like its own little package. now we cant confine the action to be a class and u must run the main method. no, it should be... 

each action should be in its own scope, its own namespace, its own package, seperate. Each action should have a docs.md file describing how to run it.... and the executor node is assigned with executing actions.

ideally we dont want to waste unnecessary tokens and llm calls to execute a node... what are the paths?

Well an action is a predefined piece of code to run. the router is always passing merely a goal and nothing more. are there any scenarios where between two different nodes we need to pass more than just a directive? Context obv but that comes from retrieval... when a coder writes code it needs to figure out where to sdave the code. one approach is to always have the same way to exexute an action package, say a file main.py with a main method to execute. but what if i have things with other languages?

wait a second. after implementing the router that recursively searches the action space i realized that it doesent need dynamic input, it just takes a single directive. okay thats good news, maybe i dont have to change the architecture. are there any agents/actions that will require more input than can be in just a string?  irdk.... i rlly cant try to predict these things i just need to implement and move forward and if new functionality is needed, ill deal with that when it arises. 

for now, i can just have a singular way to execute all actions. 

so like would the github wrapper go in memory or actions?

this goes back to the question of how we execute actions. each action should be isolated (it can still import things from memory or other places) It should have dynamic input. 



# Goal 1
Here is the first project im gonna have the swarm work on:

    We want to autonomously prospect potential clients for a real estate agent using the ChatGPT API
    We have csv files with expired listings, peoples names and their phone numbers. Create a full fledged system to prospect these people.
    First, we need to take filters from the real estate agent to narrow down the list of people to prospect.
    Then, we need to send an initial message to each person on the list to their phone number. I'll give you a template for the message.
    Then we need triggers to send follow up messages to people who respond to the initial message.
    We want to continue the conversation and continue to gather relevant information about the person pertaining to their real estate needs.
    We need to save and extract structured data from the convo to a database. I'd like to use GCP.
    We'll also want to be able to alert the agent when a person is ready to call, or when a person is ready to sell their house. If at any point the LLM 
    needs help it should also alert the real estate agent.
    We'll also want to offer things like a free home valuation, a comparative market analysis, and a free home buyers guide.
    We'll expand functionality to include emailing them, and calling them using a model like whisper to cold call.
    We may want to also automate the sending and receiving paperwork.
    You'll need to design the system, build out all the components, save, test and run the code.
    We'll want to have a test area where we can simulate conversations where the potential lead is an LLM.
    We'll want a lot more. But this is a good start. keep working, build out this initial functionality keeping in mind that we'll want to expand it later.
    
    use twilio, gcp. probably google cloud function with triggers and then we'll want some sql database to store the extracted structured data. 

Before we move forward, lets try to think about how we want the swarm to actually go through this so we can answer my many questions... im kinda overwhelmed.

break down goal, make plan ask user questions to clarify. Get the actual file from the user. analyse the schema of the file. Create an area in my local file system to save all the code pertaining to this project. Write data cleaning scripts. write the code to send messages. save all this code to the appropriate place, keep the folder organized. Write cloud functions to continue conversation, save extracted data to database. get cloud keys from user. upload gcfs. test. 

so actions like save code to this path, get file from this path. small functions like that. the swarm is probably gonna be writing lots of scripts to get info, or no. we should definitely have a predefined action node so we can easily compose all these actions. so yes 



# memory agents

Theres a couple memory agents.

Retrieval agent. This agent is like the action router. it navigates the memory tree layer by layer and finds the appropriate memory.

memory router navigates the memory tree to save something to the memory tree. Its very simple and does not create new folders.

optimizer agent. this agent aims to keep the tree balanced and creates new folders when possible

clone agent. this agent replicates data to appropriate folders to make sure they can be easily found, even if a different route is taken. a specific form of optimization i guess



# optimize memory and action space

rather than having the overhead of having a tree.json file and having to update it whenever we make a change to any of the spaces.... um.... why dont we just treat the actual file system as the space/tree? 

The action space tree contains a type and description for each node in the tree. well we can very easily add a file to each folder in the tree describing those. boom big simplification. im like working on this codebase but constantly pruning so its not rlly growing but there is new functionality which i guess is good. ive deleted about as many lines as ive added (+13000, -10000)



# implementation of memory router

now this is quite challenging. First of all, we're faced with the different types of data we might want to save. strings, files, python code, text, images, etc. 

What i reckon is that if we are faced tightly coupled system code, those areas of memory should have a specialized memory agent that knows the ins and outs of that area very well.

memory pointers. not all folders or data need to actually be in the memory folder. there can be pointers to other folders, or memory agents who are specialized in that branch that take over if a memory router comes to its branch. this should be relatively easy to implement. but the hard question is how is the specialized memory agent implemented? wait now. a specialized memory agent in a branch is rlly just gonna have extra context in its prompt. okay so we dont necessarilly need a specialized memory agent but we need a very good description of the file structure and more, enough context for the memory agent to appropriately navigate the space. the thing is, like in cursor.so these agents all need to be able to ask questions whenever it feels like it has a question that needs answering 

lets take the example of a github repo. when it first enters the repo it might - okay wait i got it. yeah we can keep the same idea of having node_info.json files with descriptions at each level. we'll have another level where we describe the type

obv we also have github api and web browsing actions. 

the memory folder seems like its more so for managing its runtime tests, work, and the actual stuff that the swarm itself is working on. cuz we wont rlly save documentation, its better to just web browse for that. 

## creation and staging of memory
so while the swarm is working and it generates something, it saves that to a temporary staging area with a unique name. alongside will also be a metadata file. this key will get passed to the memory router. memory router looks at the metadata file and finds the best place to save this data

## routing memory space to save memory
the memory router will keep the metadata of the data to save in its context and navigate the space similar to how the action router navigates the action space: by comparing the metadata of the data to the metadata of the nodes in the tree. the memory router will also have a COT step where it can generate an analysis and also ask questions if needed. now as it navigates the space it might find a couple unique things:

- pointer nodes (point to another location/folder, cloud data)
- specialized memory agents
- indexes to perform rag over

if it reaches one of these special nodes, it will pass the 

## Creation of memory space
each folder's description should contain all the information needed to navigate that level of space. which includes not just descriptions of the subfolders, but sometimes a big picture of what this is. 

### How do we decide when to index and add a RAG agent over a space?
when we have a corpus of data too large to fit in context, that cant be searched in a structured way, we need to index it.

### What do i mean by structured search?
ill give some examples. searching a codebase for a specific class or function. this ought to be done with api calls and parsers. web search - obviously dynamic and requires scripts. reading documentation that is broken into table of contents and small sections where each section is a chunk size. we can do the router search over this without indexing. although rag might be - would be - cheaper here. hm. so no. i guess the only two examples i can think of now is querying an actual database, codebases and web search.

### Hierarchical Indexes
hierarchical indexes can still be helpful. if there are clear differences between data, we dont have to dump it all into one index. they can be seperate indices. 


uhh i keep on thinking abt the swarm at scale even though im in baby stages and should be doing baby steps

every folder has _node_id.json with

{
    "name": "",
    "type: "folder, local_pointer, special",
    "description": "" 
}

special encapsulates all other types of data. it means that the folder contains a specialized memory agent that the task is to be passed to. every folder that is labeled with type: special should have a file called _memory_agent.py which takes the UUID of the data and saves it in whatever specific manner is appropriate for that branch.

## Autonomous creation of local pointers and specialized memory agents
first of all, who creates local pointers and specialized memory agents? the optimizer or the memory router? well for now im not gonna think abt this.... lets just say the optimizer does it.... even though in reality in the back of my head im kinda realizing we'll need to be able to do this on the go, im gonna ignore that thought for now.

Lets build this memory router!



what if i need to overwrite a file? how do i indicate that. no that should be a different process. if im working on a specific file, then the process that led to that should have the file, edit and then overwrite it. 




# Review break
okey dokey. so weve made quite a bit of progress. have a lot more of the specific groundwork laid all out. but its not time to break yet. theres still a lot to do before the swarm is actually useful. which is what i want. i dont want to work on any of my other coding projects i want to USE my swarm to build those projects. so lets keep going.

reviewing is hard cuz i have to step back and amalgamate everything ive built out. which is starting to grow in size.


omggggg we are getting to the cool part. ima create the action creator agent... first signs of self sufficiency. First time i start USING the swarm. i can feel it.



okay ive made the big decision to ontake the interface as a web app. gonna finish that in a week, initially getting up a start button and user input(this week). then ill add a way to visualize the swarm as a tree, past runs, configuration, and a metrics board and more in the future.

in addition on the side ima continue to build out the core of the swarm. we have the manager, action router and memory router working now. lets get integration tests, add termination and add a couple more agents:

retrieval_router
python_coder
action_creator
writer





# termination
node terminates. we go up the chain of parents until we encounter a node that is a manager or root node. if we encounter a manager node, we check if all its children are terminated. if they are.... we have a few options for how to implement:

- we can have the same manager node label the nodes as terminated, and leave them in the children list. then have it run its script again knowing that it has had the initial steps all completed. it is asked if it has completed all the tasks or if there are further steps to accomplish the goal
- we can have the same manager node label the nodes as terminated and have it spawn a new node to check if the task is done and accomplished or if we need to spawn a new manager to create new steps.

okay i got it. manager checks if all children has been terminated.

if all children terminated:     
    if manager_supervisor is one of children:
        terminate
    else:
        spawn a manager_supervisor as child

that works so smooth :) problemo solvedo
ima smooth criminal







# transition to an official pypi package and making it compatible with serverless cloud functions
for the transition to serverless cloud functions theres two primary things we have to ensure:

1. the swarm needs to be decoupled. we cannot have the swarm object running in an infinite loop checking the lifecycle queue. we just need actions and units to call each other
2. we need to make the swarm completely stateless between units. we need to just pass around identifiers of data, the swarm and the ids of nodes etc

so yeah we do this and ideally we'll have this package that is more decoupled and stateless, allowing us to use it locally or on cloud. i want the package to be able to be used locally and on cloud. When i do eventually write my cloud functions, i want them to have minimal logic. they should just consist of using the package. 

umm yeak this is a pretty big undertaking and something i didnt fully comprehend before but now i get it. this should be fun.

luckily the actions are already decoupled and stateless. the core is the only part we need to break down into a new abstraction.

the core has a lifecycle queue that receives actions that it must execute. How can we change this?

well. this is actually very simple. 

All we need is an executor to replace the core

and manage the state of the swarm. boom done lmao wait that was easy




okay map out the interaction on serverless

creation: create swarm object, load goal and execute action router with goal
    input: goal, user_id, swarm_space
    output: create swarm id (hooked to state, stage, history). pass swarm id along each node along with path to action and data.

execute manager nodes


execute children nodes

...

wait a second. we really only have 2 cloud functions.
load goal
execute node

this doesent allow for much control or flexibility from a user perspective. or a software perspective. 
like what things should be tunable, open to change for other coders? 

- Ability to add to action space
- Ability to add to memory space
- easy to add rag/action chains

so truly pre configuration stuff only


i suppose generally the core should just offer nodes that take input and produce output

and then obviously its directed deterministically users dont get a choice, but if the package is built this way then it can work on local or any cloud enviroment.

ahh yes thats key i dont want the package to be tied to any specific cloud enviroment. 

but then in addition i dont want users to struggle to set it up



compatible with serverless
not tied to any specfic cloud provider, enviroment
easy to set up over any data (local or cloud, any provider, add your own propietary data) and be able to easily add custom action and rag chains

obviously comes with what i call the internal swarm api. Actions and memory that are necessary for the swarm. 


so now i want to imagine different flows for how different users might use this package

# Usage
## application (non coders)
so application users dont care abt adaptability with providers or enviroments. they want functional features. Like:
### custom data
so the memory tree comes with pre stuff. just a folder/file structure for the swarm with the essential swarm documentation. and then very simply the user can add their own data. they dont worry about rag methods, labeling data it should all be done autonomously
### custom actions???
i guess non coders wont really want to add action chains/be able to. but they might want to give the swarm permissions, like permission to control their mouse and see their screen, in the future connections to robotic and other apis. we want the swarm to be able to build an entire software application for someone just by asking the person for requirements and showing and letting the person use stuff as the swarm builds it out. we want the swarm to be able to do research. we want the swarm to be able to build a slideshow or anything for someone. now this personal data obviously cannot be used to help build the package. 
### Users helping build action space
when a user asks for something and the swarm tries to create an action that doesent exist it creates the action and that gets added to the official swarm package and reviewed by me.
## coders
coders like hacking and really making stuff for THEIR specific use case. and people like to expand and add functionality. so whats some examples of things coders might want to do with this package?
### custom rag chains and action chains
coders will want to add their own specific rag methods over their data (already talked abt for normal users). people are self centered. coding is hard work. a coder is gonna want to profit themselves if their building on top of my framework. tbh rn its quite hard for me to think that far ahead. all im thinking is i want it to be easy for local and cloud development. thats it. and then i guess we'll come back to this in the future



um i kinda got distracted and lost my chain of thought.... fuck what was i thinking abt... recollect recollect fuckity fuckity fuck

im trying to think about how to design my package which i want to be used everywhere. i dont want to tie my code down to my local enviroment and one form of usage. I want my core code, my swarm to be much more... idk cant think of the word exactly

remember my boy. noone. noone gives a fuck - NOBODY GIVES A FUCK - about how cool or esoteric or if they even could make it useful for themselves. the key thing is that the application for non coders is USEFUL and easy and natural. even coders start from there. then when they see how useful the swarm actually is will they want to build on top of it. switching costs have to be nonexistent for people. no training video, no instructions. just log on and use.






okay i feel good abt this plan. now time to uh actually code it. im kinda overwhelmed by the magnitude of what im telling myself rn. what do i do rn?

uh right yeah decouple and make the core stateless. lets do that.
oh right i realize what i havent considered yet. custom memory spaces. How do i make it so that we can have the swarm work with and cloud provider or local memory spaces. fuck. rn i have a memory router, retriaval agent to navigate over the memory space. also i have all these paths within my package. when i make the package itll have a memory space that already has some stuff. Then how would we add stuff to that memory space from cloud from any possible source? rn the routers navigate    AHH BABY I GOT THE SOLUTION IM TOO GOOD FUCKING GET IN THERE MATE. EASY PEASY. we revert back to our old solution. Have a tree serialiable object representing the memory tree and each node pointing to location of the data. TOO EASY MAN

Tree contains metadata for each node and pointer. Pointer can be within package or to a cloud location with which you define your connection specific retrieval function in utils. come on get in there baby its too easy for me. fuck yeah



depending on your cloud enviroment youll have different ways to navigate to and add data. essentially all data uploading and retrieval should have a layer in between so


lets just literally code the swarm rn so it will work with gcp, azure and local. instead of thinking abt it abstractly lets just do it so i can choose which one i want.
im thinking so fast and my head is spinning and heating up so much - coder fever. coder fever to coders is like runners high to athletes



For coders :
path to stage


does it contain - at which part do we choose our database integrations? 

i suppose well actions obviously are in the package - or your fork of the package.

data in the memory space.
each node has a pointer. and in the metadata include the method to retrieve it. in the data include the function to retrieve it. where does this get defined? lets imagine the process of adding cutom data from a 3rd party/user persepctive.

User 1:
This user has data on azure blob storage and other azure data services

User 2:
This user has data locally on their machine.

User 3:
This user has data behind various apis


Each user has to create methods that:
- add to stage. retrieve from stage. Their stage could be a local folder, or a folder in some database
- add data to database. retrieve data from database. if ur using azure, gcp, or local, you need to tell your memory router right now where to add data. the retrieval agent will simply follow the pointer to the data along with the method to retrieve it. that method comes from the memory router. 
you only configure the memory router. 
for staging, you configure the staging method.



Swarm object:
This object maintains the state and history of the swarm

This object lets you configure the package with your staging agent, and your memory router and retrieval functions.

You add the connection to your memory and action space. 

When you configure as a developer you create your own memory and action space and staging, and memory router functions

when you configure as a user you add your data and the backend is configured for you in the manner by that backend developer.



lets think about the various layers there are.

If i create an application

I have 800 users.

Each user has a profile and can create multiple swarms. 
Each swarm a user creates has its own action and memory space.

Each user can run one of their swarms. 
An instance of a swarm has state and history.

Because this is my application, every single swarm everywhere has the same staging and routing logic and is in the same enviroment.


So theres like 3 layers:

1. Coder layer
Configure the swarm to work in you enviroment with your provider and data sources and stage
2. User layer
Configure the swarm with your data
3. Swarm layer
Run the swarm maintain its state and history.


what level is the swarm object at? we need objects with wrappers for each layer? yeah i think so.
The swarm object encapsulates the user and swarm layer.

above that we first need to create the coder layer


whats the process of swarm configuration like? is it a one time thing? yes it is a one time thing. its like a configuration file. but you can change it any time and there should be no problems. expect all your defined util functions need to exist
we should have a config folder. this contains a config file with constants and the utils pointed to by the constants.

this is at the package layer. when your doing this your modifying the actual package. thats not a good way to do things is it. that would mean developers would have to fork and constantly merge changes from the main branch. we should be able to do this in a more modular way. 

the stuff thats getting configured - whats it actually changing? 
- its changing the metadata tag that the memory router saves data with. 
- its adding functions. functions corresponding directly to the metadata tag mentioned above. 
- we can have a scan function that makes sure that you have all the necessary data functions
- you select your base memory and action space. 
    - memory space obviously has the internal swarm memory space in addition to your added data along with the aformentioned data functions and tags in the config folder
    - action space is inside the package
        a question is what if a person whats to add their own extra actions to the action space, and closed source, keep it private? how would that work. well just follow the same idea as the memory space. theres the base internal action space. this is the one inside the package. You can then add your own actions to the action space. each action in the base action space from the space has a metadata tag indicating so. your custom actions can contain a tag specfying the way to that action


## what is memory and action concretely?
now we get down to another question. what is a memory and action? And lets reconcile the conflict in my head between the agent and action.

### memory
a memory is just a piece of data. json, pdf, py, java, pt, txt, png, mov, element in table anything. see its metadata in the memory space schema

### action
an action is a script. now i genuinely do have a lot of questions around this...
an action should be a predefined deterministic unit. it should be able to take variable input. it should be able to output variable output.
This means that there might be some sequences of actions that will always call each other.
so far i only have a few actions that might result in dynamic calls. actually only one. the action router. and the action router comes after the manager.

so besides the action router and manager the chains of actions are determinstic.

so essentially the manager breaks down a directive into subtasks. and each of these subtasks will go to a chosen action chain. if the appropriate action chain doesent exist it will be created.

actually its like a giant puzzle pieces because the same actions can be composed to create different action chains. you can imagine actions as puzzle pieces with two flat sides and two puzzle sides. puzzle sides that fit together (output of one actions follows the schema of the input of another action) can be chained together. okay i mean yeah that works. so actions are the scripts. 

See the metadata for actions in the action space schema.


#### Thought process while writing schemas for memory and action space

for the action or data leaf node in the memory or action space cannot the uuid cannot be generated using the path because the optimizer might change the paths around. every action or data node must just have a uuid. do folders need uuids? do folders need uuids? fuck it just give them uuids cant hurt

can folders have different retrieval types? no. no they cant. cuz the spaces is not the actual space just the metadata overlay with ids and how to do retrieval on leaf nodes. so folders dont need ids.

wait or we can simplify things massively by having one hashmap without layers and having two different types of nodes and every node has ids. this - yes this is the approach.

### memory space schema
The memory space consists of memories and any type of thing that can hold memories. Azure blob storage, Google Firestore, SQL databases, a local folder etc. Every node in the memory space will tell you how to continue to navigate.

Node:
{
    "navigation_type": "folder, vector_index, sql_table, sql_row, sql_column, blob_storage, file_system...",    -for Uploader
    "retrieval_type": "none, sql, router, vector_similarity, choice",     -for Retriever
    "name": "",
    "id": "",
    "description": "",
    "children": [ids of children]
}

### action space schema
Nest folders with actions or folders as leaf nodes. Action type nodes must be leaf nodes

Folder:
{
    id: {
        "type": "folder",
        "name": "",
        "id": "",
        "description": "",
        "children": [ids of children]
    },
    ...
}
Action:
{
    id: {
        "type": "action",
        "name": "",
        "id": "",
        "language": "",
        "input_schema": "",
        "output_schema": "",
        "description": "",
        "dependencies": []
    },
    ...
}

### Core agents

#### executor
the executor takes the id of an action, input data and the action type.

an example of an action type is the following:
A folder that contains a python script that contains a main method. call it with the given input data in the form of a dict

that action type could be called "simple_python_script_main_method"

we could define action types for other languages or different calls. either way the action type itself would be like a function. 
so the executor would need to hold a namespace mapping action_types to the function that takes the action_id and input and executes that function

#### spawner
spawner spawns a node and updates swarm state and history and tells executor to execute

#### terminator
terminator begins a termination process

#### optimizer

#### user input

### memories
we can upload data. we can retrieve data. we need two objects. Uploader and Retriever.

#### uploader
the uploader takes the id of data in the stage 

it might need to upload to a kv store. it might need to add the data to a sql database. it might need to save to blob storage. it might need to add the data to a file system on a local machine. all of these require different methods. the uploader will need to know the method to use. how will the uploader know what method to use? The memory space should tell it.

we have "folders" and "memories" in the memory space. thats not comprehensive enough. is a sql database a folder or a memory? do the uploader and retriever search over the same memory space? 

okay i adjusted the memory space schema to work. yup thats general enough.

#### retriever
the retriever starts from the root of the memory space. it chooses the next node to go to. then the navigation_type of that node tells it what to do next. it might still be a folder so it passes it to the same router node. or it might be an index that requires a different rag method. Or a sql table that uses a specific sql method. the navigation_type tag at each node tells the retriever how to navigate the space. And the data on the bottom? is that in the memory space? 

### Swarm object
The swarm object takes the memory and action space. It configures the stage, core agents etc.
The swarm id gets passed around as a uuid along any instantiation of itself. The swarm id is the only thing that gets passed around.

### Running the swarm?
Running the swarm consists of making a swarm object. u get ur swarm id. then you simply make pass a goal to the action router to the executor and let the executor do its thing. It will begin the process to autonomously pursue the goal- ofc stopping for user input when requirements arent clear or if it needs help

The key - this is why im building agi. You chatgpt ur api is so powerful. it will be able to be used within those action scripts. And there will be an action script - to create other actions. As ai models become better i integrate them. an indivdual model with its inference is a tool. within my system its an autonomous goal fullfiller. not just a tool but something that can replace humans and surpass them.



im in the void and i dont care. u reach inner peace when u realize what ur doing is right. nothing else matters in the entire world other than building this. 

### Configuration process?
#### What they see
create your swarm object on your propietary data
1. Add your OpenAI API key and frontend URL
3. Define file storage and retrieval operations
4. Add your propietary data along with the operations to retrieve them
5. Add custom actions
6. run an optimization over memory space ? optional

You now have a swarm object connected to all your data with your custom actions.
You can run an instance of your customized swarm with a goal.
7. run swarm


what actually happens in the back:
1. Add OpenAI API key and frontend URL to swarm object
2. Copy default action space from package. Add file storage actions into action space and save action space using users chosen file storage method.
3. Add users data to memory space representation and save memory space
2. add actions to action space and save back
3. organize or add metadata if user didnt
4. add actions to action space
5. save

The swarm object holds... holds what? i guess by default the swarm has a default memory and action space. but if you configure yours differently you'll copy and the swarm object will hold the new spaces, or references to them. and everytime you instantiate an instance of a swarm you get a further copy of that.


think about the interaction between the backend and frontend.

the swarm object, node objects will remain in the backend. 

the frontend will only be taking a few things:
    - representation of memory and action space leaving out some metadata
    - some metrics about the instance of the swarm
    - a representation of state and history of the swarm
    - a list of the agents in conversation
    - message replies from user conversational agents

the backend will only be taking a few things from the frontend:
    - the username and password of the user
    - the swarm id
    - the goal string
    - requests for data it wants
    - user responses and file uploads



you create and configure a swarm object. a swarm object contains the memory space and action space (i understand when these spaces become larger it will become unmanagable. but for now). it also contains the openai api key. 

Your file storage set up automatically as you configure.
{
    swarm_blueprint: {
        memory_space
    },
    swarm_instance_1: {
        swarm_object: ___,
        goal: ""
    },
    ...
}

the package ought to be different seperate from te cloud provider remember.

you pass a node blueprint and action to the swarm. the swarm returns nodeblueprints and actions and a report.


okay NOW. now we are genuinely done with planning. i can actually start coding now.


one of the problems i have not addressed is how the uploader decides what type of node to create in the memory space.

Executor
Now a question is how does the executor execute. An action is a file, or package of files. 

the executor is given the action id and its type and its args. Given its type it will execute that action in that manner

# My thoughts while implementing confguration stage
Where do the default file storage and retrieval methods go when passed to the Swarm Blueprint object? 
It cant go in the package's default action folder. 
uhh this whole thing of passing the file storage and retrieval methods to the swarm blueprint object is a bit of a hack. i dont like it.

Here is my question. Who is the one adjusting the default file methods? 

The developer of the package leaves the default file methods blank

The developer using the package will add the default file methods to work in their enviroment. 

we have part of the action and memory space on the package. the rest will be in the specific 

save file           (data, path)
retrieve file       (path)
make folder         (path)
delete folder       (path)

the swarm blueprint and all subsequent swarms carry all keys.
the swarm blueprint carries the action and memory tree and all keys.

when we are actually executing an instance of the swarm we dont actually want to pass the whole memory and action space and all keys between each node. rather we want to have an object that can retrieve those as needed. okay try to imagine what exactly the executor will need

the executor can receive two types of things: 
1. spawn and execute a node
2. terminate a node

subsequently itll need to be able to also:
3. retrieve the action space and the memory space
4. retrieve any keys that might be necessary for some actions

i suppose we can do this by adding more metadata to each action:
    - dependencies
    - keys

and keys will just need to have consistent naming across the whole package.

i suppose in the future can u imagine the swarm needing multiple of the same key for various operations? tbh.... we're thinking to far ahead.

during config stage swarm checks actions for key requirements


chain of events when running instance of swarm

run it with:
- action id
- action args
- swarm_blueprint object
- spawn or terminate

{
    "lifecycle_command": "spawn or terminate",
    "action" : {
        "id": "",
        "args": {}
    },
    "swarm_blueprint": {
        "memory_space": {},
        "action_space": {}
    }
}

come on come on get it together what what



okay weve made some progress. implemented quite a bit. now i want the swarm to actually help me:

whats needed first is broken trees. trees with pointers to other places.


okay fuck theres sort of this infinite loop problem now. uhh let me try breaking it down

we pass keys, platform type etc


okay we've now finished implementing the configuration stage. Designed everything so the swarm is compatible with any platform!

Now we need to implement the executors and nodes.


# Consistency
This system needs consistency. Later we'll need to add so that only one node can:
    retrieve and update the state, history, or any space at one time.

But obv read only operations can be done at the same time.

Just keep this in mind!

# Action config and packages
okay we need to rethink how we do action config for each action. we need to INSTALL the dependencies not just import them. the script itself imports them. We cant do this inside the action it needs to happen outside, before we create the cloud function because, we need to know all the dependencies before we even enter the cloud function.

Cloud Function 1: spawn a node. Pass it along to the next cloud function to the swarm master to execute. This next cloud function needs to have the appropriate packages installed. Before we pass to the swarm master we need to install all packages

umm so the developer is gonna have to make this themselves for their platform.... or i can give it to them. thats definitely something for later ima leave a blank space there for now

# Action Space mistake....
well we can easily identify between a folder and action by whether they have children... expect for an empty folder. 

Guess we should add an attribute to check for that

in addition, the type for a folder should point to the action to move forward? Yeah. it should We dont need to define one for internal_swarm_folder tho.... wait a second any folder should be in the metadata space so yes, the cases where we might need to do something weird are unique ones like sql bases, indexes etc. wait im thinking abt the memory space im stupid bruh. no uhh with the action space there is one singular type of folder. so no need for anything special there i think. genuinely dont even need to specify internal swarm folder. just say folder right, cuz the folder is aklways the same no matter ur platform. 

also the types should be the proper id of the action. okey dokey. man ive wasted so much time manually editing the action space. i definitely need to automate editing the action space. ooohh..... right the action creator thatll be sick man. well first automate saving a new action then automate the creation of the action. yessirrrr we making self sufficient... im deadass just building AGI bro. ppl dont understand. i want to do it first tho. I want to be the first person in the world to build this. Then i wont a useless nobody leech to society anymore - ill have some sort of value. im a worthless piece of shit unless i contribute something back to society.

# Reflection
Okay so we just added a bunch of sick stuff and layed down a lot of the groundwork. i want to do a reflection now to make sure everything is correct before i move on, design/architecture wise.

ultimately what will using this look like for ME. 

so lally doodly lalalala

yk so im on the user interface. I have a copy of the default package. whats important is that when my local copy of the package is modifying the action space there needs to be a way to merge those created actions back into the default swarm package. this process can be called, Action Space Merging.

Where there rlly be as much of a need for Memory Space Merging? I really dont think so. No. Not really. Memory Space Merging is not a thing mate. Memory Space is created primarily manually. 

what else. user interaction ofc. Think about User Interaction components. Any User Interaction components must be standalone action units. because if we're inside a cloud function and ask for user input that blocking input will surpass the cloud function time limit. it needs to be like activate a trigger. idk depends on the platform, but we need to make user interaction compatible with any platform. Platform Interoperable User Interaction

Autonomous Action/Memory Space Optimization - we need autonomous optimization processes that look to balance the trees to aim for O(nlogn) efficiencies in the memory and action space

Add Custom Actions and Data - self explanatory. in the configuration stage, add custom data and actions to your blueprint

Visualize the Swarm - visualize the memory and action space in a tree format. visualize the state and history of the swarm.

Ensure consistency in operations that write to swarm space. Operations are fast, but one fuck up is a fuck up. we need to enforce through the package this if its possible?

what else is there? hmmmm.... config the swarm, make blueprint default copy, add custom action data to blueprint, run instance of swarm, interact through interface. lets now make sure the generality of the swarm, and think precisely about how the swarm will interact with itself and the typing stuff.

oh wait also pausing and resuming the swarm. we can simply do this by when we pause a swarm we let all current running nodes finish, and add all their output nodes to a place to be picked up when we resume the swarm. user interactions will just sit and wait.

no as for internal swarm operations. specifically we need to create these things in this order:
action router
memory router
retrieval agent
upload data agent
stage manager
action creator

# Automating Action Space Interactions
- i cant manually touch the action space. I need to have a script to add an action, move an action, move a folder etc. Im actually gonna do this rn, but first im gonna reconcile and make sure everything is correct. another nice thing would be adding a script to verify the correctness of the action space. thisll be tedious. i should have had autonomous scripts from the getgo

1. Confirm that i like the action space rn - Done
2. Manually match the action spaces up together - Done
3. Write a script to verify the correctness of the action space - Done
4. DONT TOUCH either of them. Write scripts to autonomously interact with action space - now lets break this down
    a. We want a function that takes the path to a folder or file and moves it given:
        - Select the parent. the action will be moved  to be a child of this
        - Select the metadata for the action
        - the function should perform validation. make sure the parent is a folder, make sure the type is proper and that the action actually follows the schemas and types it says

        Then we automate this!!!

One particularly interesting question is how to organize the swarm folder. So the aga_swarm/actions/swarm folder we should contain any actions pertaining to the swarm. this could include action types. i feel like action types is a horrible name. 

10 min later...

had a chat with chatgpt. soooo i dont rlly think we need action types. we do need a seperation between internal execution for initialization. but beyond that the only different types of actions would be those in different languages

so remember we cant manually touch the action space.

wait first of all whats the new execution process for actions gonna be? 

write scripts to delete from action space and add to action space externally first then add those in

lets define a concrete definition for the executor and where to use it. 