# Python script to convert multiline text into a single line string with \n and quotes for JSON

def convert_to_json_string(multiline_text):
    # Convert multiline text to a single line string with \n for new lines
    single_line_string = multiline_text.replace("\n", "\\n")
    # Add quotes around the string
    json_string = f'"{single_line_string}"'
    return json_string

# Multiline text to be converted
multiline_text = """"""

# Convert and print the string for easy copying
json_string = convert_to_json_string(multiline_text)
print(json_string)
