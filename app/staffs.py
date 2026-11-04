from flask import redirect, render_template, url_for, session, request, flash, Blueprint
from werkzeug.security import generate_password_hash
from app import db
from .models.models import User, Staff
from .utils import get_next_local_id, _t, send_email

staffs = Blueprint('staffs', __name__)

def create_staff_id(next_staff_no):
    return f"ST-{next_staff_no}"

def create_new_staff(form):
    full_name = form.get('name')
    gender = form.get('gender')
    email = form.get('email')
    phone = form.get('phone')
    password_hashed = generate_password_hash(form.get('password'))
    address = form.get('address')
    avt_url = form.get('avatar_url')

    existed_user = User.query.filter_by(email = email).first()
    existed_staff = Staff.query.filter_by(phone = phone).first()

    if existed_user or existed_staff:
        flash(_t('toast_staff_exists'), 'error')
        return redirect(url_for('staffs.staffs_page'))
    else:
        new_user_as_staff = User(email, password_hashed, full_name, role='staff')
        db.session.add(new_user_as_staff)
        db.session.commit()

        new_user_as_staff.phone = phone

        staff_info = Staff(new_user_as_staff.id, session.get('workspace_id'), full_name, phone, address, gender, avt_url)
        next_staff_no = get_next_local_id(Staff, session.get('workspace_id'))
        staff_info.local_id = next_staff_no
        staff_info.staff_code = f"ST-{next_staff_no:04d}"
        new_user_as_staff.avatar_url = staff_info.avatar_url

        db.session.add(staff_info)
        db.session.commit()
        return redirect(url_for('staffs.staffs_page'))


def edit_staff_info(form):
    staff_id = form.get('staff_id')
    email = form.get('email', '').strip()
    phone = form.get('phone', '').strip()
    password = form.get('password', '').strip()
    name = form.get('name', '').strip()

    staff_edited_info = db.session.get(Staff, staff_id)
    if not staff_edited_info:
        flash(_t('toast_staff_not_exist'), 'error')
        return redirect(url_for('staffs.staffs_page'))

    staff_edited_account = staff_edited_info.user_account
    admin_user = db.session.get(User, session.get('id'))

    old_email = staff_edited_account.email
    email_changed = False
    password_changed = False

    if email and email != old_email:
        exited_user_email = User.query.filter_by(email=email).first()
        if exited_user_email:
            flash(_t('toast_staff_exists'), 'error')
            return redirect(url_for('staffs.staffs_page'))
        staff_edited_account.email = email
        email_changed = True

    if phone and phone != staff_edited_info.phone:
        exited_staff_phone = Staff.query.filter_by(phone=phone).first()
        if exited_staff_phone:
            flash(_t('toast_staff_exists'), 'error')
            return redirect(url_for('staffs.staffs_page'))
        staff_edited_info.phone = phone
        staff_edited_account.phone = phone

    staff_edited_info.full_name = name or staff_edited_info.full_name
    staff_edited_info.gender = form.get('gender', staff_edited_info.gender)
    staff_edited_info.address = form.get('address', staff_edited_info.address)
    staff_edited_info.avatar_url = form.get('avatar_url', staff_edited_info.avatar_url)
    staff_edited_account.avatar_url = form.get('avatar_url', staff_edited_info.avatar_url)

    if password != '':
        staff_edited_account.password_hash = generate_password_hash(password)
        password_changed = True

    db.session.commit()

    # 6. GỬI MAIL THEO NGÔN NGỮ CỦA TỪNG NGƯỜI NHẬN (chỉ gửi khi commit thành công)
    if admin_user:
        admin_lang = getattr(admin_user, 'language', 'en') or 'en'
        staff_lang = getattr(staff_edited_account, 'language', 'en') or 'en'
        staff_name = staff_edited_info.full_name

        # Trường hợp A: Admin thay đổi email đăng nhập của nhân viên
        if email_changed:
            # Gửi về email mới của nhân viên (dùng staff_lang)
            sub_staff = _t('mail_staff_email_changed_subject', lang=staff_lang)
            body_staff = _t('mail_staff_email_changed_body', lang=staff_lang).format(
                staff_name=staff_name,
                old_email=old_email,
                new_email=email
            )
            send_email(email, sub_staff, body_staff)

            # Gửi xác nhận cho Admin (dùng admin_lang)
            sub_admin = _t('mail_admin_staff_email_changed_subject', lang=admin_lang)
            body_admin = _t('mail_admin_staff_email_changed_body', lang=admin_lang).format(
                admin_name=admin_user.username,
                staff_name=staff_name,
                old_email=old_email,
                new_email=email
            )
            send_email(admin_user.email, sub_admin, body_admin)

        # Trường hợp B: Admin cấp lại mật khẩu cho nhân viên
        if password_changed:
            # Gửi cho nhân viên (dùng staff_lang)
            sub_staff_pw = _t('mail_staff_pass_reset_by_admin_subject', lang=staff_lang)
            body_staff_pw = _t('mail_staff_pass_reset_by_admin_body', lang=staff_lang).format(
                staff_name=staff_name
            )
            send_email(staff_edited_account.email, sub_staff_pw, body_staff_pw)

            # Gửi xác nhận cho Admin (dùng admin_lang)
            sub_admin_pw = _t('mail_admin_staff_pass_reset_subject', lang=admin_lang)
            body_admin_pw = _t('mail_admin_staff_pass_reset_body', lang=admin_lang).format(
                admin_name=admin_user.username,
                staff_name=staff_name,
                staff_email=staff_edited_account.email
            )
            send_email(admin_user.email, sub_admin_pw, body_admin_pw)

    flash(_t('toast_staff_updated'), 'success')
    return redirect(url_for('staffs.staffs_page'))

def delete_staff(form):
    deleted_staff = db.session.get(Staff, form.get('id'))

    if deleted_staff:
        deleted_account = deleted_staff.user_account
        db.session.delete(deleted_staff)
        db.session.delete(deleted_account)
        db.session.commit()

        flash(_t('toast_staff_deleted'), 'success')
    else:
        flash(_t('toast_staff_del_fail'), 'error')

    return redirect(url_for('staffs.staffs_page'))

def filter_by_condition(form):
    condition = form.get('staff_gender')
    if condition:
        return Staff.query.filter_by(admin_id = session.get('workspace_id'), gender = condition).all()
    else: 
        admin = db.session.get(User, session.get('workspace_id'))
        return admin.managed_staffs if admin else []

@staffs.route("/staffs", methods=['GET', 'POST'])
def staffs_page():
    if not 'id' in session:
        return redirect(url_for('users.login'))

    if session.get('role') != 'admin':
        return "You do not have permission to perform this action.", 403

    form = request.form
    action = form.get('action')

    if request.method == 'POST':
        if action == 'add':
            return create_new_staff(form)
        elif action == 'edit':
            return edit_staff_info(form)
        elif action == 'delete':
            return delete_staff(form)

    staffs = filter_by_condition(form)
    
    keyword = form.get('search_staffs')
    if keyword:
        from sqlalchemy import or_
        searched_staffs = db.session.query(Staff).filter(
            Staff.admin_id == session.get('workspace_id'), 
            or_ (
                Staff.gender.like(f"%{keyword}%"),
                Staff.full_name.like(f"%{keyword}%"),
                Staff.address.like(f"%{keyword}%"),
                Staff.phone.like(f"%{keyword}%"),
                Staff.staff_code.like(f"%{keyword}%"),
            )
        ).all()
        
        staffs = list(set(searched_staffs))

    return render_template('staffs.html', staffs = staffs, user = db.session.get(User, session.get('id')))
