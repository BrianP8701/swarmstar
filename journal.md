this file is not meant to be read but i like keeping it up. by definition, i come here when my thoughts are a mess, thus everything in here is just that - a horrible fucking mess. I find this process very helpful when im faced with something difficult, but when i have all the necessary information in my head. like chatgpt cant help me anymore, i already have all the pieces - but i just need to put them together or come up with the right design and am stuck.

______________________________________________________________

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




Remember when we terminate a node we dont just go up to the most recent fork in the tree. some managers didnt do inparallel at break but had a plan with steps so u need to pass back to them



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
parallel -> retrieve_info, write text

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

Im doing this for efficiency and dare i say scalability? Efficiency obviously because we'll have llm calls running in parallel, more and more the deeper we go down the tree. And scalability.... well tbh we already discussed this part. so far our 'swarm' system we are building locally is very fast and efficient with the only bottleneck being the llm calls.

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
    This depends. In the code do we come back to this agent to review and make the next decision or does it get terminated and another agent does review and next decision? Where does review happen is the question? Do we have a seperate review agent or have review happen within the agent? review within the agent fosho. review within the agent fosho. SOoooo like... hmm. Itll be aware of what it wanted accomplished. And then its children will pass it a report. and then it will decide to terminate or create new children. so no in parallel. just output immediate goals to be done now.



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

retrieval router, action router. when the quantity of options grow to large we need to break it down into sections and layers, a tree with clone nodes allowed. the routers navigate the action and memory tree. the swarm can create new actions and memories of its own. oh yeah now we're onto something.

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
    input: goal, user_id, swarm
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
oh right i realize what i havent considered yet. custom memory spaces. How do i make it so that we can have the swarm work with and cloud provider or local memory spaces. fuck. rn i have a memory router, retriaval agent to navigate over the memory space. also i have all these paths within my package. when i make the package itll have a memory space that already has some stuff. Then how would we add stuff to that memory space from cloud from any possible source? rn the routers navigate    AHHH I GOT THE SOLUTION IM TOO GOOD FUCKING GET IN THERE MATE. EASY PEASY. we revert back to our old solution. Have a tree serialiable object representing the memory tree and each node pointing to location of the data. TOO EASY MAN

Tree contains metadata for each node and pointer. Pointer can be within package or to a cloud location with which you define your connection specific retrieval function in utils. come on get in there its too easy for me. fuck yeah



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
    "operation_type": "spawn or terminate",
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

One particularly interesting question is how to organize the swarm folder. So the swarmstar/actions/swarm folder we should contain any actions pertaining to the swarm. this could include action types. i feel like action types is a horrible name. 

10 min later...

had a chat with chatgpt. soooo i dont rlly think we need action types. we do need a seperation between internal execution for initialization. but beyond that the only different types of actions would be those in different languages

so remember we cant manually touch the action space.

wait first of all whats the new execution process for actions gonna be? 

write scripts to delete from action space and add to action space externally first then add those in

lets define a concrete definition for the executor and where to use it. 

# Memory Space
we now will begin to touch and shell out the memory space. A few things i want to note, some things to go in the memory space:
- default action space metadata
- action space metadata
- external actions
- 

internal actions are inside the package. do i...

wait i just realized. the actual... ah man fuck. this gets confusing now. memory space action space, blob storage noqsl. the actual memory and... no the annoying thing i just realized is that the action space metadata and memory space metadata can be a nosql container instead of a blob. which would be more efficient. do i say fuck interoperability and just code? Or do i truly try to strive for interoperabilty? i think purely striving for interoperability forces me to make the swarm more general. yes interoperability.

the solution has to be a flexible memory space that can store metadata of "memories" that the swarm can navigate, and any of those "memories" are labeled with a type telling us how to actually access the data. i was underestimating wait.... but now i see how powerful this can be. the combination of a completely general action and memory space. oh boy. oh boy im cooking. im cooking yessirrrrr. yessir. YESSIR BITCH ASS FAGGOT. WE MAKING THIS SHIT

these small details, getting these tiny details right will make the difference between a system that is general and a system that is not. this is not some thing thatll ill be able to think about and take time and build. any week now somebody might finish creating a recursively self improving system. I have to hurry the fuck up and make this shit

i think a mistake ive made is that the action space is not gonna contain small individual actions like 'data_transformations' and whatnot. The action space will in reality contain larger more complex scripts that are to be dynamically chained together. Write code, review reports.

The underlying memory space and action space have to be really flexible for this to work. I was thinking primarily in the action space above - but ive come to simplify the action space pretty well. Action space is partitioned along 3 axes: [language, internal or external, platform]. If internal we just do an internal import. Depeneding on language we have to yk.... interact with it differently. and then if its external, we'll need to access the action using actions specific to that platform.

on my local device im currently taking a root path and storing the action space metadata, memory space metadata, state, history, stage and swarm space metadata JSON at the given root path. 

On a cloud provider the file system corresponds to blob storage and the JSON files can be replaced with NOSQL containers. The thing is these are all gonna have some sort of overlap.

do the file and folder operations really belong in the action space alongside code python, decompose directive, review report, search ? because they arent really actions they're more like utils for actions to use. I suppose here is the question. Would an action ever get routed to them? no. no absolutely not. an action wont get routed to them but actions definitely will want to import and use them. So when the swarm is creating an action how should they find the action they need? I suppose they would want to route over a similar action tree structure and import there.... ahh i see. we wont do embedded vector rag to find helper functions and work on the swarm but just a constant routing over spaces. should the "swarm_utils" be in the action space then? I mean fuck it i guess so. when they get imported we can import the actual function instead of the main function. aight this works.

now anyway back to thinking about the memory space. fuck i wanna take a walk but let me just clear my head on the memory space first. Okay yk that folder i create locally that stores the swarm space? That is the memory space. and the memory space contains the memory metadata and swarm space within itself. this way we can have those things be blob, json or nosql. external action stuff goes in that acxtion space retrieved according to the mmeory space. OKAY woo i feel so much better. i think thats a solution there. ahh thank god.

anyway, im going to craft a local memory space for my mac. but during config the memory space wont be as simple as just copying like the action space metadata.

I need to make the action and memory space appropriate for the action and memory router. that is a clear metric for me to think about.

# Instructor and Pydantic
okay so what weve discovered is that instructor is really fucking cool and we want to use it. to review what can instructor do?

instead of passing JSON into my LLM calls we can use instructor to define the Pydantic model we want the LLM to follow. This comes with the benefit of making it much easier and faster to geenrate schemas. it also makes it much easier for the LLMs to generate schemas. furthermore, we can add validation to our models and retry mechanisms.

What changes do we want to make exactly?

    - our action space metadata should contain jsonified pydantic models for the input and output schemas. 

however the jsonified pydantic model does not contain any custom validation. i believe we definitely will want to include custom validation. what we can do is that in the script path we can define INPUT and OUTPUT pydantic models. lets think about this very carefully. 

we have the following options:

1. Put input and output schemas in ASM without custom validation                    No definitely not
2. Put input and output schemas with custom validation in the action script         Maybe
3. Put them in both                                                                 Maybe

to decide between 2 and 3 we need to think, what would be the benefit of also including the schemas in ASM? In this scenario we wouldnt have to import the input and output schemas from the action to check... nah we're going with 2. 

One thing i could see being good is narrowing the action router to only searching for actions that have the input schema of the data it has now. this means we would need consistent naming across the entire action space. i suppose this could be a good idea, and for that reason i will support it.

So thats the first thing, is making the action space use pydantic for its inputs and outputs. Secondly, we'll actually use instructor for all our LLM interactions now. We'll also really want better logging to monitor and analyze the swarm. One thing that has crossed my mind multple times is that we want to specifically monitor the LLM interactions inside the action nodes. This can just be something that is included in the report. So what we will do now is fix the action space to match the new format. Then we will integrate instructor into our actions. Then we will build the memory space, action router, memory router, review reports, python coder etc. 


# Redefining the action space again
okay again. going to need to redefine the action space. simplifying it now. The action space shall be dedicated to knowledge tasks, along the likes of decompose directive, review reports, write code etc. the things like file and folder operations are not actions. they dont take language. those are helper functions, utils of the swarm that actions might use in their scripts. this makes the action space much simpler - creates a seperation of concerns. the difference is actions are actual nodes in the swarm, whereas the utils are just imported and used amongst the swarm. and they will be navigated differently.

the util section can utilize a metadata tree and a vector db for search. im gonna redefine the schema for these now


# Package management
okay fuck so system packages just cant be downloaded on cloud functions. fuck. okay so whenever i am in a situation where a system packahe is needed gcp azure and aws offer "container-based services like AWS Fargate, Google Cloud Run, or Azure Container Instances."

after lots of talking and deciding i have decided to majorly pivot my focus. Im not going to try to make this an interoperable package for devs to easily set up on their enviroments. im already overwhelmed by the need for the swarm to be able to dynamically create environments on its own i just cant. Im honing in on just creating a product for myself. that is the focus. but the project will be open source

# Cosmos DB
3 partiton keys only

User credential:
id and partition key is username
holds user_id, password, list of user swarms

User credentials:
Partition keys:
1. username
2. bcrypt(password)
{
    user_id
}

1. user_id
2. swarm_id
3. action_space_metadata, memory_space_metadata, util_space_metadata, swarm_state
id    action_id                memory_id              util_id          node_id


Action metadata
Memory metadata
Util Metadata
Swarm Space metadata
Swarm State


So like we'll have one container:
and paths will be like this:
user_id/swarm_id/action_space_metadata
user_id/swarm_id/memory_space_metadata
user_id/swarm_id/util_space_metadata
user_id/swarm_id/swarm_space_metadata
user_id/swarm_id/swarm_state

# Cloud vs Local

Cloud:
    - runs actions on cloud functions
    - uses cosmosdb as kv and blob storage as file storage
    - uses Azure Container Instances to create dynamic enviroments for generated code

Local:
    - runs actions asynchronously in loop
    - uses LevelDB for kv and local file system for file storage
    - uses subproccesses to create dynamic enviroments for generated code

# Concern about further decoupling actions
Actions need to be further decoupled for blocking actions within them. Currently actions are the smallest unit a cloud function can take on. I do quite enjoy and believe logically within the swarm that is the correct abstraction. However, this cannot be when deployed on cloud serverless. take the situations where an action needs user input in the middle, or when they make openai calls, or when they need to make a call to a database. These are all blocking calls. I think the solution is to have a "blocking" action that can be called from within an action. This action will be able to take on the blocking calls.

First of all, i want to answer for once and for all - do all actions have the same IO? Merely the passing around of a directive? The only communication between nodes is language? this genuinely sounds crazy. Lets draw out some crazy swarm scenarios that cant happen today but that we want to happen in the future

manager breaks down directive
researcher browses the internet and does analysis and passes results to memory keeper
memory keeper saves the analysis and sources to the appropriate place in memory
requirements analysis software agent takes direvtive and makes sure we have all relevant context before passing to coder. it asks and talks to the user and the research agent some more
coder takes specifications and requirements and writes code
code tester takes context of newly written code and ! here is where we need more than just a directive comminucated. we need the tester to actually have the path to the code. but in this scenario we can bypass this by packing the coder and tester into one action. it is afterall packed together. tester tests code, based off results feedback loop happens until success and termination or asking for user input. If user input happens user will come in and fix problem manually and set the node to terminate or will have to do some traceback and swarm debugging.
action creator receives request to write action to document entire github repo, crawling through it and going through connections and iterating through the documentation. 
Gets passed to user to define alot of specifications. agent gets spawned to create pydantic models for instructor with user. models get saved to blob storage and termination. next phase begins. user interaction again. i describe the workflow i want generally for reading through the codebase and writing the documentation. the swarm writes code. DISTRACTION. I tell this branch of the swarm to spawn a new directive to focus on. i want a new feature to be added to the swarm. i want to select the lines i want the swarm to edit and the lines i want to share with it for context, and have it output only those lines, which shall be replaced. I add this logic to the backend with the swarm. We refresh the backend. We then go add a way to do this in the frontend. We pause and resume the swarm with the changes. or actually we dont have to we can continue with the new swarm actions saved in external swarm memory, code saved in blob storage with the appropriate metadata in comsosdb and we need to make changes to the frontend and test the new frontend seperately in a different enviroment. If the frontend works we'lll then have to refresh the swarm. We need to have automated CI/CD pipelines. the swarm makes changes to a fork of the frontend code. we test it. if it works and we like it while communicating with the swarm we merge the changes. after all this the distraction ends and we go back to what we were doing before. 

blah blah blah. anyway the point is - yes between action nodes it is just language being communicated. everything inside a node is predetermined. And there is a lot more user input then i expected or previously imagined. the engineer is very involved but his work is sped up even more than previously possible than with just chatgpt because now the ai is writing saving, deploying testing the code, clicking the buttons and the user gets to remain on a single interface without jumping back and forth. which admittedly might get quite boring, but if theres a lot of stuff the swarm is doing, we should lots of visualizations for all processes which might keep the engineer more engaged. this is the future of coding. its a lot to implement but when i get the ball rolling this is true acceleration. i will become somebody. i wont be a nobody -  a loser. a ghost in history to die and be unknown. ill have done something in the universe with my allocated consciousness

secondly - decoupling the actions further. so clearly we just decided that the action as we imagine it now is the fundamental unit. it is to be what occupies the action space as it is. but we just need breakpoints. right now we pass the action id, args to an executor who will execute it in its entirety. i suppose we might have an action that is broken up amongst its blocking calls. so instead of an action being an entire script, we can have a folder. when we call the action with the executor itll execute the first part. when it reaches its first blocking operation, itll return a new object (ill have to define this) with the args and the next step to call within the folder. okey dokey problem solved

so unfortunately we do need to redefine the action space metadata for like the thousandth time alread bruh. ope wait nope we dont have to. i got a different solution.... yessirski this is more clean. call the main as we do normally. when a blocking operation happens we will return the next function to call inside that script along with params. thats it. then the handler local or cloud will see "oh okay this isnt a NodeIO, we gotta just call this function at the script with the given params again" and boom itll do that

expect ofc its more complex than that. lets walk through some scenarios. uh this project man just keeps growing bigger and bigger.... and im like stuck implementing the same shit. i guess - or at least im telling myself - i need to constantly adjust the groundwork of this system as i discover more of the requirements and needs of the system. once i do reach a point where the groundwork is laid out.... oof thats fucking takeoff boy.

alright so requirements analysis agent receives a directive. it decides it needs user input. it outputs: 
{
    "node_id": "",
    "type": "user_input",
    "args": {
        "agent_message": "...",
        "swarm": swarm
    },
    "next_function_to_call": ""             This is the next function to call within the same script this action is in. 
}
{
    "node_id": "",
    "type": "instructor_completion",
    "args": {
        "model" : BaseModel,
        "messages": List[str],
        "swarm": swarm
    }
}

so actions always start from the main function but then can be broken down in this manner

so what is that thing above, "user_input" or "instructor_completion"? Is that a util? I suppose it is. yeah i mean it is thats fine that works. wait a second doonk u stupid bitch wait what oh shit yeah no it is a blocking function

also what if the thing being passed around is not serializable?

Today: manually fill out util space metadata, handle node failure, review reports action, python coder action, requirements analysis action, add get user input blocking operations, action router
Tomorrow: memory router, connect swarm package with frontend and run it


# Abstract syntax tree
we want to add further context to the util space metadata. specifically when debugging, or wanting to retrieve the code as context we dont want to ahve to retrieve the entire file string and oput it into gpt as we might not need all the context. we can use AST to mark out the precise lines of the function we want. in fact we can actually not include this in the metadata. we can perform this operation dynamically when we perform retrieval. since we have the file and the name of the object we want we already ahve enough information to perform this operation. this is my first time hearing of or thinking of ASTs. we can use this to perform tracebacks throught the swarms code i think and use it for more prercise surgical retrieval

# Pausing and resuming a swarm run
pausing a swarm is easier now because the swarm is decoupled. lets say the swarm is running. we have some nodes waiting on blocking operations from the user, some nodes in the midst of watiing for a reply from openai, some nodes

well whats the actual swarm master process? The swarm master will pass us one of two things. A blocking operation or a list of nodes. and then we execute that. We simply add an extra step before a cloud function executes to check if the swarm is still active. if not nothing happens. actually something does happen, the blocking operation or node gets added to a buffer for that swarm. when that swarm gets resumed, it can simply retrieve all of those


# Blocking operations vs actions vs nodes

so ive definitely found the right thing, execute action, decouple along blocking operation, pass context between blocking operations. between nodes we just pass messages. oh i suppose a blocking operation just passes back a blocking operation. yeah.


# User communication action
    This will go like this. we are given a list of things we need to determine. 
    1. We send a first message asking for the user to provide the information we need.
    2. The user provides the information.
    3. We check off things that we have determined. We generate a next message asking for the remaining information, and potentially further questions that have arised from the previous information.
    4. Repeat until all information has been determined.
    5. When all information has been determined we terminate this node.
    
    Now we have a bit of an issue

the issue being i suppose... no no i suppose this works. in things like the python coder we have a thing where it will double check and performa similar thing... uh wait. itll generate a list ot context/requirements it needs. then it will pass it to a retrieval agent who will be tasked with passing it to user or other retrieval methods like memory retrieval plus AST parsing to get specific pieces of code, web browsing etc.

what im realizing now is the interaction between nodes might be more complex than i initially expected. this should have been obvious in hindsight, that it wouldnt be as simple as terminate, spawn and the termination crawls up until we see a manager node at which point we do the manager review process. Every node needs to have a unique termination process. For example the node who spawned a user input node needs to take the... wait a second no the architecture still works. because the manager will receive the user comm node report and make a decision with that. Any specific nodes that have user input loops will have that happen inside itself for itself. okay so so far the architecture remains good.

Although one worry i have is the unnecesariness sometimes of passing swarm and node_id to a node. but as ive already seen and done that can be handled by context.  maybe only context and args - yes thats the way.

Also now i definitely see something i want to store in the user info section of the frontend. For example, with a user input node, display the persisted context, unknowns and current report for the user to see. 


# Goal 
okay we now have the interface with the spawn and chat done. lets define a concrete first goal for the swarm. we want the swarm to help build itself out more. Lets list a bunch of things we want the swarm to be able to do locally first. 

we need to start with a problem that is genuinely quite simple in a coupled system. we can just try to have the swarm create a web scraping tool for itself. although a web scraping tool probably requires a web scraping tool... huh. well. does a web scraping tool require a web scraping tool? Idk we'll figure it out. we'll have it build a first version. itll test on a website. if it works itll move on to a js rendered website, itll keep on trying different websites encountering errors, data parsing errors and refining itself. and then it needs to add it to the action space. 

how might this process work? We want a general predefined framework that can handle multiple types of problems not just this one. 

should we generate a plan first or just go straight into breaking down the goal? I suppose it should be more dynamic. uh fuck. when we have a problem... damn. 
no. we can give the breakdown directive person a scrap paper area to make a plan
its goal is simple: add a web browsing action to the swarms action space

# Termination Policies

I have a swarm of nodes, nodes consisting of an action which is broken along their blocking operations and can include anything including using LLMs to reason. Nodes can break down goals into smaller pieces and spawn more nodes. nodes might be given a goal and have to decide what type of node to spawn with a what action. Nodes might decide they cant accomplish their given task and need to ask another node for information or talk to the user to understand his intentions and requirements better. The swarm follows a tree starting from the first node who is given a goal and breaks it down. It then spawns child nodes. Those child nodes are assigned with deciding what type of node to spawn next, they are called action router nodes. Those children nodes may take on the form of further breaking down the goal, coding, talking to the user, writing code, browsing the internet, or creating a new action.

Now eventually as we move down this tree and it gets created a node will eventually accomplish its subbranch, its own individual goal. it will terminate. Than the node above will terminate and so forth. But ive assigned this thing called a termination policy. i need help giving names to the different types of naming policies. ill describe the different types of termination i have so far:


1. A node terminates. every node upon completion and spawning a subnode or child node will have a report of what it finished. if the node was simple and definitely suceeded and only has one child, its termination is very simple. it simply terminates and passes the terimation command to its parent
2. Nodes that break down goals into subgoals and spawn multiple children. when one of its children branches terminate and propagate the termination up to it its termination policy is different. it must make sure all its children are terminated. if not wait. if yes, it checks if there was a review node amongst the children. if not it creates a node that will review all the reports of the children. This is because the node breaks goals into parallel goals, so there might be a next set of subgoals to be done after the first set has finished. the review agent has its own termination policy of type 1. the review agent will spawn a child node that breaks down the goal further followiung the previous set. if the node that breaks down goals has all its children terminated and amongst it is a review node (which only terminates if it determines the goal is fully accomplished) then that node terminates
3. User comms. some nodes decide that they need to communicate with another agent or user. so they spawn a child and pass their questions to it. that node will find asnwer to those questions talkng to the user, or talking to another node. Eventually that node terminates, and the original node who asked the questions needs a termination policy that says it doesent terminate, but needs to spawn a new node just like itself, clone itself and pass the questions and answers. then it can change its termination policy to simple termination

so when is a node assigned its termination policy? Does its termination policy change through time? For example the decompose directive node has 3 steps, 1. wait for all children to die, 2. spawn review node, 3. simple termination and report consolidation when review node dies. So i suppose the termination policy doesent change through time. but one thing is how does the... hmm. i guess we need to think. Where there only ever be one decompose directive node? For all problems in the universe those using the decompose directive action work? It seems like a very bold claim. but what problem doesent need to be broken down? Every problem needs to be broken down. And in what manner can you break a problem down? Well i guess ive answered myself. we only have one decompose directive node. we only have one node for review. 

now to think about the comms nodes. well you dont begin life as a clone_with_questions_answered node. nobody chooses to clone themselves. Nodes dont want to live they want to terminate. my god lmao this just reminded me of mr meeseeks from rick and morty. 

i just got distracted and watched the clip of mr meeseeks on youtube. definitely including this when i make a youtube video it encapsulates what i want the agents in my swarm to be like pretty well.

anyway... uhh where was i? So we was like each node has one termination policy. right. rightyo. right right right. so ummm the comm nodes. noone is born a commy. you become a commy when u need help. so this means termination policies CAN change. and where does this change take place? Inside the action. so through the blocking operation .. uh fuck. yea this is the question that matters. so we conclude the termination policy CAN change due to a CHILD node - wait no its not the child node. it is itself. a node can only change its own termination policy. and typically.... well whatever through its output. well lets see the swarm operations and which might change the terimation policy. uh no i cant speculate this hard. but let me try. so spawnoperation definitely yes. failure operation yes. execute operation definitely no. blocking operation? Terminating operation? so idk.... should i add an extra metadata space for all nodes? no i think its much clearer to add them where i need them. i should them the same with the actionmetadata and all its different types.


should i move all reporting to within the action? I think this makes much more sense. the reason this became an issue is cuz... ah fuck it no need to explain ima just do it its definitely correct no doubt.


review all the actions one more time... start writing docs, review all the actions and write unit tests for actions


# Simplification
i really want to simplify, create some sort of common structure reusable shit for the actions. it appears that most actions consist of instructor calls, user input padded with some logic. 

So every action contains defined pydantic models, system instructions and then a chain or loop of logic. i can create a base class with a reusable method for creating messages. it can include a decorator for setting reports. So all reporting happens within the action. the abstract base class can set and just fucking hold the swarmconfig, node_id and message. 



# Logging not just action functions

right now we added decorators and wrappers to handle errors and do journalling for action functions. however we want to apply the exact same failure handling and logging process for all termination and blocking operations. this means i kinda wanna take those a level up and reapply them from some more common place. 

Whats supposed to be in the journal? I really just want to be able to look at a journal and understand and be able to see everything that node did. god what did i introduce that made everything so complex and messy? I added error handling, journal logging and an abstract base class for actions. this should all make my code better later. it should give us more insight into the behavior of the swarm and each node. 


Action

    Function (perform logic, write to journal) -> all wrapped by failure handling

Blocking operations come from actions. blocking operations should similarly be imagined as just a function expect it happens outside in the util space. it performs logic, writes to journal and is all wrapped by failure handling. 

The spawn and termination operation can be seen in a similar light. 

lets review the entire swarm lifecycle including logging, failure capture, journaling, state and history updates, blocking spawn and termination operations and the levels at which all of these happen.

So we first create the initial spawn operation, spawning the first decompose directive node. nothing gets logged, updated or created because the operation hasnt been executed yet, just created.

Then we pass the spawn operation to the swarm god. The swarm god will spawn the node. the node object gets added to the swarm state. right after the node object gets created and added to state we should immediately add the spawn operation to history.

We then proceed to call and execute the main function in the action script. This will return a blocking operation. the swarm god simply returns the blocking operation. In the action we should journal. Do we assume the swarm god doesent mess up? yes. yes we do. We have failure operation handling inside on the action functions. 

Now when we get a blocking operation we handle and execute it outside of the action function. yet we should still do all journaling inside the action function function right? Or no? No we shouldnt we should be able to raise failure operations and journal from within blocking operations. indeed. the blocking operation always gets the swarm and node_id anyway.



# What information do we want to store about each node?

We store the node action id name on top
We then have the message.
We then need to display the reports in order for what it has performed. this can get quite long. 
so everything is already stored in node, we just need to have good reporting now.

So we want to make 2 distinctions:

Logging for visualization and logging for debugging. What will both of these logs look like?





## Visualization:

For every node:
    - Display the name
    - Display the message it was sent along with a prepended string for that action id
    - Display whether it's alive or dead.

Decompose Directive:
    - Display the subdirectives it got decomposed into

Action Router:
    - Display the action it chose to take

Ask User Questions
    - Display the questions it wants to determine
    - Display the list of answers it determined 



## Debugging:

We'll want everything we have above but in addition:

For every node:
    - Display the name
    - Display the node_id
    - Display the action_id -> ?
    - Display the children_node_ids
    - Display the termination policy -> ?

Decompose Directive:
    - Display the Instructor Request
    - Display the Instructor Response
    - Display the response from openai
    - Display the children_node_ids


Action Router:
    - Display the name.
    - Display the message it was sent to decompose
    - Display the message sent


The thing is we can easily deduce what all these things are simply from the above section. But no, because the AskUserQuestions requires more insight, the conversationstate at each point. So we DO need more information for debugging each node. I suppose for debugging we want it to be easy to see everything thats going on without having to reference the code? So it should be easy for coders to come in here and learn about the system essentially and see whats going on behind the scenes



okay so what i need to add now is two types of logs for the swarm: journal, and dev_log. So the node now stores three different things:
    - reports (for internal swarm comms)
    - journal for easy visualization
    - developer_logs (for debugging and seeing more about the node)

Im confused cuz... those subdirectives that are generated might not exactly be what was pursued. ah fuck. I feel like for this node to make a good decision it needs to have an idea of what all the branches DID.So during termination, should we propogate and accumulate a report upward? The report is different from the journal. It represents what the node and all it's children have done. This could grow very large. This is notideal. So what should the report contain? Like we can have at nodes that WANT to look at children to consolidate a report by looking at all the node's journals on the spot. Can i think of something better than this right now? When searching down a branch we surely cant go all the way down to a leaf node that'd be insanity.We definitely want to stop at decompose directive nodes and simply gather the report from that node. So that means. That node does need to hold a report? I suppose upon termination you can pass a message up, so each node holds
a report of what the entire branch below it has done. this report gets built during termination. So we do need a leaf node termination process. The leaf node takes a report and just sets. A node terminate terminates and consolidates the report passed to it with it's own journal.

Okay the whole thing was pursued chronologically down the branch. We just append all the branches last journal entry together for each branch along with the subdirectives. We assume that we'll have stop nodes so this process never gets too large. Currently the only stop node is decompose directive.



# Question Router

Now this is a unique action that each user gets to configure. for example people like my mom should get NO technical questions or technical matters brought to them. They may deserve some brief simple explanation of what is needed perhaps so they can understand. on the other hand, me when using the swarm to code i will by the very nature be trying to code something difficult. in fact i will be doing things that by definition i will have to get involved in the technical matters. now quite cool is another part, imagine we have a biologist who cant code. he'll want to work on a different abstraction where he gets, if he so chooses, to receive no code related questions or matters brought to him, but he chooses to oversee and direct the (i have no idea wtf biologists do but whatever tf they do he controls.)

very cool stuff indeed.


# easier swarmconfig
sooo. what is the swarmconfig process? the swarm config process has 3 primary purposes:

1. configure to your platform, whether it be local, cloud etc. provide necessary keys and paths
2. configure with your custom data
3. user customizes swarm, things like question router etc. 

rn some things happen everytime u create a swarm config. we'll only think from the local perspective:
1. a mongodb db gets created. internal metadata gets dumped, like rn the action space.

the swarm config object then forces all action, memory util space, swarm state and history to be stored in that mongodb db. It forces all files to be saved to the specified root path. 

That is it. for every new swarm a user creates we create a new swarmconfig object. we need something using the swarm_id to get the swarmconfig object. how may we do this? well i suppose we leave it up to the developer outside the package to save store and retrieve the swarm config objects accordingly. yeah. 

another question is the following: sometimes we dont want to recreate swarms for everytime, like if we are testing. what types of things can we do on the same swarm config object without problems? multiple swarms can live in the same swarmconfig IF they each have a unique root node id. and we just need to keep track of the root node id. so in the interface we need to add root_node_id back to the swarm object. and then when testing the interface we can have one swarm space, and reuse it just keeping track of root_node_ids .

# Confirm Completion Node (renamed to review directive)

This process can be complex. Confirming the completion of a directive has many edge cases:
    - One of the subdirectives may have failed and been deemed impossible.
    - The depth of the tree is unknown. Do we review all branches at once, one at a time,
        or if a branch is extremely deep, do we have to review it in chunks?
    - How to handle the case where we realize that the overarching directive was incorrect?
    - How to handle the case where we realize that the overarching directive was correct, but
        the subdirectives were incorrect?

I suppose here is the methodology: 
    The confirm completion node is by default given the final report of every leaf node of each 
    branch. Following this, it may proceed to ask questions. These questions will get passed to 
    the question router who will get answers to these questions and return them to the confirm 
    completion node. 

What is the final report of a leaf node? A leaf node should in fact be quite well defined. And we can just set the last log of that node as the report? Okay. no wait that doesent necessarily work. ill just add a report var to each node. each node finished by stating a report comprehenisvely describing what theyve done, perhaps also including refs to like links, file paths to memory etc of things relevant. yeah that works.

this brings us to the topic of sharing constants. strings, things that need to precisely be correct. these can be navigated by routing, but how to pass them around? well you know what i always say, dont worry about that until i need it. lets just add a report var to each swarmnode

okay so ive now added reporting to all nodes. each node has like a comprehensive report of what its done, a summary of what its done. It could be computationally expensive to even just gather the report of every node recursively. I think we definitely want to stop at each decompose directive node. So we'll recursively travel to each leaf node and stopping at decompose directive nodes to gather those reports. we'll do this seperately, perhaps in parralel for each subdirective. then we'll ask decide, is this subdirective complete, or ask questions if needed. then after that process if all subdirectives are complete we can say that and check if given that all subdirectives are complete is the overarching directive complete? If not spawn a new decompose directive node with the overarching directive and all the reports along with the derived answers u got from questions. should this all be packed into one node? its quite a lot. whats concerning me is twofold:

    1. this is a lot of stuff to stuff into developer logs in the ui, its gonna be af fucking ton to read. i imagined the ui as having each node be quite manageable to read and review. but once again, the python coder and action router we can imagine will get quite long. whats more important is having individual units of each node. are there reusable components in this overarching confirm completion node aforementioned? theres utils like getting all the lead/branching node reports. not rlly that. then we ask questions abt this specific topic. not that either. than we - yeah no im wasting time. this is one giant node. if anything, in the future we adapt the UI to handle more stuff in the dev logs.
    2. The parallel blocking operation execution - when u get them back how do we know when to continue with all the results? we gotta add an execution memory to each node. yeah this is what we ought to do. what we ought to call this? lets call this node_ram? No. execution_memory. uhh... no. context? No context isnt right, i think execution memory is closer. okay who cares, execution_memory

alright now outline the steps again

1. Get reports of all leaf nodes and decompose directive nodes. Determine if the subdirective is complete given this report. ask questions if needed
    - if questions are asked, pass to question router. receive the answer, and repeat the above step, potentially asking more questions.
2. After we've determined whether each subdirective is complete or not, or whatever we finish each one off with like a conclusive report, which might have been just the leaf node report, or might be something more comprehensive including answers to questions we received. We pass all of these along with the overarching directive and ask "is this overarching directive complete, made irrelevant or impossible, or is there more steps to take to achieve this overarching directive?
    - If more steps to take, spawn a decompose directive node
    - If complete terminate.
    - If failure, create a failure node, and ill come and check it out and figure out the problem.

Note, decompose directive nodes set their reports at end of parallel review. 

mmm. encountering a problem. So i implemented the first part of the action, where we get reports of leaves and immediate child decompose directive nodes for each branch. given these we ask gpt if each branch has completed its subdirective with all these reports. True or False for completion. In addition, it can ask questions. These get passed to a question router. 

Now here's the problem im facing. For performance, we review each branch in parallel. now multiple of these might end up asking questions, thus spawning multiple route question nodes. Well the route question node gets the message, the questions. But when it completes, how does it pass the answer back to the parent? what does it need? it spawns and all it knows is the questions. its not aware of all the stuff going on above it. so something must be defined in the review node, a custom termination policy ofc. in the execution memory we can store all the branch head node ids waiting on answers. this process can be defined by a termination policy. this termination policy should simply point to a function inside the action. but when a route question node terminates, it needs to somehow pass the answers alongside with the branch head node id it corresponds to. How can we do this? we can add a new field to swarmnodes, context. Context gets passed down spawn operations and up termination operations. they can be submitted or removed by any node in the tree as they see fit.

wow this is amazing. just by talking to myself i find design choice answers every time. and obviously this is without a doubt the right answer i mean, there is no better way to do this. this is the logical optimum. i need to find logical optimums as fast as possible. so im so worried someone will create this before me and my work will be rendered irrelevant. Lets be honest, im not as experienced a developer as others. but coming to logical conclusions is something im capable of doing. noone really does this better or worst i think, this is the purest of mental labors, logic. I need to spend as much time building this out. this system is built of logic and i might have a chance of building this first in the world if i spend more time than anyone else using logic to solve these problems. 

anyway, back to the solution. so we decide we have questions to ask. spawn a route question node with branch head node id in context. set termination policy change to custom_termination_handler_handler. this termination method will look in execution memory for a variable named, \_\_action_termination_handler\_\_. this termination method will then call and return the result of that function with the child node_id that called it. this means we need to change the termination method to hold the node id of the terminator and terminated.

# group logging
New problem. Logging needs more complex handling. the problem i mentioned before? Yeah no this cant be ignored. What we have is a further addition. 

This is a log:
{
    "role": (swarmstar, system, ai or user),
    "content": "..."
}

Currently node developer_logs contains a list of logs in time order. New addition. developer logs can contain nested lists. Logs inside a nested list means those were performed in parallel. For example:

[log1, log2, [log3.1, log3.2, log3.3], log 4]

or even,

[log1, [[log2.1.1, log2.1.2, log2.1.3], [log2.2.1, log2.2.2]], log3]

So we can identify a log by the key: [index, index, index], a list as deep as the logs go. 

Now question. Currently im working on review directive completion. its why i decided i need a more complex logging system. heres the issue.

1, 2, 3                            confirm completion of branches
                    log in 4.x                              log in 5.x
                   branch A asks questions            branch B asks questions    
                   gets question answers               gets question answers

i suppose this can be passed through context? yeah that works. oh wait lol i was thinking node context when i wrote this, which is totally wrong, but it does work with the operation context. so i got it right by accident, but no i got it wrong. just a funny coincidence.


# A revelation???????

ohhhh yeah. The swarm primarily comminicates 5 things as of now: 
    - Directives
    - Context
    - Questions
    - Reports
    - Logs

My mental process was:
    1. Directive
    2. write code
    3. write tests
    4. run tests, edit code


I believe a better way is:
    1. Directive
    2. write tests
    3. write code
    4. modify tests as needed
    5. run tests edit code

i wont explain this in depth here, but i know this is da way. this is da way. where are u running? why are u running? COME BACK HERE BOI OOGA BOOGA BOOGA

I need to wake up tmrw, code for 2 hours. eat breakfast, go to the library. stay in the library until closes. come home. eat dinner. code until sleep.

After tmrw wake up code 2 hours. eat breakfast. go to library. come back at 1pm eat lunch. go back to the library before 2. stay in the library until it closes. come home. clean home. go to sleep

if i do that, wednesday u get a reward: Wake up and go on a run. then code, eat breakfast and go to the library and continue the routine.

oh btw if i want the reward, before wednesday i need to:
    - finish review directive, question router, question nodes. parallel logs in UI. Successful front to end termination for easy 2 question. Map out coder action. Map out metadatafying a repo. map out action creator. yessir we are getting somewhere. 

ok lets be honest, i cant finish all that by wednesday. BUT - within the next two days we'll put in 15 hours a day of work. we can get a lot done in 30 hours.

# Consolidating reports

First of all, what goes into the decompose directive report?
What goes into the review directive completion report. 

ahh this is where we have a problem. the decompose directive node already has a very simple report:
    self.report(
        f"Decomposed directive into immediate actionable subdirective to be independently "
        f"executed in parallel.\n\nDirective:\n{self.node.message}\n\nSubdirectives:\n{subdirectives}"
    )

and this is indeed correct. review directive completion will also have a very simple report as well. The issue that im facing now is the following

when collecting branch reports ot determine if an overarching directive has been accomplished we gather reports from all leaf nodes as well as from immediate child decompose directive nodes. this prevents us from diving too deep into the tree. u can easily imagine that this could overflow the context limit of an llm. so we want to consolidate reports at every decompose directive node i think? And grab that from the nodes stored context?

question to think about when i solve the problem above: If we have node context is the context passing back and forth through blocking operations necessary? Umm let me just answer that rn - no. I think? Hold on let me think abt this more. yeah no it is necessary. we need both yeah. 

anyway, back to creating that thing, the consolidated reports for the decompose directive node when it terminates. 

Distinction: Every node creates a report when it finishes executing it's action

the decompose directive has an extra "consolidated_reports" parameter in its context that is created when it terminates. how do we create this? The thing is this
    - all nodes that are not leaf nodes are not actually actionable actions. they were managerial actions, routing, planning, decomposing. 
    - by gathering reports from only leaf nodes we are cutting down the number of reports. We need to have a managable amount of stuff when doing review of a directives completion. we can explore more by asking questions ofc

lets set some ground rules. if a node says it did something in a report we trust that it has done what it said. it is that nodes duty to confirm what it reports it did is actually complete. So a coder must do and run tests before it reports and terminates saying it has finished coding x or y. likewise for other tasks. 

there is also the issue of if a subdirective has not been achieved. well if a subdirective has not been achieved then we are almost certainly saying the overarching directive is not complete. we would then proceed to spawn a new decompose directive node under the review node. 

i mean fuck it tbh. lets just keep it simple. the review node takes all the leaf node reports + questions and answers it got through its review process, and compresses it into a report it will pass to the decompose directive node if it has came to a decision. Oh are u asking about decompose directive nodes that spawned a review node and got passed up for not completing? What is their report then? well this is where the tree- the current tree structure is throwing me off.

mmm i suppose that the tree is not actually chronological which can throw people off, and which is throwing me off now.

okay alright i got it. heres the situation. if the review directive node itself is the one that initiates termination, yes it can consolidate reports and set the consolidated reports of the parent. however. uh wait a second no even if it spawns it passes a consolidated reports to the parent, and on the way up we just accumulate consolidated reports as we pass decompose directive junctures and compress.

[text](public/IMG_3847.png)

okay so this was too much to fit in my head, i had to resort to good old paper for this one. anyway ive got the solution. there are different scenarios:

    - review node initiates termination by decision.
        Set consolidated reports in parents context.
    - review node decides to spawn a new decompose directive node.
        still, set the consolidated reports in the parents context
    - review node propagates termination from below.
        take review child node consolidated reports and combine with parents consolidated reports. compress.

decompose directive nodes can exist in 3 scenarios:
    - root node
    - spawned by action router
    - spawned by review directive completion

Consolidated reports from dd nodes spawned by action router will be handled by the review node, as the parent dd node is still waiting on this branches completion
Consolidated reports spawned by review directive completion will combine on both sides like a sandwich. okay we're good enough waffle. lets implement this. in fact. should we implement a consolidate reports action dedicated to this? In fact here we can actually implement a token count check. if the consolidated reports are smaller than some number x than we can skip consolidation. in fact for my current small scale test goals im currently doing consolidation is not even necessary. and also granularity of compression is not that simple. You cant give a long one and say compress you have to compress at a certain granularity to a certain granularity. 

Should consolidated reports remain as just a single string?

New problem. the algo i described above will take a consolidated compressed report and combine it with another consolidated compressed report. imagine one is much deeper than the other. in fact as we know the swarm will follow sort of a series of steps. 

U have the first layer with the first set of decompose directives, then the next set below that and so forth to layer N. when layers 1-N finish and terminate and we come back to layer 0, we're going to be doing this:

We're going to take the consolidated reports that layer 0 initially had on layer 0
We're gonna take the consolidated reports of layers 1-N which are compressed

And then we'll consolidate this. The problem here is that there is this loss of information on the way down. In fact its counterintuitive, because Layer N was actually the most recent layer that was performed, and layer 0 was the first layer, so its actually got diluted in reverse time which if anything is the opposite way dilution would happen, if we even wanted dilution. which we dont. im gonna pivot and think of an entirely different approach. this might not be the right approach - i suspect the right approach is a combination of the 2. here let me explain:

at every review node we previously said we'll retrieve reports from every leaf node, but also stop at immediate child decompose directive nodes to grab their consolidated reports to prevent context overflow. Lets throw the consolidated reports idea out the window for now. Lets say at every review node, we literally just go all the way down and grab EVERY leaf node's report. and then this will obviously cause context overflow. but it will allow for like even spread of compression across all reports. which is what we want. we want reports to be compression loss to happen in the direction of depth of the tree. the problem here is the mismatch between the sort of order of propagation and current tree structure. in fact. wait. my brain is touching something. when a node sets its consolidated reports it shouldnt change it. that decompose directive node is responsible for the branch nodes it spawned, but not the decompose directive node spawned by its review node if it exists. but this raises an issue. if this decompose directive node, is a child of another decompose directive node then when that node's review node wants to go down and grab stuff what does it do? 

ive drawn another picture

[text](public/IMG_3848.heic)

as you can see, 8 and 9 get compressed multiple times whereas 5, 6 and 7 get compressed once. this leads to the reports from 8 and 9 losing much more information than 5, 6 and 7. we need to have an even distribution of compression across all reports?

okay lets not overcomplicate this. lets imagine this is a company. the company hires x people to do x tasks. when they finish, they get the reports from those x people. they then use those reports to hire y people to do y tasks after the x people. one of these y people also decide to hire z people to do z tasks, completing his task for him. those z people finish and report to the person who hired them. that person consolidates the z people's reports. Him, alongside the other y people pass their reports to the company. the company then...

hmm weird. based off this analogy my initial intuition was correct. wtf is going on. well this intuition from a company standpoint is actually more representative of the problem than anything else. AH FUCK. let me scale this example with the company up theres more edge cases i can feel them tingling my brain

Im the ceo. 

I hire A people. they finish their tasks, each giving me a report. okay okay nice reports. I need to hire B people to work on the next phase of this project. one of the B people hires B1 people to accomplish his task. One of the B1 people hires B1.1 people to accomplish his task. the B1.1 people finish and report to the B1 person who hired them. This guy checks if he has finished his job. He hasnt. he hires another B1.2 people to work on the task. those B1.2 people all finish their work. Now the B1 person who hired them reviews the B1.2 people's reports with his mission also keeping in mind the work of the B1.1 people. He decides theyve finished. By now all the other B1 people have finished and reported to me. The B1 guy who hired people then gives me a consolidated report. 

Each node in the swarm system is responsible for its own report and the reports of its direct subordinates (nodes it spawned).
When a node finishes its task: a. If it's a leaf node (no subordinates), it generates its own report. b. If it has subordinates, it waits for their reports.
Once a node receives reports from all its subordinates: a. It reviews and consolidates the reports, considering its own task and the subordinates' reports. b. It generates a consolidated report that summarizes the key information from its own task and the subordinates' reports.
The consolidated report is then passed up to the node's parent (the node that spawned it).
This process continues recursively up the tree until the root node (CEO) receives consolidated reports from all its direct subordinates.
The root node (CEO) can then review the consolidated reports, make decisions, and proceed with the next phase of the project.

this analogy leads me to see that the order of information loss is correct. the actual vector of time in which these things happen is correct. and the root level CEO node simply doesent need to do review anymore so that last information loss upward in the final termination propagation... omfg i solved it uuhhhhhhh yes my brain was aching bro, fuck.

okay lets review. First and foremost, the thing that confused me: The main trunk of the tree, there is no need to ever propagate errors up this tree as there is no review completion node to be ran on the way. the reason is because when the review completion node performs review and decides the overarching directive is not complete it spawns a completely new node, taking the overarching directive and revamping it with the set of subdirectives that was just performed. in this manner, there is never a need to propagate reports up the tree trunk. 

So lets conclude the passing of reports conclusively.

    - Whenever a node finishes executing its action and outputs its final spawn or termination operations it will submit a report concluding what it has done. managerial nodes make a decision, and leaf nodes perform a direct action torwards the goal.
    - when a leaf decompose directive node terminates it will consolidate reports of all its direct child leaves. it will store this consolidated report in its context. this consolidated report will not be touched or changed.
    - when a parent decompose directive node terminates, we'll use the method we originally planned. to take the consolidated reports of decompose directive nodes and direct leaf nodes and consolidate those.

Now lets just refine the consolidate report function. ah also do we create a seperate consolidate report function? Nah i dont think theres any need. 

# checkpoint

well. if u read this journal, youll see how earlier on i said "oh we're ready to start pushing the swarm and add capabilities!" well, it wasnt i needed more infrastrucure. but now we are. now the worst is ahead of us. the competition fucking devin pissed me off man fuck. here i wrote it down:

1. Non technical user asks for an app/plugin to be created for them. It is not meant to be scalable. The user only communicates what features they want and gives feedback. The swarm is responsible for choosing stack/architecture, building, deploying and iterating.
2. Technical user asks swarm to add a feature to his repository. The swarm tries to be autonomous as possible, but will ask the user questions about his system, design choices, patterns to follow etc if needed. How to test something, if it can add something, approval for its choices.
3. Technical user asks swarm to create a scalable product, or something more deeply technical and cutting edge. The user is involved in requestiong features, choosing direction and makes all high level choices. The swarm can make suggestions, but it must let the user make all choices. the swarm builds, and might ask the user for help on creating abstractions or system design choices. the user might not know where the project might go as a whole. it might be an iterative process, constantly ongoing and adding onto the directives. before concluding completion the swarm must always ask the user if he is happy. after a swarm has determined completion it should not be deleted. if the user wants to continue adding or changing things in the future it may come back, and the previous memory space will need to be reused.
4. Having swarmstar work on swarmstar. it must refer to me for any decisions it makes for approval, and it will need to understand itself deeply. i think this is a good place to start. if i can get swarmstar to deeply understand itself and build on itself, we should be able to get swarmstar to apply the same principles to another repository, and have it upgrade or change itself as needed during when this happens.

These are "types", different categories of directives. there are obv a lot more, these are just "software" directives. unlocking software directives means itll be able to work on itself and dynamically create new actions for itself as needed to accomplish new tasks on the spot. 

we also introduce, "general" and "specific" actions. general actions are meant to be found, searched for. specific actions are meant to be directly called upon. 

we also must now think about memory. types of things we need to save in memory:

- constant variables (website links, keys, passwords etc) these may have a unique spot in th ui to be entered, but they must be saved appropriately and be easy to find.
- user details. in the initial phase we aim to understand our user. are they technical or non technical? What is their background? How involved and how much control do they want over what is being done? 


# Node Principles

- Do NOT make assumptions. Ask questions. About intent, requirements, system.
- Each node is responsible for its own report and verifying the correctness of the report. it must be certain that what its said is done, through testing if coding etc.


# Memory space & Artificial environments aka containers for ais
ive already spent some time thinking abt this. lets walk through the flow of whats going on here. before i begin i want to preface with something:

A big problem i had in the past was trying to hard to make something dynamic, flexible. with the action space i tried to make the actions flexible to any language, to any platform, and different methods of running. in fact what i ended up doing was severely constraining and shrinking the space of the problem at the end: I defined an abstract action class and created a strict flow and way of handling actions with only 2 types internal and external actions. anyway, keep this in mind when dealing with the memory space. reduce the complexity down to only whats necessary

## memory space
lets keep it simple. actual storage of memories? Mongodb. most things, most files are under 16MB and can easily be stored in mongodb. we dont have to create any folders. the memory metadata tree contains the actual organization of the memory space. and the actual memories are just stored on mongodb in a collection called memories with UUIDS. The memory metadata space will have information about how to retrieve each memory. there will be different types of memories as well with different types of retrieval. all files (that are text files, code files) can be retrieved individually as a string.

However in addition, we have actual code projects, repositrories, stuff we need to run. with dependencies. the root node of these "projects" can be clearly labeled to indicate, "hey, this is a repository, all related meant to all be in a container together in order to run." okay. now to the actual topic - how to run code in the memory space and how to handle and manage all the enviroments.

## containers
obviously containers. docker. now we walk the flow:
the swarm needs to run, test some code it wrote. this is the first time the swarm has had to run code yet, its young. so it creates a new container. the actual LLM is only given a simple question - what language is this project using? And we'll proceed to create a blank container just off the base image for that language, python in this case lets say. itll choose the most recent version of python (idk maybe different). Anyway the container is created and is running. we first go to metadata tree and using the information there, we'll move all the files to the container, in the same format, following the same folder structure. then we'll create a poetry file and look at the dependencies of the code, and add all those to the poetry enviroment. this enviroment is stored inside the container. where do we get the dependencies from? Well every memory node includes a list of its dependencies in its metadata. so now we get the llm involved again, explaining to it, hey we have a container, with this runtime, with this code setup, maybe show the tree of the directory structure, and these dependencies installed with poetry and poetry shell on. this is the CWD. then ask it what command it wants to send to run in the terminal. maybe itll ask questions, in which case well have to answer those by passing it to the question router who will either search the memory, internet or talk to the user. if it outputs a command well pass it to the terminal, run it and return the stderr or stdout to the llm. itll analyze this and if an error occurs will begin a debugging process, until fixed. once the code runs correctly, itll either output another command or say, hey im done. i dont need the terminal anymore. 

Now we have a weird decision. as it goes off and does other stuff, we have no idea how long itll be until it needs to use the container again. how much overhead is there from having a container running, but really just waiting for tty? Maybe instead we should add a timer, so if x time passes well kill the container and (ill explain what happens here in a moment) and when the swarm decides it wants to run code again itll either send a command or just start a the container again, getting the image. So lets call that a terminal session for the swarm. it can start a terminal session to container x.

Now the actual container will persist what? It wont persist the code in a volume. everytime a terminal session starts, we instantiate the docker container by pasing files from mongodb. all changes to the code are made to mongodb, and propagated to the terminal session, if there is an active terminal session with this project. However, the container DOES store enviroment specific stuff. any poetry stuff. or runtime stuff. or system stuff. or npm stuff etc. the images are stored with environment stuff in docker registry. the code is stored in mongodb. when starting a terminal session for swarm, we get the image start a container and get the code from mongodb. Whenever we have a new different project that requires a different environment, and we want to seperate it, or actually more appropriately, the swarm decides it has a different project, we will create a new image for that swarm. okay so thats containers and how the ai runs code

another situation, what about long running code like deploying an app? Are there easy ways to host apps on like vercel, just frontends with a backend, not at all meant for scale, just one user for free? Or i guess we dont want to ask the user to deal with those details, wed want to just host it.... that is like a one off terminal command, not like running a fastapi app or next.js and having it constantly running on the temrminal session right? I think we'd want that. use some other service to host and deploy any apps we make and let the user try it out, give feedback, change redeploy. ive never deployed apps off my local machine before... so i dont know how compliocated it is.

## The memory space.
the memory space contains 4 root level folders:
- user - all convos with user, requests, descriptions of user. refer back to this for ground truth, of the users requirements intentions, and to understand when to get the user involved.
- swarmstar - documentation and stuff internal to the swarm, so it can work on itself, understand itself when working
- projects/ or containers - each folder (subfolders if theres lots of project managed by one swarm) corresponds to a project, which corresponds to an environment/ container id in docker registry. this is what we talked about above
- internet scraped stuff - stuff we gathered from searching internet, docs, code etc.


~~Implement the memory storage system using MongoDB, including the metadata tree and retrieval methods.~~
Develop the container management system using Docker, incorporating the LLM's decision-making process for determining project language and container setup.
~~Establish a mechanism for moving files between MongoDB and containers, following the folder structure defined in the metadata tree.~~
Integrate package manager for dependency management within the containers depending on the project.
Design the debugging process for the LLM to identify and resolve errors in the code.
Implement the timer functionality to kill inactive containers and optimize resource usage.
Set up a system to propagate code changes from MongoDB to active terminal sessions.
Configure the Docker registry to store container images with environment-specific configurations.
Research and test hosting and deployment options for apps created by the AI, focusing on single-user, free solutions.
Create the four root-level folders in the memory space and define their purposes and usage guidelines.


# Overarching Directive Categories

1. Non technical user asks for an app/plugin to be created for them. It is not meant to be scalable. The user only communicates what features they want and gives feedback. The swarm is responsible for choosing stack/architecture, building, deploying and iterating on user feedback.
2. Technical user asks swarm to add a feature to his repository. The swarm tries to be as autonomous as possible, but will ask the user questions about his system, design choices, patterns to follow etc if needed. How to test something, if it can add something, approval for its choices.
3. Technical user asks swarm to create a scalable product, or something more deeply technical and cutting edge. The user is involved in requestiong features, choosing direction and makes all high level choices. The swarm can make suggestions, but it must let the user make all choices. the swarm builds, and might ask the user for help on creating abstractions or system design choices. the user might not know where the project might go as a whole. it might be an iterative process, constantly ongoing and adding onto the directives. before concluding completion the swarm must always ask the user if he is happy. after a swarm has determined completion it should not be deleted. if the user wants to continue adding or changing things in the future it may come back, and the previous memory space will need to be reused.
4. Having swarmstar work on swarmstar. it must refer to me for any decisions it makes for approval, and it will need to understand itself deeply. i think this is a good place to start. if i can get swarmstar to deeply understand itself and build on itself, we should be able to get swarmstar to apply the same principles to another repository, and have it upgrade or change itself as needed during when this happens.

# Notes from autodev paper
https://arxiv.org/pdf/2403.08299.pdf

Agent operations in autodev: 
    - file editing
    - retrieval
    - build processes
    - execution
    - testing
    - git operations

Agents have access to data from:
    - files
    - compiler outputs
    - build and testing logs
    - static analysis tools
    "and more"

IDE capabilities:
    - linters
    - compilers
    - command line operations

4 parts to autodev
rules actions and objective config
conversation manager
parser
output organizer
agent scheduler

CLI Commands i should use


create a base pydantic model for instructor that includes things like ask (bool if on route question) and... other stuff idk. i can package into class that this will return to the place with something idk but yeah



## Stuff i should use!

CLI:
    grep !!!!!! this one is fire.
    find

Simple easy way to check syntax bugs and lint after ai writes code.

easy way to run tests build and execute

My system shouldnt even have the agents use vim and shit to write code. if i give an ai code and they edit, just replace that code with the rewritten code.

The Commands Interface encompasses a diverse set of
functionalities, including File Editing, Retrieval, Build and
Execution, Testing, and Git operations. . These suggested commands are then parsed by the Conversation Manager, which
subsequently directs them to the Evaluation Environment
for execution on the codebase.


https://arxiv.org/pdf/2402.14261.pdf
https://arxiv.org/pdf/2303.07263.pdf
https://arxiv.org/pdf/2310.04406.pdf
https://arxiv.org/pdf/2303.11366.pdf



# More abstractions

We will create layers of abstractions. theres lots of stuff that gets repeated here and we just want to make this code better

The swarm, the metadata trees are all made of nodes. we define a basenode. all basenodes have what in common? We can save them retrieve them update them and delete them. We can copy them when we copy a swarm. whats the difference between metadata nodes and swarm nodes? metadata nodes have an internal part.

copying the internal metadata nodes everytime is wasteful. 
long uuids are wasteful. itd be better if every swarm had ids like this:
swarm_id_op_x
swarm_id_node_x
swarm_id_am_x
swarm_id_mm_x
swarm_id_um_x

in addition, ideally we'd be able to see the swarm state at any point in time, to be able to restore it to that point without having to actually save in memory every frame.

these are some important foundational changes that will make the system as a whole more powerful

every metadata tree has an internal part and an external part. these are distinguished by the type attribute. In addition the type attribute will specify how to handle these functions. since we expect some of these things to have multiple handlers we should also define an abstract for that as well. what will have multiple handlers? there will be many ways to retrieve a memory. thats one.

however in addition to adding to the internal metadata space would a swarm ever want to change the internal metadata space in its copy? I dont think it should be allowed to. there should be special types of internal metadata nodes that are internal but can point to external children nodes. 

lets take the internal metadata space. the projects folder is empty and is defined in the internal metadata space. when the swarm wants to create a new project what will we do? well if we're creating a new project we'll know that we want to be in the projects folder. we'll then pass it to an agent dedicated to storing the project in the project folder. the first project will obviously just get thrown in the root of the projects folder. Now the projects memory metadata node is stored in the internal sqlite database. how do i add the new project as a child id? Aha! i got it! Yes! Lets go! We dont want to clone the internal metadata spaces thats wasteful. but we still need to clone all the leaf nodes of the internal metadata space. we can label the leaf nodes of the internal metadata space (the folders that is) with "portal_node". what abt when a portal node has some children that are internal, but also are meant to be able to have external child nodes? well thats no problem, well have the internal space, that portal node that pops out, and then children of that external node can be internal again. importantly a portal node cant be changed expect for its children node ids which can be appended to. should a portal node be able to change its description? Idk.

So when cloning, okay i got that. so now there are two different operations - every node has a copy operation which copies it with the swarm_id at front and its short identifier and number. actually the copying can just use regex taking the old ids and swapping swarm ids. so at an individual node level we have a copy operation. at a tree level we also have a copy operation. this traverses down and copies all nodes as such. so obv with the metadata tree we'd start from the internal root node and propagate not copying until we reached portal and external nodes. however the SwarmNode and metadata nodes will have to implement their own seperate get and copy node functions due tot he internal conflict, of which the swarm nodes dont have. in addition at a node and tree level we have a delete operation, which does exactly what it sounds like. the actual trees arent actually storing anything i think. yeah they arent. maybe they just store the root node id. the true root node of each tree should be the swarm id by itself, although we should be flexible to be able to create tree object over branches to allow subbranch routing. the swarmtree should contain a method that returns the visualization representation starting from the root node. the swarmtree should contain a method that deletes the swarm tree and one that copies it both given a swarm id. In the future we can add other operations to the swarm tree like searching over it, rather than searching over the raw swarm nodes although that doesent really matter. the main benefit of moving to an abstract class comes to the abstract class for the metadata trees. we might have multiple metadata trees. theyll each need to have a copy and delete method and clone internal with swarm id. each metadata tree will be used inside the router. so that means we need to define the metadata tree as such so the router can naviogate over it. well the metadata tree really doesent have to contain anything all it needs to contain is the root node id. and maybe provide common functions like get children descriptons and shit. okay yeah.

Now what the fuck is the purpose of the util metadata space? I think that there is no fucking purpose of the util metadata space. When we want to see utils we look at the swarmstar folder in memory. when we want to use utils we... well when will we use utils, when will the swarm use utils? When it is creating an action. when creating an action we'll want to let it see the baseaction class, an example of an action creating an action is more so about creating a new logical flow. having the swarm write prompts for itself, define instructor models and chain them together correctly to be used. But it will need access to utils and to connect with other memories. itll need context to understand each of these so it can know what questions to ask. when it creates an action it should be able to iteratively write it, test it, and then add it to its external action space so it can be used. so lets think of an example where it would need to create an example. well we'll need to add really good evaluation criterias to decide which actions to take. lets say we are searching... ah fuck i cant think this far ahead. everytime the swarm writes code. there is actually just one agent that writes code. the complexity is in the process of gathering all the relevant context for the coder. gathering relevant context could require gathering information from github issues. static analyzers. terminal error outputs. searching a codebase using grep or other methods. using abstract syntax tree parsing. searching documentation. browsing the web. when first doing a coding project we discuss the architecture and languages we are using. we create a project in the memory space. alongside this project we need project metadata which explains concretely different aspects of this project. Setup, usage, docs. When creating a project itll need to iteratively build out the setup file. an agent tasked with writing terminal commands will receive the task and keep on asking questions. but before we give the terminal manager the task we should try our very best to get the most information and context possible. we should have automatic methods that do compression, summarization when context windows are exceeded. so we always communicate in a 2 fold process. we pass the directive and the context we start with to the terminal or coder question asker. theyll keep on asking questions to gather all relevant context. we'll add to the context and compress as needed. theyll keep asking questions. eventually we pass the question askers and the directive with all its changes and context gets passed to the coder or terminal runner. the code gets changed or written, the terminal command gets written and both will get handled appropriately. if code was written, now tests will have to be run. if deemed necessary. once again same process. writing code will take many steps, deciding what file to write code to, deciding to change or add code, deciding this that blah blah blah. lots of stuff. when a terminal message is sent the output or error gets retrieved. context of why it was ran, the initial directive and all its context is packed together with the output message and passed to the question asker. the question asker asks questions and we add to the context as needed. eventually it goes back to the terminal manager or is marked as complete. the important components here is the question asking, the answering of questions, making sure questions are relevant. lets say the question asker asks a question like i need to do static analysis, but we dont have static analysis. we need to create a static analysis action, and then pop back to the action router that called for it and resume. we need to be able to pass context. we need to make the action creator understand hey heres the context ur getting. so sometimes we pass context along if its just part of the state of whats going on now, even if we dont know if the receptor will use it. but in this way we need common and well defined context names. for example current_project. In addition what about when a project has multiple rhings in it and might need seperate parts? no in that case we need two seperate containers. but then theyd need to run at the same time and communicate. what if we have a backend and frontend container. these are two seperate projects. how will the agents from one communicate with the other? Right now we stand strong on the principle of independent tasks that can be done in parallel. perhaps we develop the frontend and backend seperately in parralel with mock tests and apis and shit. but then later we're like we need to do an integration test. whenever a swarm has a project in context that container is running. if there are two parallel branches each with each container. later they both finish their seperate tasks then propagate up. then a branch will need to manage both projects and containers at the same time. so a node needs to be able to activate two containers at the same time. 


## The problem or directive:
Clearly defining the problem or directive is crucial for guiding the entire process.
Break down complex problems into smaller, more manageable sub-problems or steps.
Establish a structured representation of the problem, including any constraints, requirements, or goals.
## Gathering relevant context:
Develop a systematic approach to ask questions and retrieve relevant context from various sources.
Implement a memory system that can efficiently store and retrieve information based on the problem at hand.
Integrate techniques like information retrieval, semantic search, and natural language processing to find relevant answers in the memory.
Allow for user interaction and web browsing to gather additional context when needed.
Continuously refine and update the context based on the answers and new information obtained.
Apply summarization and compression techniques to manage the growing context effectively.
## Taking action:
Based on the gathered context, determine the appropriate action to take, whether it's writing code, executing a terminal command, or performing other tasks.
Establish clear interfaces and protocols for interacting with different components, such as code editors, terminals, or containers.
Develop a robust system for managing and orchestrating multiple containers or services running simultaneously, enabling seamless communication and coordination between them.
Implement error handling and feedback mechanisms to detect and resolve issues that may arise during the execution of code or commands.
Create a loop that allows for iterative refinement and improvement based on the results and outputs of the actions taken.

we need strong places for constants between actions and nodes. use the context of nodes to pass these.
we need to be able to create actions to answer questions. action creator.
we need to be able to understand the current project we are working on. project id in context. when question answerer receives questions about context itll be search the memory. the memory will contained predefined places to answer common questions. in addition itll contain the actual codebase.

what are key differences between the memory and action space? The action space genuinely seems much simpler. the memory space will be added to a lot. its primarily just string data. back the the util metadata space. what will its use be? Not really a use for it. when does the swarmstar do recursive self improvement? when it works on itself as a repo. the best use of swarmstar to test and push it will be to use it to build itself. we should directly be laser focused on getting that. hold on... the current problems i have... can i even MANUALLY retrieve context to get it to solve ONE of the things im doing right now? Goddamn... let me try. let me try this process rigidly myself where i mimic the directive assigner and the question asker and answerer.

# Simulating swarmstar

Okay i am brian. I will simulate swarmstar. 

Human: Overarching Directive Input: 
Create abstract base classes for SwarmNode, MemoryMetadata, ActionMetadata. Consider whether UtilMetadata and the whole Util Space is necessary. This overall system is not well documented. Really feel free to ask me questions as needed. In addition, as you ask questions help me build docs out

<<__Github link to swarmstar__>>


SS: Creates node to decide what to do with link given the directive -> We should clone the repository
At the same time default behavior is to spawn a node to save the github link into memory
There arent many folders. it stores this in user given links in constants.

Creates subdirective to clone the github repository


# Memory metadata space
starting with the default internal memory metadata space
user: contains stuff from the user and any user related stuff
projects: contains code that you are working on and can run
code: contains code that you can reference, gathered from github most likely
internet: contains data, text anything scraped from the internet

Walking through an imaginary scenario

User: provided github link and asks swarm to add feature to his codebase
Swarm: 
    Whenever a constant (github link) is provided a node gets spawned to handle it. The process with a new constant is always the same. Label it, as one of the predefined choices in the enum. If not in the enum, create a new label. for now the enum contains: github_link, openai_key. Immediately thereafter begin a save process starting from user/links folder. Saving involves stepping through folders to find a good place to save an item. in this case user/links contains no more folders since we just started so save it there. (When a node has too many children, a process will be initiated to group them into folders)

    Now a question. upon saving a github link that the user provided us, do we ALWAYS want to just immediately clone the github repo and save it to the code folder? Im assuming yes. I think yeah ill just have the github repo be cloned. But then we dont want to do anything with that data. we just save it to a folder in the code folder. with what description? I suppose we can begin by looking at the files and folders in the first layer of the repo, and letting the LLM decide what folder it wants to check out. and then whenever it does find something, itll be given the stuff inside, asked to generate a description. Do i allow the LLM to go deeper and explore to what extent? We just want a base description of the repository and save it in the memory as one giant chunk, unmetafied.

    Then the llm will proceed to look at the goal provided to it. it will inevitable have lots of questions to ask. these questions will all go to the memory space. An llm will search the repo. right now it has no metadata to search the repository. Oh wait, yes i remember


This is the save_user_provided_link action

swarm breaks down directive, asks questions about repo.
checks folder:
user
code


# Action Space
action space is suprisingly easier in some ways in design, harder in reliability
memory space is hard in design. i havent even used it yet so idfk how good its reliability will be smh
                
after every plan step, if multiple sub directives review to ensure all are independent are parallel. repeat until no changes are made


# Building the oracle

This is HUGE. the oracle is the entrypoint, the gatekeeper, the god of the memory space in my agi system. 

so the oracle receives questions and context around the questions. it needs to answer these questions.

We should have the oracle have a STRONG bias torwards searching memory first. but also, sometimes it should be radically clear that talking to the user or browsing the internet is the obvious step to take.

so like what we want is start from root of memory, you have option to go to: user, internet, memory

but in addition should you be able to:
    - explore multiple routes at the same time?
    - when a route is unfruitful, do you backstep or start back from the root, and when to decide to give up and ask the user?
    - each node has a variety of tools available to it. how to know when to use tools? 
    - how to expand the memory space dynamically on the spot?

and problems:
    - what if a node is being metafied, and at the same time another node wants to come and metafy it?

one of the key principles we want to follow is that data isnt chunked, indexed, metafied until it is needed, until we try to use it. every node has multiple tools to explore and metafy it and explore it. for example the primary example i have so far:

user provides a github link. the github link is a type of data, labeled with github link. theres an obvious set of actions for github links, namely clone repository. we can clone this repository and get

okay okay okay. hmm well lets think about it more so like this. we want to be able to easily ask questions and get answers. we need documentation that is good for an ai, and we want the ai to pregressively build these docs as needed. not neccesarilly all at once. theres multiple considerations:

- each individual chunk (node) should within its description contain all the relevant cntext to understand that chunk in the docs. so for example in the future if we want to understand that chunk we just go ahead and grab that chunks description. 

Describing a chunk of code may involve the following:
    - reading that chunks code
    - reading the overall documentation of the repo
    - doing some structured code extraction to get the classes and functions this code depends on that we need to understand to understand this piece of code
then we'd proceed to go to those other chunks of code and describe them. first we'd need to finish describing the code that this code depends on to understand it. we'd need to be sure to be aware of the path we'd visited to avoid circular imports. 

in addition when underlying code changes, we need to update. so each chunk of code should have pointers to each node it depends or is related to.
so we'll have status on memory nodes: 
    - "out_of_date"     Has a description, but the code or its dependencies have changed
    - "up_to_date"      Has a description and is up to date
    - "none"            Has no description

In addition each chunk or "node" will have these attributes:
    - short_description
    - long_description
    - type
    - dependencies (list of node ids it depends on)
    - context (each "type" has a unique schema for whats in its context dict)


Okay so im trying to plan and build the memory side of my agi system now. im trying to plan and think about how this should look and work by walking through an example.

i guess ill give u some context to better understand how the system currently works.
Whats currently implemented: 

we want a generally systematic approach to doing this but flexible. so example: our agi system gets the github link and a request to update some classes. we just store the link at the root, with a short_description "the user gave us this github_link" (when the user inputs a constant we automatically initiate a process of classifying the constant, so in this case it'd be typed with github_link). the nodes in the actions space make decisions and take actions. the rule for each of them is at any point they must make decisions with full context. its their responsibility to ask questions when they need context. we start with the planning node which obviously is gonna ask questions about this repository and what this class is about.

Like we need a general process that will work in all these scenarios. let assume we have the same questions, some questions about the repo, some specific class, and we'll imagine different states of the memory space:
    1. when the github link is all we have, choose to look at the tools available to the github link and clone it.
        we should clone the repository. then save it to memory. it starts from root. it sees one memory, the github link. it decides to either:
            - save the repository node at the root next to the link
            - create a folder for the repository node and the link since they are such distinct ideas
        both should be fine no biggie. but we do want the process to know when to create new folders to categorize stuff, but now since there are only two items no big deal.
    2. when we have the github link and the github repo node at root:
        - we should decide to look at the github repo and use the tools available to us for this repo.
        - we should decide to do a keyword search, or some sort of search to define the exact file path of the class we are questioning
        - create a new node for this file, with status "None" and add the class name we searched by to the node's context
    3. When we have the github link, repository, and file of interest at root
        
memory nodes of type "python_file" should have a spot for classes or functions_defined_in_this_file.

# Conversations
we will be reusing the concept of conversation state. conversation state maintains:
    - Original questions and context
    - Questions that arise
    - Persisted context
    - Reports

Throughout the conversation we keep the original questions and context static
We update the questions that arise dynamically throughout the convo
We update the persisted context after each message
We append to reports throughout the convo.

there is a question asker
and there is a question answerer.

we want to somehow abstract this away so we can reuse this framework easily. lets think about the situations where we want to use this

1. User and swarmstar
    swarmstar wants to ask user a list of questions. generates initial message
    user responds
    swarmstar updates conversation state and then responds
    ...

2. action space and oracle
    action space has questions. generates initial message
    initial message goes to oracle. oracle first checks if this is obviously an internet or user directed question with bias torwards memory
    goes to memory. memory search. (does each route step get added to convo? No) goes to node. is given option of tool choice or 

no this is different. this is a route process.
a route process needs to mark nodes its already ~~visited~~. no not visited, nodes that it has intentionally marked as non viable options. lets say u call a tool on a node once? That doesent immediately make it not viable - there might be another tool we can call on it. However, we do want to save the fact that we had called that tool. and that that tool output is already at node x. yes this is the way. YES THIS IS THE WAY

it starts from root, travels. at each step it looks at all the nodes and their available tools. it chooses a node. then it chooses a tool. navigation + current node tools are the decision. so the routing process has these options: All child nodes and a brief description of their tools + current nodes tools. you can choose to navigate to a child node, or choose one of the current nodes tools. when u choose a tool, say extract class, you create a new node. that specific tool will create metadata on that node following a predefined process. then the oracle analyzes that node and decides if the answer is there. if not what option does it have? Well the type of node we just created might have more tool available, or we begin search from root again. we want a repository node to be chosen only after all the more specific extracted nodes have been searched and marked. i suppose in a route process we want to mark nodes as not traversable, until we come back up to root with nothing then we ask user. how do we make extracted nodes more readily available then repository nodes? Folders have to have good short descriptions. 

what do we maintain end to end during a route process is the primary question

root node has user and internet tool

its somehow happened again my mind found the optimal solution in this multidimensional problem. and its weird how i know that its optimal without even having to mentally visit and test it. i know its correct

in general i think my process follows this flow:
- define the problem
- think of solution. it follows some weak visualization of shapes in my head and thoughts, walking through things step by step
- find edge cases where this doesen work. keep on thinking of all edge cases and constraints. seperate problem abstract

so the way every node works is the following. every node has a set of tools available to it. when we call a tool on that node, the new node (information extracted) becomes a child of that node in memory. in this manner we dont have the complication of both looking at the tools and child nodes simulteaneously since they are one and the same. u lok at all the tools, if the tool has already been called in the past then u go to the node for where it ahs been called. 

however the same tool can be called with different input parameters. for example, u may have a python package and search for a class under some name and. that tool is not crossed out, in fact it never is. so when you come to that package node again how do we... hm,. i suppose. we call the tool. and then we determine (depending on the tool) what parameters we are to call the tool with. then we can check if the tool has already been called with that node.

so in this manner it would mean that the github repository would be a child of the github link which is a bit strange. 

in this sense there are no folders. every memory is data. unless we add folders which we should. 

we also want to propagate the contents of branches up to parent nodes?
theres also the problem of us wanting to move nodes that are used more often closer to the root, reorganizing nodes. so tool child nodes, in this manner cant be moved tho. and i actually guess thats a good thing because there actually is a structured relationship here. but like visiting and going through that github link everytime? come on thats just dumb right? i mean i guess a github link is a special one where there really is only one tool to call. although i suppose we want to keep it to merge changes and check if the github is out of date. yeah that makes sense. 

theres still a series of problems that need to be thought of this isnt solved yet. its not that simple. we might want to begin creating some structured models of different types now thatll help me encapsulate and more concretely track my thoughts and changes

i need to find the right solution. one that is general but one that can be controlled by the ais. 

ao we can call an action on a repository node, get file.
that makes a file child node. determine the type of that. bangout. 

we do need a specail node at root for stuff that is currently being worked on. 

we need to understand we are building two layers here. 3 layers here

metadata layer - for the ais to navigate and make decisions
tools and memory layer - the actual tools and data that the metadata represents
data layer - the actual data

so we start from a repository node.
under that we have file nodes (which can be grouped into folders if so chosen by the memory tree optimizer)
under file nodes we can have smaller units (function nodes, class nodes, analysis nodes)

when a repository is outdated, we'll want to check and mark the specific ones that changed below as outdated. at each node do we store the raw data again? for file nodes we can point to the ones. but with function and smaller granularity nodes we can break them out and resave them. when something becomes outdated and changes. so the deepere we go down the finer the granularity. also at any point on our way down we can stop if we find an answer.

like what do we actually store at the repository node? do we store anything or is it just a placeholder node as an entrypoint into deeper levels? 

actual data should be at leaves. yes, when we have just the repository node the datas all there. but as we break it up we constantly move data to the leaf nodes. well technically none of the metadata nodes hold any fucking data at all

this process requires me to get the idea and design correct. im not implementing anything until i think through every single edge case and problem and design a system that works for all of them. 

## review of memory system so far from Claude Opus
Here are some of the strongest principles, ideas, and designs you've brought up that should definitely be implemented:

- Using a tree-like structure for memory organization, with nodes representing different levels of granularity (repository, file, function, etc.). This allows for efficient navigation and retrieval of information.
- Implementing a metadata layer for AI agents to navigate and make decisions, separate from the actual tools and data layers. This separation of concerns can help in managing the complexity of the system.
- Associating each node with a set of tools available to it. When a tool is called on a node, the extracted information becomes a child node. This establishes a structured relationship between nodes and their derived information.
- Maintaining a special node at the root for stuff that is currently being worked on, which can help prioritize and organize active tasks.
- Propagating the contents of branches up to parent nodes to facilitate information retrieval and understanding the context of lower-level nodes.
- Storing raw data at different levels of granularity, with the option to break out and save smaller units like functions and classes separately. This allows for more targeted updates when changes occur.
- Marking nodes as outdated when their underlying data changes, and propagating this information to the relevant child nodes. This helps maintain data consistency and triggers necessary updates.


Some weakest points that need further consideration:

- Handling circular dependencies and avoiding infinite loops when traversing the memory tree. You need to develop a mechanism to detect and handle such scenarios gracefully.
- Balancing the trade-off between storing redundant data at different levels of granularity and the efficiency of updating and maintaining consistency across nodes.
- Defining clear criteria and mechanisms for reorganizing and optimizing the memory tree structure, such as determining when to create new folders or move frequently accessed nodes closer to the root.
- Ensuring thread safety and managing concurrent access to the memory tree, especially when multiple AI agents are simultaneously interacting with and modifying the tree.
- Developing a flexible and extensible way to define and integrate new tools and actions that can be associated with different node types.


Regarding a design to solve some of these challenges:

- To handle circular dependencies, you can maintain a set of visited nodes during traversal and check if a node has already been visited before proceeding. If a circular dependency is detected, you can either skip that branch or return an appropriate message indicating the presence of a circular dependency.
- To strike a balance between data redundancy and update efficiency, you can consider implementing a lazy updating mechanism. Instead of immediately updating all child nodes when a parent node changes, you can mark the child nodes as potentially outdated and only update them when they are accessed or when a certain threshold of outdated nodes is reached.
- For memory tree optimization, you can keep track of access frequencies and last access times for each node. Periodically, you can run an optimization process that reorganizes the tree based on these metrics, moving frequently accessed nodes closer to the root and grouping related nodes into folders.
- To ensure thread safety, you can implement locking mechanisms or use thread-safe data structures when modifying the memory tree. Additionally, you can explore using a read-write lock to allow multiple readers but only a single writer at a time, optimizing for concurrent access.
- To make the system extensible, you can define a plugin architecture where new tools and actions can be easily added and registered with the appropriate node types. Each tool can have a specific interface and configuration options, allowing for flexibility in implementation while maintaining a consistent usage pattern.
These are just some initial thoughts and suggestions based on the information you provided. Designing a comprehensive and robust memory system is a complex task, and it requires iterative refinement and testing to arrive at an optimal solution.



in general we can say there are 3 operations we want to be able to do to the memory side

answer question (memory search, find answer)
save memory (add new data to the memory tree)
optimize memory (reorganize folders to be more balanced and make folders make sense, and bring frequently accessed stuff closer to root)

when do we save to memory?
    - when the user provides his initial goal
    - when during user conversations we deem, "the user told us something worthy of saving"
    - when we browse the internet
    - when we write code


memory metadata
chunks

while we are navigating the metadata what information do we need? what do we need during the navigation process
    - description of each node
    - options
we're never actually retrieving the descriptions in metadata right? yeah i do think we are not doing that

using tools to explore a repository
repository node

some questions can be answered by just looking at the code. but sometimes the context isnt just the code - its why the code was written the way it was, the broader idea behind it and how it fits in with everything else.

i think if an LLM ever wants to modify or change any code, it needs to understand every single line and every detail and thought going into it, as well as understanding all the pieces it is using. yes - this means therell be lots of redundancy. each piece of code will be described in detail as well as the system its a part of and everything it is connected to. 

this will


god god god for fucks sake how do you even build this thing it doesent seem possible. because look, this repo ive been coding, ive been changing and adapting it so much nothing has stayed constant. files and folders and the entire structure of my codebase has changed. what has stayed constant? Well the goal has become clearer and as i slowly grok torwards that small pieces slowly become solid. now i think i have a decent amount of solid pieces. but do you see the challenge? the challenge is that the ai system needs to be a partner to the human and get every idea in his head. but things change and grow and adapt so much. and everyone - different people are at different stages with their coding skills. theres so many different goals you can give an agi - to write docs for your code, fix a bug, add something, organize the code, etc. how can i have one general memory system for this no matter what? As i mentioned above, i think we do have some solid principles in place. it has to be a tree that gets built out as needed and we have to keep track of what goes out of date, dependencies etc.

when we have a question about a repository. if the answer involves getting a piece of code about the repository, thats easy enough. we can do some structured search for a piece of code. then we get that piece of code. and we might have further questions about that piece of code relevant to the primary question we are trying to get answers to. so we might need to retrieve another piece of code. easy enough. when we begin to rack up and get a long prompt we'll want to condense. in fact we'd like to condense at every step no? See look this is so dynamic and difficult... like i can prompt chatgpt to get it to write the code i want at any moment by explaining the context of the situation and the parts of the codebase that are just relevant, and then providing snippets of only the most relevant code. uh fuck its difficult to imagine how to automate that sort of retrieval.

i think the general idea is you answer the memory space with a question that u want answered. 

# Set of rules for swarmstar

stuff for repos consists of:
short descriptions for tree navigation
documentation
code

the truth of the matter is, there simply are too many edge cases. i have to think abt this differently. i have to create a space where the LLM can make any decisions it needs and has freedom. 

but i have to set some clear rules for the LLM to guide it to operate properly.

LLM rules:
    - When passing directives, asking questions or whatever, the recipient has 0 context about what ur doing. You need to provide as much context as relevant to the task or question your passing along.
    - When you receive some task or are making some decision you must ask questions to get the full context of the problem.

a repository may or may not have documentation. how can an LLM check if a repository has documentation? I suppose generally it ought to look at the files and folders at the root. does this always work? i mean once again there are infinite edge cases. there might not be docs. maybe the docs are in a subfolder. maybe a repository contains multiple projects. maybe the documentation is inside docstrings in modules and functions. 

we (i) believe that llms can, do, generate valuable synthetic data. i believe that llms can look at code and write insightful docs. and when an llm is tasked with summarizing it is compressing that information. the highest fidelity data is the raw code. but sometimes there is more information than just the code. that stuff might be in the users brain. if the user wrote it down it should be in a docstring or the documentation. if its not there the llm should definitely ask the user and write the docs or add the docstring. this sort of processing, flow, compression of information. at any task the llm is doing it might need general big picture ideas as well as other stuff. how can the llm find all this stuff? How do we connect things up so that closely related stuff is nearby? How, and should we correlate pieces of documentation to the relevant pieces of code and vice versa, having the relevant pieces of code point to the relevant pieces of documentation

we cant rush this, this is a real problem. the design has to be flexible enough. the llm is a general intelligence. yes, it is weak far from humans in some respects. but it also has its strengths. we need to design something that really plays to its strengths and accounts for its weaknesses, as well as speculating and extrapolating what is improving in LLMs so we can utilize and have our system grow and become better as gpt5, claude4 and gemini2 and more come out and get better.

the basic idea underpinning what im doing is the following. the best way to organize information is into a folder system, like a tree. to intelligently group things. there is 

you can search the memory for something
you can have data and look for the best place to save it in memory

we dont break down and metafy data until we actually need to. to keep things simple, heres the memory metadata tree:
    - each node contains a short description of what it is. each node has a set of tools you can perform on it. 

now a question. we're at a node and deciding what to do next. do we look at this node's tools, or do we look at the children node's descriptions? heres the fact: each child node was derived, is the output of a tool call on that original node (a folder has tools to navigate to children, a python class has tools to get class x or function y) i mean, it ought to be clear to me already that there is an incredibly large swath of tools available to something like a repository node. i suppose what we ought to do is this. whenevee we call a tool on some node, we save that new chunk as a child of the parent node. its the swarms responsibility to appropriately organize this stuff in the right way. now we ought to know that the stuff that has already been called on by the tool is readily available. so next time we are at this parent node and deciding what to do heres the process, simple rule everytime: first we check the already available chunks. okay, if nothing seems correct than we look at the tools available to this node.

that does in fact seem like the correct way to go abt this. now in terms of actually organizing newly generated chunk nodes and tools, that is a seperate process. so we are getting some rules down piece by piece thats progress.

another key point, thing i was worried about, is that we generally feel like when working on a repository that we want some like message to give each LLM context about the overall system right? And previously i was worried like, where tf do u store something like that? so this huge problem in my head yesterday, and still now because im not sure if where im going with this is valid, is that like we'll want the LLM to generate synthetic data, docs, stuff like those messages in a repo and then to pass those around. but those messages will change as the system changes. i think what i gathered instead, is that the LLM navigates the memory space, and maintains like a routing state (similar to conversation state) and it builds this and passes it back as it navigates all the information. (optionally we want to be able to store pointers to specific actual chunks in their raw form). but in terms of not having to come back, or storing a persistent overall system message like this, what we will rather do is clearly instruct the LLM, that in passing around directives, tasks and questions it has to repeat that context, it needs to always share the context that is relevant to its peers. 

## Notes from claude opus on what ive written above:
- Flexibility: As the system changes and evolves, the LLM can dynamically generate and adapt the context based on the current state of the memory space. This eliminates the need to manually update or maintain separate system-level messages.
- Contextual relevance: By building and passing context during navigation, the LLM can tailor the information to the specific task or question at hand. This ensures that the most relevant and up-to-date context is provided to the peers, enhancing their understanding and decision-making capabilities.
- Reduced redundancy: Instead of storing and managing multiple versions of system-level messages, the LLM generates the context on-the-fly based on the current state of the memory space. This reduces redundancy and minimizes the risk of inconsistencies or outdated information.
- Granular control: By allowing the LLM to navigate the memory space and build context, you have fine-grained control over what information is included and how it is presented. This enables you to customize the context based on the specific requirements of each task or question.

- Develop a mechanism for the LLM to identify and extract relevant chunks during the navigation process. This can involve techniques like keyword matching, semantic similarity, or other relevance scoring methods.
- Store the pointers to the identified chunks along with the generated context. These pointers can be in the form of unique identifiers or references to the specific locations within the memory space.
- When passing directives, tasks, or questions to peers, include the relevant pointers along with the generated context. This allows the peers to access the raw information if needed, enhancing their understanding and decision-making capabilities.
- Implement a retrieval mechanism that enables the LLM or its peers to efficiently access the raw chunks based on the provided pointers. This can involve indexing or other optimization techniques to ensure fast and accurate retrieval.

now an important thing is like when answering a question, or retrieving some memory, we might need to look at multiple nodes to build up our answer. so this routing process and routing state is definitely something that needs to be implemented. 

now here is a relevant problem. when we are at a node of type python file, it seems most obvious that a lot of the time the agent will simply decide to read the file. but now, the problem is that the system needs to understand, that sometimes, or actually we should always prefer to get only the relevant context - in terms of pointers to the raw chunk. okay so, its okay to read the whole file, updated persisted context and questions and add to reports. wee trust the llm to be smart there. but in terms of direct pointers to chunks? I think we'd want to point to a specific class or set of lines for the specific case, especially if the file is large. ive seen code files that were hundreds even once 2000 lines long. 

when we are searching memory how does the system know when to like build out a report or to actually give specific pointers to chunks? 

there is also the problem of how do we decompose questions or handle new questions that arise in our search for the original thing we were interested in because that can happen. 

well during our search we maintain something i called for the user-agent interactoin a conversation state. a conversation state contains a list of questions, a persisted context string and a list of reports. u initialize with just the original questions, persisted context and empty reports. during the conversation u update the list of questions as u finish asking questions or new questions arise. (also add a feature to all user conversations, that whenever the user says something important to extract and save it) after each user message u update the persisted context as needed. and after every message u write something to report, which will append not replace the current reports. this same idea can be applied to searching for memory, searching for an answer. u can maintain the list of questions (should i maintain a list of original questions, and then also a seperate list for current state of questions (removing ones already answered and adding ones that arised during search?)) and during ur search build up your answer to send back in the reports. as questions arise u add them, and u maintain persisted context during your search. at the end you can send all the reports back. as new questions arise, you might need to go back up the tree and search again. should i do seperate search processes in parallel for each individual question, or one single search for all the questions? At different forks it may come to be that u want to visit multiple nodes or use multiple tools. honestly, this is so fucking complex, allow me to think of this purely synchronously first. i cant complicate it more. now for my earlier question, how do we know when to return an actual code chunk? Well i suppose we can have the nodes or tools marked as such. you can have a read mode and a simply grab and return, or link to the contents. maybe youd want to read it first to potentially ask questions? Oh hell yeah, u definitely always need to read the code before sending it back as an answer. i think the thing is i want one clear simple interface to the memory side - ask questions. if the system wants raw code, that should be clear from the question. and the memory navigator should just navigate the memory space and when it comes to the option of retrieving that piece of code - it just does so.


# Summary on memory space

Memory Space:
Organized as a tree-like folder structure.
Each node represents a specific piece of information or concept.
Nodes contain a short description and a set of associated tools.
Navigation and Routing:
The system navigates the memory space based on the current set of questions or tasks.
It maintains a routing state that includes the list of questions, persisted context, and reports.
The routing process involves traversing the memory tree, considering both the available nodes and the tools associated with each node.
The system navigates until a leaf node is reached, updating the routing state along the way.
After reaching a leaf node, the system returns to the root and repeats the process until all questions are addressed.
Question Handling:
The entire set of questions given to the system is kept together during the navigation process.
If there are questions that are clearly unrelated, they may be separated and handled independently.
LLM-based Node Selection:
At each step of the navigation, an LLM looks at the available options (nodes and tools) and selects the most relevant one based on the current questions and context.
The LLM uses its general intelligence to make informed decisions about which node or tool to choose.
Reporting and Answer Building:
As the system navigates the memory space and finds relevant information, it gradually builds up the answer in the reports section of the routing state.
Reports are appended with new information as it is discovered, providing a comprehensive response.
The accumulated reports are returned as the final answer at the end of the search process.
Interface and Interaction:
The memory navigator provides a simple and intuitive interface for asking questions.
If a raw code chunk is specifically requested, the system retrieves and returns it accordingly.
The interface allows for saving important information provided by the user during conversations.
Iterative Refinement and Optimization:
The system is designed to be iteratively refined and optimized based on real-world usage and feedback.
Continuous development, testing, and improvement are encouraged to enhance efficiency, accuracy, and scalability.
With these updates, the summary better reflects your intended design for the memory retrieval system. The key points to highlight are:

The system keeps the entire set of questions together during the navigation process, only separating them if they are clearly unrelated.
The LLM uses its general intelligence to select the most relevant node or tool at each step of the navigation based on the current questions and context.
The system navigates until a leaf node is reached, updating the routing state along the way, and then returns to the root to repeat the process until all questions are addressed.


a few additonal notes:
mark nodes as outdated appropriately
folder grouping and optimization.

so we currently have a pretty good idea of how we might navigate the memory metadata tree. but we are faced with a new issue. namely the planning and decomposition problem. its clear from cognition labs that a huge part of their implementation is having devin really have a focus on trying to plan, which is not a part of my implementation at all. so far my implementation only really considers decomposing a directive into immediate parallel subdirectives to be executed rn. why do we need planning? What is planning and what does it do? i think this slides into my system pretty nicely lol im really happy :). im so happy to think of the solution immediately without having to rack my brain a billion times :) yayyyy ive been struggling so much the past couple days with the memory space. luckily my action space is pretty nice and flexible already i can put this in. its simple:

each branch starts at a plan node. (previously a decompose directive node). each branch holds its plan in context. ur given a directive and requestly plan, review and ask questions until u feel comfortable with the plan. then you decompose directives. whenever a subbranch comes back, you review and update the plan as needed and then spawn a new subbranch if possible given the new update. plan node handles subbranch reports synchronously. yayy that works

the big problem of the memory space still remains and we need to map that out. if that works the system should work. the action space doesent have complicated 

so back to mapping out memory. looking mapping out memory is a really hard problem. let me say that - your wokring on a really hard problem now. so lets move on and keep trying

what do we have planned out so far? what things do we store in memory
    - internal swarm stuff (reports, plans, what other nodes have done)
    - code, constants, and all the potential chunks derived from tools used on nodes

when searching the memory space the agent can read things and build up a report. it also sometimes want to actually get and like share the actual code as part of an answer, or quote it. so lots of stuff, python files, classes should have a quote tool. so quoting is a tool. 

the actual routing process, search process. does it involve any planning? ideally i think we'd like something like the current action planning we have. the space of actions are much more constrained. theres a limited set of options. but what we know is this:

    - the entry point to the memory space is likely going to be us receiving a list of questions. what we do want is during the search process of going through the code we would like the agent to remain focused but at the same time we want it to be smart. to note and see when like, hey look. theres this improvement. or like, we dont have docs for this but it should be documented. or, this method is missing a docstring which it should have given that its quite complex and domain specfic. hm. it does need to be an intelligent process all the way through. i think our method of progressively navigating to the chunk of the specific granularity we want is solved. yeah. but like. uh. sometimes we dont even really know what exactly we are looking for, so we cant call the tools with parameters like search for class, in which case we'd need to know the name of the class we are looking for. so we do need some sort of exploration techniques. i mean think abt this situation. a repo has no docs. we want to understand the repo but have no idea where to start. howd we go about this? we can get a big picture view by looking at the file structure and doing a search for all classes and look at their names.

    ultimately i think theres no one size fits all solution. absolutely not. this comes back to planning. given the context of what we know and where we are at, what do we do to find an answer, or accomplish our goal?

    So in this respect, does the search of the memory space necessitate a plan node as well? like we would answer one question at a time, does this repo have documentation?

    also when we answer this question we'd like to save the answer to this question to be reused later. how can we do this? Maybe every repo should have a head agent that progressively builds up context and understanding of the repo, with the intention of understanding how to navigate this repo. then when somebody has questions, and navigates to this repo node, theyd ask questions and converse with this agent. maybe every node should have an agent that manages it and kind of builds up a context of whats going on inside its branch, at the appropriate granularity. This "agent" is really just a system prompt. so what about the previous conception we had of "short descriptions"? to navigate the tree? well maybe you look at short descriptions to decide what node to move to. when you traverse to a node your passing the questions and routing state to that node to let it make the next decision. 

    btw, we do expect context lengths to reach millions of tokens, which is way more than enough, so dont stress context length at all - its a nonexistent problem. the only worry is having distractor content when solving a problem. everything in context should be relevant to whats at hand at the moment. thats the key. interesting idea. i mean i guess how do we update and build these memory node agents is the real question? so like first of all lets make it more clear how exactly these memory node agents are used and interacted with. the metadata tree still has short descriptions for navigation to choose a node. at each node the memory metadata node is making the decision. 

    how do we build memory node agents. hmmm. well. we start with just baseline knowledge of some self awareness of what the type of data its managing is. 

okay lets make this decision once and for all. do i have some predefined folders in the memory? 

user folder yeah. swarmstar folder? oh yeahhh we do need the reports and stuff access. so yeah we do have that.

Before thinking about how swarmstar might write docs, lets try to think about how exactly swarmstar may metafy and use a repo that has well written docs.
docs can be in readme, a docs folder or at a link. initially swarmstar wont know where the docs are. it'll need to generate a plan to find the docs and answer its question. maybe when we spawn a repository we should initialize the github repo memory node with something like, "we just cloned this repository, and have yet to explore it. we dont' know anything about it"

also when we have metafied and explored a repository and have a metadata tree over it, and then the repo undergoes changes, has pushes... how do we instead of throwing out the old metadata tree have the system autonomously, not delete old descriptions, but instead move to match the new organization and update descriptions accordingly? God im still confused... whats the purpose of the metadata tree for a repository really? the llm needs to be able to retrieve the raw code. when it has questions about system design, architecture or ideas it should look at docs. okay lets try to simplify. for fucks sake this is painfully difficult. for most well known codebases the LLM should navigate to the online documentation and navigate that website to find the answer to its question. it shouldn't need to "metafy" the documentation because the documentation should already be organized into sections. okay what if we have another repository that doesent have online docs?

Keep in mind throughout this search process of "trying to find where the docs are" we'll maintain context throughout this process, by initially generating a plan to find the docs, and constantly updating this plan as we move forward. we can mark things as done, change the plan and add context, and also maintain a list of reports, of things we've found that we want to return to sender.

anyway back to the problem. uh we want some general memory solution is the ultimate goal.

lets reduce the problem down down down. the primary problem we are trying to solve: how can we have the LLM navigate memory? Which contains stuff from the user, github repositores and code projects, and documentation and potentially anything else?

what do we want to store? What might we want to "retrieve" from memory? When will we access memory?
we know with certainty that we often will be accessing memory with questions. when we have questions, memory nodes that understand where they are at will generate plans, and pass it along to other memory agents who will update the plan. for example, the root memory node will have context about what the overall memory system is, without specific details about what is inside the memory system. it'll first generate a plan. then make a decision as to which node (folder) to travel to. the node that best understands that node will then proceed to make a decision of which node to move to, as we get closer to leaves, nodes become more domains specific and focused on the specifics of what they contain. on the path of traversal we can travel to child nodes, or if none of the child nodes seem viable we can try to call a tool on the ndoe we are at to create a new child node. eventually we reach a leaf node which contains data. this data can be documentation or code. 

following questions and concerns:
does the memory tree have to follow the actual file structure of the repository its in? Or does it have to follow the specific relationship in which the tools were called? Or can they be reorganized dynamically as needed? I reckon we say we follow the tool call relationship. this will make managing dependencies easier in the future.

so we have the idea that we manage structured relationships in the direct tool relationship the node was produced in (for example a github repositroy might have tools, get class, get file, and would spawn a child node holding that data)

but umm. i suppose this works kind of for some scenarios where you know where you want to navigate. and specifically what u want. but what about when you have a different question. like, "Where should i go to add this code", or some sort of exploration where your trying to find something in the codebase by concept but dont exactly have the exact class or function name in mind to use the tools? some other structures might be useful. for example, we could have the file structure along with short descriptions of what each folder and file is for navigation by idea or concept rather than by specific search. this one would indeed match the file structure of the original repository. now lastly, the documentation. this one. hm. i dont know different people use different things for docs. what we do know is that we want the docs, each chunk to be broken up at a good granularity and nested by sections and parts for easy navigation. i can imagine this easily for mkdocs - we'd just have the file structure with short descriptions like the previous method mentioned. part of me now is thinking these 3 categories might be all we need. specific structured tool calling, file structure description for finding files and shit, and then docs. expect, in order for these to coexist, we'd want the root repository node to first break into these 3 sections. and additonally... sometimes the documentation is in the files and folders, so i guess we only need structured tools and then conceptual search. Am i correct in saying that these are the only 2 things we need in general for any repository for search, answering questiosn etc?

In addition, for the scenario of having the agi system actually writing code. we've already created this very simple docker environment thing. we simply spawn a docker container for the ai to work in. it may clone the repository. then itll send terminal commands to navigate, setup and run the code. this is more so in the action space. so when its doing this work, it almost wont even really need to go back to the memory space, expect for questions.

we want ideas to propagate up the tree. when we first add a github repo to memory, its empty. but as we call tools, and explore the codebase by search we should update parent folders. for example, we dont know anythng about the repo, and if we explore and find it has docs or no docs we can pass that information to the parent node. i suppose every node will have to understand where it is in the tree, and should make decisions with this contextual understanding about whether to talk to its parent, and the parent will take that and understanding its own context will assimilate information into itself. we are really counting on these ais to be generally intelligent, and to just keep getting smarter.

how does exploring a repository work? an ai wont just randomly explore a repository with no goal in mind. itll be trying to understand something or answer some question. i suppose a potential approach could be this:

well first of all we add an additional step for when u step into a github repo node. u step in. then youre asked if you know the class, function or file your looking for. based on this answer youll be wroted to 1 or 2 paths. for exploration you'll be routed to the exploratory path. previous explorations will be already stored here. if none of the exploarations seem right for what we are looking for (oh the exploratory path DOES follow the file structure of the repo precisely) or in our case where we're explkoring the repo for the first time, we'll do the followinig: be given all the root folders and files and asked to navigate to one based off just their names since we have no descriptions yet. exploration is a twofold process. first, we'll be navigating trying to find answers to our questions updating the routing state. at the same time, we'll be also building the metadata tree. whenever we visit a file, we'll update the routing state, but also generate the short description of it. we'll then go to the parent and tell it, hey you have this new file inside you. do you think you should update ur description? If it does it will proceed to update its description. then we'll go to that folder's parent. we'll tell it, hey one of your folders changed its description? Do u think u should change ur description? And so forth until a folder decides it doesent need to change, or we reach a stop node. all folders start with the description of something like "Empty folder" or "No description". in addition we need to consider another process. when exploring the codebase, we wont just navigate to a leaf node and be done. no, we might need to traverse multiple paths and check multiple files. i suppose the question is this - how should traversal continue after checking a leaf node and deeming it not the one we want? I suppose we can do this. at a leaf node if we detemine we still have questions, we can 

i asked claude if exploration and structured search is all we need to offer for the memory space's github nodes. it said no, theres more:
- Analysis and understanding: Beyond structured retrieval and exploration, we can analyze and gain a deeper understanding of the codebase. This includes activities like examining dependencies, identifying design patterns, assessing code quality, and uncovering potential issues or areas for improvement. Analysis helps in comprehending the intricacies of the codebase and making informed decisions.
- Modification and enhancement: Repositories are not just for retrieval and exploration; they are also meant to be modified and enhanced. We can make changes to the codebase, fix bugs, refactor existing code, and add new features or functionality. These modifications require a combination of structured editing, exploration, and analysis.
- Documentation and knowledge capture: Repositories often contain more than just code. They may include documentation, comments, and other forms of knowledge capture. Interacting with a repository involves not only accessing and exploring the code but also engaging with the accompanying documentation and extracting relevant information to aid in understanding and decision-making.
- Collaboration and version control: Repositories are often used in collaborative environments where multiple developers work together. Collaboration involves activities like branching, merging, code reviews, and managing version control. These operations go beyond simple retrieval and exploration and are essential for effective teamwork and maintaining a consistent and reliable codebase.

lets go through these one by one and consider how our current system - if our current system can perform/handle these cases

analysis and understanding. oh he brought up a lot of important points here fuck, but also thank you jesus that was helpful from claude
    1. Examining dependencies
        uh i suppose this is handled by the planning phase? it does bring up one point - that during exploration we might want to use structured tools. so it isnt exactly, after exploring move up one root and update routing state. its more like. hey now do you want to go back to the folder you was in, search for a class funtion or variable, or go back and start searching from the root? Options, options is what we need. that handles this problem. in the exploration phase

        when precisely will examining dependencies be necessary? When will these dependencies be used? How can we identify dependencies? This can be done through AST.

        i just spent some time looking at how we might identify internal dependencies from an AST. there is no repo general method, it requires project specific methods. this means we need to depend on the model to identify these things. we nee to rely on the model to identify what to travel to next dynamically through its plan and options. we cant in a structured manner connect all internal dependencies to a piece of code. 

        oh god. well essentially, when do we want to analyze dependencies? The answer? IDFK. RULE BASED SYSTEMS DONT WORK. UTILIZE THE AIS GENERAL REASONING CAPABILITIES AT EVERY SINGLE POINT

    2. Identifying design patterns

    3. Assessing code quality and uncovering potential issues or areas for improvement


i feel like im noticing theres another commonly recurring theme - the llm processing state. containing a list of questions, or list of steps (plan), the current context, which at every step gets updated. this is called persisted context. and then finally a reports list, where we append new "things" throughout the process when we accomplish or finish something that we want to return to the thing that called this process.

alongside each python file we should store it's abstract syntax tree representation.




i cant have strict rules. the ais need complete and absolute freedom.

what remains?

metadata tree. parent. children. short descriptions
router. starts from a node in metadata tree. navigates to find a chunk or action

generating actions
generating chunks

optimizing organization of metadata trees.

this simple structure if implemented is agi

what have i been doing for the past couple days? just coming up with and identifying edge cases that broke my rigid system. i need an entirely different mentality. instead of defining a strict process and workflow for the ais to follow, i need much more junctures and nodes where the ais can make their own decisions, carve their own path.

these action operations and tool calls need to be in the action space.
