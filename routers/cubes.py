import uuid
from typing import Optional, List

from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Path, Query, Body, Response, HTTPException

from dbmodels.cube import Cube
from models.cube import CubeIn, CubeOut, BaseCube, _Difficulty, _Category
from config.db import session


router = APIRouter(tags=['Cubes'])


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
    '''
    **Get all cubes**

    This function allows the user to get data of all cubes stored in
    the database. It also allows filtering data
    through some query parameters.

    **price_lt:** Integer value to return only the cubes that have
              a lower price than it.

    **price_gt:** Integer value to return only the cubes that have
              a higher price than it.

    **difficulty:** A difficulty category to search for.

    **category:** A cube category to search for.

    **Returns:**
            A list of CubeOut json schemas.
    '''
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
            Cube.difficulty == str(difficulty).rpartition('.')[2].replace('_', ' ')
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
    '''
    **Add Cube**
    
    This function allows the user to add a new cube to the database.

    **Cube:** A CubeIn json schema as request body, with the new cube's data.

    **Returns:** A CubeOut json schema.
    '''
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
        session.rollback()  # Once a transacction fails must be rolled back in order to preserve db's integrity.
        if 'psycopg2.errors.UniqueViolation' in str(e):
            raise HTTPException(status_code=400, detail='Name must be unique!')

    cube = dict(cube)
    cube['SN'] = new_cube.sn

    return cube


@router.get(
    '/cubes/{cube_sn}',
    status_code=200,
    response_model=CubeOut)
def get_cube(cube_sn: str = Path(...)):
    '''
    **Get Cube**

    This function allows the user to get data of a specific cube
    identifying it with the serial number.

    **cube_sn:** A str with the sn of the cube as a path parameter.

    **Returns:** A CubeOut json schema.
    '''
    result = session.query(Cube).filter(Cube.sn == cube_sn).first()

    if result is None:
        raise HTTPException(status_code=404, detail='Unexistent cube!')

    cube = CubeOut(
        SN=result.sn,
        Name=result.name,
        Category=result.category,
        NumOfPieces=result.numofpieces,
        Brand=result.brand,
        Difficulty=result.difficulty,
        Review=result.review,
        Price=result.price
    )

    return cube


@router.put(
    '/cubes/{cube_sn}',
    status_code=200,
    response_model=CubeOut
)
def update_cube(
    cube_sn: str = Path(...),
    new_cube: BaseCube = Body(...)  # BaseCube as rquestbody because i dont want the user to set a new cube name.
):
    '''
    Update Cube

    This function allows the user to perform an update operation
    with this function the user can edit all cube's informartion (except name).

    **cube_sn:** str with the sn to the cube you want to update.
    **new_cube:** json schema with the new information of the cube.
    
    **Returns:** a CubeOut json schema.
    '''
    result = session.query(Cube).filter(Cube.sn == cube_sn)
    if result.first() is None:
        raise HTTPException(
            status_code=404,
            detail='Could not update an unexistent cube!'
        )

    result.update({
        Cube.category: str(new_cube.Category).rpartition('.')[2],
        Cube.brand: new_cube.Brand,
        Cube.numofpieces: new_cube.NumOfPieces,
        Cube.difficulty: str(new_cube.Difficulty).rpartition('.')[2].\
        replace('_', ' '),
        Cube.review: new_cube.Review,
        Cube.price: new_cube.Price
    })
    session.commit()
    new_cube = dict(new_cube)
    new_cube = new_cube | {'SN': result.first().sn, 'Name': result.first().name}

    return new_cube


@router.delete(
    '/cubes/{cube_sn}',
    status_code=204,
    response_class=Response  # I had to set this cause fastapi was converting None to null and returning a > 0 content lenght.
)
def delete_cube(cube_sn: str = Path(...)):
    '''
    Delete Cube

    This function allows the user to delete a cube record from the database.

    **cube_sn:** str with the sn of the cube you want to delete.

    **Returns:** 204 NO CONTENT.
    '''
    result = session.query(Cube).filter(Cube.sn == cube_sn)
    if result.first() is None:
        raise HTTPException(
            status_code=404,
            detail='Could not delete an unexsisten cube!'
        )

    result.delete()
    session.commit()
