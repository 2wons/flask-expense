# -*- encoding: utf-8 -*-

from flask import Blueprint

blueprint = Blueprint(
    'budget',
    __name__,
    url_prefix='/budget'
)

from app.budgets import routes