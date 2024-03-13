# -*- encoding: utf-8 -*-

from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required
from app.subscriptions import blueprint

from app.subscriptions.forms import SubscriptionForm
from app.main.util import get_accounts, get_categories

@blueprint.route('/', methods=['GET'])
@login_required
def home():
    """ form = SubscriptionForm()
    form.category.choices = get_categories()
    form.account.choices = get_accounts() """

    return render_template('subs/_layout.html')

@blueprint.get('/active')
@login_required
def active():
    content = 'active content'
    current = 'active'
    return render_template('subs/table.html', content=content, current=current)

@blueprint.get('/cancelled')
@login_required
def cancelled():
    content = 'cancelled content'
    current = 'cancelled'

    return render_template('subs/table.html', content=content, current=current)

@blueprint.get('/all')
@login_required
def all():
    content = 'all content'
    current = 'all'

    return render_template('subs/table.html', content=content, current=current)

@blueprint.get('/add')
@login_required
def add():
    form = SubscriptionForm()
    return render_template('subs/add.html', form=form)

@blueprint.get('/upcoming')
@login_required
def upcoming():
    content = 'upcoming content'
    return render_template('subs/upcoming.html', content=content)