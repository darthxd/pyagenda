import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status
from starlette.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from pyagenda.app.core.db import get_db
from pyagenda.app.core.jwt import generate_token
from pyagenda.app.users.schemas import (
    LoginResponse,
    UserCreate,
    UserGet,
    UserLogin,
    UserUpdate,
)
from pyagenda.app.users.services import (
    create,
    delete,
    get_all,
    get_by_email,
    get_by_id,
    update,
)

user_router = APIRouter(prefix="/users", tags=["users"])
auth_router = APIRouter(prefix="/auth", tags=["auth"])


@user_router.get("/{user_id}", response_model=UserGet)
def _get_user(user_id: int, db=Depends(get_db)):
    user = get_by_id(db, user_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return user


@user_router.get("", response_model=list[UserGet])
def _list_users(db=Depends(get_db)):
    return get_all(db)


@user_router.post("/", response_model=UserGet)
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


@user_router.patch("/{user_id}", response_model=UserGet)
def _update_user(id: int, r: UserUpdate, db=Depends(get_db)):
    u = get_by_id(db, id)

    if not u:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="usuario nao encontrado"
        )

    new_u = update(
        db=db,
        u=u,
        name=r.name,
        email=r.email,
        password=r.password,
    )

    return new_u


@user_router.delete("/{user_id}")
def _delete_user(id: int, db=Depends(get_db)):
    if not delete(db, id):
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail="erro ao tentar deletar o user",
        )

    return {"message": "usuario deletado com sucesso"}


@auth_router.post("/login")
def _login(r: UserLogin, db=Depends(get_db)) -> LoginResponse:
    u = get_by_email(db, r.email)
    if not u:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"usuario com email {r.email} nao encontrado",
        )

    if not bcrypt.checkpw(r.password.encode(), u.password.encode()):
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="senha incorreta")

    t = generate_token(u)

    res = LoginResponse(user=u, token=t)

    return res
