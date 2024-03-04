import logging
import os
import base64
from urllib import parse
from typing import List
from pydantic import BaseModel

from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings
from starlette.datastructures import Secret


log = logging.getLogger(__name__)


class BaseConfigurationModel(BaseModel):
    """Base configuration model used by all config options."""

    pass


def get_env_tags(tag_list: List[str]) -> dict:
    """Create dictionary of available env tags."""
    tags = {}
    for t in tag_list:
        tag_key, env_key = t.split(":")

        env_value = os.environ.get(env_key)

        if env_value:
            tags.update({tag_key: env_value})

    return tags


config = Config(".env")

LOG_LEVEL = config("LOG_LEVEL", default=logging.WARNING)
# ENV = config("ENV", default="local")


# # static files
# DEFAULT_STATIC_DIR = os.path.join(
#     os.path.abspath(os.path.dirname(__file__)), os.path.join(
#         "static", "dispatch", "dist")
# )
# STATIC_DIR = config("STATIC_DIR", default=DEFAULT_STATIC_DIR)

# # metrics
# METRIC_PROVIDERS = config(
#     "METRIC_PROVIDERS", cast=CommaSeparatedStrings, default="")

# # database
# DATABASE_HOSTNAME = config("DATABASE_HOSTNAME")
# DATABASE_CREDENTIALS = config("DATABASE_CREDENTIALS", cast=Secret)
# # this will support special chars for credentials
# _DATABASE_CREDENTIAL_USER, _DATABASE_CREDENTIAL_PASSWORD = str(
#     DATABASE_CREDENTIALS).split(":")
# _QUOTED_DATABASE_PASSWORD = parse.quote(str(_DATABASE_CREDENTIAL_PASSWORD))
# DATABASE_NAME = config("DATABASE_NAME", default="dispatch")
# DATABASE_PORT = config("DATABASE_PORT", default="5432")
# DATABASE_ENGINE_POOL_SIZE = config(
#     "DATABASE_ENGINE_POOL_SIZE", cast=int, default=20)
# DATABASE_ENGINE_MAX_OVERFLOW = config(
#     "DATABASE_ENGINE_MAX_OVERFLOW", cast=int, default=0)
# SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{_DATABASE_CREDENTIAL_USER}:{_QUOTED_DATABASE_PASSWORD}@{DATABASE_HOSTNAME}:{DATABASE_PORT}/{DATABASE_NAME}"
