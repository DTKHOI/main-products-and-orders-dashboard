from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)

from app.models.models import (
    db,
    User,
    Product,
    Category,
    OrderDetail,
)

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
# =========================================================
# PRODUCT - HIỂN THỊ DANH SÁCH
# =========================================================

@main_bp.route("/products/", methods=["GET"])
def product_list():

    products = Product.query.order_by(
        Product.id.desc()
    ).all()

    categories = {
        category.id: category.name
        for category in Category.query.all()
    }

    return render_template(
        "products.html",
        products=products,
        categories=categories
    )


# =========================================================
# PRODUCT - THÊM
# =========================================================

@main_bp.route(
    "/products/create",
    methods=["POST"]
)
def create_product():

    # -------------------------
    # Lấy dữ liệu từ form
    # -------------------------

    name = request.form.get(
        "name",
        ""
    ).strip()

    price = request.form.get(
        "price",
        ""
    ).strip()

    stock = request.form.get(
        "stock",
        ""
    ).strip()

    category_name = request.form.get(
        "category",
        ""
    ).strip()

    status = request.form.get(
        "status",
        "active"
    ).strip().lower()

    image_url = request.form.get(
        "image_url",
        ""
    ).strip()
    # -------------------------
    # Kiểm tra tên
    # -------------------------

    if not name:
        return (
            "Tên sản phẩm không được để trống!",
            400
        )

    # -------------------------
    # Kiểm tra giá và số lượng
    # -------------------------

    try:

        product_price = float(price)
        product_stock = int(stock)

    except (ValueError, TypeError):

        return (
            "Giá hoặc số lượng sản phẩm không hợp lệ!",
            400
        )

    if product_price < 0:

        return (
            "Giá sản phẩm không được âm!",
            400
        )

    if product_stock < 0:

        return (
            "Số lượng sản phẩm không được âm!",
            400
        )

    # -------------------------
    # Status
    # -------------------------

    if status == "inactive":
        product_status = "Inactive"
    else:
        product_status = "Active"

    # -------------------------
    # Category
    # -------------------------

    category_id = None

    if category_name:

        category = Category.query.filter_by(
            name=category_name
        ).first()

        if category:

            category_id = category.id

    # -------------------------
    # Tạo Product
    # -------------------------

    product = Product(
        name=name,
        category_id=category_id,
        price=product_price,
        stock=product_stock,
        image_url=(
            image_url
            if image_url
            else None
        ),
        status=product_status
    )

    db.session.add(product)

    db.session.commit()

    return redirect(
        url_for(
            "main.product_list"
        )
    )


# =========================================================
# PRODUCT - SỬA
# =========================================================

@main_bp.route(
    "/products/update",
    methods=["POST"]
)
def update_product():

    # =====================================================
    # 1. Lấy ID gốc của sản phẩm
    # =====================================================

    original_id = request.form.get(
        "original_id",
        ""
    ).strip()

    if not original_id.isdigit():

        return (
            "ID sản phẩm không hợp lệ!",
            400
        )

    product = db.session.get(
        Product,
        int(original_id)
    )

    if product is None:

        return (
            "Không tìm thấy sản phẩm!",
            404
        )

    # =====================================================
    # 2. Lấy dữ liệu từ form Edit
    # =====================================================

    name = request.form.get(
        "name",
        ""
    ).strip()

    price = request.form.get(
        "price",
        ""
    ).strip()

    # products.html của nhóm đang dùng:
    #
    # name="quantity"
    #
    # nên backend phải lấy quantity.
    stock = request.form.get(
        "quantity",
        ""
    ).strip()

    category_name = request.form.get(
        "category",
        ""
    ).strip()

    status = request.form.get(
        "status",
        "active"
    ).strip().lower()

    image_url = request.form.get(
        "image_url",
        ""
    ).strip()

    # =====================================================
    # 3. Kiểm tra tên
    # =====================================================

    if not name:

        return (
            "Tên sản phẩm không được để trống!",
            400
        )

    # =====================================================
    # 4. Kiểm tra giá và số lượng
    # =====================================================

    try:

        product_price = float(price)
        product_stock = int(stock)

    except (ValueError, TypeError):

        return (
            "Giá hoặc số lượng sản phẩm không hợp lệ!",
            400
        )

    if product_price < 0:

        return (
            "Giá sản phẩm không được âm!",
            400
        )

    if product_stock < 0:

        return (
            "Số lượng sản phẩm không được âm!",
            400
        )

    # =====================================================
    # 5. Status
    # =====================================================

    if status == "inactive":
        product_status = "Inactive"
    else:
        product_status = "Active"

    # =====================================================
    # 6. Category
    # =====================================================

    category_id = None

    if category_name:

        category = Category.query.filter_by(
            name=category_name
        ).first()

        if category:

            category_id = category.id

    # =====================================================
    # 7. Cập nhật Product
    # =====================================================

    product.name = name

    product.category_id = category_id

    product.price = product_price

    product.stock = product_stock

    product.image_url = (
        image_url
        if image_url
        else None
    )

    product.status = product_status

    # =====================================================
    # 8. Lưu database
    # =====================================================

    db.session.commit()

    # =====================================================
    # 9. Quay lại danh sách sản phẩm
    # =====================================================

    return redirect(
        url_for(
            "main.product_list"
        )
    )


# =========================================================
# PRODUCT - XÓA
# =========================================================

@main_bp.route(
    "/products/delete",
    methods=["POST"]
)
def delete_product():

    product_id = request.form.get(
        "id",
        ""
    ).strip()

    if not product_id.isdigit():

        return (
            "ID sản phẩm không hợp lệ!",
            400
        )

    product = db.session.get(
        Product,
        int(product_id)
    )

    if product is None:

        return (
            "Không tìm thấy sản phẩm!",
            404
        )

    # =====================================================
    # Nếu sản phẩm đã có trong OrderDetail
    # thì không xóa khỏi database.
    # Chỉ chuyển sang Inactive.
    # =====================================================

    order_detail = OrderDetail.query.filter_by(
        product_id=product.id
    ).first()

    if order_detail:

        product.status = "Inactive"

        db.session.commit()

    else:

        db.session.delete(product)

        db.session.commit()

    return redirect(
        url_for(
            "main.product_list"
        )
    )