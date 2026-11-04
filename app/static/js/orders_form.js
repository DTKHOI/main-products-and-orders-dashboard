let cart = [];

function isVietnamese() {
    return document.documentElement.lang === "vi";
}

// 1. Điều khiển đóng/mở Modal
function openOrderModal() {
    document.getElementById("orderModal").classList.remove("hidden");
    document.body.classList.add("overflow-hidden");
}

function closeOrderModal() {
    document.getElementById("orderModal").classList.add("hidden");
    document.body.classList.remove("overflow-hidden");
    resetOrderForm();
}

// Đóng khi click vào vùng nền mờ bên ngoài hộp thoại
window.addEventListener("click", function (e) {
    const modal = document.getElementById("orderModal");
    if (e.target === modal) {
        closeOrderModal();
    }
});

// Cập nhật thuộc tính max động khi chọn sản phẩm
function updateMaxQuantity() {
    const select = document.getElementById("prodSelect");
    const qtyInput = document.getElementById("prodQuantity");
    const warning = document.getElementById("stockWarning");
    const btnAdd = document.getElementById("btnAddProd");
    const isVi = isVietnamese();

    if (!select.value) return;

    const option = select.options[select.selectedIndex];
    const stock = parseInt(option.getAttribute("data-stock"), 10) || 0;

    qtyInput.max = stock;

    if (stock <= 0) {
        qtyInput.value = 0;
        qtyInput.disabled = true;
        btnAdd.disabled = true;
        btnAdd.classList.add("opacity-50", "cursor-not-allowed");
        warning.innerText = isVi ? "Hết hàng!" : "Out of stock!";
        warning.className = "mt-1 block text-xs text-red-500 font-semibold";
    } else {
        qtyInput.disabled = false;
        btnAdd.disabled = false;
        btnAdd.classList.remove("opacity-50", "cursor-not-allowed");
        if (parseInt(qtyInput.value, 10) > stock || parseInt(qtyInput.value, 10) <= 0) {
            qtyInput.value = 1;
        }
        warning.innerText = isVi ? `(tối đa: ${stock})` : `(max: ${stock})`;
        warning.className = "text-center text-xs text-slate-500 dark:text-slate-400";
    }
}

// Chặn người dùng gõ số vượt quá max
document.addEventListener("DOMContentLoaded", () => {
    const qtyInput = document.getElementById("prodQuantity");
    if (qtyInput) {
        qtyInput.addEventListener("input", function () {
            const max = parseInt(this.max, 10);
            const val = parseInt(this.value, 10);
            const isVi = isVietnamese();

            if (max && val > max) {
                alert(isVi ? `Số lượng tối đa có thể chọn là ${max}!` : `Maximum available stock is ${max}!`);
                this.value = max;
            }
        });
    }
});

// 2. Thêm món vào danh sách tạm
function addItem() {
    const select = document.getElementById("prodSelect");
    const qtyInput = document.getElementById("prodQuantity");
    const isVi = isVietnamese();

    const prodId = select.value;
    if (!prodId) {
        alert(isVi ? "Vui lòng chọn một sản phẩm!" : "Please select a product!");
        return;
    }

    const option = select.options[select.selectedIndex];
    const name = option.getAttribute("data-name");
    const price = parseFloat(option.getAttribute("data-price")) || 0;
    const stock = parseInt(option.getAttribute("data-stock"), 10) || 0;
    const quantity = parseInt(qtyInput.value, 10) || 1;

    if (quantity <= 0) {
        alert(isVi ? "Số lượng phải ít nhất là 1!" : "Quantity must be at least 1!");
        return;
    }

    const existing = cart.find((item) => item.id === prodId);
    const currentInCart = existing ? existing.quantity : 0;

    // Kiểm tra tổng số lượng đã chọn + số lượng muốn thêm có vượt tồn kho không
    if (currentInCart + quantity > stock) {
        alert(isVi ? `Không thể thêm: Đã có ${currentInCart} trong giỏ, tồn kho tối đa là ${stock}.` : `Addition failed: ${currentInCart} in cart, max stock is ${stock}.`);
        return;
    }

    if (existing) {
        existing.quantity += quantity;
    } else {
        cart.push({
            id: prodId,
            name: name,
            price: price,
            quantity: quantity,
            stock: stock,
        });
    }

    // Reset dropdown về ban đầu
    select.value = "";
    qtyInput.value = "1";
    qtyInput.removeAttribute("max");
    document.getElementById("stockWarning").innerText = "";
    renderCart();
}

// 3. Xóa món
function removeItem(prodId) {
    cart = cart.filter((item) => item.id !== prodId);
    renderCart();
}

// 4. Render lại giao diện giỏ hàng
function renderCart() {
    const list = document.getElementById("cartList");
    const totalDisplay = document.getElementById("totalDisplay");
    const isVi = isVietnamese();

    list.innerHTML = "";
    if (cart.length === 0) {
        list.innerHTML = `<div id="emptyText" class="p-6 text-center text-xs text-slate-400 dark:text-slate-500">${isVi ? "Chưa có sản phẩm nào được chọn." : "No products selected."}</div>`;
        totalDisplay.innerText = "0";
        return;
    }

    let total = 0;
    cart.forEach((item) => {
        const subtotal = item.price * item.quantity;
        total += subtotal;

        const row = document.createElement("div");
        row.className = "flex items-center justify-between p-3 dark:bg-slate-800 bg-white text-sm border-b border-slate-100 dark:border-slate-800 last:border-b-0";
        row.innerHTML = `
      <div>
        <p class="font-semibold dark:text-white text-slate-800">${item.name}</p>
        <p class="text-xs dark:text-slate-300 text-slate-500">${item.price.toLocaleString("vi-VN")}đ × ${item.quantity}</p>
      </div>
      <div class="flex items-center gap-3">
        <span class="font-bold text-slate-800 dark:text-slate-200">${subtotal.toLocaleString("vi-VN")}đ</span>
        <button type="button" onclick="removeItem('${item.id}')" class="text-red-500 dark:text-rose-400 hover:text-red-700 dark:hover:text-rose-300 text-xs font-medium cursor-pointer">${isVi ? "Xóa" : "Remove"}</button>
      </div>
    `;
        list.appendChild(row);
    });

    totalDisplay.innerText = total.toLocaleString("vi-VN");
}

// Reset form sau khi đóng hoặc hoàn tất
function resetOrderForm() {
    document.getElementById("custName").value = "";
    document.getElementById("custPhone").value = "";
    document.getElementById("custAddress").value = "";
    document.getElementById("prodSelect").value = "";
    document.getElementById("prodQuantity").value = "1";
    document.getElementById("stockWarning").innerText = "";
    cart = [];
    renderCart();
}

// 5. Đồng bộ thông tin vào form ẩn trước khi POST lên Flask
function prepareSubmit() {
    const name = document.getElementById("custName").value.trim();
    const phone = document.getElementById("custPhone").value.trim();
    const address = document.getElementById("custAddress").value.trim();
    const isVi = isVietnamese();

    if (!name || !phone || !address) {
        alert(isVi ? "Vui lòng cung cấp tên khách hàng, số điện thoại và địa chỉ giao hàng!" : "Please provide customer name, phone number, and delivery address!");
        return false;
    }

    if (cart.length === 0) {
        alert(isVi ? "Vui lòng thêm ít nhất một sản phẩm vào đơn hàng!" : "Please add at least one item to your order!");
        return false;
    }

    document.getElementById("hiddenName").value = name;
    document.getElementById("hiddenPhone").value = phone;
    document.getElementById("hiddenAddress").value = address;
    document.getElementById("hiddenCartData").value = JSON.stringify(cart);

    return true;
}
