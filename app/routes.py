from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.models import db, User

# Khởi tạo Blueprint
main_bp = Blueprint("main", __name__)

# TRANG CHỦ (YÊU CẦU ĐĂNG NHẬP & PHÂN QUYỀN)
@main_bp.route("/")
def index():
    # Kiểm tra xem người dùng đã đăng nhập chưa
    if 'user_id' in session:
        # Lấy thông tin người dùng từ CSDL
        current_user = User.query.get(session['user_id'])
        
        # Dùng render_template để hiển thị file index.html 
        # và truyền đối tượng current_user sang đó với tên là 'user'
        return render_template("index.html", user=current_user)
    else:
        # Nếu chưa đăng nhập, bắt buộc quay về trang login
        return redirect(url_for('main.login'))

# TRANG ĐĂNG NHẬP
@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # 1. Tìm tài khoản trong Database
        user = User.query.filter_by(username=username).first()
        
        # 2. Nếu tài khoản tồn tại VÀ mật khẩu băm khớp nhau
        if user and check_password_hash(user.password, password):
            # Lưu ID của người dùng vào Session (Đăng nhập thành công)
            session['user_id'] = user.id
            return redirect(url_for('main.index'))
        else:
            return "Sai tên đăng nhập hoặc mật khẩu! Vui lòng thử lại."
            
    return render_template("login.html")

# TRANG ĐĂNG XUẤT
@main_bp.route("/logout")
def logout():
    # Xóa 'user_id' khỏi session
    session.pop('user_id', None)
    return redirect(url_for('main.login'))

# TRANG ĐĂNG KÝ
@main_bp.route("/register", methods=["GET", "POST"])
def register():
    # Nếu người dùng bấm nút Đăng ký (Phương thức POST)
    if request.method == "POST":
        # 1. Lấy dữ liệu từ form thông qua thuộc tính 'name' của thẻ input
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        
        # 2. Kiểm tra xem tên đăng nhập này đã tồn tại trong DB chưa
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Tên đăng nhập đã tồn tại. Vui lòng chọn tên khác!"
            
        # 3. YÊU CẦU BẮT BUỘC: Mã hóa mật khẩu
        hashed_password = generate_password_hash(password)
        
        # 4. Khởi tạo đối tượng User mới với dữ liệu đã băm
        new_user = User(username=username, password=hashed_password, email=email, role='Staff')
        
        # 5. Lưu vào Cơ sở dữ liệu
        db.session.add(new_user)
        db.session.commit()
        
        return f"Đăng ký thành công tài khoản: {username}. Mật khẩu đã được mã hóa an toàn!"
        
    # Nếu chỉ truy cập link bình thường (GET), hiển thị form HTML
    return render_template("register.html")