# BÀI TẬP CÁ NHÂN PYTHON FLASK

## 1. Thông tin đề tài

- **Tên đề tài:** Xây dựng trang web quản lý sản phẩm và đơn hàng
- **Môn học:** Lập trình Python
- **Thời gian thực hiện:** 21 / 09 / 2026
- **Thời gian hoàn thành:** 05 / 11 / 2026

## 2. Thông tin sinh viên

- **Họ tên:** Dương Tuấn Khôi
- **MSSV:** N24DCCN133
- **Lớp:** D24CQCN02-N
- **Trường:** Học viện Công nghệ Bưu chính Viễn thông cơ sở tại Thành phố Hồ Chí Minh

## 3. Công nghệ sử dụng

- **Ngôn ngữ lập trình:** Python 3, JavaScript (ES6+)
- **Backend Framework & Thư viện:** Flask, Flask-SQLAlchemy (ORM), Flask-WTF (Bảo vệ CSRF), Werkzeug, python-dotenv
- **Frontend & Giao diện:** TailwindCSS, Jinja2 Template, HTML
- **Cơ sở dữ liệu:** SQLite (Local Development) / PostgreSQL (Production)
- **Công cụ & Môi trường:** Git, GitHub, Gunicorn, DB Browser for SQLite
- **Công cụ AI hỗ trợ (Vibe Coding):** Google Antigravity, Gemini, Claude

## 4. Đóng góp và sử dụng AI hỗ trợ

Trong quá trình thực hiện dự án, có sự hỗ trợ từ **Gemini, Claude** nhằm tăng tốc độ phát triển và đưa gợi ý giải pháp

- **Tự thực hiện:**
    - Lên ý tưởng đề tài và thiết kế luồng nghiệp vụ hệ thống.
    - Định hướng giải pháp kỹ thuật, phân chia cấu trúc thư mục dạng Blueprint.
    - Trực tiếp kiểm thử, debug, cấu hình triển khai và kiểm soát toàn bộ chất lượng mã nguồn.
    - Cắt giao diện từ Figma
    - Viết các tính năng CRUD, lọc, tìm kiếm, xác thực người dùng và phân quyền

- **Phần AI hỗ trợ:**
    - Xây dựng cơ sở dữ liệu
    - Viết tính năng dịch thuật và quên mật khẩu
    - Hỗ trợ viết tài liệu kiểm thử, đánh giá source code.
    - Viết giao diện cho các modal form, thông báo dạng toast và JavaScript cho các tính năng như xác thực, toast
    - Tối ưu responsive hỗ trợ nhiều kích thước màn hình.
    - Soạn thảo tài liệu dự án, cấu hình môi trường production (PostgreSQL trên Render).

## 5. Các tính năng chính của hệ thống

1. **Xác thực & Người dùng (Authentication):**
    - Đăng nhập, đăng ký tài khoản người dùng và nhân viên.
    - Quên mật khẩu, gửi mã OTP xác thực qua Email và đặt lại mật khẩu mới an toàn.
    - Quản lý thông tin hồ sơ cá nhân (Profile).

2. **Tổng quan & Báo cáo (Dashboard):**
    - Thống kê thời gian thực: doanh thu, tổng số đơn hàng, tổng sản phẩm và nhân sự.

3. **Quản lý sản phẩm (Products):**
    - Xem danh sách, phân trang, tìm kiếm và lọc sản phẩm theo danh mục.
    - Thêm mới, chỉnh sửa thông tin sản phẩm (giá bán, số lượng tồn kho, hình ảnh) và xóa sản phẩm.

4. **Quản lý đơn hàng (Orders):**
    - Danh sách đơn hàng với trạng thái trực quan (Pending, Processing, Completed, Cancelled).
    - Xem chi tiết từng đơn hàng (Order Details) và cập nhật trạng thái đơn hàng.

5. **Quản lý nhân sự (Staffs):**
    - Quản lý danh sách tài khoản nhân viên và phân quyền truy cập chức năng.

## 6. Cấu trúc thư mục dự án

```text
.
├── app/
│   ├── models/              # Định nghĩa schema cơ sở dữ liệu (models.py)
│   ├── static/              # Tài nguyên tĩnh (CSS, JS, hình ảnh)
│   │   ├── css/
│   │   └── js/
│   ├── templates/           # Giao diện HTML (Jinja2 Templates)
│   ├── dashboard.py         # Route & logic trang tổng quan Dashboard
│   ├── products.py          # Quản lý danh mục & sản phẩm
│   ├── orders.py            # Quản lý và xử lý đơn hàng
│   ├── staffs.py            # Quản lý nhân sự & tài khoản nhân viên
│   ├── users.py             # Xử lý xác thực (Đăng nhập, đăng ký, đăng xuất)
│   ├── profile.py           # Quản lý hồ sơ người dùng
│   ├── new_pass.py          # Xử lý quên mật khẩu & xác thực OTP qua Email
│   ├── utils.py             # Các hàm tiện ích & helper hỗ trợ
│   └── __init__.py          # Khởi tạo Flask app, database & cấu hình bảo mật
├── .gitignore
├── requirements.txt         # Danh sách thư viện phụ thuộc
└── run.py                   # Điểm khởi chạy ứng dụng (Entry point)
```

## 7. Hướng dẫn chạy dự án

### Bước 1: Tạo và kích hoạt môi trường ảo

- **Tạo môi trường ảo:**
    ```bash
    python -m venv .venv
    ```
- **Kích hoạt môi trường ảo:**
    - Trên Windows:
        ```bash
        .venv\Scripts\activate
        ```
    - Trên macOS/Linux:
        ```bash
        source .venv/bin/activate
        ```

### Bước 2: Cài đặt các thư viện phụ thuộc

```bash
pip install -r requirements.txt
```

### Bước 3: Cấu hình biến môi trường (Tùy chọn)

Tạo file `.env` tại thư mục gốc hoặc trong thư mục `app/` để cấu hình các khóa bảo mật và thông tin gửi mail (nếu cần dùng tính năng gửi OTP):

```env
KEY=your_secret_key_here
DATABASE_NAME=database.db
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
```

### Bước 4: Khởi chạy ứng dụng

```bash
python run.py
```

Sau khi khởi chạy thành công, truy cập ứng dụng tại trình duyệt:
**http://127.0.0.1:5000** hoặc **http://localhost:5000**

## 8. Hình ảnh giao diện sản phẩm

- **Landing Page:**

    ![Landing Page](app\static\img\landing_page.png)

- **Tổng quan Dashboard:**

    ![Dashboard](app\static\img\dashboard.png)

- **Quản lý sản phẩm:**

    ![Products](app\static\img\products.png)

- **Quản lý đơn hàng:**

    ![Orders](app\static\img\orders.png)

- **Chi tiết đơn hàng:**

    ![Order Details](app\static\img\order_details.png)

- **Quản lý nhân viên:**

    ![Staffs](app\static\img\staffs.png)

- **Thông tin người dùng:**

    ![Profile](app\static\img\profile.png)

- **Đăng nhập & Xác thực OTP:**

    ![Auth & OTP](app\static\img\login.png)
    ![Auth & OTP](app\static\img\otp_confirmation.png)

## 9. Tài liệu tham khảo & Thư viện sử dụng

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask-WTF Documentation](https://flask-wtf.readthedocs.io/)
- [TailwindCSS Documentation](https://tailwindcss.com/docs)
- [Werkzeug Documentation](https://werkzeug.palletsprojects.com/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)

## 10. Liên kết dự án & Công cụ hỗ trợ

- **Trang sản phẩm đã deploy (Live Demo):** [Link Live Demo](https://main-products-and-orders-dashboard.onrender.com/)
- **File thiết kế giao diện (Figma):** [Link Figma Design](https://www.figma.com/make/0GmiJYf4PWjtmt1pxpsmp3/Product-Management-Dashboard--Community-?t=IpS36xETkxOb2314-1)
- **Công cụ quản trị CSDL SQLite (Local):** [DB Browser for SQLite](https://sqlitebrowser.org/)
- **Các web tool hỗ trợ khác:**
    - Nén hình ảnh: [tinypng](https://tinypng.com/)
    - Tạo favicon: [RealFaviconGenerator](https://realfavicongenerator.net/)
    - Nền tảng triển khai dự án: [render](https://render.com/)
