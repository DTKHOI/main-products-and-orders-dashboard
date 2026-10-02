from datetime import datetime

from sqlalchemy import inspect, text

from app import create_app
from app.models.models import (
    db,
    User,
    Employee,
    Product,
    Category,
    Order,
    OrderDetail,
)


# Khởi tạo ứng dụng Flask
app = create_app()


with app.app_context():

    # 1. Tạo các bảng chưa tồn tại
    db.create_all()

    # 2. Kiểm tra cột created_at trong bảng product
    inspector = inspect(db.engine)

    product_columns = [
        column['name']
        for column in inspector.get_columns('product')
    ]

    # 3. Nếu database cũ chưa có created_at thì bổ sung
    if 'created_at' not in product_columns:

        db.session.execute(
            text(
                "ALTER TABLE product "
                "ADD COLUMN created_at DATETIME"
            )
        )

        db.session.commit()

        print("Đã thêm cột created_at vào bảng product.")

    # 4. Gán ngày hiện tại cho sản phẩm cũ chưa có ngày tạo
    db.session.execute(
        text(
            """
            UPDATE product
            SET created_at = :created_at
            WHERE created_at IS NULL
            """
        ),
        {
            'created_at': datetime.utcnow().strftime(
                '%Y-%m-%d %H:%M:%S'
            )
        }
    )

    # 5. Các Category mặc định
    categories = [
        "Electronics",
        "Clothing",
        "Accessories",
        "Footwear"
    ]

    # 6. Chỉ thêm Category nếu chưa tồn tại
    for category_name in categories:

        category = Category.query.filter_by(
            name=category_name
        ).first()

        if category is None:

            db.session.add(
                Category(name=category_name)
            )

    # 7. Lưu thay đổi
    db.session.commit()

    print("Đã tạo/kiểm tra các bảng database!")
    print("Đã kiểm tra và thêm Category mặc định!")
    print("Đã kiểm tra ngày tạo sản phẩm!")