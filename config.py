from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    DATABASE_URL: str

    FIDS_DEPLOY_URL: str
    FIDS_AUTH_TOKEN: str
    FIDS_SCRIPT_PATH: str
    FIDS_REMOTE_PATH: str
    FIDS_DEVICE_USERNAME: str
    FIDS_DEVICE_PASSWORD: str
    FIDS_LOG_FILE_PATH: str

    FIDS_APP_MONITOR_URL: str
    FIDS_APP_MONITOR_COOKIE: str

    ALLOWED_FIDS_IPS: str = "10.0.89.199"

    DEFAULT_LOCATION: str = "RGIA"
    DEFAULT_APP_NAME: str = "FIDS"
    DEFAULT_ERROR_TYPE: str = "display_down"
    DEFAULT_ASSIGNEE: str = "FIDS Support"

    @property
    def allowed_ips(self) -> list[str]:
        return [ip.strip() for ip in self.ALLOWED_FIDS_IPS.split(",")]


settings = Settings()