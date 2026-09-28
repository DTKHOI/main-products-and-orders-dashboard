// Mở modal
function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.remove("hidden");
    // Khóa cuộn trang khi mở modal (tuỳ chọn)
    document.body.classList.add("overflow-hidden");
  }
}

// Đóng modal
function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.add("hidden");
    document.body.classList.remove("overflow-hidden");

    // Tự động xóa sạch dữ liệu nhập dở trong form khi đóng modal
    const form = modal.querySelector("form");
    if (form) {
      form.reset();
    }
  }
}

// 3. Xử lý đóng modal khi click ra ngoài nền mờ (loại bỏ window.addEventListener)
document.addEventListener("DOMContentLoaded", () => {
  const modals = document.querySelectorAll(".modal-overlay");

  modals.forEach((modal) => {
    modal.addEventListener("click", (e) => {
      // Chỉ đóng khi click đích danh vào phần nền đen (e.target === modal)
      // Không đóng nếu click vào khung trắng của form bên trong
      if (e.target === modal) {
        closeModal(modal.id);
      }
    });
  });
});

// Hàm mở Modal Chỉnh Sửa và lấy dữ liệu
function openEditModal(buttonElement) {
  // Lấy thẻ <div> cha chứa thông tin của cả dòng (chứa data-id, data-name...)
  const rowItem = buttonElement.closest(".item");
  if (!rowItem) return;

  // Lấy dữ liệu từ các attribute data-*
  const id = rowItem.getAttribute("data-id");
  const name = rowItem.getAttribute("data-name");
  const price = rowItem.getAttribute("data-price");
  const quantity = rowItem.getAttribute("data-quantity");
  const status = rowItem.getAttribute("data-status");
  const category = rowItem.getAttribute("data-category");

  // Lấy url ảnh từ thẻ <img> bên trong dòng đó
  const imgElement = rowItem.querySelector("img");
  const imgUrl = imgElement ? imgElement.getAttribute("src") : "";

  // Đổ dữ liệu vào Form Edit Modal
  document.getElementById("edit_original_id").value = id;
  document.getElementById("edit_product_id").value = id;
  document.getElementById("edit_product_name").value = name;
  document.getElementById("edit_product_price").value = price;
  document.getElementById("edit_product_quantity").value = quantity;
  document.getElementById("edit_product_img").value = imgUrl;

  // Đặt trạng thái cho thẻ <select>
  const categorySelect = document.getElementById("edit_product_category");
  Array.from(categorySelect.options).forEach((opt) => {
    if (opt.value.toLowerCase() === category.toLowerCase()) opt.selected = true;
  });

  // Đặt trạng thái cho Radio button (Status)
  if (status === "active") {
    document.getElementById("edit_status_active").checked = true;
  } else {
    document.getElementById("edit_status_inactive").checked = true;
  }

  // Gọi hàm mở Modal chuẩn
  openModal("editModal");
}

// Hàm mở Modal Xóa và truyền ID
function openDeleteModal(buttonElement) {
  const rowItem = buttonElement.closest(".item");
  if (!rowItem) return;

  const id = rowItem.getAttribute("data-id");
  const name = rowItem.getAttribute("data-name");

  // Đưa tên lên thông báo để người dùng chắc chắn
  document.getElementById("delete_product_name").innerText = name;
  // Đưa ID vào input ẩn để gửi form lên server xóa
  document.getElementById("delete_product_id").value = id;

  openModal("deleteModal");
}

function openEditOrderModal(buttonElement) {
  const rowItem = buttonElement.closest(".item");
  if (!rowItem) return;

  const orderId = rowItem.getAttribute("data-order-id");
  const name = rowItem.getAttribute("data-name");
  const phone = rowItem.getAttribute("data-phone") || "";
  const email = rowItem.getAttribute("data-email") || "";
  const address = rowItem.getAttribute("data-address");
  const status = (
    rowItem.getAttribute("data-status") || "pending"
  ).toLowerCase();

  // Đổ dữ liệu vào text inputs
  document.getElementById("display_order_id").innerText = `#${orderId}`;
  document.getElementById("edit_order_id").value = orderId;
  document.getElementById("edit_customer_name").value = name;
  document.getElementById("edit_customer_phone").value = phone;
  document.getElementById("edit_customer_email").value = email;
  document.getElementById("edit_customer_address").value = address;

  // Tự động chọn radio button theo status
  const statusRadio = document.getElementById(`status_${status}`);
  if (statusRadio) {
    statusRadio.checked = true;
  }

  openModal("editOrderModal");
}
