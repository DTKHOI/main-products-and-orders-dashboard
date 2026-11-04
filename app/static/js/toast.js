// Hàm hiển thị Toast dùng chung toàn hệ thống
function showToast(message, type = "success") {
    let container = document.getElementById("toast-container");

    // Nếu trang nào chưa có container, tự động tạo mới và gắn vào cuối body
    if (!container) {
        container = document.createElement("div");
        container.id = "toast-container";
        container.className = "fixed bottom-5 right-5 z-50 flex flex-col gap-3 pointer-events-none";
        document.body.appendChild(container);
    }

    const toast = document.createElement("div");

    // Định nghĩa giao diện theo loại thông báo (success / error)
    let bgClass = "bg-slate-900 text-white"; // Mặc định
    let iconSvg = "";

    if (type === "success") {
        bgClass = "bg-emerald-600 text-white"; // Xanh lá khi thành công
        iconSvg = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M20 6L9 17l-5-5"/></svg>`;
    } else if (type === "error") {
        bgClass = "bg-rose-600 text-white"; // Đỏ khi lỗi / thất bại
        iconSvg = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 6L6 18M6 6l12 12"/></svg>`;
    }

    toast.className = `pointer-events-auto flex items-center justify-between gap-4 px-5 py-3.5 rounded-2xl shadow-2xl transform translate-y-4 opacity-0 transition-all duration-300 ease-out ${bgClass}`;

    toast.innerHTML = `
        <div class="flex items-center gap-3">
            ${iconSvg}
            <span class="text-sm font-medium">${message}</span>
        </div>
        <button type="button" onclick="this.parentElement.remove()" class="text-white/80 hover:text-white cursor-pointer p-1">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6L6 18M6 6l12 12"/></svg>
        </button>
    `;

    container.appendChild(toast);

    // Hiệu ứng trượt lên và hiện rõ
    setTimeout(() => {
        toast.classList.remove("translate-y-4", "opacity-0");
    }, 10);

    // Tự động biến mất sau 3.5 giây
    setTimeout(() => {
        toast.classList.add("translate-y-4", "opacity-0");
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, 3500);
}
