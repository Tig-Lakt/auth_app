from sqlalchemy.orm import Session
from typing import List
from app.core.logger import logger
from app.models.user import User
from app.schemas.user import UserCreate
from app.services.auth import get_password_hash


def get_user_by_email(db: Session, email: str):
    """Получить пользователя по email."""
    logger.info(f"Поиск пользователя по email: {email}")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        logger.warning(f"Пользователь с email {email} не найден")
    return user


def get_user_by_username(db: Session, username: str):
    """Получить пользователя по username."""
    logger.info(f"Поиск пользователя по username: {username}")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        logger.warning(f"Пользователь {username} не найден")
    return user


def create_user(db: Session, user: UserCreate):
    """Создать нового пользователя."""
    try:
        logger.info(
            f"Создание пользователя: {user.username} ({user.email})"
        )
        
        hashed_password = get_password_hash(user.password)
        db_user = User(
            email=user.email,
            username=user.username,
            hashed_password=hashed_password,
            is_active=True,
            is_superuser=False
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        logger.info(
            f"Успешно создан пользователь ID {db_user.id}: "
            f"{db_user.username}"
        )
        return db_user
        
    except Exception as e:
        logger.error(
            f"Ошибка при создании пользователя {user.username}: {str(e)}"
        )
        db.rollback()
        raise