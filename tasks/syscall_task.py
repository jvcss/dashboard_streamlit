import asyncio
import subprocess

class SyscallTask:
    def __init__(self, command):
        self.command = command

    async def execute(self):
        process = await asyncio.create_subprocess_shell(self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = await process.communicate()
        if process.returncode != 0:
            raise RuntimeError(f"Command failed: {stderr.decode().strip()}")
        return stdout.decode().strip()
