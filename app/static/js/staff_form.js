document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("staff-form");
  if (!form) return;

  // Regex kiểm tra mật khẩu: >=8 ký tự, ít nhất 1 hoa, 1 thường, 1 số, 1 ký tự đặc biệt
  const passwordRegex =
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]).{8,}$/;
  // Regex kiểm tra email
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  // Regex kiểm tra số điện thoại (10 số bắt đầu bằng 0)
  const phoneRegex = /^0\d{9}$/;

  const fields = [
    {
      input: document.getElementById("staff_name"),
      validate: (val) => val.trim().length > 0,
    },
    {
      input: document.getElementById("staff_id"),
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
    const wrapper = item.input.closest("div.border");
    const errorMsg = item.input
      .closest(".flex-col")
      .querySelector(".error-msg");

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

  // Chặn submit nếu có trường sai quy cách
  form.addEventListener("submit", (e) => {
    let isValid = true;

    fields.forEach((item) => {
      if (!item.input) return;
      const valid = item.validate(item.input.value);
      toggleError(item, !valid);
      if (!valid) {
        isValid = false;
      }
    });

    if (!isValid) {
      e.preventDefault();
    }
  });

  // Tự động xóa viền đỏ và thông báo lỗi khi người dùng nhập lại
  fields.forEach((item) => {
    if (!item.input) return;
    item.input.addEventListener("input", () => {
      if (item.validate(item.input.value)) {
        toggleError(item, false);
      }
    });
  });
});

// Hàm tiện ích lấy dữ liệu từ dòng
function getStaffDataFromRow(buttonElement) {
  const rowItem = buttonElement.closest(".item");
  if (!rowItem) return null;
  return {
    id: rowItem.getAttribute("data-staff-id"),
    name: rowItem.getAttribute("data-name"),
    email: rowItem.getAttribute("data-email"),
    phone: rowItem.getAttribute("data-phone"),
    address: rowItem.getAttribute("data-address"),
    gender: (rowItem.getAttribute("data-gender") || "male").toLowerCase(),
    avatar: rowItem.getAttribute("data-avatar"),
  };
}

// Mở Modal Xem Chi Tiết
function openViewStaffModal(buttonElement) {
  const data = getStaffDataFromRow(buttonElement);
  if (!data) return;

  document.getElementById("view_staff_id").innerText = data.id;
  document.getElementById("view_staff_name").innerText = data.name;
  document.getElementById("view_staff_email").innerText = data.email;
  document.getElementById("view_staff_phone").innerText = data.phone;
  document.getElementById("view_staff_address").innerText = data.address;
  document.getElementById("view_staff_gender").innerText = data.gender;

  const avatarContainer = document.getElementById(
    "view_staff_avatar_container",
  );
  // Xử lý khung ảnh rỗng nếu không có URL
  if (data.avatar && data.avatar.trim() !== "") {
    avatarContainer.innerHTML = `<img src="${data.avatar}" alt="${data.name}" class="size-full object-cover">`;
  } else {
    avatarContainer.innerHTML = `<svg class="w-10 h-10 text-gray-300" fill="currentColor" viewBox="0 0 24 24"><path d="M24 20.993V24H0v-2.996A14.977 14.977 0 0112.004 15c4.904 0 9.26 2.354 11.996 5.993zM16.002 8.999a4 4 0 11-8 0 4 4 0 018 0z" /></svg>`;
  }

  openModal("viewStaffModal");
}

// Mở Modal Chỉnh Sửa
function openEditStaffModal(buttonElement) {
  const data = getStaffDataFromRow(buttonElement);
  if (!data) return;

  document.getElementById("edit_original_staff_id").value = data.id;
  document.getElementById("edit_staff_id").value = data.id;
  document.getElementById("edit_staff_name").value = data.name;
  document.getElementById("edit_staff_email").value = data.email;
  document.getElementById("edit_staff_phone").value = data.phone;
  document.getElementById("edit_staff_address").value = data.address;
  document.getElementById("edit_staff_avatar").value = data.avatar || "";

  // Xóa trắng mật khẩu mỗi lần mở form
  document.getElementById("edit_staff_password").value = "";

  if (data.gender === "female") {
    document.getElementById("edit_gender_female").checked = true;
  } else {
    document.getElementById("edit_gender_male").checked = true;
  }

  openModal("editStaffModal");
}

// Mở Modal Xác Nhận Xóa
function openDeleteStaffModal(buttonElement) {
  const data = getStaffDataFromRow(buttonElement);
  if (!data) return;

  document.getElementById("delete_staff_name").innerText = data.name;
  document.getElementById("delete_staff_id").value = data.id;

  openModal("deleteStaffModal");
}
