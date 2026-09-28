let cart = [];

// 1. Điều khiển đóng/mở Modal
function openOrderModal() {
  document.getElementById("orderModal").classList.remove("hidden");
}

function closeOrderModal() {
  document.getElementById("orderModal").classList.add("hidden");
}

// Đóng khi click vào vùng nền mờ bên ngoài hộp thoại
window.addEventListener("click", function (e) {
  const modal = document.getElementById("orderModal");
  if (e.target === modal) {
    closeOrderModal();
  }
});

// 2. Thêm món vào danh sách tạm
function addItem() {
  const select = document.getElementById("prodSelect");
  const qtyInput = document.getElementById("prodQuantity");

  const prodId = select.value;
  if (!prodId) {
    alert("Please select a product!");
    return;
  }

  const option = select.options[select.selectedIndex];
  const name = option.getAttribute("data-name");
  const price = parseInt(option.getAttribute("data-price"));
  const quantity = parseInt(qtyInput.value) || 1;

  const existing = cart.find((item) => item.id === prodId);
  if (existing) {
    existing.quantity += quantity;
  } else {
    cart.push({
      id: prodId,
      name: name,
      price: price,
      quantity: quantity,
    });
  }

  select.value = "";
  qtyInput.value = "1";
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
  const emptyText = document.getElementById("emptyText");
  const totalDisplay = document.getElementById("totalDisplay");

  list.innerHTML = "";
  if (cart.length === 0) {
    list.appendChild(emptyText);
    totalDisplay.innerText = "0";
    return;
  }

  let total = 0;
  cart.forEach((item) => {
    const subtotal = item.price * item.quantity;
    total += subtotal;

    const row = document.createElement("div");
    row.className = "flex items-center justify-between p-3 bg-white text-sm";
    row.innerHTML = `
                    <div>
                        <p class="font-semibold text-slate-800">${item.name}</p>
                        <p class="text-xs text-slate-500">${item.price.toLocaleString("vi-VN")}đ × ${item.quantity}</p>
                    </div>
                    <div class="flex items-center gap-3">
                        <span class="font-bold text-slate-800">${subtotal.toLocaleString("vi-VN")}đ</span>
                        <button type="button" onclick="removeItem('${item.id}')" class="text-red-500 hover:text-red-700 text-xs font-medium">Xóa</button>
                    </div>
                `;
    list.appendChild(row);
  });

  totalDisplay.innerText = total.toLocaleString("vi-VN");
}

// 5. Đồng bộ thông tin vào form ẩn trước khi POST lên Flask
function prepareSubmit() {
  const name = document.getElementById("custName").value.trim();
  const phone = document.getElementById("custPhone").value.trim();
  const address = document.getElementById("custAddress").value.trim();

  if (!name || !phone || !address) {
    alert("Please provide your full name, phone number, and delivery address!");
    return false;
  }

  if (cart.length === 0) {
    alert("Please add at least one item to your order!");
    return false;
  }

  // Gán dữ liệu vào các thẻ hidden input
  document.getElementById("hiddenName").value = name;
  document.getElementById("hiddenPhone").value = phone;
  document.getElementById("hiddenAddress").value = address;
  document.getElementById("hiddenCartData").value = JSON.stringify(cart);

  return true;
}
