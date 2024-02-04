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
