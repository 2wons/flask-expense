# -*- encoding: utf-8 -*-

from re import S, sub
from turtle import update
from flask import render_template, flash, url_for, request
from flask_login import login_required, current_user
from app.subscriptions import blueprint
from app.utils import HXRedirect

from app.subscriptions.forms import SubscriptionForm, create_subscription, update_subscription
from app.main.util import get_accounts, get_categories

from app import db
import sqlalchemy as sa
from app.models import Subscription, SubType

@blueprint.route('/', methods=['GET'])
@login_required
def home():

    return render_template('subs/_layout.html')

@blueprint.get('/active')
@login_required
def active():
    content = Subscription.get_subs_from_user(current_user.id, SubType.ACTIVE)
    current = 'active'
    return render_template('subs/table.html', content=content.all(), current=current)

@blueprint.get('/cancelled')
@login_required
def cancelled():
    content = Subscription.get_subs_from_user(current_user.id, SubType.CANCELLED)
    current = 'cancelled'

    return render_template('subs/table.html', content=content.all(), current=current)

@blueprint.get('/all')
@login_required
def all():
    content = Subscription.get_subs_from_user(current_user.id)
    current = 'all'

    return render_template('subs/table.html', content=content.all(), current=current)

@blueprint.get('/modal')
@login_required
def modal():
    sub_id = request.args.get('sub_id', default=None, type=int)
    return render_template('subs/add.html', sub_id=sub_id)

@blueprint.route('/add', methods=['GET', 'POST'])
@login_required
def add():

    form = SubscriptionForm()
    form.category.choices = get_categories('expense')
    form.account.choices = get_accounts()

    if form.validate_on_submit():
        subscription = create_subscription(form)

        db.session.add(subscription)
        db.session.commit()

        flash('Subscription added successfully', 'success')
        return HXRedirect(url_for('subs.home'))

    return render_template('subs/form.html', form=form)

@blueprint.route('/edit/<int:sub_id>', methods=['GET', 'PUT'])
@login_required
def edit(sub_id):

    sub = Subscription.query.get_or_404(sub_id)

    form = SubscriptionForm()
    form.category.choices = get_categories('expense')
    form.account.choices = get_accounts()
    print(form.account.choices)


    if form.validate_on_submit():
        sub = update_subscription(sub, form)
        db.session.commit()

        flash('Subscription updated successfully', 'success')
        return HXRedirect(url_for('subs.home'))

    form.fill_from_model(sub)
    form.submit.label.text = 'Update Subscription'
    
    return render_template('subs/form.html', form=form, sub_id=sub_id)

@blueprint.get('/upcoming')
@login_required
def upcoming():
    content = Subscription.get_upcoming(current_user.id)
    return render_template('subs/upcoming.html', content=content)

@blueprint.delete('/delete/<int:sub_id>')
@login_required
def delete(sub_id):
    sub = Subscription.query.get_or_404(sub_id)
    db.session.delete(sub)
    db.session.commit()
    return ""