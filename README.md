# Todo List REST API

Простой REST API для управления задачами с аутентификацией по JWT. 

## Технологии
- Python 3.12
- FastAPI
- SQLAlchemy + Alembic
- PostgreSQL
- Docker

## Запуск (3 команды)

```bash
git clone https://github.com/your-username/todo-api.git
cd todo-api
docker-compose up --build
```

API будет доступен на `http://localhost:8000`. Документация: `http://localhost:8000/docs`.

## Переменные окружения
В `docker-compose.yml` заданы:
- `DATABASE_URL` — строка подключения к БД
- `JWT_SECRET` — секретный ключ для подписи токенов
- `JWT_ALGORITHM` — алгоритм (по умолчанию HS256)

## Основные эндпоинты
- `POST /auth/register` — регистрация (email, password)
- `POST /auth/login` — получение JWT токена
- `GET /tasks/` — список задач пользователя
- `POST /tasks/` — создать задачу
- `GET /tasks/{id}` — получить задачу
- `PUT /tasks/{id}` — обновить задачу
- `DELETE /tasks/{id}` — удалить задачу

## Разработка
Установка без Docker:
```bash
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

## Цель
Проект создан в качестве демонстрации навыков автоматизации развертывания.