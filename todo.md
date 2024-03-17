# TODO List



# 3/14/24 - 
- [x] create containers and utils for swarm to create environments and execute code, create terminal sessions
- [ ] Implement the timer functionality to kill inactive containers and optimize resource usage.
- [ ] Set up a system to propagate code changes from MongoDB to active terminal sessions.
- [ ]
- [ ] web host frontend, deploy backend to serverless
- [ ] share constants
- [ ] metafy repo/data
- [ ] add swarm memory to ui
- [ ] add sequential plan to decompose directive node
- [ ] upload files/folders in ui
- [ ] constant chat in ui
- [ ] history slider in ui
- [ ] edit swarm in ui
- [ ] step mode in ui

Actions to implement:
- [ ] action creator
- [ ] route question
- [ ] route failure
- [ ] find constant
- [ ] save constant
- [ ] write tests
- [ ] write code
- [ ] get text from web
- [ ] get answers from web

Utils to implement:
- [ ] abstract syntax tree parsing functions (abstract interface then python implementation)
- [ ] various external data apis (github, gmail, google docs etc)
- [ ] search apis
- [ ] web scrapers
- [ ] 

## 1/18/24 - 
- [x] test manager
- [x] integration test
- [x] add handling for termination in core
- [x] change all node executions to output report and operation_type instead of just "output"
- [x] add manager_supervisor agent
- [x] integration test with termination
- [x] add action router
- [x] define all pydantic schemas and integrate them in the swarm architecture
- [x] get new swarm architecture working locally across the entire lifecycle of a swarm
- [ ] automate the process of manually adding swarm actions
- [ ] create action creator
- [half did this?? i did it manually. impossible to have swarm do stuff without thes operations] use new swarm architecture to add all cloud storage and file storage operations
- [x] decouple and make core stateless
- [x] make node ids uuids
- [x] add consistency for read-write operations to swarm space
- [x] revert memory and action space to have a seperate tree representation for metadata.
- [x] add configuration for coder layer with data sources and custom router functions
- [x] add pydantic models to action space
- [x] replace all tools with instructor
- [x] make executor do validation
- [x] decouple openai calls from actions
- [irrelevant] add ACI spin up for external python functions with different dependencies
- [x] build initial memory space
- [ ] add config functions to add custom data to memory and action space
- [ ] test with multiple enviroments
- [x] create web app interface for swarm with user input to threads
- [ ] add retrieval agent
- [ ] have swarm add more specifc file operation actions
- [ ] have swarm add github actions
- [irrelevant] add multi platform support for autonomous package installation between swarm frames
- [!!!] action space merging
- [x] platform interoperable user interaction
- [!!!] autonomous action/memory space optimization
- [!!!] visualize the memory and action space
- [x] visualize the swarm state
- [x] ensure consistency in operations that write to swarm space
- [x] add feature to pause and resume the swarm
- [ ] allow devs to implement their own env configuration
- [ ] have swarm fill in util space metadata
- [ ] have swarm fill in util space consumer metadata
- [x] correct all swarm updates and spawn operation
- [x] add choice for user to customize question router mode... add question route first
- [ ] add python coder
- [ ] add python code tester (this gets a lot more complicated)
- [x] differentiate between actions meant to be routed to and actions that are not supposed to be callable by action router
- [ ] add slider and stuff to see the swarm state's evolution through time
- [ ] add options to choose mode to view swarm tree (directive box, or not, other options etc)
- [x] make node logging use append to list with versioning instead of update_node

Cloud Optimizations:
- [x] in cloud functions decouple blocking openai calls. decouple all blocking calls in cloud functions. or look into durable azure functions
- [ ] when cosmosdb python sdk supports it, use hierarchical partition keys: user_id/swarm_id/category with id for query
I think i might use mongodb atlas instead of cosmosdb so this might be irrelevant
Serverless Framework Plugins: If you're using the Serverless Framework to deploy your Azure Functions, there are plugins like serverless-mongodb-atlas that handle connection management for you. These plugins create a singleton database connection that's reused across all function invocations.


## 12/23/23 - 1/18/24

################################# Irrelevant old goals ###################################################################################################
- [x] have swarm write github wrapper
- [x] Create user assistance agent and integrate with python coder and manger (router is simpler, just has user choose next action instead of the complex interaction with the user assistance agent)
- [x] Add initial python script tester agent
- [half did this? Termination is a lot more complex than i initially thought] Add terminate algo
- [ ] Add web scraper
- [x] Add place to hold documentation
- [ ] Get v2 run to work in all components
- [ ] Change descriptions in node_scripts
- [ ] Remember theres a temp stitch in break_down_goal with is_parallel cuz im not sure how to handle it yet
- [ ] Fix snapshot save its not working
- [ ] Add system to download dependencies. Add dependency requirements to each script, chunk of code etc
- [ ] Line 54 in agents.json enum shit
- [ ] Create custom namespace for task handler
################################# Irrelevant old goals ###################################################################################################
So a lot of the goals outlined above have actually been rendered irrelevant because ive changed the architecture and inner workings of the swarm so much. im just gonna renew the todo list below