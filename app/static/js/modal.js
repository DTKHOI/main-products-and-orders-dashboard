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

function updateOrderStatusUI(currentStatus, originalStatus) {
    const badge = document.getElementById("current_status_badge");
    const btnNext = document.getElementById("btn_next_status");
    const btnNextText = document.getElementById("btn_next_status_text");
    const btnCancel = document.getElementById("btn_cancel_status");
    const isVi = document.documentElement.lang === "vi";

    if (!badge) return;

    const statusConfig = {
        pending: {
            label: isVi ? "Chờ xử lý" : "Pending",
            class: "bg-yellow-100 dark:bg-amber-950/60 text-yellow-800 dark:text-amber-400 border border-transparent dark:border-amber-800/50",
        },
        processing: {
            label: isVi ? "Đang xử lý" : "Processing",
            class: "bg-blue-100 dark:bg-blue-950/60 text-blue-800 dark:text-blue-400 border border-transparent dark:border-blue-800/50",
        },
        completed: {
            label: isVi ? "Hoàn thành" : "Completed",
            class: "bg-green-100 dark:bg-emerald-950/60 text-green-800 dark:text-emerald-400 border border-transparent dark:border-emerald-800/50",
        },
        canceled: {
            label: isVi ? "Đã hủy" : "Canceled",
            class: "bg-rose-100 dark:bg-rose-950/60 text-red-400 dark:text-rose-400 border border-transparent dark:border-rose-800/50",
        },
    };

    const cfg = statusConfig[currentStatus] || statusConfig.pending;
    badge.className = `inline-flex items-center rounded-full px-3 py-1 text-xs font-semibold ${cfg.class}`;
    badge.innerText = cfg.label;

    // Nếu trạng thái ban đầu là completed hoặc canceled thì không thể thay đổi trạng thái
    if (originalStatus === "completed" || originalStatus === "canceled") {
        if (btnNext) btnNext.classList.add("hidden");
        if (btnCancel) btnCancel.classList.add("hidden");
        return;
    }

    if (currentStatus === "pending") {
        if (btnNext) {
            btnNext.classList.remove("hidden");
            if (btnNextText) btnNextText.innerText = isVi ? "Chuyển sang Đang xử lý" : "Move to Processing";
        }
        if (btnCancel) btnCancel.classList.remove("hidden");
    } else if (currentStatus === "processing") {
        if (btnNext) {
            btnNext.classList.remove("hidden");
            if (btnNextText) btnNextText.innerText = isVi ? "Hoàn thành đơn hàng" : "Mark as Completed";
        }
        if (btnCancel) btnCancel.classList.remove("hidden");
    } else {
        if (btnNext) btnNext.classList.add("hidden");
        if (btnCancel) btnCancel.classList.add("hidden");
    }
}

function advanceOrderStatus() {
    const statusInput = document.getElementById("edit_order_status");
    if (!statusInput) return;

    const current = statusInput.value;
    const original = statusInput.dataset.originalStatus;

    if (original === "completed") {
        const isVi = document.documentElement.lang === "vi";
        const msg = isVi ? "Không thể chỉnh sửa đơn hàng đã hoàn thành." : "Cannot update completed order.";
        if (typeof showToast === "function") showToast(msg, "error");
        return;
    }

    let nextStatus = current;
    if (current === "pending") {
        nextStatus = "processing";
    } else if (current === "processing") {
        nextStatus = "completed";
    }

    statusInput.value = nextStatus;
    updateOrderStatusUI(nextStatus, original);
}

function cancelOrderStatus() {
    const statusInput = document.getElementById("edit_order_status");
    if (!statusInput) return;

    const original = statusInput.dataset.originalStatus;
    if (original === "completed") {
        const isVi = document.documentElement.lang === "vi";
        const msg = isVi ? "Không thể chỉnh sửa đơn hàng đã hoàn thành." : "Cannot update completed order.";
        if (typeof showToast === "function") showToast(msg, "error");
        return;
    }

    statusInput.value = "canceled";
    updateOrderStatusUI("canceled", original);
}

function openEditOrderModal(buttonElement) {
    const rowItem = buttonElement.closest(".item");
    if (!rowItem) return;

    const orderId = rowItem.getAttribute("data-order-id");
    const name = rowItem.getAttribute("data-name");
    const phone = rowItem.getAttribute("data-phone") || "";
    const email = (rowItem.getAttribute("data-email") || "").trim();
    const address = rowItem.getAttribute("data-address");
    const status = (rowItem.getAttribute("data-status") || "pending").toLowerCase();

    // Đổ dữ liệu vào text inputs
    document.getElementById("display_order_id").innerText = `#${orderId}`;
    document.getElementById("edit_order_id").value = orderId;
    document.getElementById("edit_customer_name").value = name;
    document.getElementById("edit_customer_phone").value = phone;
    document.getElementById("edit_customer_email").value = email;
    document.getElementById("edit_customer_address").value = address;

    // Cập nhật trạng thái
    const statusInput = document.getElementById("edit_order_status");
    if (statusInput) {
        statusInput.value = status;
        statusInput.dataset.originalStatus = status;
    }

    updateOrderStatusUI(status, status);

    // Khóa chỉnh sửa nếu đơn hàng đã completed hoặc canceled
    const isCompleted = status === "completed";
    const isCanceled = status === "canceled";
    const isLocked = isCompleted || isCanceled;

    const form = document.getElementById("edit-order-form");
    if (form) {
        const inputs = form.querySelectorAll("input:not([type=hidden]), textarea");
        inputs.forEach((input) => {
            input.readOnly = isLocked;
            if (isLocked) {
                input.classList.add("opacity-70", "cursor-not-allowed");
            } else {
                input.classList.remove("opacity-70", "cursor-not-allowed");
            }
        });
    }

    const submitBtn = document.getElementById("edit-order-submit-btn");
    if (submitBtn) {
        if (isLocked) {
            submitBtn.classList.add("opacity-50", "cursor-not-allowed");
        } else {
            submitBtn.classList.remove("opacity-50", "cursor-not-allowed");
        }
    }

    openModal("editOrderModal");
}

document.addEventListener("DOMContentLoaded", () => {
    const editOrderForm = document.getElementById("edit-order-form");
    if (editOrderForm) {
        editOrderForm.addEventListener("submit", function (e) {
            const statusInput = document.getElementById("edit_order_status");
            const originalStatus = statusInput ? statusInput.dataset.originalStatus : "";
            const isVi = document.documentElement.lang === "vi";

            if (originalStatus === "completed") {
                e.preventDefault();
                const msg = isVi ? "Không thể chỉnh sửa đơn hàng đã hoàn thành." : "Cannot update completed order.";
                if (typeof showToast === "function") {
                    showToast(msg, "error");
                } else {
                    alert(msg);
                }
                return false;
            }

            if (originalStatus === "canceled") {
                e.preventDefault();
                const msg = isVi ? "Không thể cập nhật đơn hàng đã hủy." : "Cannot update cancelled order.";
                if (typeof showToast === "function") {
                    showToast(msg, "error");
                } else {
                    alert(msg);
                }
                return false;
            }
        });
    }
});

// Hàm đóng/mở dropdown có thể dùng ở bất kỳ trang nào
window.toggleDropdown = function (dropdownId, event) {
    if (event) {
        event.stopPropagation(); // Ngăn sự kiện nổi bọt lên window
    }
    const dropdown = document.getElementById(dropdownId);
    if (!dropdown) return;

    // Đóng tất cả các dropdown khác đang mở trước khi mở dropdown này
    document.querySelectorAll(".dropdown-menu").forEach((el) => {
        if (el.id !== dropdownId) el.classList.add("hidden");
    });

    // Đảo trạng thái hiển thị
    dropdown.classList.toggle("hidden");
};

// Lắng nghe sự kiện click bất kỳ đâu trên màn hình: nếu click ra ngoài khoảng trống thì tự động đóng menu
window.addEventListener("click", (e) => {
    document.querySelectorAll(".dropdown-menu").forEach((menu) => {
        // Nếu click ra ngoài menu và không phải click vào menu đó
        if (!menu.classList.contains("hidden") && !menu.contains(e.target)) {
            menu.classList.add("hidden");
        }
    });
});
