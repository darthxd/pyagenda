from pyagenda.app.users.models import User


def get_user_by_id(db, id: int) -> User | None:
    """Recupera o user pelo ID"""
    return db.query(User).filter(User.id == id).first()
