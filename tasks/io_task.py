import aiofiles

class IoTask:
    def __init__(self, file_path, mode, content=None):
        self.file_path = file_path
        self.mode = mode
        self.content = content

    async def execute(self):
        if self.mode == "read":
            async with aiofiles.open(self.file_path, "r") as f:
                return await f.read()
        elif self.mode == "write":
            async with aiofiles.open(self.file_path, "w") as f:
                await f.write(self.content)
                return f"File written to {self.file_path}"
