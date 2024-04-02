# -*- encoding: utf-8 -*-

from venv import create
from flask import render_template, flash, redirect, url_for, request, abort
from flask_migrate import current
from app.records import blueprint
from app.main.util import get_accounts, get_categories
from app.main.forms import RecordForm
from app.main.forms import create_record
from app.utils import HXRedirect


import sqlalchemy as sa
from app import db
from app.models import Account, Record

from flask_login import current_user, login_required

# TODO: remove
@blueprint.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return ""

@blueprint.get('/modal')
@login_required
def modal():
    prev_url = request.args.get('redirect', default=None, type=str)
    rtype = request.args.get('rtype', default=None, type=str)
    account_id = request.args.get('acid', default=None, type=int)
    legend = 'add record'
    return render_template('records/add.html', 
                           legend=legend,
                           rtype=rtype,
                           account_id=account_id, 
                           prev_url=prev_url)
    

@blueprint.route('/add', methods=['GET','POST'])
@login_required
def add():
    record_type = request.args.get('type', default=None, type=str)
    # passing an account id is optional
    acid = request.args.get('acid', default=None, type=int)
    prev_url = request.args.get('prev', default=None, type=str)

    form = RecordForm()

    if acid and not current_user.has_account(acid):
        abort(404)
    
    form.account.data = acid
    # TODO: throw error on invalid record type
    form.category.choices = get_categories(record_type)

    if form.validate_on_submit():
        """ record = create_record(form)
        db.session.add(record)
        db.session.commit() """
        flash(f'{type} successfully added.', 'success')
        return HXRedirect(url_for(prev_url))


    return render_template('records/form.html', form=form)