from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.core.logger import logger

from app.models.user import User
from app.crud.users import get_user_by_email, create_user
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserOut
from app.services.auth import (
    authenticate_user,
    create_access_token,
    get_password_hash
)
from app.db.session import get_db
from app.core.config import settings


router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Эндпоинт для получения JWT токена."""
    try:
        logger.info(f"Попытка входа пользователя: {form_data.username}")
        user = authenticate_user(db, form_data.username, form_data.password)
        
        if not user:
            logger.info(
                f"Неудачная попытка входа для пользователя: {form_data.username}"
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверное имя пользователя или пароль",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        access_token = create_access_token(
            data={"sub": user.username},
            expires_delta=access_token_expires
        )
        
        logger.info(f"Успешный вход пользователя: {user.username}")
        return {"access_token": access_token, "token_type": "bearer"}
        
    except Exception as e:
        logger.error(f"Ошибка при аутентификации: {str(e)}")
        raise


@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED
)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """Эндпоинт для регистрации нового пользователя."""
    try:
        logger.info(
            f"Попытка регистрации пользователя: {user_data.username}"
        )
        
        # Проверяем, не занят ли email
        db_user = get_user_by_email(db, email=user_data.email)
        if db_user:
            logger.info(
                f"Попытка регистрации с занятым email: {user_data.email}"
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email уже зарегистрирован"
            )
        
        # Проверяем, не занят ли username
        db_user = db.query(User).filter(
            User.username == user_data.username
        ).first()
        
        if db_user:
            logger.info(
                f"Попытка регистрации с занятым username: {user_data.username}"
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username уже занят"
            )
        
        new_user = create_user(db=db, user=user_data)
        logger.info(f"Успешная регистрация пользователя: {new_user.username}")
        return new_user
        
    except Exception as e:
        logger.error(f"Ошибка при регистрации пользователя: {str(e)}")
        raise