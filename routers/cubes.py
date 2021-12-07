import uuid
from typing import Optional, List

from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Path, Query, Body, Response, HTTPException

from dbmodels.cube import Cube
from models.cube import CubeIn, CubeOut, _Difficulty, _Category
from config.db import session


router = APIRouter()


@router.get('/cubes', response_model=List[CubeOut])
def get_all_cubes(
    price_lt: Optional[float] = Query(
        None,
        gt=0
    ),
    price_gt: Optional[float] = Query(
        None,
        gt=0
    ),
    difficulty: Optional[_Difficulty] = Query(
        None
    ),
    category: Optional[_Category] = Query(
        None
    )
):
    if price_lt and price_gt:
        results = session.query(Cube).filter(
            Cube.price < price_lt,
            Cube.price > price_gt
        ).all()
    elif price_lt:
        results = session.query(Cube).filter(
            Cube.price < price_lt
        ).all()
    elif price_gt:
        results = session.query(Cube).filter(
            Cube.price > price_gt
        ).all()
    elif category:
        results = session.query(Cube).filter(
            Cube.category == str(category).rpartition('.')[2]
        ).all()
    elif difficulty:
        results = session.query(Cube).filter(
            Cube.difficulty == str(difficulty).rpartition('.')[2].replace('_',' ')
        ).all()
    else:
        results = session.query(Cube).all()

    cubes = []
    for cube in results:
        cubes.append(
            CubeOut(
                SN=cube.sn,
                Name=cube.name,
                Category=cube.category,
                Brand=cube.brand,
                NumOfPieces=cube.numofpieces,
                Difficulty=cube.difficulty,
                Review=cube.review,
                Price=cube.price
            )
        )

    return cubes


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
    
    try:
        session.add(new_cube)
        session.commit()
    except IntegrityError as e:
        if 'psycopg2.errors.UniqueViolation' in str(e):
            raise HTTPException(status_code=400, detail='Name must be unique!')
    
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


