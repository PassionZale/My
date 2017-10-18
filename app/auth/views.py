from datetime import datetime
from flask import render_template, redirect, flash, url_for, session, request
from flask_login import login_user, logout_user, login_required
from . import auth
from .forms import LoginForm, RegisterForm
from ..models import FlaskyConfigs
from .. import db


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = FlaskyConfigs.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            user.last_login_at = datetime.utcnow()
            db.session.commit()
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('console.index'))
        else:
            flash('用户名或密码错误')
    return render_template('auth/login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        configs = FlaskyConfigs(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data, )
        db.session.add(configs)
        db.session.commit()
        flash('欢迎, %s !您已注册成功,请登陆' % form.username.data)
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('注销成功.')
    return redirect(url_for('auth.login'))