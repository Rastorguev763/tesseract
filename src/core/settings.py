import os

from pydantic import Field
from pydantic_settings import BaseSettings


class Setting(BaseSettings):

    # Базовые настройки проекта
    MODE: str = Field(default="DEV", alias="MODE")
    PROJECT_NAME: str = Field(default="Tesseract API", alias="PROJECT_NAME")
    INTERNAL_SERVICE_TOKEN: str = Field(default="secret", alias="INTERNAL_SERVICE_TOKEN")

    # Настройки логирования
    LOGGING_LEVEL: str = Field(default="DEBUG", alias="LOGGING_LEVEL")
    LOG_TO_FILE: bool = Field(default=False, alias="LOG_TO_FILE")
    BASE_DIR_LOGS: str = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    LOG_DIRECTORY: str = Field(
        default=os.path.join(BASE_DIR_LOGS, "logs"), alias="LOG_DIRECTORY"
    )

    @property
    def log_file_path(self):
        os.makedirs(settings.LOG_DIRECTORY, exist_ok=True)

        return os.path.join(self.LOG_DIRECTORY, "debug.log")


settings = Setting()
