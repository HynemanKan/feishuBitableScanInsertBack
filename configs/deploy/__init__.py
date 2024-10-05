from typing import  Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class LoggingConfig(BaseSettings):
    """
    Logging configs
    """

    LOG_LEVEL: str = Field(
        description="Log output level, default to INFO. It is recommended to set it to ERROR for production.",
        default="INFO",
    )

    LOG_FILE: Optional[str] = Field(
        description="logging output file path",
        default=None,
    )

    LOG_FORMAT: str = Field(
        description="log format",
        default="%(asctime)s.%(msecs)03d %(levelname)s [%(threadName)s] [%(filename)s:%(lineno)d] - %(message)s",
    )

    LOG_DATEFORMAT: Optional[str] = Field(
        description="log date format",
        default=None,
    )

    LOG_TZ: Optional[str] = Field(
        description="specify log timezone, eg: America/New_York",
        default=None,
    )

class BaseInfoConfig(BaseSettings):
    CURRENT_VERSION:str = Field(
        description="current version",
        default="0.0.1",
    )

class SecurityConfig(BaseSettings):
    SCANNING_APP_SECRET:str = Field(
        description="scan app secret",
        default="9SeTsR4T2GeGjbaoPbojsOvLRO6TD4lx",
    )
class DeployConfig(LoggingConfig,BaseInfoConfig,SecurityConfig):
    pass