


from utils.logger import Logger

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
