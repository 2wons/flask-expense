# -*- encoding: utf-8 -*-

from flask import Blueprint

blueprint = Blueprint(
    'subs',
    __name__,
    url_prefix='/subscriptions'
)

from app.subscriptions import routes