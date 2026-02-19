import time
from contextlib import asynccontextmanager
from urllib.request import Request

import uvicorn
from fastapi import FastAPI

from db.engine import check_db
from endpoints.exercises import exercises_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    await check_db()
    yield
    print("приложение отключено")




app = FastAPI(title="Quazort_Up", lifespan=lifespan)
app.include_router(exercises_router)

@app.middleware("http")
async def middleware(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    print(f"process_time: {process_time}")
    return response


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="127.0.0.1", port=8000)


