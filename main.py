from fastapi import FastAPI

from routers import cubes

app = FastAPI()

app.add_router(cubes.router)
