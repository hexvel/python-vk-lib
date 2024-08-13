import asyncio
from typing import Callable, Dict

from .api import VkAPI
from .models import MessageEvent


class VkBot:
    def __init__(self, token: str, group_id: int | None = None):
        self.token = token
        self.group_id = group_id
        self.api = None
        self.handlers: Dict[str, Callable[[MessageEvent], asyncio.Future]] = {}
        self.default_handler: Callable[[MessageEvent], asyncio.Future] = None

    def on_command(self, command: str):
        def decorator(func: Callable[[MessageEvent], asyncio.Future]):
            self.handlers[command] = func
            return func

        return decorator

    def on_message(self, handler: Callable[[MessageEvent], asyncio.Future]):
        self.default_handler = handler

    async def handle_event(self, event: MessageEvent):
        """Обрабатывает событие типа сообщение"""
        if event.text.startswith("/"):
            command = event.text.split(" ")[0][1:]
            handler = self.handlers.get(command)
            if handler:
                await handler(event)
            elif self.default_handler:
                await self.default_handler(event)
        else:
            if self.default_handler:
                await self.default_handler(event)

    async def listen(self):
        async with VkAPI(self.token) as api:
            self.api = api
            while True:
                try:
                    response = await self.api.messages.getLongPollServer(
                        group_id=self.group_id
                    )
                    server, key, ts = (
                        response["server"],
                        response["key"],
                        response["ts"],
                    )

                    if not all([server, key, ts]):
                        raise ValueError(
                            "One or more required values are missing: server, key, or ts"
                        )

                    longpoll_url = (
                        f"https://{server}?act=a_check&key={key}&ts={ts}&wait=25"
                    )

                    async with self.api.session.get(longpoll_url) as resp:
                        data = await resp.json()
                        for update in data.get("updates", []):
                            if update[0] == 4:
                                message_id = update[1]
                                message_data = await self.api.messages.getById(
                                    message_ids=message_id
                                )
                                message_event = MessageEvent(**message_data["items"][0])
                                await self.handle_event(message_event)

                except Exception as e:
                    print(f"Error in listen: {e}")
                    await asyncio.sleep(5)

    async def send_message(self, peer_id: int, text: str):
        if self.api:
            await self.api.messages.send(peer_id=peer_id, message=text, random_id=0)

    async def run(self):
        await self.listen()
