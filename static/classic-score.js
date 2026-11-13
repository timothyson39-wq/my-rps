(() => {
  const form = document.querySelector('form[aria-label="Choose your move"]');
  const round = document.querySelector(".round-display");
  const reset = document.querySelector("#reset-score");
  const error = document.querySelector("#round-error");
  const playerScore = document.querySelector("#player-score");
  const computerScore = document.querySelector("#computer-score");
  const picker = document.querySelector(".mode-picker");
  const modes = [...picker.querySelectorAll("[data-mode]")];
  const dialog = document.querySelector("#switch-mode");
  const roulette = document.querySelector("#roulette");
  const wheel = roulette.querySelector(".wheel");
  const status = document.querySelector("#spin-status");
  const spin = document.querySelector("#spin");
  const stop = document.querySelector("#stop");
  const moves = ["rock", "paper", "scissors"];
  const initialRound = round.innerHTML;
  const emptyScore = () => ({ player: 0, computer: 0 });
  const scores = Object.fromEntries(modes.map(({ dataset: { mode } }) => [
    mode, JSON.parse(sessionStorage.getItem("rps." + mode + ".score")) ?? emptyScore(),
  ]));
  let mode = sessionStorage.getItem("rps.mode") === "roulette" ? "roulette" : "classic";
  let phase = "idle";

  function showScore() {
    playerScore.textContent = scores[mode].player;
    computerScore.textContent = scores[mode].computer;
  }

  function saveScore() {
    sessionStorage.setItem("rps." + mode + ".score", JSON.stringify(scores[mode]));
    showScore();
  }

  function clearRound() {
    round.innerHTML = initialRound;
    error.hidden = true;
    status.textContent = "";
    wheel.style.transform = "";
    if (mode === "roulette") {
      round.querySelector("#game-heading").textContent = "Roulette";
      round.querySelector(".result p").textContent = "Spin to choose both moves.";
    }
  }

  function showMode() {
    form.hidden = mode !== "classic";
    roulette.hidden = mode !== "roulette";
    for (const button of modes) {
      button.setAttribute("aria-pressed", String(button.dataset.mode === mode));
    }
    showScore();
    clearRound();
  }

  function setPhase(next) {
    phase = next;
    const busy = phase !== "idle";
    for (const button of modes) button.disabled = busy;
    reset.disabled = busy;
    spin.hidden = phase === "player";
    spin.disabled = busy;
    stop.hidden = phase !== "player";
    wheel.classList.toggle("spinning", phase === "player" || phase === "computer");
  }

  async function play(body, reveal = Promise.resolve()) {
    error.hidden = true;
    try {
      const response = await fetch(form.action, { method: "POST", body });
      if (!response.ok) throw new Error("Round request failed");

      const page = new DOMParser().parseFromString(await response.text(), "text/html");
      const nextRound = page.querySelector(".round-display");
      if (!nextRound) throw new Error("Round response is missing");

      await reveal;
      const outcome = nextRound.querySelector("[data-outcome]")?.dataset.outcome;
      if (outcome === "win") scores[mode].player += 1;
      if (outcome === "lose") scores[mode].computer += 1;
      saveScore();
      round.replaceChildren(...nextRound.childNodes);
      if (mode === "roulette") {
        const computer = round.querySelector("[data-computer]")?.dataset.computer;
        const index = moves.indexOf(computer);
        if (index !== -1) wheel.style.transform = "rotate(" + (-60 - 120 * index) + "deg)";
      }
    } catch {
      await reveal;
      error.textContent = "Could not play this round. Try again.";
      error.hidden = false;
    } finally {
      status.textContent = "";
      setPhase("idle");
      if (mode === "roulette") spin.focus();
    }
  }

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    if (phase !== "idle" || !event.submitter) return;
    setPhase("classic");
    play(new FormData(form, event.submitter));
  });

  spin.addEventListener("click", () => {
    if (phase !== "idle") return;
    clearRound();
    setPhase("player");
    status.textContent = "Your wheel is spinning.";
    stop.focus();
  });

  stop.addEventListener("click", () => {
    if (phase !== "player") return;
    const move = moves[Math.floor(Math.random() * moves.length)];
    setPhase("computer");
    status.textContent = "You spun " + move + ". The computer is spinning.";
    const reveal = new Promise((resolve) => setTimeout(resolve, 950));
    play(new URLSearchParams({ move }), reveal);
  });

  reset.addEventListener("click", () => {
    scores[mode] = emptyScore();
    saveScore();
    clearRound();
  });

  function switchMode(target) {
    scores[mode] = emptyScore();
    saveScore();
    mode = target;
    sessionStorage.setItem("rps.mode", mode);
    showMode();
  }

  for (const button of modes) {
    button.addEventListener("click", () => {
      const target = button.dataset.mode;
      if (target === mode || phase !== "idle") return;
      if (scores[mode].player || scores[mode].computer) {
        dialog.returnValue = "cancel";
        dialog.addEventListener("close", () => {
          if (dialog.returnValue === "continue") switchMode(target);
        }, { once: true });
        dialog.showModal();
      } else {
        switchMode(target);
      }
    });
  }

  showMode();
  picker.hidden = false;
  reset.hidden = false;
})();
