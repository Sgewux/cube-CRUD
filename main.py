from fastapi import FastAPI

from routers import cubes

DESCRIPTION = '''
Cube-CRUD is a simple example of a REST API CRUD 
in a context of rubik's cube review service.
It uses Sqlalchemy ORM to mannage the connection and database operations.
'''
app = FastAPI(
    title='Cube-CRUD',
    description=DESCRIPTION
)

app.include_router(cubes.router)
