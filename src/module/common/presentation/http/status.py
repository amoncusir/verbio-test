import logging

from fastapi import APIRouter

router = APIRouter(prefix="/status", tags=["status"])

logger = logging.getLogger(__name__)


@router.get("/healthcheck", status_code=204)
async def healthcheck():
    """
    Healthcheck endpoint that checks all app services are operational.
    Returns 204 code if the service is up without body response.
    """
    logger.debug("Healthcheck endpoint called")
