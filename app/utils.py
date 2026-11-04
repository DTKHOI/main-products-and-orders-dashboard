from flask import session
import os
import smtplib
from email.message import EmailMessage
try:
    from translations import TRANSLATIONS
except ImportError:
    from .translations import TRANSLATIONS
from sqlalchemy import func
from .models.models import Product, Order, Staff
from app import db

def _t(key, lang=None):
    """
    Nếu truyền lang (khi gửi mail): dùng trực tiếp lang của người nhận.
    Nếu không truyền lang: lấy từ session hiện tại.
    """
    if not lang:
        lang = session.get('language', 'en')
    return TRANSLATIONS.get(lang, {}).get(key, TRANSLATIONS.get('en', {}).get(key, key))

def get_next_local_id(model_class, admin_id):
    """
    Lấy số thứ tự tiếp theo dành riêng cho một Admin.
    Bắt đầu từ 1 nếu chưa có dữ liệu nào.
    Dù có xóa bản ghi thì số tiếp theo vẫn luôn tăng, không bao giờ bị lùi.
    """
    max_id = db.session.query(func.max(model_class.local_id))\
                       .filter(model_class.admin_id == admin_id)\
                       .scalar()
    return 1 if max_id is None else max_id + 1

def send_email(to_email, subject, content):
    """Hàm gửi email qua Gmail SMTP SSL"""
    sender_email = os.environ.get("MAIL_USERNAME")
    sender_password = os.environ.get("MAIL_PASSWORD")

    # In ra Terminal để luôn luôn thấy mã OTP dù mạng lỗi
    print(f"\n==================== [DEBUG EMAIL] ====================")
    print(f"To: {to_email}")
    print(f"Subject: {subject}")
    print(f"Content:\n{content}")
    print(f"=======================================================\n")

    if not sender_email or not sender_password:
        print("[LỖI EMAIL]: Chưa cấu hình MAIL_USERNAME hoặc MAIL_PASSWORD trong môi trường (.env)!")
        return False

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = f"ProductFlow System <{sender_email}>"
    msg["To"] = to_email
    msg.set_content(content)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"[LỖI SMTP KHI GỬI EMAIL]: {e}")
        return False


def send_password_change_alert(user, db_session, User_model):
    """
    Gửi thông báo đổi mật khẩu theo đúng ngôn ngữ cài đặt của từng người nhận:
    1. Gửi cho user đổi mật khẩu (dùng user.language).
    2. Nếu là Staff: gửi thêm cho Admin quản lý (dùng admin.language).
    """
    user_lang = getattr(user, 'language', 'en') or 'en'
    subject_user = _t('mail_pass_changed_subject', lang=user_lang)
    body_user = _t('mail_pass_changed_body', lang=user_lang).format(username=user.username)
    send_email(user.email, subject_user, body_user)

    if user.role == 'staff' and user.staff_profile:
        admin_user = db_session.get(User_model, user.staff_profile.admin_id)
        if admin_user:
            admin_lang = getattr(admin_user, 'language', 'en') or 'en'
            subject_admin = _t('mail_admin_staff_pass_alert_subject', lang=admin_lang).format(
                staff_name=user.staff_profile.full_name
            )
            body_admin = _t('mail_admin_staff_pass_alert_body', lang=admin_lang).format(
                admin_name=admin_user.username,
                staff_name=user.staff_profile.full_name,
                staff_code=user.staff_profile.staff_code,
                staff_email=user.email
            )
            send_email(admin_user.email, subject_admin, body_admin)