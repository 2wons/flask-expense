# -*- encoding: utf-8 -*-

from flask import Blueprint

blueprint = Blueprint(
    'incomes',
    __name__,
    url_prefix='/incomes'
)

from app.incomes import routes