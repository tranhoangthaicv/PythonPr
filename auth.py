from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login.utils import login_required, login_user, logout_user , current_user
from sqlalchemy.sql.expression import true
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST','PUT','PATCH','DELETE','HEAD'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                # Ghi nhớ cookie người dùng mới sau khi session hết hạn
                login_user(user , remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password , try again', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html" , user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exist.',category='error')
        if len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 characters.', category='error')
        elif password1 != password2:
            flash('Password don\'t match', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            # Session kết nối tới database  và tiến hành thao tác
            db.session.add(new_user)
            db.session.commit()
            # Ghi nhớ cookie ngườu dùng mới sau khi session hết hạn
            login_user(new_user, remember=true)
            flash('Account created', category='success')
        return redirect(url_for('auth.login'))
    return render_template("sign_up.html", user=current_user)

