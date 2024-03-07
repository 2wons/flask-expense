# -*- encoding: utf-8 -*-

from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required
from app.subscriptions import blueprint


@blueprint.route('/', methods=['GET'])
@login_required
def home():
    return render_template('new.html')




