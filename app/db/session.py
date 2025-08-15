from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.core.logger import logger


engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Генератор сессий БД для зависимостей FastAPI."""
    db = SessionLocal()
    try:
        logger.info("Открытие новой сессии БД")
        yield db
    finally:
        logger.info("Закрытие сессии БД")
        db.close()


# Явная проверка подключения
try:
    with engine.connect() as conn:
        logger.info("Проверка подключения к БД")
        result = conn.execute(text("SELECT 1"))
        logger.info(
            f"Подключение к БД успешно. Результат теста: {result.scalar()}"
        )
except Exception as e:
    logger.critical(f"Ошибка подключения к БД: {str(e)}")
    raise