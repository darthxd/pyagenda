from datetime import UTC, datetime

import bcrypt

from fastapi import HTTPException
from pyagenda.app.users.models import User
from starlette.status import HTTP_409_CONFLICT


def get_by_id(db, id: int) -> User | None:
    """Recupera o user pelo ID"""
    return db.query(User).filter(User.id == id).first()


def get_by_email(db, email: str) -> User | None:
    """Recupera o user pelo Email"""
    return db.query(User).filter(User.email == email).first()


def get_all(db) -> list[User]:
    """Recupera todos os users cadastrados"""
    return db.query(User).all()


def create(db, name: str, email: str, password: str) -> User:
    """Cadastra um novo user"""
    u = User(
        name=name,
        email=email.lower(),
        password=_hash_password(password),
        is_active=True,
        is_superuser=False,
        created_at=datetime.now(tz=UTC),
    )

    db.add(u)
    db.commit()
    db.refresh(u)

    return u


def update(db, u: User, name=None, email=None, password=None):
    updates = {}
    if name is not None:
        updates["name"] = name
    if email is not None:
        if get_by_email(db, email):
            raise HTTPException(
                status_code=HTTP_409_CONFLICT,
                detail="ja existe um usuario com esse email cadastrado"
            )
        updates["email"] = email.lower()
    if password is not None:
        updates["password"] = _hash_password(password)

    for k, v in updates.items():
        setattr(u, k, v)

    db.commit()
    db.refresh(u)

    return u


def delete(db, id: int):
    u = get_by_id(db, id)

    if not u:
        return False

    db.delete(u)
    db.commit()

    return True


def _hash_password(p: str) -> str:
    s = bcrypt.gensalt()
    h = bcrypt.hashpw(p.encode(), s)

    return h.decode()
