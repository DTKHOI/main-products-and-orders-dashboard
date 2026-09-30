from app import create_app
from app.models.models import db, User, Product, Order

# Khởi tạo ứng dụng
app = create_app()

# Bật ngữ cảnh ứng dụng và ra lệnh tạo bảng
with app.app_context():
    db.create_all()
    print("Đã tạo thành công CSDL database.db!")