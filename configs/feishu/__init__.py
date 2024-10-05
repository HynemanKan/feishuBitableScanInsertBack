from pydantic import Field
from pydantic_settings import BaseSettings

class FeishuConfig(BaseSettings):
    FEISHU_APP_ID:str = Field(
        description="feishu app id",
        default="APP_ID",
    )

    FEISHU_APP_SECRET:str = Field(
        description="feishu app secret",
        default="APP_SECRET",
    )