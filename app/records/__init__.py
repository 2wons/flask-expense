# -*- encoding: utf-8 -*-

from flask import Blueprint

blueprint = Blueprint(
    'records',
    __name__,
    url_prefix='/r'
)

from app.records import routes