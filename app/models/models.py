from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Khởi tạo đối tượng đại diện cho CSDL
db = SQLAlchemy()

# 1. BẢNG NGƯỜI DÙNG (Quản lý Tài khoản & Phân quyền)

class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False) 
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(20), default='Staff')
    
    # Quan hệ 1-N: Một User (nhân viên) có thể tạo nhiều Order
    orders = db.relationship('Order', backref='creator', lazy=True)

# 2. BẢNG SẢN PHẨM (Kho hàng)

class Product(db.Model):
    __tablename__ = 'product'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    # Tạm thời cấu hình category_id là Integer, 
    # nếu nhóm em có bạn khác làm bảng Category, khóa ngoại sẽ liên kết đến đó.
    category_id = db.Column(db.Integer, nullable=True) 
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), default='Active')

# 3. BẢNG ĐƠN HÀNG

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
    
    # Khóa ngoại liên kết với bảng User (Để biết ai tạo đơn)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)