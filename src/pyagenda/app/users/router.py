from fastapi import APIRouter, Depends, HTTPException, status
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from pyagenda.app.core.db import get_db
from pyagenda.app.users.schemas import UserCreate, UserGet
from pyagenda.app.users.services import (
    create,
    get_all,
    get_by_email,
    get_by_id,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}", response_model=UserGet)
def _get_user(user_id: int, db=Depends(get_db)):
    user = get_by_id(db, user_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return user


@router.get("", response_model=list[UserGet])
def _list_users(db=Depends(get_db)):
    return get_all(db)


@router.post("/", response_model=UserGet)
def _create_user(r: UserCreate, db=Depends(get_db)):
    if get_by_email(db, r.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="um usuario com esse email ja existe",
        )

    try:
        u = create(db=db, name=r.name, email=r.email, password=r.password)
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"erro ao tentar criar o usuario: {e}",
        )

    return u
