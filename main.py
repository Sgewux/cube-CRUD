from fastapi import FastAPI

from routers import cubes

app = FastAPI()

app.include_router(cubes.router)
