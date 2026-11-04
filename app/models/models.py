from app import db
from datetime import datetime
import pytz
from zoneinfo import ZoneInfo

# lấy thời gian hiện tại theo múi giờ Việt Nam
def get_vietnam_date():
    return datetime.now(ZoneInfo("Asia/Ho_Chi_Minh"))

def get_vietnam_datetime():
    tz = pytz.timezone("Asia/Ho_Chi_Minh")
    return datetime.now(tz).replace(tzinfo=None)

# User - Authentication admin & staff
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='admin')   # 'admin' hoặc 'staff'

    phone = db.Column(db.String(15), nullable=True)
    avatar_url = db.Column(db.String(255), nullable=True)
    language = db.Column(db.String(10), default='en')   # 'vi' hoặc 'en'
    theme = db.Column(db.String(10), default='light')   # 'light' hoặc 'dark'

    # Quan hệ nối bảng
    staff_profile = db.relationship('Staff', foreign_keys='Staff.user_id', backref='user_account', uselist=False, cascade='all, delete-orphan')
    managed_staffs = db.relationship('Staff', foreign_keys='Staff.admin_id', backref='manager', lazy=True)
    products = db.relationship('Product', backref='owner', lazy=True, cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='owner', lazy=True, cascade='all, delete-orphan')

    def __init__(self, email, password_hash, username, role='admin'):
        self.email = email
        self.username = username
        self.password_hash = password_hash
        self.role = role


# Staff (Workspace & Profile)
class Staff(db.Model):
    __tablename__ = 'staff'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)      # Nối với tài khoản đăng nhập
    local_id = db.Column(db.Integer, nullable=False, default=1)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)                 # Nối với Admin quản lý trực tiếp
    staff_code = db.Column(db.String(50), nullable=True)                                      # Mã nhân viên (e.g., NV-001)
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False, unique=True)
    address = db.Column(db.String(255), nullable=True)
    gender = db.Column(db.String(10), nullable=False, default='male')                          # 'male' hoặc 'female'
    avatar_url = db.Column(db.String(255), nullable=False, default='')

    def __init__(self, user_id, admin_id, full_name, phone, address, gender, avatar_url):
        self.user_id = user_id
        self.admin_id = admin_id
        self.full_name = full_name
        self.phone = phone
        self.address = address
        self.gender = gender
        self.avatar_url = avatar_url

# Product
class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # Phân vùng kho theo Admin
    local_id = db.Column(db.Integer, nullable=False, default=1)
    sku = db.Column(db.String(50), nullable=True) # Mã SKU sẽ hiển thị ở giao diện: PRD-0001
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    image_url = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), nullable=False, default='active') # 'active' / 'inactive'    
    created_at = db.Column(db.DateTime, default=get_vietnam_date) 

    # Thuộc tính lấy ngày tháng năm theo format Việt Nam
    @property
    def get_vn_date(self):
        if self.created_at:
            return self.created_at.strftime('%d/%m/%Y')
        return ""

    # Quan hệ với chi tiết đơn
    order_items = db.relationship('OrderItem', backref='product', lazy=True)

    def __init__(self, admin_id, name, status, category, price=0, stock=0, image_url=''):
        self.admin_id = admin_id
        self.name = name
        self.status = status
        self.category = category
        self.price = price
        self.stock = stock
        self.image_url = image_url

# Order
class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    local_id = db.Column(db.Integer, nullable=False, default=1)
    ord = db.Column(db.String(50), nullable=True) # Mã Order_id sẽ hiển thị ở giao diện: ORD-0001
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # Đơn hàng thuộc cửa hàng nào
    customer_name = db.Column(db.String(100), nullable=False)
    customer_phone = db.Column(db.String(15), nullable=False)
    customer_email = db.Column(db.String(100), nullable=True)
    customer_id = db.Column(db.String(15), nullable=True)
    shipping_address = db.Column(db.String(255), nullable=False)
    total_amount = db.Column(db.Float, nullable=False, default=0.0)
    status = db.Column(db.String(20), nullable=False, default='pending') # 'pending', 'processing', 'completed', 'canceled'
    created_at = db.Column(db.DateTime, nullable=False, default=get_vietnam_datetime)

    # Quan hệ danh sách món hàng trong đơn
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')

    def __init__(self, admin_id, customer_name, customer_phone, shipping_address, total_amount, customer_email = ''):
        self.admin_id = admin_id
        self.customer_name = customer_name
        self.customer_phone = customer_phone
        self.shipping_address = shipping_address
        self.total_amount = total_amount   

# Order detail - danh sách sản phẩm trong đơn hàng
class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete='SET NULL'), nullable=True) # Cho phép null nếu sản phẩm bị xóa
    product_name = db.Column(db.String(100), nullable=False) # Lưu tên sản phẩm lúc mua
    product_sku = db.Column(db.String(50), nullable=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)

    def __init__(self, order_id, product_name, quantity, unit_price, product_sku, product_id=None):
        self.order_id = order_id
        self.product_name = product_name
        self.quantity = quantity
        self.unit_price = unit_price
        self.total_price = unit_price * quantity
        self.product_sku = product_sku
        self.product_id = product_id