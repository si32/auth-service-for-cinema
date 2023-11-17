from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from api.v1 import users

from core.config import settings

from db import storage
from db.redis import RedisStorage


@asynccontextmanager
async def lifespan(app: FastAPI):
    storage.nosql_storage = RedisStorage(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=0,
        decode_responses=True
    )
    yield

    await storage.nosql_storage.close()


app = FastAPI(
    description='Сервис по авторизации и аутентификации пользователей',
    version='1.0.0',
    title=settings.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=JSONResponse,
    lifespan=lifespan
)


app.include_router(users.router, prefix='/api/v1/users', tags=['users'])


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        reload=True
    )