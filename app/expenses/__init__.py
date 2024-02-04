# -*- encoding: utf-8 -*-

from flask import Blueprint

blueprint = Blueprint(
    'expenses',
    __name__,
    url_prefix='/expenses'
)

from app.expenses import routes