from typing import Any, Dict

from lib.api import VkAPI


class Method:
    def __init__(self, api: VkAPI):
        self.api = api

    async def getLongPollServer(self, **params: Any) -> Dict[str, Any]:
        cleaned_params = {k: v for k, v in params.items() if v is not None}
        return await self.api.request("messages.getLongPollServer", cleaned_params)

    async def getById(self, **params: Any) -> Dict[str, Any]:
        cleaned_params = {k: v for k, v in params.items() if v is not None}
        return await self.api.request("messages.getById", cleaned_params)

    async def send(self, **params: Any) -> Dict[str, Any]:
        cleaned_params = {k: v for k, v in params.items() if v is not None}
        return await self.api.request("messages.send", cleaned_params)
