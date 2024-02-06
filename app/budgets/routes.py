from flask import render_template, flash, redirect, url_for, request, session, current_app, abort
from app.budgets import blueprint
from app.main.util import get_categories
from app.main.forms import RecordForm

import sqlalchemy as sa
from app import db
from app.models import Account, Record

from flask_login import current_user, login_required

budgets = {
    "🍕 Food": {
        "limit": 25000.00,
        "spent": 500.00
    },
    "📄 Bill": {
        "limit": 25000.00,
        "spent": 500.00
    },
    "🎉Entertainment": {
        "limit": 25000.00,
        "spent": 500.00
    },
    "✈ Travel": {
        "limit": 25000.00,
        "spent": 500.00
    },
    "🔍 Other": {
        "limit": 25000.00,
        "spent": 500.00
    },
}

@blueprint.route("/")
@login_required
def home():
    return render_template('budgets.html', budgets=budgets)

@blueprint.route("/new", methods=['GET', 'POST'])
@login_required
def create():
    return render_template('create_budget.html')

@blueprint.route("/<int:year>/<int:month>", methods=['GET', 'POST'])
@login_required
def view():
    return ""

