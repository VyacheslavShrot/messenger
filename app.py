import logging

from fastapi import FastAPI

from messages_api import messages_router

app = FastAPI(
    title="Messanger"
)


@app.get("/app-status")
async def app_status():
    return {"status": "success"}


logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)

app.include_router(messages_router)
