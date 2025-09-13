import uvicorn

from .config import uvicorn_config


if __name__ == '__main__':
    uvicorn.run(
        'infrastructure.main:app',
        host=uvicorn_config.HOST,
        port=uvicorn_config.PORT,
        log_level=uvicorn_config.LOG_LEVEL,
        reload=uvicorn_config.RELOAD
    )
