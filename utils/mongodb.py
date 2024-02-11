import os

from motor import motor_asyncio

from utils.logger import logger


async def get_db():
    try:
        username = os.environ.get("MONGO_INITDB_ROOT_USERNAME")
        password = os.environ.get("MONGO_INITDB_ROOT_PASSWORD")
        auth_source = os.environ.get("MONGO_DB_AUTH_SOURCE")

        client = motor_asyncio.AsyncIOMotorClient(
            "mongo", 27017,
            username=username,
            password=password,
            authSource=auth_source
        )
        db = client.messenger
        logger.info("Database connection successful")

        return db
    except Exception as e:
        logger.error(f"An error occurred when connect to mongodb | {e}")
