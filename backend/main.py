import time
from contextlib import asynccontextmanager
from fastapi import Request

import uvicorn
from fastapi import FastAPI

from backend.db.engine import check_db
from backend.endpoints.auth import auth_router
from backend.endpoints.exercises import exercises_router
from fastapi.middleware.cors import CORSMiddleware
from backend.logger.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Приложение  включено")
    await check_db()
    yield
    logger.info("Приложение отключено")

app = FastAPI(title="Quazort_Up", lifespan=lifespan)
app.include_router(exercises_router)
app.include_router(auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def middleware(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    logger.debug(f"Endpoint {request.url.path} finished in {process_time:.4f} sec")
    return response


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="127.0.0.1", port=8000)