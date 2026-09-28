// 1. Mở modal: gỡ bỏ class 'hidden'
function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.remove("hidden");
    // Khóa cuộn trang khi mở modal (tuỳ chọn)
    document.body.classList.add("overflow-hidden");
  }
}

// 2. Đóng modal: thêm lại class 'hidden'
function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.add("hidden");
    // Mở lại cuộn trang
    document.body.classList.remove("overflow-hidden");
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

const table = document.getElementById("table");
const main = document.querySelector("main");

table.addEventListener("click", (e) => {
  const product = e.target.closest(".item");
  const editBtn = e.target.closest("#edit-modal");

  if (product && editBtn) {
    const productId = product.dataset.id;
    const productName = product.dataset.name;
    const productCate = product.dataset.category;
    const productPrice = product.dataset.price;
    const productQuantity = product.dataset.quantity;
    const productStatus = product.dataset.status;

    const editModal = document.createElement("div");
    editModal.innerHTML = `<div
            id="edit-modal"
            class="fixed inset-0 z-10 flex w-screen items-center justify-center bg-[#00000073] p-4"
          >
            <div
              class="w-[90vw] overflow-y-auto rounded-2xl bg-white shadow-2xl md:w-lg lg:w-xl xl:w-2xl"
            >
              <div class="px-6 pt-6">
                <div class="flex items-center justify-between">
                  <div class="">
                    <h2 class="text-2xl font-bold text-[#101828]">
                      Edit Product
                    </h2>
                    <p>Update product details</p>
                  </div>
                  <button type="button" class="p-2">
                    <svg
                      width="24"
                      height="24"
                      viewBox="0 0 24 24"
                      fill="none"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path
                        d="M18 6L6 18"
                        stroke="#4A5565"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                      />
                      <path
                        d="M6 6L18 18"
                        stroke="#4A5565"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                      />
                    </svg>
                  </button>
                </div>
              </div>
              <div class="my-6 h-0.5 bg-[#E5E7EB]"></div>
              <form
                method="post"
                id="edit-form"
                class="flex flex-col gap-6 px-6 pb-6"
              >
                <div class="flex flex-col gap-2">
                  <label for="product_name">Product Name *</label>
                  <div class="rounded-2xl border border-gray-200">
                    <input
                        value = "${productName}"
                      id="product_name"
                      name="name"
                      type="text"
                      class="text-neutral-95 size-full rounded-2xl px-4 py-3 focus:outline-blue-600"
                    />
                  </div>
                </div>
                <div class="flex flex-col gap-2">
                  <label for="product_id">ID *</label>
                  <div class="rounded-2xl border border-gray-200">
                    <input
                        value = "${productId}"
                      id="product_id"
                      name="id"
                      type="text"
                      class="text-neutral-95 size-full rounded-2xl px-4 py-3 focus:outline-blue-600"
                    />
                  </div>
                </div>
                <div class="flex gap-4">
                  <div>
                    <label for="product_price">Price ($) *</label>
                    <div class="mt-2 rounded-2xl border border-gray-200">
                      <input
                        value = "${productPrice}"
                        id="product_price"
                        name="price"
                        type="number"
                        class="text-neutral-95 size-full rounded-2xl px-4 py-3 focus:outline-blue-600"
                      />
                    </div>
                  </div>
                  <div>
                    <label for="product_quantity">Stock *</label>
                    <div class="mt-2 rounded-2xl border border-gray-200">
                      <input
                        value = "${productQuantity}"
                        id="product_quantity"
                        name="quantity"
                        type="number"
                        class="text-neutral-95 size-full rounded-2xl px-4 py-3 focus:outline-blue-600"
                      />
                    </div>
                  </div>
                </div>
                <div class="flex flex-col gap-2">
                  <label for="product_category">Category *</label>
                  <div
                    class="flex items-center justify-between rounded-2xl border border-gray-200"
                  >
                    <input
                      value="${productCate}"
                      id="product_category"
                      name="category"
                      type="button"
                      class="text-neutral-95 size-full rounded-2xl px-4 py-3 text-left focus:outline-blue-600"
                    />
                    <div class="px-3">
                      <svg
                        width="10"
                        height="6"
                        viewBox="0 0 10 6"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                      >
                        <path
                          d="M1 1L5 5L9 1"
                          stroke="#0A0A0A"
                          stroke-width="1.5"
                          stroke-linecap="round"
                          stroke-linejoin="round"
                        />
                      </svg>
                    </div>
                  </div>
                </div>
                <div class="flex flex-col gap-2">
                  <label for="">Status</label>
                  <div class="flex items-center gap-4">
                    <div class="flex items-center gap-2">
                      <input
                        ${productStatus === "active" ? `checked` : ``}
                        value="active"
                        id="product_active"
                        name="status"
                        type="radio"
                      />
                      <label for="product_active">Active</label>
                    </div>
                    <div class="flex items-center gap-2">
                      <input
                        ${productStatus === "active" ? `checked` : ``}
                        id="product_inactive"
                        name="status"
                        value="inactive"
                        type="radio"
                      />
                      <label for="product_inactive">Inactive</label>
                    </div>
                  </div>
                </div>
                <div class="flex flex-col gap-2">
                  <label for="product_id">Image URL</label>
                  <div class="rounded-2xl border border-gray-200">
                    <input
                      id="product_img"
                      name="product_img"
                      type="text"
                      class="text-neutral-95 size-full rounded-2xl px-4 py-3 focus:outline-blue-600"
                    />
                  </div>
                </div>
              </form>
              <div
                class="flex items-center justify-end gap-1 rounded-br-2xl rounded-bl-2xl bg-[#F9FAFB] px-3 py-3 sm:gap-3 sm:px-6 sm:py-6"
              >
                <button
                  type="button"
                  ${onclick}
                  class="cursor-pointer rounded-xl bg-white px-6 py-3 outline outline-gray-200"
                >
                  <span class="text-center font-medium text-gray-700"
                    >Cancel</span
                  >
                </button>
                <button
                  form="edit-form"
                  type="submit"
                  class="cursor-pointer rounded-xl bg-linear-to-r from-blue-600 to-purple-600 px-6 py-3 shadow-lg"
                >
                  <span class="text-center font-medium text-white">
                    Update Product
                  </span>
                </button>
              </div>
            </div>
          </div>`;

    main.appendChild(editModal);
  }
});
