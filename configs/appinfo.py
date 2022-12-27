from pydantic import BaseSettings

class Setting(BaseSettings):
    app_name: str
    app_version: str
    app_framework: str
    app_date: str
    owner_name: str