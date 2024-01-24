# -*- encoding: utf-8 -*-

from flask import render_template
from app.main import blueprint

@blueprint.route('/home')
def home():
    return render_template('dashboard.html', segment='index')

@blueprint.route('/expenses')
def expenses():
    return render_template('expenses.html', segment='expenses')

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