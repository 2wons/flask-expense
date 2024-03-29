from typing import Optional, List
from decimal import Decimal
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.sql import case
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from enum import Enum

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

    budgets: so.Mapped[List['Budget']] = so.relationship(
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

    subscriptions: so.Mapped[List['Subscription']] = so.relationship(
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
    def get_expenses_from_user(cls, user_id):
        return cls.query.join(Account) \
                        .filter(Account.user_id == user_id) \
                        .filter(Record.type=='expense')
    
    @classmethod
    def get_incomes_from_user(cls, user_id):
        return cls.query.join(Account) \
                        .filter(Account.user_id == user_id) \
                        .filter(Record.type=='income')


    """ def __repr__(self) -> str:
        return '<Record, id: {},{}>'.format(self.id, self.category) """


class Budget(db.Model):

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    year: so.Mapped[int] = so.mapped_column(sa.Integer,
                                            index=True)
    month: so.Mapped[int] = so.mapped_column(sa.Integer,
                                             index=True)
    amount: so.Mapped[Decimal] = so.mapped_column(sa.Numeric(12,2))

    # store limits per category through json format
    # {<category>: <limit_value>}
    limits_dict: so.Mapped[Optional[dict|list]] = so.mapped_column(sa.JSON)

    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                                index=True)

    user: so.Mapped[User] = so.relationship(back_populates="budgets")

    __table_args__ = (
        sa.UniqueConstraint('year', 'month', 'user_id', name='unique_year_month_user'),
    )

    @classmethod
    def find_from_user_and_month(cls, user_id, year, month):
        return cls.query.filter_by(user_id=user_id, year=year, month=month).first()

class SubType(Enum):
    ACTIVE = 'active'
    CANCELLED = 'cancelled'

class BillingType(Enum):
    MONTHLY = 'Monthly'
    YEARLY = 'Yearly'

class Subscription(db.Model):

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    provider: so.Mapped[str] = so.mapped_column(sa.String(64),
                                                index=True)
    status: so.Mapped[str] = so.mapped_column(sa.String(16),
                                                index=True)
    price: so.Mapped[Decimal] = so.mapped_column(sa.Numeric(12,2))
    billing: so.Mapped[str] = so.mapped_column(sa.String(16),
                                                index=True)
    start_date: so.Mapped[date] = so.mapped_column(sa.Date)
    category: so.Mapped[str] = so.mapped_column(sa.String(32),
                                                index=True)

    # payment method
    account_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Account.id),
                                                  index=True)
    account: so.Mapped[Account] = so.relationship(back_populates='subscriptions')

    @classmethod
    def get_subs_from_user(cls, user_id, status: SubType=None):
        if not status:
            return cls.query.join(Account) \
                            .filter(Account.user_id == user_id)
        else:
            return cls.query.join(Account) \
                            .filter(Account.user_id == user_id) \
                            .filter(Subscription.status==status.value)
    
    @classmethod
    def get_next_date(cls, start_date, cycle: BillingType):
        current_date = datetime.now().date()

        next_date = None
        if (cycle == BillingType.MONTHLY.value):
            cycles = (current_date.year - start_date.year) * 12 + current_date.month - start_date.month
            next_date = start_date + relativedelta(months=cycles + 1)
        else:
            cycles = current_date.year - start_date.year
            next_date = start_date + relativedelta(years=cycles + 1)
        
        return next_date
    
    @classmethod
    def get_upcoming(cls, user_id):
        current_date = datetime.now().date()
        
        upcoming = []

        subs = cls.get_subs_from_user(user_id, SubType.ACTIVE)
        for sub in subs:
            next_date = cls.get_next_date(sub.start_date, sub.billing)
            if next_date <= (current_date + relativedelta(days=30)):
                upcoming.append({
                    'subscription': sub,
                    'next_date': next_date
                })
        
        return upcoming

    def __repr__(self) -> str:
        return '<Subscription {},{}>'.format(self.id, self.provider)