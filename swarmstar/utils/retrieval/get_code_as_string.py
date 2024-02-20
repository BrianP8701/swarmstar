from swarmstar.utils.retrieval.ast_chunking import find_class_start_end_lines
from swarmstar.utils.retrieval.get_lines import get_lines

def get_class_as_string(file_path: str, class_name: str) -> str:
    """
    Extracts the code for a class from a file.

    Parameters:
    - file_path: str - The path to the file from which to extract the code.
    - class_name: str - The name of the class to extract.

    Returns:
    - str - The extracted code as a string.
    """

    # Find the start and end lines of the class
    start_line, end_line = find_class_start_end_lines(file_path, class_name)

    # Extract the code for the class
    class_code = get_lines(file_path, (start_line, end_line))

    return class_code