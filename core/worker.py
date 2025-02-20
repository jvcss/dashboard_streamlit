
import asyncio
import json
import time

from tasks.sql_task import SqlTask
from tasks.api_task import ApiTask
from tasks.io_task import IoTask
from tasks.nosql_task import NoSqlTask
from tasks.syscall_task import SyscallTask

from utils.logger import Logger

class Worker:
    def __init__(self, name, stream_manager):
        self.name = name
        self.queue = asyncio.Queue()
        self.stream_manager = stream_manager
        self.running = True

    async def add_task(self, task):
        """
        Adds a task to the worker's processing queue.
        """
        await self.queue.put(task)

    async def process_task(self, task):
        """
        Processes a task and sends the result downstream.
        """
        if not isinstance(task, (ApiTask, SqlTask, NoSqlTask, IoTask, SyscallTask)):
            Logger.info(f"\n\n\n\nWorker {self.name}: Unsupported task type: {task.__class__.__name__}\n\n\n\n")
            return
        Logger.info(f"Worker {self.name}: Processing task {task.__class__.__name__}")
        try:
            result = await task.execute()
            if isinstance(task, ApiTask):
                formatted_result = json.dumps(result, indent=2) if isinstance(result, dict) else str(result)
            elif isinstance(task, SqlTask):
                formatted_result = f"SQL Result: {result}"  # Handle SQL results as a list of records
            else:
                formatted_result = str(result)  # Fallback for other task types


            Logger.info(f"Worker {self.name}: Task result: {formatted_result}")
            await self.stream_manager.send(self.name, result) # TODO
        except Exception as e:
            Logger.error(f"Worker {self.name}: Error processing task: {e}")

    async def run(self):
        """
        Main loop to process tasks from the queue.
        """
        while self.running:
            task = await self.queue.get()
            if task is None:
                break  # Exit loop if None is received
            await self.process_task(task)

