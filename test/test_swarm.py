goal = '''
    We want to autonomously prospect potential clients for a real estate agent using the ChatGPT API
    We have csv files with expired listings, peoples names and their phone numbers. Create a full fledged system to prospect these people.
    First, we need to take filters from the real estate agent to narrow down the list of people to prospect.
    Then, we need to send an initial message to each person on the list to their phone number. I'll give you a template for the message.
    Then we need triggers to send follow up messages to people who respond to the initial message.
    We want to continue the conversation and continue to gather relevant information about the person pertaining to their real estate needs.
    We need to save and extract structured data from the convo to a database. I'd like to use GCP.
    We'll also want to be able to alert the agent when a person is ready to call, or when a person is ready to sell their house. If at any point the LLM 
    needs help it should also alert the real estate agent.
    We'll also want to offer things like a free home valuation, a comparative market analysis, and a free home buyers guide.
    We'll expand functionality to include emailing them, and calling them using a model like whisper to cold call.
    We may want to also automate the sending and receiving paperwork.
    You'll need to design the system, build out all the components, save, test and run the code.
    We'll want to have a test area where we can simulate conversations where the potential lead is an LLM.
    We'll want a lot more. But this is a good start. keep working, build out this initial functionality keeping in mind that we'll want to expand it later.
    
    use twilio, gcp. probably google cloud function with triggers and then we'll want some sql database to store the extracted structured data. 
'''