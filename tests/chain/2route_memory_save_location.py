"""
Finding where to save a chunk of data to memory

prompt: choose_folder + current_folder_description + child_folder_descriptions + string_of_data_to_be_saved

No questions



Root folder simply just starts with a user folder

when passing in data to save pass:
actual memory id of the chunk being saved (mongodb id)
string of data. (if its already a string pass it. but i mean if its a constant, image, table etc we pass a description of it + the memory id)

If the data is from the user prepend: "The user wrote this:"
if overaching goal prepend: "This is the overarching goal the user told us they want accomplish: "


we stop navigating to find a place when we reach a leaf folder or when we think there is no appropriate folder to save the data to given the options
"""
from swarmstar.utils.ai import Instructor
import asyncio

from typing import Optional
from pydantic import BaseModel, Field


instructor = Instructor()

# When finding place to save memory, no questions can be asked
class Model(BaseModel):
    folder: Optional[int] = Field(None, description="The index of folder to save the data to. None if no folder is appropriate.")

system_prompt = """
You have to save the given data to memory. This is a general prompt that is used on all types of data.
The memory is a file/folder system, like a tree. You need to navigate to the best location and save the data.
You'll be given a description of the folder your currently in, and decriptions of direct child folders. Choose the best folder to navigate to.
If none of the folders seem appropriate, choose None
"""

current_folder_description = "Current folder: This is the root folder of the memory system."

child_folder_names = ["user"]
child_folder_descriptions = ["Data related to the user. Strictly for stuff stuff that is explicitly from/about the user. Only save stuff here if the word 'user' is explicitly mentioned."]

child_folder_descriptions_string = ""
for i in range(len(child_folder_descriptions)):
    child_folder_descriptions_string += str(i) + " " + child_folder_names[i] + ": " + child_folder_descriptions[i] + "\n"

data_to_be_saved = """https://github.com/BrianP8701/swarmstar"""

message = system_prompt + "\n\n\n" + current_folder_description + "\n\n" + child_folder_descriptions_string + "\n\n" + data_to_be_saved

messages = [{"role": "system", "content": message}]
output = asyncio.run(instructor.completion(messages, Model))

print(output)









output_string = output.model_dump_json(indent=4)

txt_file = '/Users/brianprzezdziecki/swarmstar_world/swarmstar/tests/history.txt'

with open(txt_file, 'w') as file:
    file.write("\n\n\n\n\n\n" + message + "\n\n" + output_string + "\n\n\n\n\n")

