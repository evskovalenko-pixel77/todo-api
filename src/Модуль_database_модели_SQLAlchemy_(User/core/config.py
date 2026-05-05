from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/todo"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
