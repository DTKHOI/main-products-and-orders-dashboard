# new_pass.py
import random
from flask import redirect, render_template, url_for, session, request, flash, Blueprint
from werkzeug.security import generate_password_hash
from app import db
from .models.models import User
from .utils import _t, send_email, send_password_change_alert
import time

new_pass = Blueprint('new_pass', __name__)

@new_pass.route("/forgot_pass", methods=['GET', 'POST'])
def forgot_page():
    # Xóa trạng thái xác thực cũ mỗi khi truy cập lại trang Quên mật khẩu
    session['otp_verified'] = False

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        user = User.query.filter_by(email=email).first()

        if not user:
            flash(_t('err_email'), "error")
            return redirect(url_for('new_pass.forgot_page'))

        # otp = str(random.randint(100000, 999999))
        import secrets
        otp = f"{secrets.randbelow(900000) + 100000}" 
        session['reset_email'] = email
        session['reset_otp'] = otp
        session['otp_verified'] = False
        session['otp_created_at'] = time.time()
        session['otp_attempts'] = 0

        user_lang = getattr(user, 'language', None) or session.get('language', 'en')

        subject = _t('mail_otp_subject', lang=user_lang)
        content = _t('mail_otp_body', lang=user_lang).format(username=user.username, otp=otp)
        
        # Kiểm tra kết quả gửi mail thực tế
        mail_sent = send_email(email, subject, content)

        if mail_sent:
            flash(_t('toast_otp_sent', lang=user_lang), "success")
        else:
            flash(_t('toast_otp_send_fail', lang=user_lang), "warning")

        # BẮT BUỘC chuyển sang trang nhập mã OTP (otp.html)
        return redirect(url_for('new_pass.otp_page'))

    return render_template('forgot_pass.html')


@new_pass.route("/confirm_otp", methods=['GET', 'POST'])
def otp_page():
    if 'reset_email' not in session or not session.get('reset_otp'):
        return redirect(url_for('new_pass.forgot_page'))

    user = User.query.filter_by(email=session['reset_email']).first()
    user_lang = getattr(user, 'language', None) or session.get('language', 'en')

    if request.method == 'POST':
        action = request.form.get('action')

        if time.time() - session.get('otp_created_at', 0) > 300: # 5 phút hết hạn
            session.pop('reset_otp', None)
            flash(_t('toast_otp_expired', lang=user_lang), "error")
            return redirect(url_for('new_pass.forgot_page'))
        
        session['otp_attempts'] = session.get('otp_attempts', 0) + 1
        if session['otp_attempts'] > 5: # Tối đa 5 lần thử sai
            session.pop('reset_otp', None)
            flash(_t('toast_otp_max_attempts', lang=user_lang), "error")
            return redirect(url_for('new_pass.forgot_page'))

        if action == 'resend':
            otp = str(random.randint(100000, 999999))
            session['reset_otp'] = otp
            subject = _t('mail_otp_subject', lang=user_lang)
            content = _t('mail_otp_body', lang=user_lang).format(
                username=user.username if user else "User",
                otp=otp
            )
            mail_sent = send_email(session['reset_email'], subject, content)
            if mail_sent:
                flash(_t('toast_otp_resent', lang=user_lang), "success")
            else:
                flash(_t('toast_otp_resend_fail', lang=user_lang), "warning")
            return redirect(url_for('new_pass.otp_page'))

        entered_otp = request.form.get('otp_code', '').strip()
        if entered_otp and entered_otp == session.get('reset_otp'):
            session['otp_verified'] = True
            flash(_t('toast_otp_verified', lang=user_lang), "success")
            return redirect(url_for('new_pass.new_pass_page'))
        else:
            flash(_t('toast_otp_invalid', lang=user_lang), "error")
            return redirect(url_for('new_pass.otp_page'))

    return render_template('otp.html')


@new_pass.route("/new_password", methods=['GET', 'POST'])
def new_pass_page():
    # BẢO VỆ CHẶT CHẼ: Chưa nhập đúng OTP thì tuyệt đối không cho vào trang này
    if not session.get('otp_verified') or 'reset_email' not in session:
        flash(_t('toast_otp_verify_first'), "error")
        return redirect(url_for('new_pass.forgot_page'))

    if request.method == 'POST':
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if password != confirm_password or len(password) < 8:
            flash(_t('err_password_mismatch'), "error")
            return redirect(url_for('new_pass.new_pass_page'))

        user = User.query.filter_by(email=session['reset_email']).first()
        if user:
            user.password_hash = generate_password_hash(password)
            db.session.commit()

            send_password_change_alert(user, db.session, User)

        # Xóa sạch phiên sau khi đổi mật khẩu thành công
        session.pop('reset_email', None)
        session.pop('reset_otp', None)
        session.pop('otp_verified', None)

        flash(_t('toast_pass_updated'), "success")
        return redirect(url_for('users.login'))

    return render_template('new_pass.html')
