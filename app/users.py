import re
from flask import redirect, render_template, url_for, session, request, flash, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from .models.models import User
from .utils import _t

users = Blueprint('users', __name__)

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def is_strong_password(password):
    if not password or len(password) < 8:
        return False
    return (any(c.isupper() for c in password) and
            any(c.islower() for c in password) and
            any(c.isdigit() for c in password) and
            any(not c.isalnum() for c in password))

@users.route("/register", methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        form = request.form
        username = form.get('username', '').strip()
        email = form.get('email', '').strip()
        password = form.get('password', '')
        confirm_password = form.get('confirm_password', '')

        if not username:
            flash(_t('err_full_name'), 'error')
            return redirect(url_for('users.register'))

        if not email or not EMAIL_REGEX.match(email):
            flash(_t('err_email'), 'error')
            return redirect(url_for('users.register'))

        if not is_strong_password(password):
            flash(_t('err_password_short'), 'error')
            return redirect(url_for('users.register'))

        if password != confirm_password:
            flash(_t('err_password_mismatch'), 'error')
            return redirect(url_for('users.register'))

        user = User.query.filter_by(email=email).first()
        if user:
            flash(_t('toast_email_exists'), 'error')
            return redirect(url_for('users.register'))

        password_hash = generate_password_hash(password)
        new_user = User(email, password_hash, username)

        db.session.add(new_user)
        db.session.commit()

        flash(_t('toast_account_created'), "success")

        return redirect(url_for('users.login'))

    return render_template("register.html")

@users.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = request.form
        email = form.get('email')
        password = form.get('password')
        remember_me = form.get('remember-me')


        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password_hash, password):
                session.clear()
                session['email'] = user.email
                session['role'] = user.role
                session['id'] = user.id
                session['username'] = user.username
                session['language'] = getattr(user, 'language', 'en') or 'en'

                if user.role == 'admin':
                    session['workspace_id'] = user.id
                elif user.role == 'staff':
                    # lấy admin_id từ bảng staff thông qua relationship staff_profile được khai báo ở model User
                    staff_record = user.staff_profile
                    session['workspace_id'] = staff_record.admin_id

                if remember_me:
                    session.permanent = True
                else:
                    session.permanent = False

                flash('You have successfully logged in.', 'success')
                return redirect(url_for('users.login'))
            else:
                flash("Invalid email or password.", 'error')
                return redirect(url_for('users.login'))
        else:
            flash('Email is not registered.', 'error')
            return redirect(url_for('users.login'))
    
    if 'email' in session:
        if session.get('role') == 'admin':
            return redirect(url_for('dashboard.dashboard_page'))
        else: return redirect(url_for('products.products_page'))


    return render_template("login.html")

@users.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('users.login'))

@users.route("/")
def landing_page():
    return render_template('index.html', user = db.session.get(User, session.get('id')))
