import asyncio
import os

from dotenv import load_dotenv

from lib.bot import VkBot
from lib.models import MessageEvent

load_dotenv()


bot = VkBot(token=os.getenv("TOKEN"))


@bot.on_command("hello")
async def hello_command(message: MessageEvent):
    await bot.send_message(message.peer_id, "Ку. Как я могу помочь?")


@bot.on_command("info")
async def info_command(message: MessageEvent):
    await bot.send_message(message.peer_id, "Ку. Введи /hello для приветствия")


@bot.on_message
async def default_message_handler(message: MessageEvent):
    await bot.send_message(
        message.peer_id,
        "Команда не распознана. Введи /info для получения информации",
    )


async def main():
    await bot.run()


asyncio.run(main())
