# -*- encoding: utf-8 -*-

from flask import Blueprint

blueprint = Blueprint(
    'budgets',
    __name__,
    url_prefix='/budgets'
)

from app.budgets import routes