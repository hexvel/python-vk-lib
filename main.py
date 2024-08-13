import asyncio
import os

from dotenv import load_dotenv

from lib.api import VkAPI

load_dotenv()


async def main():
    async with VkAPI(token=os.getenv("TOKEN")) as api:
        messages = api.messages
        users = api.users

        response = await messages.getLongPollServer()
        print(response)

        user_info = await users.get(user_ids="1,2,3", fields="photo_50")
        print(user_info)


asyncio.run(main())
