from flask import Flask
from app.models.models import db

def create_app() -> Flask:
    app = Flask(__name__)

    # Cấu hình vị trí lưu CSDL (File sẽ tên là database.db nằm trong thư mục instance)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Khai báo khóa bí mật để sử dụng được Session
    app.secret_key = 'ai_diem_secret_key_bao_mat'
    
    # Liên kết CSDL với ứng dụng Flask
    db.init_app(app)

    from .routes import main_bp

    app.register_blueprint(main_bp)
    return app