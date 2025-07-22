import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
from pymongo import AsyncMongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
from pymongo.collection import Collection
from pymongo.database import Database


class MongoClient:

    _client: AsyncMongoClient = None
    _instance = None

    def __new__(cls):
        if MongoClient._instance is None:
            cls._instance = super(MongoClient, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.load_config()

    def load_config(self):
        self.mongo_uri = os.getenv("MONGO_URI")
        self.mongo_retry_attempts = int(os.getenv("MONGO_RETRY_ATTEMPT"))
        self.mongo_retry_delay_ms = int(os.getenv("MONGO_RETRY_MS"))
        self.db_name = os.getenv("DATABASE_NAME")

    async def connect(self):
        if MongoClient._client is not None:
            return
        retry_attempt = 0
        while retry_attempt < self.mongo_retry_attempts:
            try:
                MongoClient._client = AsyncMongoClient(
                    self.mongo_uri, connectTimeoutMS=30 * 60 * 1000
                )
                await MongoClient._client.admin.command("ping")
                return

            except (ServerSelectionTimeoutError, ConnectionFailure) as e:
                print(e)
                retry_attempt += 1
                if retry_attempt >= self.mongo_retry_attempts:
                    raise ConnectionError("Connection to MongoDB failed")
                asyncio.sleep(self.mongo_retry_delay_ms / 1000)

    def get_db(self) -> Database:
        if not MongoClient._client:
            raise RuntimeError("MongoDB client not initialized. Call connect() first.")
        return MongoClient._client[self.db_name]

    async def close_connection(self):
        await MongoClient._client.close()


def get_chat_collection() -> Collection:
    db = MongoClient().get_db()
    return db["chats"]
