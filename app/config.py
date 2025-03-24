from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str = "localhost"
    database_port: str = "5432"
    database_name: str = "local"
    database_username: str = "postgres"
    database_password: str = "Aswin2000"

settings = Settings()
