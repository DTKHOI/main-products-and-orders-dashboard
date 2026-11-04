document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("create-staff-form");
    if (!form) return;

    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]).{8,}$/;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const phoneRegex = /^0\d{9}$/;

    const fields = [
        {
            input: document.getElementById("staff_name"),
            validate: (val) => val.trim().length > 0,
        },
        {
            input: document.getElementById("staff_email"),
            validate: (val) => emailRegex.test(val.trim()),
        },
        {
            input: document.getElementById("staff_phone"),
            validate: (val) => phoneRegex.test(val.trim()),
        },
        {
            input: document.getElementById("staff_password"),
            validate: (val) => passwordRegex.test(val),
        },
    ];

    function toggleError(item, hasError) {
        if (!item.input) return;
        const wrapper = item.input.closest("div.border");
        const errorMsg = item.input.closest(".flex-col")?.querySelector(".error-msg");

        if (hasError) {
            if (wrapper) {
                wrapper.classList.remove("border-gray-200");
                wrapper.classList.add("border-rose-500", "ring-2", "ring-rose-100");
            }
            if (errorMsg) errorMsg.classList.remove("hidden");
        } else {
            if (wrapper) {
                wrapper.classList.remove("border-rose-500", "ring-2", "ring-rose-100");
                wrapper.classList.add("border-gray-200");
            }
            if (errorMsg) errorMsg.classList.add("hidden");
        }
    }

    form.addEventListener("submit", (e) => {
        let isValid = true;
        fields.forEach((item) => {
            if (!item.input) return;
            const valid = item.validate(item.input.value);
            toggleError(item, !valid);
            if (!valid) isValid = false;
        });

        if (!isValid) e.preventDefault();
    });

    fields.forEach((item) => {
        if (!item.input) return;
        item.input.addEventListener("input", () => {
            if (item.validate(item.input.value)) {
                toggleError(item, false);
            }
        });
    });
});

// Hàm tiện ích: Trích xuất dữ liệu từ các thuộc tính data-* của hàng được bấm
function getStaffDataFromRow(buttonElement) {
    const rowItem = buttonElement.closest(".item");
    if (!rowItem) return null;
    return {
        id: rowItem.getAttribute("data-staff-id") || "",
        code: rowItem.getAttribute("data-staff-code") || "",
        name: rowItem.getAttribute("data-name") || "",
        email: rowItem.getAttribute("data-email") || "",
        phone: rowItem.getAttribute("data-phone") || "",
        address: rowItem.getAttribute("data-address") || "",
        gender: (rowItem.getAttribute("data-gender") || "male").toLowerCase(),
        avatar: rowItem.getAttribute("data-avatar") || "",
    };
}

// 1. Mở Modal Xem chi tiết nhân viên
window.openViewStaffModal = function (buttonElement) {
    const data = getStaffDataFromRow(buttonElement);
    if (!data) return;

    document.getElementById("view_staff_id").innerText = data.code;
    document.getElementById("view_staff_name").innerText = data.name;
    document.getElementById("view_staff_email").innerText = data.email;
    document.getElementById("view_staff_phone").innerText = data.phone;
    document.getElementById("view_staff_address").innerText = data.address;
    const isVi = document.documentElement.lang === "vi";
    const genderDisplay = data.gender === "female" ? (isVi ? "Nữ" : "Female") : (isVi ? "Nam" : "Male");
    document.getElementById("view_staff_gender").innerText = genderDisplay;

    const avatarContainer = document.getElementById("view_staff_avatar_container");
    if (avatarContainer) {
        if (data.avatar && data.avatar.trim() !== "") {
            avatarContainer.innerHTML = `<img src="${data.avatar}" alt="${data.name}" class="size-full object-cover">`;
        } else {
            avatarContainer.innerHTML = `<svg class="w-10 h-10 text-gray-300" fill="currentColor" viewBox="0 0 24 24"><path d="M24 20.993V24H0v-2.996A14.977 14.977 0 0112.004 15c4.904 0 9.26 2.354 11.996 5.993zM16.002 8.999a4 4 0 11-8 0 4 4 0 018 0z" /></svg>`;
        }
    }

    openModal("viewStaffModal");
};

// 2. Mở Modal Chỉnh sửa nhân viên
window.openEditStaffModal = function (buttonElement) {
    const data = getStaffDataFromRow(buttonElement);
    if (!data) return;

    // Gán ID vào input ẩn
    const staffId = document.getElementById("edit_staff_id");
    const staffName = document.getElementById("edit_staff_name");
    const staffEmail = document.getElementById("edit_staff_email");
    const staffPhone = document.getElementById("edit_staff_phone");
    const staffAddress = document.getElementById("edit_staff_address");
    const staffAvatar = document.getElementById("edit_staff_avatar");
    const staffPw = document.getElementById("edit_staff_password");

    if (staffId) staffId.value = data.id;
    if (staffName) staffName.value = data.name;
    if (staffEmail) staffEmail.value = data.email;
    if (staffPhone) staffPhone.value = data.phone;
    if (staffAddress) staffAddress.value = data.address;
    if (staffAvatar) staffAvatar.value = data.avatar;
    if (staffPw) staffPw.value = ""; // Để trống mật khẩu khi mở

    // Thiết lập radio button cho giới tính
    const radioFemale = document.getElementById("edit_gender_female");
    const radioMale = document.getElementById("edit_gender_male");
    if (data.gender === "female") {
        if (radioFemale) radioFemale.checked = true;
    } else {
        if (radioMale) radioMale.checked = true;
    }

    openModal("editStaffModal");
};

// 3. Mở Modal Xóa nhân viên
window.openDeleteStaffModal = function (buttonElement) {
    const data = getStaffDataFromRow(buttonElement);
    if (!data) return;

    const delName = document.getElementById("delete_staff_name");
    const delId = document.getElementById("delete_staff_id");

    if (delName) delName.innerText = data.name;
    if (delId) delId.value = data.id;

    openModal("deleteStaffModal");
};
