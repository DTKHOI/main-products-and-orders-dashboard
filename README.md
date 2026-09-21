# BÀI TẬP NHÓM PYTHON FLASK

## 1. Thông tin đề tài
- **Tên đề tài:** Xây dựng trang web quản lý sản phẩm và đơn hàng
- **Mã lớp / Môn học:** Lập trình python
- **Giảng viên hướng dẫn:** ................................................
- **Thời gian thực hiện:** 21 / 09 / 2026

## 2. Thông tin nhóm
- **Thành viên 1:** Dương Tuấn Khôi - N24DCCN133
- **Thành viên 2:** Nguyễn Thị Ái Diễm - N24DCCN106
- **Thành viên 3:** Phạm Anh Hào - N24DCCN117
- **Thành viên 4:** Nguyễn Xuân Bảo - N24DCCN097
- **Thành viên 5:** Nguyễn Lưu Triệu Quang - N24DCCN158

## 3. Công nghệ sử dụng
- **Ngôn ngữ lập trình:** Python, JavaScript
- **Framework:** Flask, TailwindCSS
- **Cơ sở dữ liệu:** SQLite
- **Công cụ khác:** Jinja2, Flask-SQLAlchemy (ORM), HTML5 & CSS3, Git & GitHub, DB Browser for SQLite

## 4. Cấu trúc thư mục dự án
```text
.
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── models/
│   ├── services/
│   ├── utils/
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   └── templates/
│       └── index.html
├── tests/
├── .gitignore
├── requirements.txt
└── run.py
```

## 5. Hướng dẫn chạy dự án
1. Tạo môi trường ảo:
   ```bash
   python -m venv .venv
   ```
2. Kích hoạt môi trường ảo:
   - Windows: `.venv\Scripts\activate`
   - macOS/Linux: `source .venv/bin/activate`
3. Cài thư viện:
   ```bash
   pip install -r requirements.txt
   ```
4. Chạy ứng dụng:
   ```bash
   python run.py
   ```

## 6. Phân công công việc
- **Dương Tuấn Khôi: ** Xây dựng giao diện trang web, làm slide thuyết trình, tính năng tìm kiếm, lọc sản phẩm
- **Nguyễn Thị Ái Diễm: ** Đăng ký, đăng nhập, xây dựng class cơ sở dữ liệu, kiểm tra đăng nhập
- **Phạm Anh Hào: ** Lập trình thêm, sửa, xóa, đọc sản phẩm tiếp nhận dữ liệu từ form ở giao diện (form thêm, form xóa, form chỉnh sửa), hiện danh sách sản phẩm kho ra bên phía giao diện. 
- **Nguyễn Xuân Bảo: ** Đơn hàng: hiển thị danh sách đơn hàng ra giao diện, tạo đơn hàng mới với thông tin từ form gửi lên, cập nhật trạng thái đơn hàng, logic trừ kho
- **Nguyễn Lưu Triệu Quang: ** Vẽ sơ đồ Use Case và đặc tả cho từng chức năng, UML, kiểm thử trang web, bảng dữ liệu cho hệ thống. Tổng hợp tất cả rồi hoàn thiện báo cáo đồ án, thuyết trình
