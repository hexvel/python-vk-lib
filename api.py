import aiohttp


class VkClient:
    """
    Пример использования:
    vk = VkClient("your_token")
    response = await vk.request("users.get", {"user_ids": "1"})
    """

    BASE_URL = "https://api.vk.com/method/"

    def __init__(self, token: str, version: str = "5.199"):
        self.token = token
        self.version = version
        self.session = aiohttp.ClientSession()

    async def request(self, method: str, params: dict) -> dict:
        params.update({"access_token": self.token, "v": self.version})
        async with self.session.get(self.BASE_URL + method, params=params) as response:
            return await response.json()

    async def close(self):
        await self.session.close()
