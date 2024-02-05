import uvicorn

from app import logger
from test_app import test_main_route


async def run_server():
    try:
        await test_main_route()
        logger.info("The application test has been successfully executed")
    except Exception as e:
        logger.error(f"An error occurred when running tests | {e}")

    uvicorn_cmd = "app:app"
    uvicorn.run(uvicorn_cmd, host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    try:
        import asyncio

        asyncio.run(run_server())
    except Exception as e:
        logger.error(f"An error occurred when starting the server | {e}")
