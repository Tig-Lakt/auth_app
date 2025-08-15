from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings
from app.core.logger import logger
from app.models.user import User


pwd_context = CryptContext(
    schemes=["bcrypt"],
    bcrypt__ident="2b",  
    bcrypt__min_rounds=12,
    deprecated="auto"
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет соответствие пароля и хеша."""
    try:
        result = pwd_context.verify(plain_password, hashed_password)
        if not result:
            logger.warning("Неверный пароль")
        return result
    except Exception as e:
        logger.error(f"Ошибка проверки пароля: {str(e)}")
        raise


def get_password_hash(password: str) -> str:
    """Генерирует хеш пароля."""
    try:
        logger.info("Генерация хеша пароля")
        return pwd_context.hash(password)
    except Exception as e:
        logger.error(f"Ошибка хеширования пароля: {str(e)}")
        raise


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Создает JWT токен с указанными данными."""
    try:
        logger.info("Создание JWT токена")
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        
        to_encode.update({"exp": expire})
        
        token = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
        
        logger.info("JWT токен успешно создан")
        return token
        
    except Exception as e:
        logger.error(f"Ошибка создания токена: {str(e)}")
        raise


def authenticate_user(db, username: str, password: str):
    """Аутентифицирует пользователя по username и паролю."""
    try:
        logger.info(f"Аутентификация пользователя: {username}")
        
        user = db.query(User).filter(User.username == username).first()
        
        if not user:
            logger.warning(f"Пользователь {username} не найден")
            return False
            
        if not verify_password(password, user.hashed_password):
            logger.warning(f"Неверный пароль для пользователя {username}")
            return False
            
        logger.info(f"Успешная аутентификация: {username}")
        return user
        
    except Exception as e:
        logger.error(f"Ошибка аутентификации: {str(e)}")
        raise