from datetime import UTC, datetime, timedelta

import jwt

from pyagenda.app.users.models import User

from .config import config


def generate_token(u: User) -> str:
    payload = {
        "sub": u.id,
        "iat": datetime.now(tz=UTC),
        "exp": datetime.now(tz=UTC) + timedelta(hours=24),
    }

    return jwt.encode(payload, config.JWT_SECRET, algorithm="HS256")
