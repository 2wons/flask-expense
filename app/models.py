from typing import Optional
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
