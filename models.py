from app import db, db2
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(16), index=True, unique=True)
    email: Mapped[str] = mapped_column(String(120), index=True)
    password_hashed = mapped_column(String(256))

    def set_password(self, password):
        self.password_hashed = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hashed, password)

    def __repr__(self):
        return 'Username: {}'.format(self.username)


def add_expense(username, category, item, price, date):
    expense_db = db2.cx['expenses']
    expense = {'category': category, 'item': item, 'price': price, 'date': date}
    return expense_db[username].insert_one(expense)
