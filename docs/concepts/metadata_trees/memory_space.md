# Memory Space
This is where the swarm stores it's memory. Memory contains:

- Logs, reports, directives and context from swarm nodes
- Information from and about the user
- Internal swarmstar documentation
- Work produced by the swarm
- Information scraped from the internet
- ...

Memory is accessed whenever a question is asked. If answers can't be found, another method will be used. Talking to user, browsing web etc.

## Data Models
Memories can be stored anywhere. We have a memory metadata tree, in which leaf nodes (memories) will be labeled with a "type". Each "type" has it's own handler functions. Thus, we have a singular memory metadata tree to organize data and search over, but can store our data anywhere.

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

| Attribute     | Description                          |
| :-----------  | :----------------------------------- |
| `id`          | UUID to identify in MongoDB  |
| `is_folder`   | True if folder, false if data |
| `type`        | Differentiates how to retrieve and use memory, where it is stored or whether the memory is internal or external.  |
| `name`        | Human readable name |
| `description` | Description of folder or data. Used by LLMs to find data and to organize the memory space. |
| `parent`      | id of parent node |
| `children_ids`| List of children ids |
| `context`     | Each type will has a defined schema that will be stored here |

### Memory types

| Memory type         | Description                                   |
| :------------------ | :-------------------------------------------- |
| folder              | Folders that are created by the swarm or user |
| internal_folder     | Default immutable folders                     |
| project_root_folder | Marks the root of a project. When using this project, the entire branch starting from this node will be migrated to a docker container |
| project_file_bytes  | A file stored as bytes in MongoDB. This file is a part of a project |

#### Memory type context schemas

```yaml
folder:

internal_folder:

project_root_folder:

project_file_bytes:
  file_path: "Where to place the file in a docker container when using the project"
```
Some memory types don't utilize context.

## Internal memory space
By default the memory space has these 4 folders:

### swarmstar
This contains data specific to the swarm. Logs, reports, directives and information about nodes. The overarching plan and directive at any moment. Documentation about how things in the swarm works for LLMs to make better decisions. 
### user
This contains information about the user, as well as the raw conversations we had with the user. For example it contains a user_preferences.md file that we can refer to determine whether or not to get the user involved (It'll describe how much the user wants to be involved, what they want to be involved in, their background etc). In addition it'll contain a requested_features.md, user_requirements.md file and more.
### projects
Each "project" is a software project. It can be anything, ranging from small scripts, a python package, a clone of some github repository or a web app. 
### references
Here we store any documentation and code we scrape from the internet that's related to our projects or goal, data etc.
