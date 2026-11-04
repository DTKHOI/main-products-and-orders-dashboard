document.addEventListener("DOMContentLoaded", () => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]).{8,}$/;

    // Helper: Ẩn/hiện thông báo lỗi và đổi màu viền input
    function setFieldError(inputEl, errorEl, hasError) {
        if (!inputEl) return;
        if (hasError) {
            inputEl.classList.remove("border-gray-300", "dark:border-slate-700");
            inputEl.classList.add("border-red-500", "ring-1", "ring-red-500");
            if (errorEl) errorEl.classList.remove("invisible", "opacity-0");
        } else {
            inputEl.classList.remove("border-red-500", "ring-1", "ring-red-500");
            inputEl.classList.add("border-gray-300", "dark:border-slate-700");
            if (errorEl) errorEl.classList.add("invisible", "opacity-0");
        }
    }

    // =========================================================
    // 1. TRANG NHẬP EMAIL (forgot_pass.html)
    // =========================================================
    const forgotForm = document.getElementById("forgot-form");
    if (forgotForm) {
        const emailInput = document.getElementById("email");
        const emailError = document.getElementById("email-error");
        const submitBtn = document.getElementById("btn-send-otp");

        emailInput.addEventListener("input", () => {
            if (emailRegex.test(emailInput.value.trim())) {
                setFieldError(emailInput, emailError, false);
            }
        });

        forgotForm.addEventListener("submit", (e) => {
            const isValid = emailRegex.test(emailInput.value.trim());
            setFieldError(emailInput, emailError, !isValid);

            if (!isValid) {
                e.preventDefault();
                return;
            }

            // Khóa nút tránh bấm đúp nhiều lần khi server đang gửi email SMTP
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = `<span>Sending OTP...</span>`;
            }
        });
    }

    // =========================================================
    // 2. TRANG NHẬP MÃ OTP 6 SỐ (otp.html)
    // =========================================================
    const otpForm = document.getElementById("otp-form");
    if (otpForm) {
        const otpBoxes = Array.from(document.querySelectorAll(".otp-box"));
        const otpHidden = document.getElementById("otp-hidden");
        const otpError = document.getElementById("otp-error");
        const resendBtn = document.getElementById("btn-resend-otp");
        const timerSpan = document.getElementById("otp-timer");

        // Tự động focus vào ô đầu tiên
        if (otpBoxes.length > 0) otpBoxes[0].focus();

        // Cập nhật giá trị chuỗi 6 số vào input hidden
        function syncOtpValue() {
            const code = otpBoxes.map((box) => box.value.trim()).join("");
            if (otpHidden) otpHidden.value = code;
            return code;
        }

        otpBoxes.forEach((box, index) => {
            // Chỉ nhận ký tự số và tự nhảy sang ô tiếp theo
            box.addEventListener("input", (e) => {
                box.value = box.value.replace(/[^0-9]/g, "");
                syncOtpValue();

                if (box.value !== "") {
                    setFieldError(box, otpError, false);
                    if (index < otpBoxes.length - 1) {
                        otpBoxes[index + 1].focus();
                    }
                }
            });

            // Hỗ trợ phím Backspace lùi về ô trước và phím mũi tên Trái/Phải
            box.addEventListener("keydown", (e) => {
                if (e.key === "Backspace" && box.value === "" && index > 0) {
                    otpBoxes[index - 1].focus();
                } else if (e.key === "ArrowLeft" && index > 0) {
                    otpBoxes[index - 1].focus();
                } else if (e.key === "ArrowRight" && index < otpBoxes.length - 1) {
                    otpBoxes[index + 1].focus();
                }
            });

            // Hỗ trợ dán (Paste) nguyên chuỗi 6 số từ email
            box.addEventListener("paste", (e) => {
                e.preventDefault();
                const pastedData = (e.clipboardData || window.clipboardData)
                    .getData("text")
                    .replace(/[^0-9]/g, "")
                    .slice(0, otpBoxes.length);

                pastedData.split("").forEach((char, i) => {
                    if (otpBoxes[i]) {
                        otpBoxes[i].value = char;
                        setFieldError(otpBoxes[i], otpError, false);
                    }
                });

                syncOtpValue();
                const focusIndex = Math.min(pastedData.length, otpBoxes.length - 1);
                if (otpBoxes[focusIndex]) otpBoxes[focusIndex].focus();
            });
        });

        otpForm.addEventListener("submit", (e) => {
            const code = syncOtpValue();
            if (code.length < 6) {
                e.preventDefault();
                if (otpError) otpError.classList.remove("invisible", "opacity-0");
                otpBoxes.forEach((box) => {
                    if (box.value === "") {
                        box.classList.add("border-red-500", "ring-1", "ring-red-500");
                    }
                });
            }
        });

        // Bộ đếm ngược 60s cho nút Resend OTP
        if (resendBtn && timerSpan) {
            let timeLeft = 60;
            const countdown = setInterval(() => {
                timeLeft--;
                timerSpan.textContent = timeLeft;
                if (timeLeft <= 0) {
                    clearInterval(countdown);
                    resendBtn.disabled = false;
                    resendBtn.textContent = "Resend Now";
                }
            }, 1000);
        }
    }

    // =========================================================
    // 3. TRANG ĐẶT MẬT KHẨU MỚI (new_pass.html)
    // =========================================================
    const newPassForm = document.getElementById("new-pass-form");
    if (newPassForm) {
        const newPass = document.getElementById("password");
        const confirmPass = document.getElementById("confirm-password");
        const passError = document.getElementById("password-error");
        const confirmError = document.getElementById("confirm-error");

        if (newPass) {
            newPass.addEventListener("input", () => {
                const isValid = passwordRegex.test(newPass.value);
                setFieldError(newPass, passError, newPass.value.length > 0 && !isValid);

                if (confirmPass && confirmPass.value.length > 0) {
                    const isMatch = confirmPass.value === newPass.value;
                    setFieldError(confirmPass, confirmError, !isMatch);
                }
            });
        }

        if (confirmPass) {
            confirmPass.addEventListener("input", () => {
                const isMatch = confirmPass.value === newPass.value;
                setFieldError(confirmPass, confirmError, confirmPass.value.length > 0 && !isMatch);
            });
        }

        newPassForm.addEventListener("submit", (e) => {
            let isValid = true;

            if (!passwordRegex.test(newPass.value)) {
                setFieldError(newPass, passError, true);
                isValid = false;
            } else {
                setFieldError(newPass, passError, false);
            }

            if (confirmPass.value !== newPass.value || confirmPass.value.length === 0) {
                setFieldError(confirmPass, confirmError, true);
                isValid = false;
            } else {
                setFieldError(confirmPass, confirmError, false);
            }

            if (!isValid) e.preventDefault();
        });
    }
});
