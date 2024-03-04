import logging
from fastapi import FastAPI

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded


from app.api import api_router
from app.logging import configure_logging
from app.rate_limiter import limiter

from app.auth import models
from app.database.core import engine

models.Base.metadata.create_all(bind=engine)


log = logging.getLogger(__name__)

# we configure the logging level and format
configure_logging()

# we create the ASGI for the app
app = FastAPI(
    title="MyAPI",
    description="Welcome to MyAPI's API documentation! Here you will able to discover all of the ways you can interact with the MyAPI API.",
    root_path="/api/v1",
    openapi_url="/docs/openapi.json",
    redoc_url="/docs",
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# we add all API routes to the Web API framework
app.include_router(api_router)
