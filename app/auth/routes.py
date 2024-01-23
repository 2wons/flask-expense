# -*- encoding: utf-8 -*-

from flask import render_template
from app.auth import blueprint

@blueprint.route('/')
@blueprint.route('/login')
def login():
    return render_template('auth/login.html')


@blueprint.route('/register')
def register():
    return render_template('auth/register.html')