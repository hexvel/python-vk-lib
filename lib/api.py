import importlib
from typing import Any, Dict

import aiohttp


class VkAPIError(Exception):
    pass


class VkAPI:
    def __init__(self, token: str, session: aiohttp.ClientSession = None):
        self.token = token
        self.session = session or aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False)
        )
        self.methods = {}

    async def request(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        params["access_token"] = self.token
        params["v"] = "5.199"

        url = f"https://api.vk.com/method/{method}"
        async with self.session.get(url, params=params) as response:
            data = await response.json()
            if "error" in data:
                raise VkAPIError(data["error"])
            return data["response"]

    def __getattr__(self, name: str) -> Any:
        if name not in self.methods:
            try:
                module = importlib.import_module(f"lib.methods.{name}")
                self.methods[name] = module.Method(self)
            except ModuleNotFoundError:
                raise AttributeError(f"Method {name} not found in VK API")
        return self.methods[name]

    async def close(self):
        await self.session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()
