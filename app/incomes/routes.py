# -*- encoding: utf-8 -*-

from flask import render_template, flash, redirect, url_for, request, session, current_app, abort
from app.incomes import blueprint
from app.main.util import get_accounts, get_categories
from app.main.forms import RecordForm

import sqlalchemy as sa
from app import db
from app.models import Account, Record

from flask_login import current_user, login_required

# TODO: remove
@blueprint.route('/', methods=['GET', 'POST'])
@login_required
def home():
    """manages expenses"""
    form = RecordForm()
    form.category.choices = get_categories("income")
    form.account.choices = get_accounts()

    if form.validate_on_submit():

        expense = Record(
            name=form.name.data,
            amount=form.amount.data,
            date=form.date_spent.data,
            category=form.category.data,
            note=form.note.data,
            type='income',
            account_id=form.account.data
        )
        db.session.add(expense)
        db.session.commit()
        flash("income added.", "success")
        return redirect(url_for('incomes.home'))

    page = request.args.get('page', 1, type=int)

    incomes = Record.get_incomes_from_user(current_user.id)

    count = incomes.count()
    # get the total sum of all incomes from user
    sum = incomes.with_entities(
        sa.func.sum(Record.amount).label('total_amount')).scalar()

    paginated_results = incomes.order_by(Record.date.desc()) \
        .paginate(page=page, per_page=10)

    return render_template('expenses.html', 
                           results=paginated_results,
                           legend="Income",
                           count=count, 
                           sum=sum, 
                           form=form)


@blueprint.route('<int:record_id>/', methods=['GET','POST'])
@login_required
def income(record_id):
    form = RecordForm()
    form.category.choices = get_categories("income")
    form.account.choices = get_accounts()
    record = Record.query.get_or_404(record_id)
    account = Account.query.filter(Account.id == record.account_id).first()
    #if account.user != current_user or record.type != 'expense':
        #abort(404)
    
    if request.method == 'POST':
        if '_method' in request.form and request.form['_method'] == 'DELETE':
            db.session.delete(record)
            db.session.commit()
            flash('Record Successfully deleted', 'danger')
            return redirect(url_for('incomes.home'))


    if form.validate_on_submit():
        record.name = form.name.data
        record.amount = form.amount.data
        record.category = form.category.data
        record.date = form.date_spent.data
        record.note = form.note.data
        record.account_id = form.account.data
        db.session.commit()
        flash('Record Successfully updated', 'success')
        return redirect(url_for('incomes.income', record_id=record.id))

    # pre-populate data with existing record details
    form.fill_from_record(record)
    form.submit.label.text = 'Update'

    return render_template('record_item_page.html', form=form, item=record)
