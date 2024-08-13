from typing import Any, Dict

from lib.api import VkAPI


class Method:
    def __init__(self, api: VkAPI):
        self.api = api

    async def getLongPollServer(self, group_id: int = None) -> Dict[str, Any]:
        params = {"group_id": group_id} if group_id is not None else {}
        return await self.api.request("messages.getLongPollServer", params)

    async def getById(self, message_ids: str) -> Dict[str, Any]:
        return await self.api.request("messages.getById", {"message_ids": message_ids})

    async def send(
        self, peer_id: int, message: str, random_id: int = 0
    ) -> Dict[str, Any]:
        return await self.api.request(
            "messages.send",
            {"peer_id": peer_id, "message": message, "random_id": random_id},
        )
