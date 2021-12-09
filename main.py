from fastapi import FastAPI

from routers import cubes

DESCRIPTION = '''
Cube-CRUD is a simple example of a REST API CRUD
in a context of rubik's cube review service.
It uses Sqlalchemy ORM to mannage the connection and database operations.
'''

LICENSE_INFO = {
    'name': 'BSD 3-Clause License',
    'url': 'https://opensource.org/licenses/BSD-3-Clause'
}


app = FastAPI(
    title='Cube-CRUD',
    description=DESCRIPTION,
    license_info=LICENSE_INFO
)

app.include_router(cubes.router)
