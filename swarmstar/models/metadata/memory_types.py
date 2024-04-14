from enum import Enum

class MemoryType(str, Enum):
    # general types
    REPOSITORY = "repository"
    FOLDER = "folder"

    # constant strings
    GITHUB_LINK = "github_link"
    OPENAI_KEY = "openai_key"

    # file types
    JSON = "json"
    CSV = "csv"
    MARKDOWN = "markdown"
    PYTHON = "python"
    JAVASCRIPT = "javascript"

    # specific python types
    PYTHON_CLASS = "python_class"
    PYTHON_FUNCTION = "python_function"
    PYTHON_VARIABLE = "python_variable"

    OTHER = "other"


memory_type_to_tools = {
    "repository": [
        "find_file", 
        "find_class", 
        "find_function", 
        "find_variable",
        "find_string"
    ],
    # But its not this simple...
    # Depending on the state, we might want to clone to read it
    # Or clone to be able to write to it and make changes
    "github_link": [
        "clone",
        "pull",
        ""
    ]
}

