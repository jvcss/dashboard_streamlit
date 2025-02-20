import asyncio
import json
import aiohttp

from databases import Database
from tasks.io_task import IoTask
from tasks.nosql_task import NoSqlTask
from tasks.syscall_task import SyscallTask
from utils.config import Config


class Logger:
    @staticmethod
    def info(message):
        print(f"[INFO] {message}")

    @staticmethod
    def error(message):
        print(f"[ERROR] {message}")


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


class SqlTask:
    def __init__(self, db_url, query, params=None):
        self.db_url = db_url
        self.query = query
        self.params = params

    async def execute(self):
        database = Database(self.db_url)
        await database.connect()
        try:
            if self.params:
                return await database.fetch_all(self.query, self.params)
            return await database.fetch_all(self.query)
        finally:
            await database.disconnect()


class ControlPanel:
    def __init__(self):
        self.workers = []
        self.stream_manager = StreamManager()

    def create_worker(self, name):
        worker = Worker(name, self.stream_manager)
        self.workers.append(worker)
        return worker

    async def run_pipeline(self):
        tasks = [worker.run() for worker in self.workers]
        await asyncio.gather(*tasks)

    def register_stream(self, from_worker, to_worker):
        self.stream_manager.register(from_worker.name, to_worker)

    async def add_initial_task(self, worker, task):
        await worker.add_task(task)


class StreamManager:
    def __init__(self):
        # Maps worker names to their task callback
        self.streams = {}

    def register(self, from_worker, to_worker):
        """
        Registers a data stream from one worker to another.
        """
        if from_worker not in self.streams:
            self.streams[from_worker] = []
        self.streams[from_worker].append(to_worker)

    async def send(self, from_worker, data):
        """
        Sends data from one worker to its registered downstream workers.
        """
        if from_worker in self.streams:
            for to_worker_callback in self.streams[from_worker]:
                try:
                    Logger.info(f"Sending data from {from_worker} to {to_worker_callback.__self__.name}: {data}")
                    await to_worker_callback(data)
                except Exception as e:
                    Logger.error(f"Error sending data from {from_worker} to {to_worker_callback.__self__.name}: {e}")
        else:
            Logger.error(f"No downstream workers registered for {from_worker}")


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


# Example of registering streams and adding tasks
async def test_pipeline():
    control_panel = ControlPanel()

    # Create workers
    worker1 = control_panel.create_worker("API_WORKER")
    worker2 = control_panel.create_worker("SQL_WORKER")

    # Register data streams
    control_panel.register_stream(worker1, worker2.add_task)

    # Add initial tasks
    await control_panel.add_initial_task(worker1, ApiTask("https://jsonplaceholder.typicode.com/posts/1"))
    query = "SELECT * FROM hbrd_finan_boleto WHERE id_pessoa = 2"
    await control_panel.add_initial_task(worker2, SqlTask(Config().NOVA_PROTECAO_DATABASE_URL, query))

    # Run the pipeline
    await control_panel.run_pipeline()


if __name__ == "__main__":
    asyncio.run(test_pipeline())
