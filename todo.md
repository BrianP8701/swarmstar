# TODO List

## 12/23/23 - 1/18/24
- [x] have swarm write github wrapper
- [x] Create user assistance agent and integrate with python coder and manger (router is simpler, just has user choose next action instead of the complex interaction with the user assistance agent)
- [x] Add initial python script tester agent
- [ ] Add terminate algo
- [ ] Add web scraper
- [x] Add place to hold documentation
- [ ] Get v2 run to work in all components
- [ ] Change descriptions in node_scripts
- [ ] Remember theres a temp stitch in break_down_goal with is_parallel cuz im not sure how to handle it yet
- [ ] Fix snapshot save its not working
- [ ] Add system to download dependencies. Add dependency requirements to each script, chunk of code etc
- [ ] Line 54 in agents.json enum shit
- [ ] Create custom namespace for task handler

So a lot of the goals outlined above have actually been rendered irrelevant because ive changed the architecture and inner workings of the swarm so much. im just gonna renew the todo list below

## 1/18/24 - 
- [x] test manager
- [x] integration test
- [x] add handling for termination in core
- [x] change all node executions to output report and lifecycle_command instead of just "output"
- [x] add manager_supervisor agent
- [x] integration test with termination
- [ ] add action router
- [x] define all pydantic schemas and integrate them in the swarm architecture
- [ ] get new swarm architecture working locally across the entire lifecycle of a swarm
- [ ] automate the process of manually adding swarm actions
- [ ] create action creator
- [ ] use new swarm architecture to add all cloud storage and file storage operations
- [x] decouple and make core stateless
- [x] make node ids uuids
- [ ] add consistency for read-write operations to swarm space
- [x] revert memory and action space to have a seperate tree representation for metadata.
- [x] add configuration for coder layer with data sources and custom router functions
- [x] add pydantic models to action space
- [x] replace all tools with instructor
- [ ] make executor do validation
- [ ]
- [ ] build memory space
- [ ] add config functions to add custom data to memory and action space
- [ ] test with multiple enviroments
- [ ] create web app interface for swarm with user input to threads
- [ ] add retrieval agent
- [ ] have swarm add more specifc file operation actions
- [ ] have swarm add github actions
- [ ] add multi platform support for autonomous package installation between swarm frames
- [ ] action space merging
- [ ] platform interoperable user interaction
- [ ] autonomous action/memory space optimization
- [ ] visualize the memory and action space
- [ ] visualize the swarm state and history
- [ ] ensure consistency in operations that write to swarm space
- [ ] add feature to pause and resume the swarm
- [ ] allow devs to implement their own env configuration

Cloud Optimizations:
- [ ] in cloud functions decouple blocking openai calls. decouple all blocking calls in cloud functions. or look into durable azure functions
- [ ] consider sql for some data

User input needed at:
- aga_swarm/actions/swarm/manager/manager.py
- all action types (when missing a config var)