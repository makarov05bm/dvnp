// Minimal client-side touch so pages don't feel static.
document.addEventListener("DOMContentLoaded", () => {
  const rows = document.querySelectorAll(".status-row, .log-table tbody tr");
  rows.forEach((row, i) => {
    row.style.opacity = "0";
    row.style.transition = "opacity 0.3s ease";
    setTimeout(() => { row.style.opacity = "1"; }, 60 * i);
  });
});
