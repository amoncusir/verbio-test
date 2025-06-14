from logging import getLogger
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict

from src.app import get_app, Application

router = APIRouter(prefix="/task", tags=["task"])

_logger = getLogger(__name__)


class TaskRequest(BaseModel):
    model_config = ConfigDict(frozen=True)

    command_ref: str
    request: dict


@router.post("", status_code=204)
async def trigger_task(request: TaskRequest, app: Annotated[Application, Depends(get_app)]):

    command_manager = app.dependency_manager
    executor = app.task_executor

    provider = command_manager.find_command_by_ref(request.command_ref)
    command_type = provider.cls
    request_type = command_type.get_request_type()

    request = request_type(**request.request)

    _logger.warning("Triggering task %s with request %s", command_type, request)

    await executor.execute_async(command_type, request)


class TaskReferencesResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    references: list[str]


@router.get("/references")
async def get_task_references(app: Annotated[Application, Depends(get_app)]):
    """
    Get all command references
    """
    command_manager = app.dependency_manager

    references = [r.reference for r in command_manager.command_references if r.is_referencable]
    return TaskReferencesResponse(references=references)
