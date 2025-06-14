from typing import List, Callable

from fastapi import APIRouter, FastAPI

from src.config.api import ApiSettings
from src.config.app import AppConfig


def build_router(routes: List[APIRouter]) -> APIRouter:
    router = APIRouter()

    for route in routes:
        router.include_router(route)

    return router


def build_fastapi(router: APIRouter, api_settings: ApiSettings, app_config: AppConfig, lifespan: Callable) -> FastAPI:

    api = FastAPI(
        name=app_config.name,
        debug=app_config.debug,
        lifespan=lifespan,
        root_path=api_settings.root_path,
    )

    api.include_router(router)

    return api
