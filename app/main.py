import os
import sys

project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_path)

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.logger import logger
from app.db.init_db import init_db
from app.api import auth, moscow_time
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Контекст жизненного цикла приложения."""
    try:
        logger.info("Инициализация базы данных...")
        init_db()
        logger.info("База данных успешно инициализирована")
        yield
    except Exception as e:
        logger.critical(f"Ошибка инициализации базы данных: {e}")
        raise


app = FastAPI(
    title="Auth Service API",
    description="API для аутентификации пользователей",
    version="1.0.0",
    lifespan=lifespan
)


# Подключение роутеров
app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Аутентификация"]
)


app.include_router(
    moscow_time.router,
    prefix="/api",
    tags=["Время"]
)


@app.on_event("startup")
async def startup_event():
    """Обработчик события запуска приложения."""
    logger.info("Сервер запущен")


@app.on_event("shutdown")
async def shutdown_event():
    """Обработчик события остановки приложения."""
    logger.info("Сервер остановлен")