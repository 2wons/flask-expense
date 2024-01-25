# -*- encoding: utf-8 -*-

from flask import render_template
from app.main import blueprint
from app.main.util import test_expenses

@blueprint.route('/home')
def home():
    return render_template('dashboard.html', segment='index')

@blueprint.route('/expenses')
def expenses():
    """manages expenses"""
    expenses = test_expenses()
    return render_template('expenses.html', segment='expenses', expenses=expenses)


@blueprint.route('/income')
def income():
    return render_template('income.html', segment='income')

@blueprint.route('/test')
def test():
    return render_template('index.html', segment='blank')

@blueprint.route('/accounts/cash')
def accounts_cash():
    return render_template('accounts.html', segment='accounts/cash')

@blueprint.route('/accounts/banks')
def accounts_banks():
    return render_template('accounts.html', segment='accounts/banks')

@blueprint.route('/accounts/credit')
def accounts_credit():
    return render_template('accounts.html', segment='accounts/credit')