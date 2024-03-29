from calendar import month_name
from flask import render_template, flash, redirect, url_for, request, session, current_app, abort
from app.budgets import blueprint
from app.budgets.util import get_category_emote
from app.budgets.forms import BudgetForm

import sqlalchemy as sa
from app import db
from app.models import Account, Record, Budget
from collections import defaultdict

from flask_login import current_user, login_required
from calendar import month_name

@blueprint.route("/")
@login_required
def home():
    # get the latest budget
    latest_budget = db.session.query(
        Budget
    ).filter(
        Budget.user == current_user
    ).order_by(
        Budget.year.desc(),
        Budget.month.desc()
    ).first()

    if latest_budget:
        # view latest added budget if there is one
        return redirect(url_for('budgets.view', year=latest_budget.year, month=latest_budget.month))
    
    months = []
    # render empty budget page if user has no budgets at all
    return render_template('budgets/budgets_empty.html', legend='empty', year=0, all_budgets=months, month=0 )


@blueprint.route("/new", methods=['GET', 'POST'])
@login_required
def create():
    form = BudgetForm()

    if form.validate_on_submit():
        if Budget.find_from_user_and_month(
            current_user.id, int(form.year.data), int(form.month.data)
        ):
            flash(f'Budget for {month_name[int(form.month.data)]} {form.year.data} already exists', 'danger')
            return redirect(url_for('budgets.create'))
        
        limits = form.limits_to_dict()
        amount = form.limit_sum()
        year = int(form.year.data)
        month = int(form.month.data)
        budget = Budget(
            year = year,
            month = month,
            amount = amount,
            limits_dict = limits,
            user = current_user
        )
        db.session.add(budget)
        db.session.commit()
        
        flash(f'Budget for {month} {year} created', 'success')
        return redirect(url_for('budgets.view', year=year, month=month))

    return render_template('budgets/budget_setting.html', form=form, legend="create")

@blueprint.route("/<int:year>/<int:month>/setting", methods=['GET', 'POST'])
@login_required
def setting(year, month):

    # retreive budget instance for the given year and month
    budget = db.session.query(
        Budget
    ).filter(
        Budget.user == current_user,
        Budget.year == year,
        Budget.month == month
    ).first()
    if budget is None:
        abort(404)

    form = BudgetForm()
    form.month.data = str(month)
    form.year.data = str(year)

    if form.validate_on_submit():
        budget.limits_dict = form.limits_to_dict()
        budget.amount = form.limit_sum()
        
        db.session.commit()
        
        flash(f'Budget for {month_name[month]} {year} updated', 'success')
        return redirect(url_for('budgets.view', year=year, month=month))
    else:
        current_app.logger.debug(form.errors)
    
    form.fill_from_budget(budget)
    form.submit.label.text = "Update"

    return render_template('budgets/budget_setting.html', form=form, legend="update", month=month, year=year)

@blueprint.route("/<int:year>/<int:month>", methods=['GET', 'POST'])
@login_required
def view(year, month):
    current_app.logger.debug(month)

    # retreive budget instance for the given year and month
    budget = db.session.query(
        Budget
    ).filter(
        Budget.user == current_user,
        Budget.year == year,
        Budget.month == month
    ).first()
    if budget is None:
        abort(404)

    # retreive expenses by category for the given year and month
    expenses_by_category = db.session.query(
        Record.category,
        sa.func.sum(Record.amount).label('total_amount'),
    ).join(Account)                                     \
    .filter(
        Account.user == current_user,
        Record.type == 'expense',
        sa.extract('year', Record.date) == year,
        sa.extract('month', Record.date) == month
    ).group_by(
        Record.category
    ).all()

    # retreive all months for for the given year with budgets
    budgets_year = db.session.query(
        Budget.month
    ).filter(
        Budget.user == current_user,
        Budget.year == year
    ).distinct().order_by(Budget.month).all()
    # transform to dictionary
    budgets_year = [t_month[0] for t_month in budgets_year]
    
    # retrieve all of the user's budgets, select only the year and months
    all_budgets = db.session.query(
        Budget.year,
        Budget.month
    ).filter(
        Budget.user == current_user
    ).distinct().order_by(Budget.month).all()
    # transform to dictionary
    budgets_dict = defaultdict(list)
 
    for x_year, y_month in all_budgets:
        budgets_dict[x_year].append(y_month)

    # Initialize budgets dictionary with category limits from budget_instance
    budgets = defaultdict(lambda: {"limit": 0, "spent": 0})
    for category, limit in budget.limits_dict.items():
        if limit != 0:
            budgets[get_category_emote(category)]["limit"] = float(limit)

    # Update the "spent" values based on expenses_by_category
    for category, total_amount in expenses_by_category:
        category_with_emoji = get_category_emote(category.lower())
        
        if category_with_emoji in budgets: 
            budgets[category_with_emoji]["spent"] = float(total_amount) * -1
    
    # month name of month 
    month_names = month_name[month]
    total_spent = sum([budgets[category]["spent"] for category in budgets])
    remaining = float(budget.amount) - total_spent
    
    return render_template(
        'budgets/budgets.html',
        budgets=budgets, 
        month_name=month_names, 
        month=month,
        year=year,
        remaining=remaining,
        total_spent=total_spent, 
        all_budgets=budgets_dict)

