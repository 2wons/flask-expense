# -*- encoding: utf-8 -*-

from flask import render_template, flash, redirect, url_for, request
from app.main import blueprint
from app.main.util import get_accounts, get_categories
from app.main.forms import AccountForm, RecordForm

import sqlalchemy as sa
from app import db
from app.models import Account, Record

from flask_login import current_user, login_required

@blueprint.route('/home')
@login_required
def home():
    return render_template('dashboard.html')

@blueprint.route('/expenses', methods=['GET', 'POST'])
@login_required
def expenses():
    """manages expenses"""
    form = RecordForm()
    form.category.choices = get_categories("expense")
    form.account.choices = get_accounts()

    if form.validate_on_submit():

        expense = Record(
            name=form.name.data,
            amount=-form.amount.data,
            date=form.date_spent.data,
            category=form.category.data,
            note=form.note.data,
            type='expense',
            account_id=form.account.data
        )
        db.session.add(expense)
        db.session.commit()
        flash("Expense added.", "success")
        return redirect(url_for('main.expenses'))

    page = request.args.get('page', 1, type=int)

    expenses = Record.get_expenses_from_user(current_user.id) \
        .order_by(Record.date.desc()) \
        .paginate(page=page, per_page=10)
    
    return render_template('expenses.html', expenses=expenses, form=form)


@blueprint.route('/income', methods=['GET', 'POST'])
@login_required
def income():
    form = RecordForm()
    form.category.choices = get_categories("income")
    form.account.choices = get_accounts()

    if form.validate_on_submit():

        income = Record(
            name=form.name.data,
            amount=form.amount.data,
            date=form.date_spent.data,
            category=form.category.data,
            note=form.note.data,
            type='income',
            account_id=form.account.data
        )
        db.session.add(income)
        db.session.commit()
        flash("income added.", "success")
        return redirect(url_for('main.income'))

    page = request.args.get('page', 1, type=int)

    incomes = Record.get_incomes_from_user(current_user.id) \
        .order_by(Record.date.desc()) \
        .paginate(page=page, per_page=10)

    form.account.choices = get_accounts()
    return render_template('income.html', incomes=incomes, form=form)

@blueprint.route('/add-account', methods=['GET', 'POST'])
@login_required
def create_account():
    form = AccountForm()

    if form.validate_on_submit():

        account = Account(
            name=form.name.data,
            group=form.group.data,
            user=current_user
        )
        db.session.add(account)
        db.session.commit()

        flash('Account succesfully added.', 'success')
        return redirect(url_for('main.create_account'))
    
    return render_template('index.html', form=form)

@blueprint.route('/accounts/cash')
@login_required
def accounts_cash():
    return render_template('accounts.html')

@blueprint.route('/accounts/banks')
@login_required
def accounts_banks():
    return render_template('accounts.html')

@blueprint.route('/accounts/credit')
@login_required
def accounts_credit():
    return render_template('accounts.html')
