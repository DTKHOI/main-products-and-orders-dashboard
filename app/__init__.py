from flask import Flask, session
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from werkzeug.middleware.proxy_fix import ProxyFix
from datetime import timedelta
import os

db = SQLAlchemy()
csrf = CSRFProtect()

load_dotenv()
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

def create_database(app):
    """Tự động khởi tạo bảng dữ liệu nếu chưa tồn tại"""
    with app.app_context():
        db.create_all()


def create_app():
    app = Flask(__name__)

    secret_key = os.environ.get("SECRET_KEY") or os.environ.get("KEY", "productflow-secret-fallback-key-2026")
    app.config['SECRET_KEY'] = secret_key

    csrf.init_app(app)
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

    database_url = os.environ.get("DATABASE_URL")
    if database_url:
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql+psycopg2://", 1)
        elif database_url.startswith("postgresql://") and not database_url.startswith("postgresql+psycopg2://"):
            database_url = database_url.replace("postgresql://", "postgresql+psycopg2://", 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        db_name = os.environ.get("DATABASE_NAME", "database.db")
        base_dir = os.path.abspath(os.path.dirname(__file__))
        app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(base_dir, db_name)}"

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    db.init_app(app)

    from .models import models
    create_database(app)

    # Hỗ trợ reverse proxy của Render (đảm bảo request.is_secure và HTTPS hoạt động đúng)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    from .utils import _t

    @app.after_request
    def set_no_cache(response):
        if 'id' in session:
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response.headers['Pragma'] = 'no-cache'
        return response

    @app.context_processor
    def inject_global_translations():
        return dict(
            _t=_t,
            current_lang=session.get('language', 'en')
        )

    from .users import users
    from .products import products
    from .orders import orders
    from .staffs import staffs
    from .dashboard import dashboard
    from .profile import profile
    from .new_pass import new_pass

    app.register_blueprint(users)
    app.register_blueprint(products)
    app.register_blueprint(orders)
    app.register_blueprint(staffs)
    app.register_blueprint(dashboard)
    app.register_blueprint(profile)
    app.register_blueprint(new_pass)

    return app