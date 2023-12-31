# agents.json
Tool schemas are designed for OpenAI LLM function calls, guiding the LLM to produce JSON strings in a predefined format. This structure prompts the LLM to output data that aligns with specific requirements.

File Schema:
The value corresponding to each agent name is the format for tools in OpenAI ChatCompletions API
{
    agent_name: {
        instructions: str,
        tools: [
            {
                type: function,
                function: {
                    name: str,
                    description: str,
                    parameters: {
                        type: object,
                        properties: {
                            variable_name: {
                                type: str,
                                description: str
                            },
                            ... more variables
                        }
                    }
                }
            },
            ... more tools 
        ]
    },
    ... more agents
}

So far, I believe I will only be allowing every agent to have one tool. I have reasons for this in my subconscious, but I can't quite articulate them yet.

# node_scripts.json
Swarm scripts are stored as strings to allow for automated self-extension. This matches LLMs' string output, enabling the swarm to autonomously develop and enhance its functionality.

File Schema:
{
    agent_name: {
        script: str,
        description: str,
        language: str
    }
}

# node_scripts.py
This file just contains the scripts from the node_scripts.json file, but in python format. For readability and maintenance purposes.

# synthetic_code.json
This file contains code written by the swarm.

File Schema:
{
    code_name: {
        language: str,
        code_type: str,
        code: str,
        description: str
    }
}

