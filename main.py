import asyncio
import os

from dotenv import load_dotenv

from lib.bot import VkBot
from lib.models import MessageEvent

load_dotenv()


async def message_handler(bot: VkBot, message: MessageEvent):
    print(f"Новое сообщение - {message.from_id}: {message.text}")
    await bot.send_message(message.peer_id, "Ку")


async def main():
    bot = VkBot(token=os.getenv("TOKEN"))
    bot.on_message(lambda message: message_handler(bot, message))
    await bot.run()


asyncio.run(main())
