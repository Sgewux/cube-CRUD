from typing import Optional

from fastapi import APIRouter, Path, Query, Body

from config.db import connection

router = APIRouter()


@router.get('/cubes')
def get_all_cubes(
    brand: Optional[str] = Query(
        None, 
        max_length=20, 
        min_lenght=1
    ), price: Optional[float] = Query(
        None,
        gt=1
    )
):
    pass

@router.post('/cubes/add')
def add_cube():
    pass

@router.get('/cubes/{cube_id}')
def get_cube():
    pass

@router.put('/cubes/{cube_id}')
def update_cube():
    pass

@router.delete('/cubes/{cube_id}')
def delete_cube():
    pass


