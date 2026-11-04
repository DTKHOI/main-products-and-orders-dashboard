from flask import redirect, render_template, url_for, session, request, flash, Blueprint
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from .models.models import User, Staff
from .utils import _t

profile = Blueprint('profile', __name__)

def edit_profile(form):
    user = db.session.get(User, session.get('id'))
    if not user:
        return redirect(url_for('users.login'))

    email = form.get('email', '').strip()
    phone = form.get('phone', '').strip()
    username = form.get('username', '').strip()
    avatar_url = form.get('avt_url', '').strip()

    if email and email != user.email:
        existed_email = User.query.filter(User.email == email).first()
        if existed_email and existed_email.id != user.id:
            flash(_t('toast_email_exists'), 'error')
            return redirect(url_for('profile.profile_page'))
        user.email = email
        session['email'] = email
            
    if phone != (user.phone or ''):
        if phone:
            existed_phone = User.query.filter(User.phone == phone).first()
            if existed_phone and existed_phone.id != user.id:
                flash(_t('toast_phone_exists'), 'error')
                return redirect(url_for('profile.profile_page'))
        user.phone = phone

    if username:
        user.username = username
        session['username'] = username

    if session.get('role') == 'staff' and user.staff_profile:
        user.staff_profile.phone = phone
        user.staff_profile.avatar_url = avatar_url  # Đồng bộ ảnh đại diện

    user.avatar_url = avatar_url

    db.session.commit()
    flash(_t('toast_prof_updated'), 'success')
    return redirect(url_for('profile.profile_page'))

def change_pass(form):
    user = db.session.get(User, session.get('id'))
    if not user:
        return redirect(url_for('users.login'))

    current_pass = form.get('current_password')

    if check_password_hash(user.password_hash, current_pass):
        new_pass = form.get('new_password')
        user.password_hash = generate_password_hash(new_pass)
        db.session.commit()
        flash(_t('toast_pass_updated'), 'success')
    else:
        flash(_t('toast_pass_incorrect'), 'error')

    return redirect(url_for('profile.profile_page'))

def change_language(form):
    new_lang = form.get('language', 'en')
    session['language'] = new_lang
    user = db.session.get(User, session.get('id'))

    if user:
        user.language = new_lang
        db.session.commit()

    flash(_t('toast_lang_updated'), 'success')
    return redirect(url_for('profile.profile_page'))

def change_theme(form):
    theme = form.get('theme')
    user = db.session.get(User, session.get('id'))

    if user:
        if theme in ['light', 'dark']:
            user.theme = theme
        else:
            user.theme = 'light'
        db.session.commit()

    flash(_t('toast_theme_updated'), 'success')
    return redirect(url_for('profile.profile_page'))

@profile.route("/profile", methods=['GET', 'POST'])
def profile_page():
    if not 'id' in session:
        return redirect(url_for('users.login'))

    user = db.session.get(User, session.get('id'))
    if not user:
        session.clear()
        return redirect(url_for('users.login'))

    if request.method == 'POST':
        form = request.form
        action = form.get('action')
        
        if action == 'edit_profile':
            return edit_profile(form)
        elif action == 'change_pass':
            return change_pass(form)
        elif action == 'change_language':
            return change_language(form)
        elif action == 'change_theme':
            return change_theme(form)
    
    return render_template('profile.html', user=user)
