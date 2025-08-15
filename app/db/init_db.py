from app.core.logger import logger
from app.models.base import Base
from app.db.session import engine
from sqlalchemy import inspect


def init_db():
    """Инициализирует базу данных, создавая все таблицы."""
    try:
        logger.warning("Начало инициализации базы данных")
        
        # Проверка существующих таблиц
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        logger.info(f"Существующие таблицы: {existing_tables}")
        
        # Создание таблиц
        Base.metadata.create_all(bind=engine)
        
        # Проверка результата
        new_tables = inspector.get_table_names()
        created_tables = set(new_tables) - set(existing_tables)
        
        if created_tables:
            logger.info(f"Созданы таблицы: {created_tables}")
        else:
            logger.warning("Новые таблицы не созданы")
        
        logger.info("Инициализация базы данных завершена")
        
    except Exception as e:
        logger.critical(f"Ошибка инициализации БД: {str(e)}")
        raise