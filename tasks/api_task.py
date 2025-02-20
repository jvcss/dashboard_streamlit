import aiohttp

class ApiTask:
    def __init__(self, url, method="GET", params=None, data=None):
        self.url = url
        self.method = method
        self.params = params
        self.data = data

    async def execute(self):
        async with aiohttp.ClientSession() as session:
            async with session.request(self.method, self.url, params=self.params, json=self.data) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"API Error: {response.status}: {await response.text()}")
