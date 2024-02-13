# -*- encoding: utf-8 -*-

from webbrowser import get
from flask import current_app, render_template, flash, redirect, url_for, abort
from app.main import blueprint
from app.main.util import calculate_percent_increase, get_categories, get_accounts
from app.main.forms import AccountForm, RecordForm

import sqlalchemy as sa
from app import db
from app.models import Account, Record

from flask_login import current_user, login_required
from datetime import datetime
import json


def calc_sum(month, year, record_type):
    return db.session.query(
        sa.func.sum(Record.amount)
    ).join(
        Account, Record.account_id == Account.id
    ).filter(
        Account.user_id == current_user.id, 
        Record.type == record_type, 
        sa.extract('month', Record.date) == month, 
        sa.extract('year', Record.date) == year
    ).scalar()

@blueprint.route('/home')
@login_required
def home():

    # retrieve top 3 categories of expense from current user
    top_3 = db.session.query(
        Record.category, sa.func.sum(Record.amount).label('total')
    ).join(
        Account, Record.account_id == Account.id
    ).filter(
        Account.user_id == current_user.id
    ).group_by(
        Record.category
    ).order_by(
        sa.desc('total')
    ).limit(3).all()

    # retrieve total expenses of user
    total_expenses = db.session.query(
        sa.func.sum(Record.amount)
    ).join(
        Account, Record.account_id == Account.id
    ).filter(
        Account.user_id == current_user.id,
        Record.type == 'expense'
    ).scalar()

    # retrieve total incomes of user
    total_incomes = db.session.query(
        sa.func.sum(Record.amount)
    ).join(
        Account, Record.account_id == Account.id
    ).filter(
        Account.user_id == current_user.id,
        Record.type == 'income'
    ).scalar()

    # retrieve total net worth of current user
    total_net_worth = db.session.query(
        sa.func.sum(Record.amount)
    ).join(
        Account, Record.account_id == Account.id
    ).filter(
        Account.user_id == current_user.id
    ).scalar()

    # retrieve the last 8 records of the user
    last_8_records = db.session.query(
        Record
    ).join(
        Account, Record.account_id == Account.id
    ).filter(
        Account.user_id == current_user.id
    ).order_by(
        Record.date.desc()
    ).limit(8).all()

    # retrieve the total expense of each month from the last 6 months
    monthly_expenses = db.session.query(
        sa.func.extract('month', Record.date).label('month'),
        sa.func.extract('year', Record.date).label('year'),
        sa.func.sum(Record.amount).label('total')
    ).join(
        Account, Record.account_id == Account.id
    ).filter(
        Account.user_id == current_user.id,
    ).group_by(
        sa.func.extract('month', Record.date),
        sa.func.extract('year', Record.date)
    ).order_by(
        sa.desc('year'),
        sa.desc('month')
    ).limit(6).all()

    if total_expenses is not None:
        total_expenses = total_expenses*-1

    # Get the current and previous month and year
    now = datetime.now()
    cur_month, cur_year = now.month, now.year
    prev_month, prev_year = (cur_month - 1, cur_year) if cur_month != 1 else (12, cur_year - 1)

    # Calculate the sums for the current and previous month
    cur_incomes = calc_sum(cur_month, cur_year, 'income')
    cur_expenses = calc_sum(cur_month, cur_year, 'expense')
    prev_incomes = calc_sum(prev_month, prev_year, 'income')
    prev_expenses = calc_sum(prev_month, prev_year, 'expense')

    if cur_incomes is None:
        cur_incomes = 0
    
    if cur_expenses is None:
        cur_expenses = 0

    if prev_incomes is None:
        prev_incomes = 0
    
    if prev_expenses is None:
        prev_expenses = 0

    # Calculate the percentage increase
    income_increase =  round(calculate_percent_increase(cur_incomes, prev_incomes), 2) \
        if prev_incomes else None
    expense_increase = round(calculate_percent_increase(cur_expenses, prev_expenses) *-1, 2) \
        if prev_expenses else None
    total_increase = round(calculate_percent_increase(cur_incomes - cur_expenses, prev_incomes - prev_expenses), 2) \
        if prev_incomes or prev_expenses else None
    
    # Create a list of the last 6 months
    # previous year is included in case prev year overlaps
    # - with the last 6 months
    last_6_months_years = [((now.month - i) % 12 or 12, now.year - (i >= now.month)) for i in range(6)]

    # Update monthly_expenses to ensure it always contains data for the last 6 months
    monthly_expenses = [
        next(({'month': m.month, 'year': m.year, 'total': m.total} for m in monthly_expenses if m.month == month and m.year == year), {'month': month, 'year': year, 'total': 0})
        for month, year in last_6_months_years
    ]

    # Convert the data to a dictionary
    data = {category: round(float(value),2 ) for category, value in top_3}

    # Convert the dictionary to JSON
    top3_json = json.dumps(data)

    return render_template(
        'dashboard.html',
        top_3=top_3,
        top3_json=top3_json,
        total_expenses=total_expenses,
        total_incomes=total_incomes,
        total_net_worth=total_net_worth,
        last_8_records=last_8_records,
        monthly_expenses=monthly_expenses,
        income_increase=income_increase,
        expense_increase=expense_increase,
        total_increase=total_increase)

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

@blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():

    return render_template('profile.html', me=current_user)

@blueprint.route('/view-accounts')
@login_required
def accounts_home():
    accounts = current_user.accounts
    return render_template('accounts.html', accounts=accounts)

@blueprint.route('/accounts/<int:account_id>', methods=['GET', 'POST'])
@login_required
def accounts_view(account_id):
    
    account = db.session.query(
        Account
    ).filter(
        Account.user_id == current_user.id,
        Account.id == account_id
    ).first()
    if account is None:
        abort(404)

    form = RecordForm()
    form.account.data = account_id
    form.category.choices = get_categories('income')
    form.account.choices = get_accounts()

    if form.type.data and form.type.data == 'expense':
        form.category.choices = get_categories('expense')

    if form.validate_on_submit():
        type = form.type.data
        record = Record(
            name=form.name.data,
            amount=form.amount.data,
            date=form.date_spent.data,
            account_id=form.account.data,
            category=form.category.data,
            note=form.note.data,
            type=type
        )
        db.session.add(record)
        db.session.commit()

        flash(f'{type} successfully added.', 'success')
        return redirect(url_for('main.accounts_view', account_id=account_id))

    account = db.session.query(
        Account
    ).filter(
        Account.user_id == current_user.id,
        Account.id == account_id
    ).first()
    if account is None:
        abort(404)

    transactions = db.session.query(
        Record
    ).filter(
        Record.account_id == account_id
    ).order_by(
        Record.date.desc()
    ).all()

    # get the total sum of the transactions
    balance = 0
    earnings = 0
    spent = 0
    for record in transactions:
        balance += record.amount
        if record.type == 'income':
            earnings += record.amount
        else:
            spent += record.amount
    
    name = account.name
    
    return render_template(
        'accounts_view.html',
        name=name,
        form=form,
        transactions=transactions,
        balance=balance,
        earnings=earnings,
        spent=spent)