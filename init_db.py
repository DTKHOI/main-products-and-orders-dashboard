from app import create_app
from app.models.models import db, User, Product, Order, Category


# Khởi tạo ứng dụng
app = create_app()


# Bật ngữ cảnh ứng dụng và tạo bảng
with app.app_context():
    db.create_all()

    # Các Category mặc định
    categories = [
        "Electronics",
        "Clothing",
        "Accessories",
        "Footwear"
    ]

    # Thêm Category nếu chưa tồn tại
    for category_name in categories:
        category = Category.query.filter_by(
            name=category_name
        ).first()

        if category is None:
            db.session.add(
                Category(name=category_name)
            )

    db.session.commit()

    print("Đã tạo thành công CSDL database.db!")
    print("Đã kiểm tra và thêm Category mặc định!")