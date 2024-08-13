from typing import Any, Dict

from lib.api import VkAPI


class Method:
    def __init__(self, api: VkAPI):
        self.api = api

    async def get(self, **params: Any) -> Dict[str, Any]:
        return await self.api.request("users.get", params)
