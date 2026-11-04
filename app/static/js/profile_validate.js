document.addEventListener("DOMContentLoaded", () => {
    // Regex chuẩn kiểm tra email, SĐT Việt Nam (10 số) và mật khẩu mạnh
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const phoneRegex = /^0\d{9}$/;
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]).{8,}$/;

    // ==========================================
    // 1. VALIDATE FORM THÔNG TIN (EMAIL & PHONE)
    // ==========================================
    const profileForm = document.querySelector('form[action="/profile"]');
    if (profileForm) {
        // Tìm input email và phone trong form thông tin
        const emailInput = Array.from(profileForm.querySelectorAll("input")).find((i) => (i.type === "text" && i.value.includes("@")) || i.id === "profile_email" || i.getAttribute("name") === "email") || profileForm.querySelectorAll("input")[2]; // fallback dòng Email thứ 3
        const phoneInput = profileForm.querySelector('input[type="tel"]') || profileForm.querySelectorAll("input")[1]; // fallback dòng Phone thứ 2

        // Hàm helper hiển thị/ẩn lỗi cho form thông tin
        function toggleProfileError(input, isValid, message) {
            if (!input) return;
            const parentRow = input.closest(".grid");
            let errorMsg = parentRow.querySelector(".profile-error-msg");

            if (!isValid) {
                input.classList.add("border", "border-red-500", "ring-1", "ring-red-500");
                if (!errorMsg) {
                    errorMsg = document.createElement("p");
                    errorMsg.className = "profile-error-msg text-[11px] font-medium text-red-500 text-right col-span-2 -mt-1 mb-1";
                    parentRow.appendChild(errorMsg);
                }
                errorMsg.innerText = message;
                errorMsg.classList.remove("hidden");
            } else {
                input.classList.remove("border", "border-red-500", "ring-1", "ring-red-500");
                if (errorMsg) {
                    errorMsg.classList.add("hidden");
                }
            }
        }

        function getProfileErrorMsg(type) {
            const isVi = document.documentElement.lang === "vi";
            if (type === "email") {
                return isVi ? "Định dạng email không hợp lệ (VD: user@domain.com)" : "Invalid email format (e.g. user@domain.com)";
            }
            if (type === "phone") {
                return isVi ? "Số điện thoại phải gồm 10 chữ số bắt đầu bằng số 0" : "Phone number must be 10 digits starting with 0";
            }
            return "";
        }

        // Lắng nghe sự kiện gõ phím
        if (emailInput) {
            emailInput.addEventListener("input", () => {
                toggleProfileError(emailInput, emailRegex.test(emailInput.value.trim()), getProfileErrorMsg("email"));
            });
        }
        if (phoneInput) {
            phoneInput.addEventListener("input", () => {
                toggleProfileError(phoneInput, phoneRegex.test(phoneInput.value.trim()), getProfileErrorMsg("phone"));
            });
        }

        // Kiểm tra khi submit form thông tin
        profileForm.addEventListener("submit", (e) => {
            let isValid = true;
            if (emailInput && !emailRegex.test(emailInput.value.trim())) {
                toggleProfileError(emailInput, false, getProfileErrorMsg("email"));
                isValid = false;
            }
            if (phoneInput && !phoneRegex.test(phoneInput.value.trim())) {
                toggleProfileError(phoneInput, false, getProfileErrorMsg("phone"));
                isValid = false;
            }

            if (!isValid) {
                e.preventDefault();
            }
        });
    }

    // ==========================================
    // 2. VALIDATE CARD BẢO MẬT (SECURITY)
    // ==========================================
    const currentPass = document.getElementById("current_password");
    const newPass = document.getElementById("password");
    const confirmPass = document.getElementById("confirm-password");
    const passError = document.getElementById("password-error");
    const confirmError = document.getElementById("confirm-error");

    const securityForm = currentPass ? currentPass.closest("form") : null;

    // Helper ẩn/hiện lỗi ở card Security dựa vào class invisible và opacity-0 sẵn có
    function setVisibility(element, show) {
        if (!element) return;
        if (show) {
            element.classList.remove("invisible", "opacity-0");
        } else {
            element.classList.add("invisible", "opacity-0");
        }
    }

    function toggleInputHighlight(input, hasError) {
        if (!input) return;
        if (hasError) {
            input.classList.remove("border-gray-300");
            input.classList.add("border-red-500", "ring-1", "ring-red-500");
        } else {
            input.classList.remove("border-red-500", "ring-1", "ring-red-500");
            input.classList.add("border-gray-300");
        }
    }

    // Kiểm tra định dạng mật khẩu mới
    if (newPass) {
        newPass.addEventListener("input", () => {
            const val = newPass.value;
            const validFormat = passwordRegex.test(val);

            // Chỉ hiển thị lỗi nếu người dùng đã bắt đầu gõ mà chưa đủ chuẩn
            if (val.length > 0 && !validFormat) {
                setVisibility(passError, true);
                toggleInputHighlight(newPass, true);
            } else {
                setVisibility(passError, false);
                toggleInputHighlight(newPass, false);
            }

            // Kiểm tra lại xác nhận mật khẩu nếu ô confirm đã có chữ
            if (confirmPass && confirmPass.value.length > 0) {
                const isMatch = newPass.value === confirmPass.value;
                setVisibility(confirmError, !isMatch);
                toggleInputHighlight(confirmPass, !isMatch);
            }
        });
    }

    // Kiểm tra khớp xác nhận mật khẩu
    if (confirmPass) {
        confirmPass.addEventListener("input", () => {
            const isMatch = newPass.value === confirmPass.value;
            if (confirmPass.value.length > 0 && !isMatch) {
                setVisibility(confirmError, true);
                toggleInputHighlight(confirmPass, true);
            } else {
                setVisibility(confirmError, false);
                toggleInputHighlight(confirmPass, false);
            }
        });
    }

    // Xử lý khi nhấn nút gửi form đổi mật khẩu
    if (securityForm) {
        securityForm.addEventListener("submit", (e) => {
            let isValid = true;

            // 1. Bắt buộc nhập mật khẩu hiện tại
            if (currentPass && currentPass.value.trim().length === 0) {
                toggleInputHighlight(currentPass, true);
                isValid = false;
            } else if (currentPass) {
                toggleInputHighlight(currentPass, false);
            }

            // 2. Kiểm tra mật khẩu mới
            if (newPass && !passwordRegex.test(newPass.value)) {
                setVisibility(passError, true);
                toggleInputHighlight(newPass, true);
                isValid = false;
            }

            // 3. Kiểm tra mật khẩu xác nhận
            if (confirmPass && (confirmPass.value !== newPass.value || confirmPass.value.length === 0)) {
                setVisibility(confirmError, true);
                toggleInputHighlight(confirmPass, true);
                isValid = false;
            }

            if (!isValid) {
                e.preventDefault();
            }
        });
    }
});
