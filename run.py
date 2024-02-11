import uvicorn
from fastapi import HTTPException

from test_app import test_db_route
from utils.env import get_env
from utils.logger import logger


async def _run_server():
    try:
        await get_env()
    except Exception as e:
        logger.error(f"An error occurred when get env variables | {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred when get env variables | {e}")

    try:
        from test_app import test_main_route

        await test_main_route()

        await test_db_route()
        logger.info("The application test has been successfully executed")
    except Exception as e:
        logger.error(f"An error occurred when running tests | {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred when running tests | {e}")

    uvicorn_cmd = "app:app"
    uvicorn.run(uvicorn_cmd, host="0.0.0.0", port=8001, reload=True)


if __name__ == "__main__":
    import asyncio

    asyncio.run(_run_server())
