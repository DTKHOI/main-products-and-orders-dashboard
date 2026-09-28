const username = document.getElementById("username");
const email = document.getElementById("email-input");
const password = document.getElementById("password");
const confirmPassword = document.getElementById("confirm-password");
const form = document.getElementById("form");

const usernameError = document.getElementById("error-username");
const emailError = document.getElementById("error-email");
const passwordError = document.getElementById("password-error");
const confirmError = document.getElementById("confirm-error");

function setFieldState(inputEl, errorEl, isValid) {
  if (!isValid) {
    inputEl.classList.replace(
      "focus:outline-blue-500",
      "focus:outline-red-500",
    );
    errorEl.classList.remove("opacity-0", "invisible");
  } else {
    inputEl.classList.replace(
      "focus:outline-red-500",
      "focus:outline-blue-500",
    );
    errorEl.classList.add("opacity-0", "invisible");
  }
}

function isEmptyUsername() {
  const isValid = username.value === "";
  setFieldState(username, usernameError, !isValid);
  return username.value === "";
}

function validateEmail() {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const isValid = regex.test(email.value.trim());
  setFieldState(email, emailError, isValid);
  return isValid;
}

function isStrongPassword() {
  const userPassword = password.value;
  if (typeof userPassword !== "string") return false;

  const chars = userPassword.split("");
  let isOverLength = false;
  let hasUpperChar = false;
  let hasLowerChar = false;
  let hasDigit = false;
  let hasSpecialChar = false;

  for (let i = 0; i < chars.length; i++) {
    const decCode = chars[i].charCodeAt();

    if (userPassword.length >= 8) isOverLength = true;
    if (decCode >= 65 && decCode <= 90) hasUpperChar = true;
    if (decCode >= 97 && decCode <= 122) hasLowerChar = true;
    if (decCode >= 48 && decCode <= 57) hasDigit = true;
    if (
      (decCode >= 33 && decCode <= 47) ||
      (decCode >= 58 && decCode <= 64) ||
      (decCode >= 91 && decCode <= 96) ||
      (decCode >= 123 && decCode <= 126)
    )
      hasSpecialChar = true;
  }
  const isValid =
    hasUpperChar && hasLowerChar && hasDigit && hasSpecialChar && isOverLength;
  setFieldState(password, passwordError, isValid);

  // Kiểm tra lại cả confirm password nếu người dùng sửa password sau
  if (confirmPassword.value) validateConfirmPassword();
  return isValid;
}

function validateConfirmPassword() {
  const isValid =
    password.value === confirmPassword.value && confirmPassword.value !== "";
  console.log(confirmPassword.value);
  setFieldState(confirmPassword, confirmError, isValid);
  return isValid;
}

username.addEventListener("input", isEmptyUsername);
email.addEventListener("input", validateEmail);
password.addEventListener("input", isStrongPassword);
confirmPassword.addEventListener("input", validateConfirmPassword);

// Ngăn chặn người dùng submit khi chưa thỏa mãn email, password, confirm password hợp lệ
form.addEventListener("submit", (e) => {
  const isEmpty = isEmptyUsername();
  const isGoodPassword = isStrongPassword();
  const isGoodEmail = validateEmail();
  const isCorrectPassword = validateConfirmPassword();

  console.log(form);
  console.log(e);

  if (!isCorrectPassword || !isGoodEmail || !isGoodPassword || isEmpty)
    e.preventDefault();
});
