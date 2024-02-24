def get_lines(file_path, line_range):
    """
    Extracts code from a file given a range of line numbers.

    Parameters:
    - file_path: str - The path to the file from which to extract the code.
    - line_range: tuple(int, int) - A tuple containing the start and end line numbers.

    Returns:
    - str: The extracted code as a string.
    """
    start_line, end_line = line_range
    extracted_code = ""

    with open(file_path, "r") as file:
        for current_line_number, line in enumerate(file, start=1):
            if start_line <= current_line_number <= end_line:
                extracted_code += line
            elif current_line_number > end_line:
                break

    return extracted_code
