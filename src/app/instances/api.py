"""
!! IMPORTANT !!

DO NOT import this module!
"""

from contextlib import asynccontextmanager

from src.app.container import MainContainer
from src.app.application import Application  # nopep8

application = Application.init_with_container(MainContainer)


@asynccontextmanager
async def initializer(_):
    print("Starting up...")
    await application.init()

    yield

    print("Shutting down...")
    await application.shutdown()


api = application.fastapi(lifespan=initializer)
