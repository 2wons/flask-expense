# -*- encoding: utf-8 -*-
from flask import Blueprint

blueprint = Blueprint(
    'auth',
    __name__
)

from app.auth import routes