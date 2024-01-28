# -*- encoding: utf-8 -*-

from flask import render_template, flash, redirect, url_for, request
from app.auth import blueprint
from app.auth.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user
import sqlalchemy as sa
from app import db
from app.models import User
from urllib.parse import urlsplit

import sqlalchemy as sa
from app import db
from app.models import User

@blueprint.route('/', methods=['GET', 'POST'])
@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = LoginForm()

    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.email == form.email.data)
        )
        if user is None:
            flash('Invalid Email.', 'danger')
        elif not user.check_password(form.password.data):
            flash('Invalid Password', 'danger')
        else:
            login_user(user, remember=form.remember_me.data)
            
            # redirect user to previous locked page before login
            next_page = request.args.get('next')
            if not next_page or urlsplit(next_page).netloc != '':
                flash('Login Successful.', 'success')
                return redirect(url_for('main.home'))
            
            return redirect(next_page)

    return render_template('auth/login.html', form=form)


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():

        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash(f'Account created for {form.email.data}.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)

@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))