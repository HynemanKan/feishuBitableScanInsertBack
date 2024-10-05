from pydantic_settings import SettingsConfigDict

from configs.deploy import DeployConfig
from configs.feishu import FeishuConfig


class AppConfig(FeishuConfig,DeployConfig):
    model_config = SettingsConfigDict(
        # read from dotenv format config file
        env_file=".env",
        env_file_encoding="utf-8",
        frozen=True,
        # ignore extra attributes
        extra="ignore",
    )

    # Before adding any config,
    # please consider to arrange it in the proper config group of existed or added
    # for better readability and maintainability.
    # Thanks for your concentration and consideration.