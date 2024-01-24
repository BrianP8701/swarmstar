import asyncio

async def get_user_input(prompt: str):
    print(prompt)
    loop = asyncio.get_event_loop()
    user_input = await loop.run_in_executor(None, input)
    return user_input