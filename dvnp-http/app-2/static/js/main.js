document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      btn.textContent = "...";
      setTimeout(() => { btn.textContent = "Run"; }, 500);
      console.log("[dev] action stubbed, no backend wired up yet");
    });
  });
});
