from logging import getLogger

from fastapi import APIRouter

from src.config.app import AppConfig

_logger = getLogger(__name__)


def build_router(app_config: AppConfig) -> APIRouter:
    # Module routers
    from .status import router as status_router  # pylint: disable=C0415

    router = APIRouter()
    router.include_router(status_router)

    if app_config.contains_profile('api-task-trigger'):
        _logger.warning("Enabled task trigger API. This is not recommended for production.")
        from .trigger_task import router as task_router  # pylint: disable=C0415

        router.include_router(task_router)

    return router
