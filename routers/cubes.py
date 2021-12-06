import uuid
from typing import Optional

from sqlalchemy import text
from fastapi import APIRouter, Path, Query, Body, Response

from dbmodels.cube import Cube
from models.cube import CubeIn, CubeOut
from config.db import connection, session


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

@router.post(
    '/cubes/add', 
    status_code=201, 
    response_model=CubeOut,
    response_model_exclude_unset=True
)
def add_cube(cube: CubeIn = Body(...)):
    new_cube = Cube(
        sn=uuid.uuid1().hex,
        name=cube.Name,
        brand=cube.Brand,
        category=str(cube.Category).rpartition('.')[2],
        difficulty=str(cube.Difficulty).rpartition('.')[2].replace('_', ' '),
        numofpieces=cube.NumOfPieces,
        review=cube.Review,
        price=cube.Price
    )

    session.add(new_cube)
    session.commit()
    
    cube = dict(cube)
    cube['SN'] = new_cube.sn

    return cube
    
@router.get('/cubes/{cube_id}')
def get_cube():
    pass

@router.put('/cubes/{cube_id}')
def update_cube():
    pass

@router.delete('/cubes/{cube_id}')
def delete_cube():
    pass


