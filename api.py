from typing import List, Optional

from fastapi import APIRouter, Depends

from pydantic import BaseModel
from starlette.responses import JSONResponse

from dispatch.auth.service import get_current_user

class ErrorMessage(BaseModel):
    msg: str


class ErrorResponse(BaseModel):
    detail: Optional[List[ErrorMessage]]


api_router = APIRouter(
    default_response_class=JSONResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)

# WARNING: Don't use this unless you want unauthenticated routes
authenticated_api_router = APIRouter()

api_router.include_router(
    authenticated_api_router,
    dependencies=[Depends(get_current_user)],
)
