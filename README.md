 FastAPI-сервис аутентификации с JWT токенами и PostgreSQL  

## Требования 
Docker 20.10+  
Docker Compose 2.0+  
Python 3.10+ (для локальной разработки)  

## Установка

### 1. Клонирование репозитория
  
bash  
git clone https://github.com/Tig-Lakt/auth_app  
cd auth-service  

### 2. Настройка окружения 
 
Создайте файл .env в корне проекта:  
Пример содержимого (замените значения на свои):  

## PostgreSQL  
POSTGRES_HOST=db  
POSTGRES_PORT=5432  
POSTGRES_USER=admin  
POSTGRES_PASSWORD=strong_password123!  
POSTGRES_DB=auth_db  

## Auth  
SECRET_KEY=your_very_strong_secret_key_here  
ALGORITHM=HS256  
ACCESS_TOKEN_EXPIRE_MINUTES=30  
 
### 3. Запуск проекта  

docker-compose -f docker-compose.prod.yml up -d --build  

### 4. Доступ к API   
 
После запуска сервис будет доступен:  
Документация Swagger: http://localhost:8000/docs  

### 5. Эндпоинты  
 
POST /auth/register - Регистрация  
POST /auth/token - Получение JWT токена  
GET /api/moscow_time - Текущее время в Москве  

### 6. Тестирование  

Проверить до создания пользователя защищенный метод  
http://localhost/api/moscow_time  

Создать нового пользователя  
curl -X POST "http://localhost:8000/auth/register" \  
-H "Content-Type: application/json" \  
-d '{"email":"test@example.com","username":"testuser","password":"StrongPass123"}'  

Получить токен  
curl -X POST "http://localhost:8000/auth/token" \  
-H "Content-Type: application/x-www-form-urlencoded" \  
-d "username=testuser" \  
-d "password=StrongPass123"  

После получения токена его надо скопировать  

Получение московского времени (только для авторизованных пользователей)   
curl -X GET "http://localhost:8000/api/moscow_time" \  
-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0dXNlciIsImV4cCI6MTc1NTMyODM4OX0.-jlTiXTf_IyHaNbgZdrdl1yBJL_55vdM9QTYAs-83KI"
