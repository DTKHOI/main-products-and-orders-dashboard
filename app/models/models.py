from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from datetime import datetime

# Khởi tạo đối tượng database
db = SQLAlchemy()

# 1. Bảng User (Quản lý Tài khoản & Phân quyền)
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) # Mã định danh
    username = db.Column(db.String(50), unique=True, nullable=False) # Tên đăng nhập không trùng
    password = db.Column(db.String(255), nullable=False) # Mật khẩu đã băm
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(20), default='Staff') 
    
    # Ràng buộc CHECK role IN ('Admin', 'Staff', 'User')
    __table_args__ = (
        db.CheckConstraint("role IN ('Admin', 'Staff', 'User')", name='check_role_valid'),
    )

    # Quan hệ 1-1 với Employee
    employee = db.relationship('Employee', backref='user', uselist=False, cascade='all, delete')
    # Quan hệ 1-N với Order
    orders = db.relationship('Order', backref='user_creator', lazy=True)

# 2. Bảng Employee (Hồ sơ Chi tiết Nhân viên)
class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), unique=True) # Khóa ngoại 1-1
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    avatar = db.Column(db.String(255), nullable=True)
    address = db.Column(db.String(255), nullable=True)

    __table_args__ = (
        db.CheckConstraint("gender IN ('Nam', 'Nữ', 'Khác')", name='check_gender_valid'),
    )

# Bảng phụ: Category (Danh mục - Bắt buộc phải có để Product tham chiếu)
class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    products = db.relationship('Product', backref='category', lazy=True)

# 3. Bảng Product (Quản lý Kho Sản phẩm)
# 3. Bảng Product (Quản lý Kho Sản phẩm)
class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey('category.id', ondelete='SET NULL'),
        nullable=True
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    stock = db.Column(
        db.Integer,
        nullable=False
    )

    image_url = db.Column(
        db.String(255),
        nullable=True
    )

    status = db.Column(
        db.String(20),
        default='Active'
    )

    # Ngày giờ thêm sản phẩm
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    __table_args__ = (
        db.CheckConstraint(
            'price >= 0',
            name='check_price_positive'
        ),
        db.CheckConstraint(
            'stock >= 0',
            name='check_stock_positive'
        ),
        db.CheckConstraint(
            "status IN ('Active', 'Inactive')",
            name='check_product_status'
        ),
    )

# 4. Bảng Order (Quản lý Đơn hàng)
class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(100), nullable=True)
    customer_phone = db.Column(db.String(15), nullable=False)
    shipping_address = db.Column(db.String(255), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'), nullable=True)

    __table_args__ = (
        db.CheckConstraint('total_amount >= 0', name='check_total_amount'),
        db.CheckConstraint("status IN ('Pending', 'Processing', 'Completed', 'Canceled')", name='check_order_status'),
    )
    
    # Liên kết với chi tiết đơn hàng
    order_details = db.relationship('OrderDetail', backref='order', cascade='all, delete')

# 5. Bảng OrderDetail (Chi tiết đơn hàng)
class OrderDetail(db.Model):
    __tablename__ = 'order_detail'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete='RESTRICT'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    __table_args__ = (
        db.CheckConstraint('quantity > 0', name='check_quantity'),
        db.CheckConstraint('price >= 0', name='check_detail_price'),
    )