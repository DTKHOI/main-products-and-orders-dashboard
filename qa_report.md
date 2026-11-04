# 📋 BÁO CÁO KIỂM THỬ & ĐÁNH GIÁ CHẤT LƯỢNG (QA/QC)
### Dự án: **ProductFlow** — Ứng dụng Quản lý Kho hàng & Đơn hàng
> **Người thực hiện:** Sinh viên năm 3 CNTT — vai trò Tester / QA-QC  
> **Công nghệ:** Flask · Jinja2 · Tailwind CSS · SQLAlchemy · SQLite  
> **Thời điểm review:** Trước khi deploy Cloud & thuyết trình giảng viên  
> **Phạm vi:** Toàn bộ thư mục `app/` (Python backend + HTML templates)

---

## MỤC LỤC

1. [Kiểm thử Tính năng (Functional Testing)](#1-kiểm-thử-tính-năng)
2. [Kiểm thử Bảo mật & Phân quyền (Security & Authorization)](#2-kiểm-thử-bảo-mật--phân-quyền)
3. [Kiểm tra Chất lượng Mã nguồn (Code Quality)](#3-kiểm-tra-chất-lượng-mã-nguồn)
4. [Kịch bản Kiểm thử & Demo Checklist](#4-kịch-bản-kiểm-thử--demo-checklist)

---

## 1. Kiểm thử Tính năng

### 🔴 BUG-01 — `orders.py` dòng 51: Crash khi tạo đơn hàng có sản phẩm vượt tồn kho

**Mức độ:** CRITICAL — có thể gây **lỗi 500** ngay giữa buổi demo.

**Vị trí:** [`orders.py` dòng 51](file:///d:/Workspace/teamwork/Nhóm Python - Quản lý đơn hàng và sản phẩm/source-code/products-and-orders-dashboard/app/orders.py#L51)

**Mô tả vấn đề:**  
Hàm `total()` có hai đường trả về khác nhau:
- Nếu stock đủ → trả về `float` (tổng tiền).
- Nếu stock không đủ → trả về một **`Response` object** (là kết quả của `redirect()`).

Vấn đề nằm ở chỗ giá trị trả về của `total()` được truyền thẳng vào constructor `Order(...)` dưới dạng `total_amount=total(cart_items)`. Khi stock vượt mức, `total_amount` nhận vào một `Response` object thay vì `float`, khiến **SQLAlchemy ném ngoại lệ** ngay lập tức → **HTTP 500**.

**Code lỗi:**
```python
# orders.py — dòng 25-40: hàm total() trả về 2 kiểu dữ liệu khác nhau!
def total(products):
    total = 0
    ...
    for item in products:
        if not stored_item or stored_item.stock < buy_qty:
            flash(...)
            return redirect(url_for('orders.orders_page'))  # ← trả về Response!
        total += ...
    return total  # ← trả về float

# orders.py — dòng 51: giá trị trả về được truyền thẳng vào Model!
new_order = Order(workspace_id, customer_name, shipping_address=address,
                  total_amount=total(cart_items),  # ← BUG: có thể là Response object!
                  customer_phone=phone)
```

**Cách sửa đề xuất:**
```python
# Tách kiểm tra ra trước khi gọi create_order
def create_order(cart_items, form):
    workspace_id = session.get('workspace_id')
    total_amount = total(cart_items)

    # Kiểm tra xem total() có trả về redirect không
    if not isinstance(total_amount, (int, float)):
        return total_amount  # Trả về Response redirect luôn

    customer_name = form.get('customer_name')
    ...
    new_order = Order(workspace_id, customer_name, ..., total_amount=total_amount, ...)
    ...
```

---

### 🔴 BUG-02 — `products.py` dòng 66: Logic bảo vệ stock=0 bị ghi đè ngay sau khi tính

**Mức độ:** HIGH — sản phẩm hết hàng vẫn có thể được lưu trạng thái `active`.

**Vị trí:** [`products.py` dòng 63-66](file:///d:/Workspace/teamwork/Nhóm Python - Quản lý đơn hàng và sản phẩm/source-code/products-and-orders-dashboard/app/products.py#L63)

**Mô tả vấn đề:**  
Dòng 64 tính toán đúng: nếu `stock <= 0` thì đặt status là `inactive`.  
Nhưng dòng 66 lập tức **ghi đè lại bằng giá trị từ form** — xóa sạch kết quả vừa tính.

**Code lỗi:**
```python
request_status = form.get('status', 'active')
prod_status = 'inactive' if prod_stock <= 0 else request_status  # ← dòng 64: tính đúng
                                                                   
prod_status = form.get('status')  # ← dòng 66: GHI ĐÈ! Vô hiệu hoá dòng 64
prod_img_url = form.get('image_url')
```

> [!NOTE]
> Đây là lỗi thừa code (dead assignment). Logic bảo vệ cho hành động **Edit** (`elif action == 'edit'`) đã đúng ở dòng 102-105. Chỉ hành động **Add** (`if action == 'add'`) bị ảnh hưởng.

**Cách sửa:** Xóa dòng 66 đi là đủ.
```python
request_status = form.get('status', 'active')
prod_status = 'inactive' if prod_stock <= 0 else request_status
# ← XÓA: prod_status = form.get('status')
prod_img_url = form.get('image_url')
```

---

### 🔴 BUG-03 — `users.py` dòng 65-66: Đăng nhập email sai bị redirect sai trang

**Mức độ:** MEDIUM — người dùng nhập email chưa đăng ký sẽ bị văng sang trang `/products` (bị redirect tiếp sang login do chưa đăng nhập), thay vì ở lại trang login để xem thông báo lỗi.

**Vị trí:** [`users.py` dòng 65-66](file:///d:/Workspace/teamwork/Nhóm Python - Quản lý đơn hàng và sản phẩm/source-code/products-and-orders-dashboard/app/users.py#L65)

**Code lỗi:**
```python
else:
    flash('Email is not registered.', 'error')
    return redirect(url_for('products.products_page'))  # ← BUG: nên redirect về login!
```

**Cách sửa:**
```python
else:
    flash('Email is not registered.', 'error')
    return redirect(url_for('users.login'))  # ← Đúng rồi
```

---

### 🟠 BUG-04 — `orders.html` dòng 141: Nút Logout trong mobile menu bị sai `action`

**Mức độ:** MEDIUM — Nút "Sign Out" trong mobile drawer của trang Orders **không hoạt động** vì `action` bị gõ sai thành `accept` thay vì `action`.

**Vị trí:** [`orders.html` dòng 141](file:///d:/Workspace/teamwork/Nhóm Python - Quản lý đơn hàng và sản phẩm/source-code/products-and-orders-dashboard/app/templates/orders.html#L141)

**Code lỗi:**
```html
<!-- orders.html — mobile menu logout -->
<form accept="/logout">   <!-- ← BUG: thuộc tính sai! Phải là action="/logout" -->
    <button type="submit" ...>Sign Out</button>
</form>
```

**Cách sửa:**
```html
<form action="/logout">
    <button type="submit" ...>Sign Out</button>
</form>
```

> [!CAUTION]
> Đây là lỗi **UI rất dễ bị nhìn thấy trong demo** nếu giảng viên mở app trên màn hình nhỏ (tablet/điện thoại). Cần sửa ngay trước khi thuyết trình.

---

### 🟡 BUG-05 — `staffs.py` dòng 143-179: Dead code sau lệnh `return`

**Mức độ:** LOW — không gây crash, nhưng gây nhầm lẫn khi đọc code.

**Vị trí:** [`staffs.py` dòng 142-179](file:///d:/Workspace/teamwork/Nhóm Python - Quản lý đơn hàng và sản phẩm/source-code/products-and-orders-dashboard/app/staffs.py#L142)

**Mô tả:** Sau lệnh `return redirect(...)` ở dòng 142, toàn bộ 37 dòng code bên dưới (phiên bản cũ của hàm `edit_staff_info`) là **dead code** — Python sẽ không bao giờ thực thi chúng. Khuyến nghị xóa đi để code sạch hơn.

---

### 📋 Kiểm tra Form Validation & CSRF

| Form | CSRF Token | Validation Client-side | Ghi chú |
|------|-----------|----------------------|---------|
| Đăng nhập | ✅ Có | `required` HTML5 | OK |
| Đăng ký | ✅ Có | `required` HTML5 | OK |
| Thêm sản phẩm | ✅ Có (`csrf_token()`) | `required` HTML5 | OK |
| Sửa sản phẩm | ✅ Có | `required` HTML5 | OK |
| Tạo đơn hàng | ✅ Có | JS validate cart | OK |
| Quên mật khẩu | ✅ Có | `required` HTML5 | OK |
| OTP | ✅ Có | JS 6 số | OK |
| Profile — đổi mật khẩu | ✅ Có | Không có min-length | ⚠️ Xem SEC-04 |
| Thêm/Sửa nhân viên | ✅ Có | `required` HTML5 | OK |

---

## 2. Kiểm thử Bảo mật & Phân quyền

### 🔴 SEC-01 — `new_pass.py` dòng 24: OTP tạo bằng `random` không an toàn

**Mức độ:** HIGH (Security Risk)

**Vị trí:** [`new_pass.py` dòng 24](file:///d:/Workspace/teamwork/Nhóm Python - Quản lý đơn hàng và sản phẩm/source-code/products-and-orders-dashboard/app/new_pass.py#L24)

**Mô tả:** Module `random` của Python sử dụng thuật toán **Mersenne Twister** — là PRNG (Pseudo-Random Number Generator), **không phải CSPRNG** (Cryptographically Secure). Trong lý thuyết, kẻ tấn công quan sát đủ output của `random` có thể dự đoán OTP tiếp theo.

**Code lỗi:**
```python
import random
otp = str(random.randint(100000, 999999))  # ← KHÔNG đủ bảo mật cho OTP!
```

**Cách sửa:**
```python
import secrets
otp = str(secrets.randbelow(900000) + 100000)  # ← Luôn ra số 6 chữ số, đủ bảo mật
```

---

### 🔴 SEC-02 — `orders.py` dòng 134: Kiểm tra role không chính xác

**Mức độ:** HIGH (Logic Security Bug)

**Vị trí:** [`orders.py` dòng 134](file:///d:/Workspace/teamwork/Nhóm Python - Quản lý đơn hàng và sản phẩm/source-code/products-and-orders-dashboard/app/orders.py#L134)

**Mô tả:** Điều kiện cho phép **sửa trạng thái đơn hàng** chỉ kiểm tra `session.get('role')` là "truthy" (tức là khác rỗng/None) — không kiểm tra cụ thể là `'admin'`. Điều này có nghĩa **cả nhân viên (staff) cũng được phép chỉnh sửa đơn hàng**. So sánh với dòng 173 cùng file — tạo đơn hàng mới đúng là kiểm tra `== 'admin'`.

**Code lỗi:**
```python
# Dòng 134 — cho CÙNG staff sửa được!
if session.get('role') and action == 'edit':
    ...

# Dòng 173 — chính xác, chỉ admin mới tạo được
elif session.get('role') == 'admin' and action == 'add':
    ...
```

**Đây là lỗi thiết kế có chủ ý hay không?** Cần xác nhận với nhóm:
- Nếu **staff được phép sửa trạng thái đơn** → logic đúng, nhưng cần comment giải thích rõ.
- Nếu **chỉ admin mới được sửa** → phải đổi thành `session.get('role') == 'admin'`.

---

### 🟠 SEC-03 — `users.py` dòng 46-57: Không xóa session cũ khi đăng nhập

**Mức độ:** MEDIUM (Session Fixation Risk)

**Vị trí:** [`users.py` dòng 46](file:///d:/Workspace/teamwork/Nhóm Python - Quản lý đơn hàng và sản phẩm/source-code/products-and-orders-dashboard/app/users.py#L46)

**Mô tả:** Khi đăng nhập thành công, code chỉ **thêm** các key vào session (`session['id'] = ...`) mà không xóa session cũ bằng `session.clear()` trước. Nếu có dữ liệu dư từ phiên trước (ví dụ `workspace_id` của admin cũ), dữ liệu đó sẽ tiếp tục tồn tại — có thể gây rò rỉ thông tin.

**Code hiện tại:**
```python
if check_password_hash(user.password_hash, password):
    session['email'] = user.email      # ← chỉ thêm vào, không xóa cái cũ
    session['role'] = user.role
    session['id'] = user.id
    ...
```

**Cách sửa:**
```python
if check_password_hash(user.password_hash, password):
    session.clear()  # ← Xóa sạch trước khi set mới
    session['email'] = user.email
    session['role'] = user.role
    ...
```

---

### 🟠 SEC-04 — `profile.py` dòng 53-54: Không validate độ dài mật khẩu mới

**Mức độ:** MEDIUM (Security Gap)

**Vị trí:** [`profile.py` dòng 52-54](file:///d:/Workspace/teamwork/Nhóm Python - Quản lý đơn hàng và sản phẩm/source-code/products-and-orders-dashboard/app/profile.py#L52)

**Mô tả:** Hàm `change_pass()` không kiểm tra độ dài của mật khẩu mới trước khi lưu. Người dùng có thể đặt mật khẩu rỗng (`""`) hoặc 1 ký tự — điều này không nhất quán với luồng `new_pass.py` (yêu cầu `len >= 8`).

**Code lỗi:**
```python
def change_pass(form):
    ...
    if check_password_hash(user.password_hash, current_pass):
        new_pass = form.get('new_password')
        user.password_hash = generate_password_hash(new_pass)  # ← không check len!
```

Thêm vào: `db.session.commit()` ở dòng 59 **luôn được gọi** dù password sai (không thay đổi gì) — không gây lỗi nhưng là commit thừa.

**Cách sửa:**
```python
def change_pass(form):
    ...
    if check_password_hash(user.password_hash, current_pass):
        new_pass = form.get('new_password', '')
        if len(new_pass) < 8:  # ← Thêm validation
            flash(_t('err_password_too_short'), 'error')
            return redirect(url_for('profile.profile_page'))
        user.password_hash = generate_password_hash(new_pass)
        db.session.commit()  # ← Chỉ commit khi thực sự thay đổi
        flash(_t('toast_pass_updated'), 'success')
    else:
        flash(_t('toast_pass_incorrect'), 'error')
    return redirect(url_for('profile.profile_page'))
```

---

### 🟡 SEC-05 — `users.py` dòng 77-84: Logout không xóa `workspace_id`

**Mức độ:** LOW-MEDIUM

**Vị trí:** [`users.py` dòng 75-84](file:///d:/Workspace/teamwork/Nhóm Python - Quản lý đơn hàng và sản phẩm/source-code/products-and-orders-dashboard/app/users.py#L75)

**Code lỗi:**
```python
@users.route("/logout")
def logout():
    if 'id' in session:
        session.pop('id')
        session.pop('email')
        session.pop('role')
        session.pop('username')
        session.pop('language', None)
        # ← THIẾU: session.pop('workspace_id', None)
    return redirect(url_for('users.login'))
```

**Giải pháp đơn giản nhất** — thay toàn bộ bằng `session.clear()`:
```python
@users.route("/logout")
def logout():
    session.clear()  # ← Xóa sạch, không sót gì
    return redirect(url_for('users.login'))
```

---

### ✅ Phân quyền route — Đánh giá chung

| Route | Kiểm tra đăng nhập | Kiểm tra Admin-only | Kết quả |
|-------|---------------------|----------------------|---------|
| `/dashboard` | ✅ | ✅ `role == 'admin'` | ✅ OK |
| `/products` | ✅ | Không cần (staff xem được) | ✅ OK |
| `/orders` | ✅ | Không cần (staff xem được) | ✅ OK (xem SEC-02) |
| `/staffs` | ✅ | ✅ `role != 'admin'` → 403 | ✅ OK |
| `/profile` | ✅ | Không cần (ai cũng vào được) | ✅ OK |
| `/forgot_pass` | Không cần | Không cần | ✅ OK |
| `/new_password` | ✅ `otp_verified` | Không cần | ✅ OK |

---

## 3. Kiểm tra Chất lượng Mã nguồn

### 🟠 QA-01 — `staffs.py`: Hàm `search_staffs()` là dead function

**Vị trí:** [`staffs.py` dòng 204-215](file:///d:/Workspace/teamwork/Nhóm Python - Quản lý đơn hàng và sản phẩm/source-code/products-and-orders-dashboard/app/staffs.py#L204)

**Mô tả:** Hàm `search_staffs()` được định nghĩa (dòng 204) nhưng **không bao giờ được gọi**. Toàn bộ logic search được sao chép y chang và viết lại trực tiếp bên trong `staffs_page()` (dòng 238-246). Đây là vi phạm nguyên tắc DRY (Don't Repeat Yourself) và tạo nên code thừa gây nhầm lẫn.

---

### 🟠 QA-02 — N+1-adjacent Query Pattern trong Search (3 files)

**Vị trí:**
- [`products.py` dòng 47-52](file:///d:/Workspace/teamwork/Nhóm Python - Quản lý đơn hàng và sản phẩm/source-code/products-and-orders-dashboard/app/products.py#L47)
- [`orders.py` dòng 122-129](file:///d:/Workspace/teamwork/Nhóm Python - Quản lý đơn hàng và sản phẩm/source-code/products-and-orders-dashboard/app/orders.py#L122)
- [`staffs.py` dòng 240-244](file:///d:/Workspace/teamwork/Nhóm Python - Quản lý đơn hàng và sản phẩm/source-code/products-and-orders-dashboard/app/staffs.py#L240)

**Mô tả:** Mỗi khi tìm kiếm, code chạy **5-8 query riêng biệt** (một query cho mỗi trường), rồi gộp kết quả và dùng `list(set(...))` để loại trùng. Pattern này sẽ **chậm đáng kể** khi data lớn và tạo gánh nặng cho database.

**Code hiện tại (products.py):**
```python
searched_products = db.session.query(Product).filter(..., Product.name.like(...)).all()
searched_products += db.session.query(Product).filter(..., Product.sku.like(...)).all()
searched_products += db.session.query(Product).filter(..., Product.category.like(...)).all()
searched_products += db.session.query(Product).filter(..., Product.price.like(...)).all()
searched_products += db.session.query(Product).filter(..., Product.stock.like(...)).all()
searched_products += db.session.query(Product).filter(..., Product.status.like(...)).all()
products = list(set(searched_products))  # ← 6 queries!
```

**Cách tối ưu (dùng `or_()`):**
```python
from sqlalchemy import or_
searched_products = Product.query.filter(
    Product.admin_id == session.get('workspace_id'),
    or_(
        Product.name.like(f"%{keyword}%"),
        Product.sku.like(f"%{keyword}%"),
        Product.category.like(f"%{keyword}%"),
        Product.status.like(f"%{keyword}%"),
    )
).all()  # ← 1 query duy nhất!
```

> [!TIP]
> Với quy mô đồ án (dưới vài trăm bản ghi), hiệu năng hiện tại vẫn chấp nhận được và sẽ không crash trong demo. Đây là điểm tối ưu nên làm sau khi thuyết trình.

---

### 🟡 QA-03 — `orders.py` dòng 79, 87, 98: `db.session.commit()` trong vòng lặp

**Vị trí:**
- [`orders.py` dòng 79](file:///d:/Workspace/teamwork/Nhóm Python - Quản lý đơn hàng và sản phẩm/source-code/products-and-orders-dashboard/app/orders.py#L79) — `create_order_items()`
- [`orders.py` dòng 87](file:///d:/Workspace/teamwork/Nhóm Python - Quản lý đơn hàng và sản phẩm/source-code/products-and-orders-dashboard/app/orders.py#L87) — `reduce_stock()`
- [`orders.py` dòng 98](file:///d:/Workspace/teamwork/Nhóm Python - Quản lý đơn hàng và sản phẩm/source-code/products-and-orders-dashboard/app/orders.py#L98) — `restock_returned_item()`

**Mô tả:** `db.session.commit()` được gọi **bên trong vòng lặp** — mỗi item tạo ra một transaction riêng. Nếu tạo đơn hàng có 10 sản phẩm → 10 commits riêng lẻ. Ngoài hiệu năng kém, nếu lỗi xảy ra ở item thứ 5, items 1-4 đã được lưu nhưng items 5-10 thì không → **dữ liệu bất nhất** (partial commit).

**Cách sửa:**
```python
def create_order_items(items, order_id):
    for item in items:
        ...
        db.session.add(new_order_item)
        # ← KHÔNG commit trong loop
    db.session.commit()  # ← Commit một lần sau khi add hết
```

---

### 🟡 QA-04 — `products.py` dòng 21: `filter_by_condition()` trả về kiểu dữ liệu không nhất quán

**Vị trí:** [`products.py` dòng 18-23](file:///d:/Workspace/teamwork/Nhóm Python - Quản lý đơn hàng và sản phẩm/source-code/products-and-orders-dashboard/app/products.py#L18)

**Mô tả:** Hàm trả về 3 kiểu dữ liệu khác nhau tùy nhánh:
- `low_stock` → `list` (`.all()`)
- Có `condition` khác → **`Query` object** (chưa `.all()`)
- Không có `condition` → `list` (relationship ORM)

Điều này có thể gây lỗi nếu template hoặc caller mong đợi một kiểu cố định.

```python
def filter_by_condition(form):
    condition = form.get('product_status')

    if condition == 'low_stock':
        return Product.query.filter(...).all()    # ← list
    elif condition:
        return Product.query.filter_by(...)       # ← Query object (THIẾU .all()!)
    
    return db.session.get(User, ...).products     # ← list (relationship)
```

**Cách sửa:**
```python
elif condition:
    return Product.query.filter_by(admin_id=session.get('workspace_id'), status=condition).all()
    #                                                                                     ↑ Thêm .all()
```

---

### 🟡 QA-05 — Dark Mode: Một số phần tử thiếu class `dark:`

**Phạm vi kiểm tra:** `products.html`, `orders.html`, `dashboard.html`

Nhìn chung, các template đã áp dụng dark mode khá đầy đủ. Tuy nhiên, phát hiện một số điểm cần lưu ý:

| Vị trí | Vấn đề | Ghi chú |
|--------|---------|---------|
| `orders.html` dòng 141 | `<form accept="/logout">` | Sai thuộc tính (xem BUG-04) |
| Modal overlay | `bg-[#00000073]` | Nên thêm `dark:bg-black/75` để tối hơn |
| Text cứng `text-[#101828]` | Không responsive với dark mode | Nên dùng `text-gray-900 dark:text-slate-100` |
| Các input `border-gray-200` | Đa phần đã có `dark:border-slate-700` | ✅ OK |
| Sidebar background `bg-white` | Đã có `dark:bg-slate-900` | ✅ OK |

> [!NOTE]
> Hệ thống dark mode được kiểm soát bằng class `dark` trên thẻ `<html>` — cơ chế này đúng và nhất quán với cách Tailwind CSS v3 hoạt động trong chế độ `class strategy`.

---

## 4. Kịch bản Kiểm thử & Demo Checklist

### 🧪 7 Test Case Bắt buộc trước giờ thuyết trình

---

#### TC-01: Đăng nhập và phân quyền Admin vs Staff

**Bước thực hiện:**
1. Mở trình duyệt ở chế độ Incognito
2. Đăng nhập bằng tài khoản **Admin** → kiểm tra:
   - Sidebar hiển thị đầy đủ 5 tab (Dashboard, Products, Orders, Staffs, Profile)
   - Tự động chuyển về `/dashboard`
3. Logout → Đăng nhập bằng tài khoản **Staff** → kiểm tra:
   - Sidebar **không có** tab Dashboard và Staffs
   - Chỉ thấy Products, Orders, Profile
   - Thử nhập URL `/dashboard` → phải bị redirect về login hoặc `/products`
   - Thử nhập URL `/staffs` → phải nhận HTTP 403

**Kết quả kỳ vọng:** ✅ Phân quyền hoạt động đúng  
**Mức độ ưu tiên:** 🔴 PHẢI PASS

---

#### TC-02: Tạo đơn hàng với sản phẩm đủ tồn kho (Happy path)

**Bước thực hiện:**
1. Đăng nhập Admin
2. Vào `/orders` → bấm "Tạo đơn hàng mới"
3. Thêm ít nhất 2 sản phẩm vào giỏ hàng, số lượng **trong phạm vi tồn kho**
4. Điền thông tin khách hàng → Submit

**Kết quả kỳ vọng:**
- Đơn hàng được tạo thành công
- Tồn kho các sản phẩm giảm đúng số lượng
- Hiện toast "Tạo đơn hàng thành công"

**Mức độ ưu tiên:** 🔴 PHẢI PASS — đây là flow demo chính

---

#### TC-03: Tạo đơn hàng vượt tồn kho (Edge case — BUG-01)

**Bước thực hiện:**
1. Tạo một sản phẩm với stock = 2
2. Vào tạo đơn hàng → chọn sản phẩm đó với quantity = 10
3. Submit

**Kết quả kỳ vọng:** Flash thông báo lỗi, không tạo đơn, không có lỗi 500  
**Mức độ ưu tiên:** 🔴 CẦN TEST — nếu thấy lỗi 500 thì **phải sửa BUG-01 trước demo**

---

#### TC-04: Luồng Quên mật khẩu → OTP → Đặt mật khẩu mới

**Bước thực hiện:**
1. Logout → vào `/forgot_pass`
2. Nhập email hợp lệ → Submit
3. Kiểm tra console server để lấy OTP (hoặc kiểm tra email nếu mail được cấu hình)
4. Nhập OTP đúng → Submit
5. Nhập mật khẩu mới (>= 8 ký tự) → Submit
6. Đăng nhập lại bằng mật khẩu mới

**Kết quả kỳ vọng:** Đổi mật khẩu thành công, đăng nhập được  
**Mức độ ưu tiên:** 🟠 NÊN TEST

---

#### TC-05: Thêm và xóa nhân viên (Admin only)

**Bước thực hiện:**
1. Đăng nhập Admin → vào `/staffs`
2. Thêm nhân viên mới với đầy đủ thông tin
3. Kiểm tra nhân viên xuất hiện trong danh sách
4. Bấm Sửa → đổi tên → kiểm tra cập nhật
5. Bấm Xóa → xác nhận → kiểm tra nhân viên biến mất

**Kết quả kỳ vọng:** CRUD nhân viên hoạt động đúng  
**Mức độ ưu tiên:** 🟠 NÊN TEST

---

#### TC-06: Đổi Dark/Light Mode và đổi ngôn ngữ VI/EN

**Bước thực hiện:**
1. Vào `/profile`
2. Chuyển sang Dark Mode → bấm lưu → kiểm tra toàn bộ giao diện (sidebar, modal, bảng data)
3. Chuyển sang Light Mode → kiểm tra lại
4. Đổi ngôn ngữ sang Tiếng Việt → kiểm tra nhãn menu và nút bấm
5. Đổi lại Tiếng Anh

**Kết quả kỳ vọng:**
- Dark mode áp dụng đồng bộ cho tất cả trang
- Ngôn ngữ thay đổi đồng bộ

**Mức độ ưu tiên:** 🟡 NÊN TEST — đây là feature showcase ấn tượng

---

#### TC-07: Cập nhật trạng thái đơn hàng (State Machine)

**Bước thực hiện:**
1. Chọn một đơn hàng đang `pending`
2. Sửa trạng thái → `processing` → kiểm tra OK
3. Sửa → `completed` → kiểm tra OK
4. Thử sửa đơn đã `completed` → kiểm tra bị chặn với thông báo lỗi
5. Chọn đơn `processing` → sửa về `pending` → phải bị chặn (không phải chuyển hợp lệ)

**Kết quả kỳ vọng:** State machine hoạt động đúng theo bảng `valid_transitions`  
**Mức độ ưu tiên:** 🟠 NÊN TEST

---

### 🎯 Kịch bản Demo Gây Ấn tượng với Giảng viên

**Gợi ý trình tự demo mượt (khoảng 8-10 phút):**

```
1. [1 phút] Giới thiệu + Đăng nhập Admin
   → Màn hình login đẹp, nhập email/pass, bấm login
   → Dashboard hiện ra với số liệu tổng quan

2. [2 phút] Quản lý sản phẩm
   → Hiện danh sách sản phẩm
   → Dùng tính năng TÌM KIẾM (gõ tên SP)
   → Lọc theo trạng thái (active/inactive/low_stock)
   → Thêm 1 sản phẩm mới (điền form modal)

3. [2 phút] Quản lý đơn hàng
   → Tạo đơn hàng mới (thêm 2-3 sản phẩm vào giỏ)
   → Xem chi tiết đơn hàng vừa tạo
   → Cập nhật trạng thái pending → processing

4. [1 phút] Quản lý nhân viên (Admin only)
   → Hiện danh sách nhân viên
   → Nói: "Staff đăng nhập sẽ không thấy tab này"

5. [1 phút] Đăng xuất → Đăng nhập Staff
   → Sidebar ẩn tab Dashboard và Staffs
   → Thử nhập /staffs → 403 Forbidden

6. [1 phút] Profile + Dark Mode
   → Vào Profile
   → Bật Dark Mode → toàn bộ UI chuyển ngay lập tức
   → Đổi ngôn ngữ VI/EN

7. [1 phút] Forgot Password
   → Nhập email → nhận OTP → xác thực → đặt mật khẩu mới
```

> [!TIP]
> **Chuẩn bị trước demo:** Tạo sẵn 1 tài khoản Admin + 2 nhân viên + 5-10 sản phẩm + 3-5 đơn hàng ở các trạng thái khác nhau. Tránh demo trên database trống vì bảng rỗng trông không thuyết phục.

> [!IMPORTANT]
> **Ưu tiên sửa trước demo:**
> 1. **BUG-01** (crash khi tạo đơn vượt stock) — nguy cơ 500 error cao nhất
> 2. **BUG-02** (stock=0 nhưng status=active khi thêm sản phẩm) — dữ liệu sai
> 3. **BUG-04** (nút Logout mobile không hoạt động trong orders.html) — dễ nhìn thấy
> 4. **BUG-03** (redirect sai trang khi email không tồn tại) — UX kém

---

## 📊 Tổng kết

| Mức độ | Số lượng | Danh sách |
|--------|----------|-----------|
| 🔴 Critical/High Bug | 3 | BUG-01, BUG-02, SEC-01 |
| 🟠 Medium Bug/Security | 5 | BUG-03, BUG-04, SEC-02, SEC-03, SEC-04 |
| 🟡 Low/Code Quality | 6 | BUG-05, SEC-05, QA-01~05 |
| ✅ Đã ổn | — | CSRF, Auth check, State machine, Dark mode cơ bản |

**Đánh giá tổng thể:** Dự án ở mức **tốt cho đồ án sinh viên** — UI/UX sạch sẽ, có đầy đủ tính năng, phân quyền cơ bản hoạt động. Các lỗi nghiêm trọng tập trung ở **logic xử lý đơn hàng** và **bảo mật OTP**. Cần xử lý BUG-01, BUG-04 trước giờ demo để tránh bị "lật xe".
