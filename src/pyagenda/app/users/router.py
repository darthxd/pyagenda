from fastapi import APIRouter, Depends, HTTPException, status

from pyagenda.app.core.db import get_db
from pyagenda.app.users.schemas import UserGet
from pyagenda.app.users.services import get_user_by_id

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}", response_model=UserGet)
def get_user(user_id: int, db=Depends(get_db)):
    user = get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return user
