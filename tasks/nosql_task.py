from motor.motor_asyncio import AsyncIOMotorClient

class NoSqlTask:
    def __init__(self, db_url, db_name, collection_name, query):
        self.client = AsyncIOMotorClient(db_url)
        self.db_name = db_name
        self.collection_name = collection_name
        self.query = query

    async def execute(self):
        db = self.client[self.db_name]
        collection = db[self.collection_name]
        return await collection.find(self.query).to_list(length=100)
