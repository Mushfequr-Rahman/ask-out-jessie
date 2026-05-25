const CONFIG = {
  // Free option: create a form at https://formspree.io and paste its endpoint here.
  // Example: "https://formspree.io/f/xabcwxyz"
  formEndpoint: "https://formspree.io/f/xvzywalq",
  fallbackEmail: ""
};

const noButton = document.querySelector("#noButton");
const form = document.querySelector("#dateForm");
const statusEl = document.querySelector("#formStatus");

const playfulNoLabels = [
  "Are you sure?",
  "Nope, try yes",
  "Too cute to refuse",
  "Over here",
  "Still yes?"
];

let noEscapes = 0;

function moveNoButton() {
  if (!noButton) return;

  const padding = 18;
  const rect = noButton.getBoundingClientRect();
  const maxLeft = Math.max(padding, window.innerWidth - rect.width - padding);
  const maxTop = Math.max(padding, window.innerHeight - rect.height - padding);
  const left = padding + Math.random() * (maxLeft - padding);
  const top = padding + Math.random() * (maxTop - padding);

  noButton.classList.add("is-running");
  noButton.style.left = `${left}px`;
  noButton.style.top = `${top}px`;
  noButton.textContent = playfulNoLabels[noEscapes % playfulNoLabels.length];
  noEscapes += 1;
}

function buildFallbackMailto(data) {
  const subject = encodeURIComponent("Jessie picked a date");
  const body = encodeURIComponent(
    [
      `Name: ${data.get("name")}`,
      `Plan: ${data.get("plan")}`,
      `Date: ${data.get("date")}`,
      `Time: ${data.get("time")}`,
      `Notes: ${data.get("notes") || "None"}`
    ].join("\n")
  );

  return `mailto:${CONFIG.fallbackEmail}?subject=${subject}&body=${body}`;
}

async function submitDate(event) {
  event.preventDefault();
  const data = new FormData(form);

  if (!CONFIG.formEndpoint && CONFIG.fallbackEmail) {
    window.location.href = buildFallbackMailto(data);
    statusEl.textContent = "Opening an email with the date details.";
    return;
  }

  if (!CONFIG.formEndpoint) {
    statusEl.textContent = "Add your free Formspree endpoint in script.js before publishing.";
    return;
  }

  statusEl.textContent = "Sending...";

  try {
    const response = await fetch(CONFIG.formEndpoint, {
      method: "POST",
      body: data,
      headers: { Accept: "application/json" }
    });

    if (!response.ok) {
      throw new Error("Form submission failed");
    }

    form.reset();
    statusEl.textContent = "Sent. Date night is officially in motion.";
  } catch (error) {
    statusEl.textContent = "That did not send. Please try again, or text me the plan.";
  }
}

if (noButton) {
  noButton.addEventListener("mouseenter", moveNoButton);
  noButton.addEventListener("focus", moveNoButton);
  noButton.addEventListener("touchstart", (event) => {
    event.preventDefault();
    moveNoButton();
  });
  noButton.addEventListener("click", (event) => {
    event.preventDefault();
    moveNoButton();
  });
}

if (form) {
  form.addEventListener("submit", submitDate);
}
