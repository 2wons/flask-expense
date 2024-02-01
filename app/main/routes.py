# -*- encoding: utf-8 -*-

from flask import render_template, flash, redirect, url_for, request
from app.main import blueprint
from app.main.util import get_accounts, get_categories
from app.main.forms import AccountForm, ExpenseForm, IncomeForm

import sqlalchemy as sa
from app import db
from app.models import Account, Expense, Income

from flask_login import current_user, login_required

@blueprint.route('/home')
@login_required
def home():
    return render_template('dashboard.html', segment='index')

@blueprint.route('/expenses', methods=['GET', 'POST'])
@login_required
def expenses():
    """manages expenses"""
    form = ExpenseForm()
    form.category.choices = get_categories()
    form.account.choices = get_accounts()

    if form.validate_on_submit():

        expense = Expense(
            name=form.name.data,
            amount=form.amount.data,
            date_spent=form.date_spent.data,
            category=form.category.data,
            note=form.note.data,
            account_id=form.account.data
        )
        db.session.add(expense)
        db.session.commit()
        flash("Expense added.", "success")
        return redirect(url_for('main.expenses'))

    page = request.args.get('page', 1, type=int)
    expenses = Expense.query \
                      .join(Account) \
                      .filter(Account.user_id == current_user.id) \
                      .order_by(Expense.date_spent.desc()) \
                      .paginate(page=page, per_page=10)
    
    return render_template('expenses.html', segment='expenses', expenses=expenses, form=form)


@blueprint.route('/income')
@login_required
def income():
    form = IncomeForm()
    form.category.choices = get_categories()
    form.account.choices = get_accounts()

    if form.validate_on_submit():

        income = Income(
            name=form.name.data,
            amount=form.amount.data,
            date_received=form.date_received.data,
            category=form.category.data,
            note=form.note.data,
            account_id=form.account.data
        )
        db.session.add(income)
        db.session.commit()
        flash("Income added.", "success")
        return redirect(url_for('main.income'))

    return render_template('income.html', segment='income')

@blueprint.route('/test', methods=['GET', 'POST'])
@login_required
def test():
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
        return redirect(url_for('main.test'))
    
    return render_template('index.html', segment='blank', form=form)

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