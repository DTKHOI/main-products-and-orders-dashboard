// Hàm thiết lập ẩn/hiện mật khẩu có thể gọi lại ở mọi trang
function setupPasswordToggle(inputId, showBtnId, hideBtnId) {
    const passInput = document.getElementById(inputId);
    const showPass = document.getElementById(showBtnId);
    const hidePass = document.getElementById(hideBtnId);

    // Nếu không tìm thấy các phần tử trên trang này thì dừng lại để tránh lỗi
    if (!passInput || !showPass || !hidePass) return;

    // 1. Theo dõi sự kiện gõ phím để ẩn/hiện icon con mắt
    passInput.addEventListener("input", () => {
        if (passInput.value.trim() !== "") {
            // Có chữ -> Hiện nút mở mắt (showPass) mặc định, ẩn nút nhắm (hidePass)
            if (passInput.getAttribute("type") === "password") {
                showPass.classList.remove("hidden");
                hidePass.classList.add("hidden");
            } else {
                hidePass.classList.remove("hidden");
                showPass.classList.add("hidden");
            }
        } else {
            // Ô input rỗng -> Ẩn sạch cả 2 icon
            showPass.classList.add("hidden");
            hidePass.classList.add("hidden");
        }
    });

    // 2. Khi bấm vào nút mở mắt (để xem mật khẩu)
    showPass.addEventListener("click", () => {
        passInput.setAttribute("type", "text");
        showPass.classList.add("hidden");
        hidePass.classList.remove("hidden");
    });

    // 3. Khi bấm vào nút nhắm mắt (để ẩn mật khẩu đi)
    hidePass.addEventListener("click", () => {
        passInput.setAttribute("type", "password");
        hidePass.classList.add("hidden");
        showPass.classList.remove("hidden");
    });
}

// Tự động kích hoạt cho các trang khi load xong
document.addEventListener("DOMContentLoaded", () => {
    // Trường hợp 1: Dùng cho trang Đăng nhập (hoặc trường mật khẩu đơn)
    setupPasswordToggle("password", "show-pass", "hide-pass");

    // Trường hợp 2: Dùng cho trang Đăng ký (Có thêm trường xác nhận mật khẩu)
    // Bạn chỉ cần đặt ID tương ứng bên file HTML đăng ký và gọi thêm 1 dòng thế này:
    setupPasswordToggle("confirm_password", "show-confirm-pass", "hide-confirm-pass");
});

setupPasswordToggle("password", "show-pass", "hide-pass");
setupPasswordToggle("confirm-password", "confirm-show-pass", "confirm-hide-pass");
setupPasswordToggle("staff_password", "staff_show-pass", "staff_hide-pass");
setupPasswordToggle("edit_staff_password", "edit-show-pass", "edit-hide-pass");
