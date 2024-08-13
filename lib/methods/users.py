from typing import Any, Dict

from lib.api import VkAPI


class Method:
    def __init__(self, api: VkAPI):
        self.api = api

    async def get(self, user_ids: str, fields: str = None) -> Dict[str, Any]:
        params = {"user_ids": user_ids}
        if fields:
            params["fields"] = fields
        return await self.api.request("users.get", params)
