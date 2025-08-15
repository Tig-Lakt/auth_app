import logging
import os
from pathlib import Path

# Создаем папку logs, если её нет
logs_dir = Path(__file__).parent.parent / "logs"
logs_dir.mkdir(exist_ok=True)

# Настройка логгера
def setup_logger():
    logger = logging.getLogger("auth_app")
    logger.setLevel(logging.INFO)  
    # Формат сообщений
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Обработчик для записи в файл
    file_handler = logging.FileHandler(
        filename=logs_dir / "logs.txt",
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

logger = setup_logger()