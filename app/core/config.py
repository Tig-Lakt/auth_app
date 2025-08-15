from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, Field, field_validator
import os


class Settings(BaseSettings):
    # Настройки БД 
    POSTGRES_HOST: str = Field(..., min_length=1)
    POSTGRES_PORT: str = Field(..., min_length=2)
    POSTGRES_USER: str = Field(..., min_length=1)
    POSTGRES_PASSWORD: str = Field(..., min_length=1)
    POSTGRES_DB: str = Field(..., min_length=1)

    # Настройки аутентификации 
    SECRET_KEY: str = Field(..., min_length=10)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    @property
    def DATABASE_URL(self) -> PostgresDsn:
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @field_validator('POSTGRES_PORT')
    def validate_port(cls, v):
        if not v.isdigit():
            raise ValueError("PORT must be numeric")
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "forbid"  # Запрещает лишние переменные в .env


# Явная проверка загрузки .env
if not os.path.exists(".env"):
    raise RuntimeError("Файл .env не найден в корне проекта")

settings = Settings()