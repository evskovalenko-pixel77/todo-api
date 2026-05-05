from fastapi import FastAPI
from core.error_handlers import add_exception_handlers


def create_app() -> FastAPI:
    app = FastAPI(
        title="Todo List REST API",
        version="1.0.0",
        description="API for personal task management",
    )
    add_exception_handlers(app)
    # Routers will be added later
    return app


app = create_app()
