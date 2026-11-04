from flask import Flask, session
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from datetime import timedelta
import os

db = SQLAlchemy()
csrf = CSRFProtect()

load_dotenv()
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
SECRET_KEY = os.environ.get("KEY", "a0a96f9b7a707ec3e30718d5bc870b3f5b093845b4902ef0140ce71eb166818a")
DB_NAME = os.environ.get("DATABASE_NAME", "database.db")



def create_database(app):
        if not os.path.exists('app/' + DB_NAME):
            with app.app_context():
                db.create_all()
            print("Created DB!")

def create_app():
    app = Flask(__name__)

    # Tạo khóa bí mật
    app.config['SECRET_KEY'] = SECRET_KEY

    # Tạo mã chống giả mạo form
    csrf.init_app(app)

    # Cu hình thời gian sống của session ghi nhớ:
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

    # Khởi tạo database
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Avoids a warning
    db.init_app(app)
    from .models import models
    create_database(app)

    from .utils import _t

    @app.after_request
    def set_no_cache(response):
        if 'id' in session:
            response.headers['Cache-Control'] = 'no-store'
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
