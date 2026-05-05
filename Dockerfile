FROM python:3.12-slim
WORKDIR /app
COPY src/backend-core/ .
RUN pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose passlib bcrypt pydantic-settings alembic --no-cache-dir
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
