from turtle import back
from typing import Optional, List
from decimal import Decimal
from datetime import date
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    last_name: so.Mapped[str] = so.mapped_column(sa.String(64), 
                                                 index=True) 
    first_name: so.Mapped[str] = so.mapped_column(sa.String(64),
                                                  index=True) 
    email: so.Mapped[str] = so.mapped_column(sa.String(120), 
                                             unique=True)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(256))

    accounts: so.Mapped[List['Account']] = so.relationship(
        back_populates='user', cascade='all, delete-orphan'
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {},{}>'.format(self.id, self.email)

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class Account(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64))
    group: so.Mapped[str] = so.mapped_column(sa.String(64),
                                             index=True)
    metadata_json: so.Mapped[Optional[dict|list]] = so.mapped_column(sa.JSON)

    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                               index=True)
    user: so.Mapped[User] = so.relationship(back_populates="accounts")

    records: so.Mapped[List['Record']] = so.relationship(
        back_populates='account', cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return '<Account {},{}>'.format(self.id, self.name)

class Record(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64),
                                            index=True)
    amount: so.Mapped[Decimal] = so.mapped_column(sa.Numeric(12,2))
    date: so.Mapped[date] = so.mapped_column(sa.Date)
    category: so.Mapped[str] = so.mapped_column(sa.String(32),
                                                index=True)
    type: so.Mapped[str] = so.mapped_column(sa.String(16),
                                             index=True)
    note: so.Mapped[Optional[str]] = so.mapped_column(sa.String(80))

    account_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Account.id),
                                                  index=True)
    account: so.Mapped[Account] = so.relationship(back_populates='records')

    @classmethod
    def get_expenses(cls):
        return cls.query.filter_by(type='expense').all()
    
    @classmethod
    def get_incomes(cls):
        return cls.query.filter_by(type='income').all()


    def __repr__(self) -> str:
        return '<Account {},{}>'.format(self.id, self.category)

class Expense(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64),
                                            index=True)
    amount: so.Mapped[Decimal] = so.mapped_column(sa.Numeric(12, 2))
    date_spent: so.Mapped[date] = so.mapped_column(sa.Date)
    category: so.Mapped[str] = so.mapped_column(sa.String(32),
                                                index=True)
    note: so.Mapped[Optional[str]] = so.mapped_column(sa.String(80))
    
    account_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Account.id),
                                                  index=True)
    account: so.Mapped[Account] = so.relationship(back_populates='expenses')

    def __repr__(self) -> str:
        return '<Expense {},{}>'.format(self.id, self.category)

class Income(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64),
                                            index=True)
    amount: so.Mapped[Decimal] = so.mapped_column(sa.Numeric(12, 2))
    date_received: so.Mapped[date] = so.mapped_column(sa.Date)
    category: so.Mapped[str] = so.mapped_column(sa.String(32),
                                                index=True)
    note: so.Mapped[Optional[str]] = so.mapped_column(sa.String(80))
    
    account_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Account.id),
                                                  index=True)
    account: so.Mapped[Account] = so.relationship(back_populates='incomes')

    def __repr__(self) -> str:
        return '<Income {},{}>'.format(self.id, self.category)