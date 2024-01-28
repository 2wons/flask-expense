# -*- encoding: utf-8 -*-

from flask import render_template
from app.main import blueprint
from app.main.util import test_expenses

import sqlalchemy as sa
from app import db
from app.models import User

from flask_login import current_user, login_required

@blueprint.route('/home')
@login_required
def home():
    return render_template('dashboard.html', segment='index')

@blueprint.route('/expenses')
@login_required
def expenses():
    """manages expenses"""
    expenses = test_expenses()
    return render_template('expenses.html', segment='expenses', expenses=expenses)


@blueprint.route('/income')
@login_required
def income():
    return render_template('income.html', segment='income')

@blueprint.route('/test')
@login_required
def test():
    return render_template('index.html', segment='blank')

@blueprint.route('/accounts/cash')
@login_required
def accounts_cash():
    return render_template('accounts.html', segment='accounts/cash')

@blueprint.route('/accounts/banks')
@login_required
def accounts_banks():
    return render_template('accounts.html', segment='accounts/banks')

@blueprint.route('/accounts/credit')
@login_required
def accounts_credit():
    return render_template('accounts.html', segment='accounts/credit')