document.addEventListener("DOMContentLoaded", () => {
  const menuBtn = document.getElementById("menu-btn");
  const closeBtn = document.getElementById("close-btn");
  const closeXBtn = document.getElementById("close-x-btn");
  const mobileMenu = document.getElementById("mobile-menu");
  const backdrop = document.getElementById("menu-backdrop");

  if (!menuBtn || !mobileMenu || !backdrop) {
    console.error("Không tìm thấy các phần tử của menu:", {
      menuBtn,
      mobileMenu,
      backdrop,
    });
    return;
  }

  function openMenu() {
    backdrop.classList.remove("hidden");
    mobileMenu.classList.remove("translate-x-full");
    mobileMenu.classList.add("translate-x-0");
    document.body.classList.add("overflow-hidden");
  }

  function closeMenu() {
    backdrop.classList.add("hidden");
    mobileMenu.classList.remove("translate-x-0");
    mobileMenu.classList.add("translate-x-full");
    document.body.classList.remove("overflow-hidden");
  }

  menuBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    openMenu();
  });

  if (closeBtn) closeBtn.addEventListener("click", closeMenu);
  if (closeXBtn) closeXBtn.addEventListener("click", closeMenu);
  backdrop.addEventListener("click", closeMenu);
});
