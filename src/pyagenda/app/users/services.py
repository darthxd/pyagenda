from datetime import UTC, datetime

import bcrypt

from pyagenda.app.users.models import User


def get_by_id(db, id: int) -> User | None:
    """Recupera o user pelo ID"""
    return db.query(User).filter(User.id == id).first()


def get_by_email(db, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_all(db) -> list[User]:
    return db.query(User).all()


def create(db, name: str, email: str, password: str) -> User:
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


def _hash_password(p: str) -> str:
    s = bcrypt.gensalt()
    h = bcrypt.hashpw(p.encode(), s)

    return str(h)
