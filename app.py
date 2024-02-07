from fastapi import FastAPI

from apis.messages_api import messages_router
from apis.users_api import users_router
from utils.mongodb import get_db

app = FastAPI(
    title="Messanger"
)


@app.get("/app-status")
async def app_status():
    return {"status": "success"}


@app.get("/db-status")
async def db_status():
    await get_db()
    return {"status": "success"}


app.include_router(messages_router)
app.include_router(users_router)
