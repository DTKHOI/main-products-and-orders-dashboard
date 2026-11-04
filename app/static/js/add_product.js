document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("add-form");
  if (!form) return;

  const fields = [
    {
      input: document.getElementById("product_name"),
      validate: (val) => val.trim().length > 0,
    },
    {
      input: document.getElementById("product_id"),
      validate: (val) => val.trim().length > 0,
    },
    {
      input: document.getElementById("product_price"),
      validate: (val) =>
        val.trim() !== "" && !isNaN(val) && parseFloat(val) >= 0,
    },
    {
      input: document.getElementById("product_quantity"),
      validate: (val) =>
        val.trim() !== "" && !isNaN(val) && parseInt(val, 10) >= 0,
    },
    {
      input: document.getElementById("product_category"),
      validate: (val) => val && val.trim().length > 0,
    },
  ];

  // Hàm đổi kiểu viền và thông báo
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

  // Lắng nghe sự kiện Submit Form
  form.addEventListener("submit", (e) => {
    let isFormValid = true;

    fields.forEach((item) => {
      if (!item.input) return;
      const valid = item.validate(item.input.value);
      toggleError(item, !valid);
      if (!valid) {
        isFormValid = false;
      }
    });

    // Nếu có trường sai sót, ngăn chặn POST lên server
    if (!isFormValid) {
      e.preventDefault();
    }
  });

  // Lắng nghe người dùng gõ vào để tự xóa viền đỏ tức thì
  fields.forEach((item) => {
    if (!item.input) return;
    const eventType =
      item.input.tagName.toLowerCase() === "select" ? "change" : "input";
    item.input.addEventListener(eventType, () => {
      if (item.validate(item.input.value)) {
        toggleError(item, false);
      }
    });
  });
});
