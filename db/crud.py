from sqlalchemy.orm import Session
from passlib.context import CryptContext
from passlib.hash import bcrypt

from . import models, schemas

crypt = CryptContext(schemes=["bcrypt"])


def get_user(db: Session, username: str) -> models.User | None:
    return db.query(models.User).filter(models.User.username == username).first()


def verify_password(db: Session, username: str, password: str) -> bool:
    user = db.query(models.User).filter(
        models.User.username == username).first()
    if user and bcrypt.verify(password, user.hashed_password):
        return True
    return False


def create_user(db: Session, user: schemas.UserCreate) -> None:
    hashed_password = bcrypt.hash(user.password)
    db_user = models.User(username=user.username,
                          hashed_password=hashed_password,
                          name=user.name, email=user.email, lastname=user.lastname)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
