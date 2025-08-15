from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
import pytz
from app.core.logger import logger
from app.api.deps import get_current_user
from app.models.user import User


router = APIRouter()


@router.get("/moscow_time")
async def get_moscow_time(
    current_user: User = Depends(get_current_user)
):
    """
    Получение текущего времени в Москве (только для авторизованных пользователей).
    
    Returns:
        dict: Словарь с текущим временем, часовым поясом и email пользователя
    """
    try:
        logger.info(
            f"Запрос времени от пользователя: {current_user.email}"
        )
        
        # Устанавливаем московскую временную зону
        tz = pytz.timezone('Europe/Moscow')
        moscow_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        
        logger.info(
            f"Успешный запрос времени для пользователя: {current_user.email}"
        )
        
        return {
            "status": "success",
            "time": moscow_time,
            "timezone": "Europe/Moscow",
            "user": current_user.email
        }
        
    except pytz.UnknownTimeZoneError as e:
        logger.error(
            f"Ошибка часового пояса для пользователя {current_user.email}: {str(e)}"
        )
        raise HTTPException(
            status_code=400,
            detail=f"Ошибка часового пояса: {str(e)}"
        )
        
    except Exception as e:
        logger.error(
            f"Неожиданная ошибка для пользователя {current_user.email}: {str(e)}"
        )
        raise HTTPException(
            status_code=400,
            detail=f"Ошибка при получении времени: {str(e)}"
        )