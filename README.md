# Проект для самообучения University FastAPI

REST API для университетской системы управления, построенный с использованием FastAPI(асинхронная версия).

## Возможности

- Аутентификация и авторизация пользователей
- Управление пользователями (студенты, преподаватели)
- Управление курсами
- Управление группами
- Управление факультетами
- Новостная лента

## Технологии

- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- Python
- Docker
- Docker Compose

## Структура проекта

```
src/
├── core/           # Основные настройки и конфигурации
├── crud/           # CRUD операции для работы с базой данных(DAO модели)
├── models/         # SQLAlchemy модели
├── routers/        # API эндпоинты
├── schemas/        # Pydantic модели
├── service/        # Бизнес-логика
└── settings.py     # Настройки приложения
```

## Установка и запуск

### Локальный запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/SmellsBa11s/university-fastapi.git
cd university-fastapi
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate     # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Настройте переменные окружения:


5. Запустите приложение:
```bash
uvicorn src.main:app --reload
```

### Запуск через Docker

1. Убедитесь, что у вас установлены Docker и Docker Compose

2. Клонируйте репозиторий:
```bash
git clone https://github.com/SmellsBa11s/university-fastapi.git
cd university-fastapi
```

3. Создайте файл `.env` на основе `.env.example`:
```bash
cp .env.example .env
```

4. Запустите приложение с помощью Docker Compose:
```bash
docker-compose up -d
```

После запуска будут доступны следующие сервисы:
- API приложение: `http://localhost:8000`
- Swagger документация: `http://localhost:8000/docs`
- Adminer (управление базой данных): `http://localhost:8080`
  - Система: PostgreSQL
  - Сервер: db
  - Пользователь: postgres
  - Пароль: postgres
  - База данных: university

Для остановки приложения:
```bash
docker-compose down
```


## Авторы

- Матвей - *SmellsBa11s* - [Ваш GitHub](https://github.com/SmellsBa11s)

