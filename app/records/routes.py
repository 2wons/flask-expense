# -*- encoding: utf-8 -*-

from venv import create
from flask import render_template, flash, redirect, url_for, request, abort
from app.records import blueprint
from app.main.util import get_accounts, get_categories
from app.main.forms import RecordForm
from app.main.forms import create_record
from app.utils import HXRedirect

from app import db
from app.models import  Record

from flask_login import current_user, login_required
import logging
logging.basicConfig(level=logging.DEBUG)

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
    legend = request.args.get('legend', default=None, type=str)
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
    logging.debug(f'record_type: {record_type}')
    logging.debug(f'acid: {acid}')
    logging.debug(f'prev_url: {prev_url}')

    form = RecordForm()
    form.type.data = 'expense'

    if acid and not current_user.has_account(acid):
        abort(404)
    
    form.account.data = acid
    # TODO: throw error on invalid record type
    form.account.choices = get_accounts()

    form.category.choices = get_categories(record_type)

    if form.validate_on_submit():
        form.type.data = record_type
        record = create_record(form)
        db.session.add(record)
        db.session.commit()
        flash(f'{type} successfully added.', 'success')
        return HXRedirect(prev_url)


    return render_template('records/form.html', form=form, rtype=record_type, account_id=acid, prev_url=prev_url)

@blueprint.route('/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    form = RecordForm()
    form.category.choices = get_categories("expense")
    form.account.choices = get_accounts()
    record = Record.query.get_or_404(id)

    redirect_url = url_for('incomes.home')
    if record.type == 'expense':
        redirect_url = url_for('expenses.home')
    
    if request.method == 'POST':
        if '_method' in request.form and request.form['_method'] == 'DELETE':
            db.session.delete(record)
            db.session.commit()
            flash('Record Successfully deleted', 'danger')
            return redirect(url_for(redirect_url))


    if form.validate_on_submit():
        record.name = form.name.data
        record.amount = form.amount.data
        if record.type == 'expense' and record.amount > 0:
            record.amount = -record.amount
        record.category = form.category.data
        record.date = form.date_spent.data
        record.note = form.note.data
        record.account_id = form.account.data

        db.session.commit()

        flash('Record Successfully updated', 'success')
        return redirect(url_for('records.edit', id=record.id))

    # pre-populate data with existing record details
    form.fill_from_record(record)
    form.submit.label.text = 'Update'
    legend = "Expense" if record.type == 'expense' else "Income"

    return render_template('record_item_page.html', form=form, item=record, legend=legend)

@blueprint.delete('/delete/<int:id>')
@login_required
def delete(id):
    sub = Record.query.get_or_404(id)
    db.session.delete(sub)
    db.session.commit()
    return ""