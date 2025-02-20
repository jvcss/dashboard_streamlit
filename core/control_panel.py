import asyncio
from core.worker import Worker
from core.stream_manager import StreamManager

class ControlPanel:
    """
        Essa implementação é uma versão simplificada de um pipeline de processamento de dados.\n
        O pipeline é composto por um control panel, workers e tasks.\n
        O Control panel é responsável por criar os workers e gerenciar o fluxo de dados entre eles.\n
        Cada worker é responsável por processar as tasks que recebe.\n
        As tasks são as operações que serão realizadas em cada worker.
    """
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

