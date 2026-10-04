import json

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
    Order,
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
# =========================================================
# ORDER - HIỂN THỊ DANH SÁCH ĐƠN HÀNG
# =========================================================

@main_bp.route("/orders/", methods=["GET"])
def order_list():

    # Lấy tất cả đơn hàng, đơn mới nhất nằm trên cùng
    orders = Order.query.order_by(Order.id.asc()).all()

    # Lấy sản phẩm còn kinh doanh và còn hàng
    products = Product.query.filter(
        Product.status == "Active",
        Product.stock > 0
    ).order_by(
        Product.id.desc()
    ).all()

    return render_template(
        "orders.html",
        orders=orders,
        products=products
    )


# =========================================================
# ORDER - CHI TIẾT ĐƠN HÀNG
# =========================================================

@main_bp.route("/orders/<int:order_id>", methods=["GET"])
def order_detail(order_id):

    order = Order.query.get_or_404(order_id)

    return render_template(
        "order_detail.html",
        order=order
    )


# =========================================================
# ORDER - TẠO ĐƠN HÀNG
# =========================================================

@main_bp.route("/orders/submit", methods=["POST"])
def create_order():

    # -----------------------------------------------------
    # 1. Lấy thông tin khách hàng từ form
    # -----------------------------------------------------

    customer_name = request.form.get(
        "customer_name",
        ""
    ).strip()

    customer_phone = request.form.get(
        "phone",
        ""
    ).strip()

    customer_email = request.form.get(
        "email",
        ""
    ).strip() or None

    shipping_address = request.form.get(
        "address",
        ""
    ).strip()

    cart_data = request.form.get(
        "cart_data",
        ""
    )

    # -----------------------------------------------------
    # 2. Kiểm tra thông tin khách hàng
    # -----------------------------------------------------

    if (
        not customer_name
        or not customer_phone
        or not shipping_address
    ):
        return (
            "Vui lòng nhập đầy đủ tên, "
            "số điện thoại và địa chỉ!",
            400
        )

    # -----------------------------------------------------
    # 3. Đọc giỏ hàng JSON từ JavaScript
    # -----------------------------------------------------

    try:

        cart = json.loads(cart_data)

    except (TypeError, ValueError, json.JSONDecodeError):

        return (
            "Dữ liệu sản phẩm không hợp lệ!",
            400
        )

    if not isinstance(cart, list) or not cart:

        return (
            "Đơn hàng phải có ít nhất một sản phẩm!",
            400
        )

    # -----------------------------------------------------
    # 4. Gom sản phẩm theo product_id
    # -----------------------------------------------------

    quantities = {}

    try:

        for item in cart:

            product_id = int(item.get("id"))
            quantity = int(item.get("quantity"))

            if product_id <= 0 or quantity <= 0:
                raise ValueError

            quantities[product_id] = (
                quantities.get(product_id, 0)
                + quantity
            )

    except (AttributeError, TypeError, ValueError):

        return (
            "ID sản phẩm hoặc số lượng không hợp lệ!",
            400
        )

    # -----------------------------------------------------
    # 5. Kiểm tra tồn kho và lấy GIÁ TỪ DATABASE
    # -----------------------------------------------------

    order_items = []
    total_amount = 0.0

    for product_id, quantity in quantities.items():

        product = db.session.get(
            Product,
            product_id
        )

        if product is None:

            return (
                f"Không tìm thấy sản phẩm ID {product_id}!",
                404
            )

        if product.status != "Active":

            return (
                f"Sản phẩm '{product.name}' "
                "hiện không kinh doanh!",
                400
            )

        if product.stock < quantity:

            return (
                f"Sản phẩm '{product.name}' không đủ tồn kho. "
                f"Còn {product.stock}, yêu cầu {quantity}.",
                400
            )

        # QUAN TRỌNG:
        # Lấy giá thật từ Database
        subtotal = product.price * quantity

        total_amount += subtotal

        order_items.append(
            (
                product,
                quantity,
                product.price
            )
        )

    # -----------------------------------------------------
    # 6. Tạo Order + OrderDetail + Trừ kho
    # -----------------------------------------------------

    try:

        new_order = Order(
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            shipping_address=shipping_address,
            total_amount=total_amount,
            status="Pending",
            user_id=session.get("user_id")
        )

        db.session.add(new_order)

        # Lấy ID của Order vừa tạo
        db.session.flush()

        for product, quantity, unit_price in order_items:

            detail = OrderDetail(
                order_id=new_order.id,
                product_id=product.id,
                quantity=quantity,
                price=unit_price
            )

            db.session.add(detail)

            # ===============================
            # TRỪ KHO
            # ===============================
            product.stock -= quantity

        # Lưu tất cả thay đổi
        db.session.commit()

    except Exception:

        # Nếu có lỗi thì hoàn tác toàn bộ
        db.session.rollback()

        return (
            "Không thể tạo đơn hàng. "
            "Dữ liệu chưa được lưu.",
            500
        )

    # -----------------------------------------------------
    # 7. Quay lại danh sách đơn hàng
    # -----------------------------------------------------

    return redirect(
        url_for("main.order_list")
    )
# =========================================================
# ORDER - CẬP NHẬT ĐƠN HÀNG
# =========================================================

@main_bp.route("/orders/update", methods=["POST"])
def update_order():

    # -----------------------------------------------------
    # 1. Lấy Order ID
    # -----------------------------------------------------

    order_id = request.form.get(
        "order_id",
        ""
    ).strip()

    if not order_id.isdigit():

        return (
            "ID đơn hàng không hợp lệ!",
            400
        )

    # -----------------------------------------------------
    # 2. Tìm Order
    # -----------------------------------------------------

    order = db.session.get(
        Order,
        int(order_id)
    )

    if order is None:

        return (
            "Không tìm thấy đơn hàng!",
            404
        )

    # -----------------------------------------------------
    # 3. Lấy dữ liệu form Edit
    # -----------------------------------------------------

    customer_name = request.form.get(
        "customer_name",
        ""
    ).strip()

    customer_phone = request.form.get(
        "phone",
        ""
    ).strip()

    customer_email = request.form.get(
        "email",
        ""
    ).strip() or None

    shipping_address = request.form.get(
        "address",
        ""
    ).strip()

    new_status = request.form.get(
        "status",
        ""
    ).strip().capitalize()

    # -----------------------------------------------------
    # 4. Kiểm tra dữ liệu
    # -----------------------------------------------------

    allowed_statuses = {
        "Pending",
        "Processing",
        "Completed",
        "Canceled"
    }

    if (
        not customer_name
        or not customer_phone
        or not shipping_address
    ):

        return (
            "Tên, số điện thoại và địa chỉ "
            "không được để trống!",
            400
        )

    if new_status not in allowed_statuses:

        return (
            "Trạng thái đơn hàng không hợp lệ!",
            400
        )

    # -----------------------------------------------------
    # 5. Lấy trạng thái cũ
    # -----------------------------------------------------

    old_status = order.status

    # -----------------------------------------------------
    # 6. Không cho đơn đã hủy quay lại
    # -----------------------------------------------------

    if (
        old_status == "Canceled"
        and new_status != "Canceled"
    ):

        return (
            "Đơn hàng đã hủy không thể "
            "chuyển lại trạng thái khác!",
            400
        )

    # -----------------------------------------------------
    # 7. Cập nhật
    # -----------------------------------------------------

    try:

        order.customer_name = customer_name
        order.customer_phone = customer_phone
        order.customer_email = customer_email
        order.shipping_address = shipping_address

        # -------------------------------------------------
        # Nếu chuyển sang Canceled → hoàn kho
        # -------------------------------------------------

        if (
            old_status != "Canceled"
            and new_status == "Canceled"
        ):

            for detail in order.order_details:

                product = db.session.get(
                    Product,
                    detail.product_id
                )

                if product is not None:

                    product.stock += detail.quantity

        order.status = new_status

        db.session.commit()

    except Exception:

        db.session.rollback()

        return (
            "Không thể cập nhật đơn hàng. "
            "Dữ liệu chưa được lưu.",
            500
        )

    return redirect(
        url_for("main.order_list")
    )