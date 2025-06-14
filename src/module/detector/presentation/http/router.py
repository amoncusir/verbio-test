from logging import getLogger

from fastapi import APIRouter

_logger = getLogger(__name__)


def build_router() -> APIRouter:
    # Module routers
    from .text_detection.palindrome import router as palindrome  # pylint: disable=C0415
    from .text_detection.detection import router as detection  # pylint: disable=C0415
    from .text_detection.search import router as search  # pylint: disable=C0415

    router = APIRouter()
    router.include_router(palindrome)
    router.include_router(detection)
    router.include_router(search)

    return router
