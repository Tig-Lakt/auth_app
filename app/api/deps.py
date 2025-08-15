from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.core.logger import logger

from app.crud.users import get_user_by_username
from app.db.session import get_db
from app.core.config import settings
from app.schemas.token import TokenData


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Зависимость для получения текущего пользователя по JWT токену."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        logger.info("Начало проверки токена")
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        
        if username is None:
            logger.error("В токене отсутствует идентификатор пользователя (sub)")
            raise credentials_exception
            
        token_data = TokenData(username=username)
        logger.info(f"Токен проверен для пользователя: {username}")
        
    except jwt.ExpiredSignatureError:
        logger.error("Попытка использования просроченного токена")
        raise credentials_exception
    except JWTError as e:
        logger.error(f"Ошибка проверки токена: {str(e)}")
        raise credentials_exception
    
    user = get_user_by_username(db, username=token_data.username)
    if user is None:
        logger.error(f"Пользователь не найден в БД: {token_data.username}")
        raise credentials_exception
    
    logger.info(f"Успешная аутентификация пользователя: {user.username}")
    return user