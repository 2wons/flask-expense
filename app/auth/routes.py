# -*- encoding: utf-8 -*-

from flask import render_template
from app.auth import blueprint

@blueprint.route('/')
def index():
    return render_template(('index.html'))