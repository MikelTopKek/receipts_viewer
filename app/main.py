import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.conf.settings import Settings, settings


def init_middlewares(app_api: FastAPI) -> None:
    """Initialize all middlewares."""
    app_api.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def init_routes(app_api: FastAPI) -> None:
    """Initialize all service routes."""


def init_exception_handlers(app_api: FastAPI) -> None:
    """Initialize all exception handlers"""


def create_app(app_settings: Settings | None = None) -> "FastAPI":
    """Create app with including configurations."""
    app_settings = app_settings if app_settings is not None else settings
    app_api = FastAPI(title="Receipts Viewer", debug=app_settings.DEBUG)
    init_middlewares(app_api)
    init_routes(app_api)
    init_exception_handlers(app_api)

    return app_api


app = create_app()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT, loop="uvloop")  # noqa:S104
