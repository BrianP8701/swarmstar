# Memory Space
This is where the swarm stores it's memory and where it goes to find answers to it's questions.

## When do we use the memory space?
Some examples of things memory contains:
- Logs, reports, directives and context from swarm nodes
- Information from and about the user
- Internal swarmstar documentation
- Work produced by the swarm
- Information scraped from the internet
...

While executing swarm operations, if an AI ever asks a question it will be directed to a question router. The question router will determine whether we should search the memory space, ask the user, browse the internet or use some api like Github to retrieve information. However, it will be urged to have a bias torwards checking the memory space first, as we'd prefer to not bother the user, and we'd like to check if our memory already has the answer before browsing the web.

## Data Models
Each "memory" is labeled with metadata to allow an LLM to traverse the memory space, which is organized as a tree, like a folder system.

<span class="pathname">swarmstar/models/memory_metadata.py</span>
``` py
class MemoryMetadata(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: generate_uuid('memory'))
    is_folder: bool
    type: Literal[
        "folder",
        "internal_folder",
        "project_root_folder",
        "project_file_bytes",
    ]
    name: str
    description: str
    parent: Optional[str] = None
    children_ids: Optional[List[str]] = None
    context: Optional[Dict[str, Any]] = {}
```

| Attribute   | Description                          |
| :---------- | :----------------------------------- |
| `id`        | UUID to identify in MongoDB  |
| `is_folder` | True if folder, false if data |
| `type`      | Differentiates how to retrieve and use memory, where it is stored or whether the memory is internal or external.  |
| `name` | Human readable name |
| `description` | Description of folder or data. Used by LLM to navigate and find data and to organize the memory space. |
| `parent` | id of parent node |
| `children_ids` | List of children ids |
| `context` | Each type will has a defined schema that will be stored here |



## Internal memory space
By default the memory space has 4 folders:
- swarmstar: This contains data specific to the actual swarm. Logs, reports, directives and information about nodes. The overarching plan and directive at any moment. Documentation about how things in the swarm works for LLMs to make better decisions. 
- user: This contains information about the user, as well as the raw conversations we had with the user. For example it contains a user_preferences.md file that we can refer to determine whether or not to get the user involved (It'll describe how much the user wants to be involved, what they want to be involved in, their background etc). In addition it'll contain a requested_features.md, user_requirements.md file and more.
- projects: Each "project" is a software project. It can be anything, ranging from small scripts, a python package, a clone of some github repository or a web app. 
- resources: Here we store any other miscellaneous information that doesen't fit in the other categories. Documentation and code we scrape from the internet that's related to our projects or goal, data etc.




## Memory types
