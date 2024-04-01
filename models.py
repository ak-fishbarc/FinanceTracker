from app import db
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(16), index=True, unique=True)
    email: Mapped[str] = mapped_column(String(120), index=True)
    password_hashed = mapped_column(String(256))

    def __repr__(self):
        return 'Username: {}'.format(self.username)

