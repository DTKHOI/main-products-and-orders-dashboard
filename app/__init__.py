from flask import Flask
from app.models.models import db


def create_app() -> Flask:
    app = Flask(__name__)

    # Cấu hình vị trí lưu CSDL
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Khóa bí mật cho Session
    app.secret_key = 'ai_diem_secret_key_bao_mat'

    # Liên kết CSDL với Flask
    db.init_app(app)

    # Import models để SQLAlchemy biết tất cả các bảng
    from app.models.models import User, Employee, Category, Product, Order, OrderDetail

    # Tạo các bảng nếu chưa tồn tại
    with app.app_context():
        db.create_all()

    # Đăng ký Blueprint
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app