function switchRole(role) {
  const tabAdmin = document.getElementById("tab-admin");
  const tabStaff = document.getElementById("tab-staff");
  const roleInput = document.getElementById("login_role");
  const identityLabel = document.getElementById("identity_label");
  const identityInput = document.getElementById("identity_input");
  const signupPrompt = document.getElementById("signup-prompt");

  if (role === "admin") {
    // Cập nhật thẻ hidden cho Backend
    roleInput.value = "admin";

    // Styling Tab Admin (Active)
    tabAdmin.className =
      "flex-1 py-3 text-sm font-medium text-blue-600 border-b-2 border-blue-600 transition";
    // Styling Tab Staff (Inactive)
    tabStaff.className =
      "flex-1 py-3 text-sm font-medium text-gray-500 hover:text-gray-700 transition";

    // Thay đổi Input
    identityLabel.innerText = "Email address";
    identityInput.type = "email";
    identityInput.placeholder = "admin@example.com";
    identityInput.value = ""; // Xóa text cũ

    // Hiện nút đăng ký
    signupPrompt.style.display = "block";
  } else if (role === "staff") {
    // Cập nhật thẻ hidden cho Backend
    roleInput.value = "staff";

    // Styling Tab Staff (Active)
    tabStaff.className =
      "flex-1 py-3 text-sm font-medium text-blue-600 border-b-2 border-blue-600 transition";
    // Styling Tab Admin (Inactive)
    tabAdmin.className =
      "flex-1 py-3 text-sm font-medium text-gray-500 hover:text-gray-700 transition";

    // Thay đổi Input: Staff có thể đăng nhập bằng Staff ID hoặc Email
    identityLabel.innerText = "Staff ID or Email";
    identityInput.type = "text"; // Đổi thành text để nhập được mã NV
    identityInput.placeholder = "e.g., NV-001 or staff@company.com";
    identityInput.value = ""; // Xóa text cũ

    // Ẩn nút đăng ký (Nhân viên do Admin tạo, không tự đăng ký)
    signupPrompt.style.display = "none";
  }
}
