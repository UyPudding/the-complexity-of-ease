// ================= THEME =================
const toggleSwitch = document.querySelector(
  '.theme-switch input[type="checkbox"]'
);

const currentTheme = localStorage.getItem("theme");

if (currentTheme) {
  document.documentElement.setAttribute("data-theme", currentTheme);
  if (currentTheme === "light") {
    toggleSwitch.checked = true;
  }
}

function switchTheme(e) {
  const theme = e.target.checked ? "light" : "dark";
  document.documentElement.setAttribute("data-theme", theme);
  localStorage.setItem("theme", theme);
}

toggleSwitch.addEventListener("change", switchTheme);

// ================= ACTIVE BUTTON HANDLER =================
function handleActiveSelection(containerSelector, buttonSelector, storageKey) {
  const container = document.querySelector(containerSelector);
  if (!container) return;

  const savedValue = sessionStorage.getItem(storageKey);

  if (savedValue) {
    const buttons = container.querySelectorAll(buttonSelector);
    buttons.forEach((btn) => {
      const btnText = btn.innerText.split("\n")[0].trim();
      if (btnText === savedValue) {
        container.querySelector(".active")?.classList.remove("active");
        btn.classList.add("active");
      }
    });
  }

  container.addEventListener("click", (e) => {
    const clickedBtn = e.target.closest(buttonSelector);

    if (clickedBtn && !clickedBtn.classList.contains("disabled")) {
      container.querySelector(".active")?.classList.remove("active");
      clickedBtn.classList.add("active");

      const selectedText = clickedBtn.innerText.split("\n")[0].trim();
      sessionStorage.setItem(storageKey, selectedText);
    }
  });
}

// ================= RENDER MATH =================
function renderExpression(latex) {
  const resultDiv = document.getElementById("math-expression");
  resultDiv.innerHTML = `$$${latex}$$`;

  if (window.MathJax) {
    MathJax.typesetPromise();
  }
}

// ================= LOADING =================
let overlay = document.getElementById("loading-overlay");

function showLoading() {
  overlay.classList.add("active");
}

function hideLoading() {
  overlay.classList.remove("active");
}

// ================= LEVEL ====================
const level_map = {
  Elementary: 1,
  Middle: 2,
  High: 3
};

// ================= GENERATE EXPRESSION =================
async function generateExpression() {
  try {
    showLoading(); 

    const index_level = sessionStorage.getItem("selectedLevel") || "Elementary";

    const level = level_map[index_level];

    const response = await fetch("/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ level }),
    });

    if (!response.ok) {
      throw new Error("Server error");
    }

    const data = await response.json();

    sessionStorage.setItem("expression", data.latex);

    renderExpression(data.latex);

  } catch (error) {
    console.error("Error:", error);
    alert("Server is busy. Please try again.");

  } finally {
    hideLoading();
  }
}

// ================= DOM READY =================
document.addEventListener("DOMContentLoaded", () => {
  // Active buttons
  handleActiveSelection(".level-container", ".level-btn", "selectedLevel");
  handleActiveSelection(".result-picker", ".res-btn", "selectedResult");

  // Load saved expression
  const saved = sessionStorage.getItem("expression");
  if (saved) {
    renderExpression(saved);
  }

  const resetBtn = document.getElementById("reset-btn");

  if (resetBtn) {
    resetBtn.addEventListener("click", () => {
      sessionStorage.removeItem("selectedLevel");
      sessionStorage.removeItem("selectedResult");
      sessionStorage.removeItem("expression");

      resetBtn.innerHTML = "Cleaning...";

      setTimeout(() => {
        window.location.reload();
      }, 300);
    });
  }

});


