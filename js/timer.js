(function () {
  "use strict";

  function format(seconds) {
    const minutes = Math.floor(seconds / 60).toString().padStart(2, "0");
    const remainder = (seconds % 60).toString().padStart(2, "0");
    return `${minutes}:${remainder}`;
  }

  document.addEventListener("club:topic-ready", function (event) {
    const root = document.querySelector("#timerRoot");

    if (event.detail.mode !== "host") {
      root.hidden = true;
      root.replaceChildren();
      return;
    }

    root.hidden = false;
    root.className = "timer-panel";

    const label = document.createElement("label");
    label.setAttribute("for", "timerMinutes");
    label.textContent = "Discussion time／討論時間";

    const select = document.createElement("select");
    select.id = "timerMinutes";
    [["5", "5 minutes"], ["10", "10 minutes"], ["15", "15 minutes"]]
      .forEach(function ([value, text]) {
        const option = document.createElement("option");
        option.value = value;
        option.textContent = text;
        if (value === "10") option.selected = true;
        select.append(option);
      });

    const display = document.createElement("output");
    display.id = "timerDisplay";
    display.setAttribute("aria-label", "Time remaining");

    const controls = document.createElement("div");
    controls.className = "timer-controls";

    function button(id, text) {
      const element = document.createElement("button");
      element.id = id;
      element.type = "button";
      element.textContent = text;
      return element;
    }

    const start = button("timerStart", "Start／開始");
    const pause = button("timerPause", "Pause／暫停");
    const reset = button("timerReset", "Reset／重設");
    controls.append(start, pause, reset);

    const status = document.createElement("p");
    status.id = "timerStatus";
    status.setAttribute("aria-live", "assertive");

    root.replaceChildren(label, select, display, controls, status);

    let state = "idle";
    let intervalId = null;
    let remaining = initialSeconds();

    function initialSeconds() {
      return Number(select.value) * 60;
    }

    function render() {
      display.textContent = format(remaining);
      status.textContent = state === "expired" ? "Time is up／時間到！" : "";
      root.dataset.timerState = state;
    }

    function stopInterval() {
      if (intervalId !== null) {
        window.clearInterval(intervalId);
        intervalId = null;
      }
    }

    function startTimer() {
      if (state === "running" || remaining <= 0) return;
      state = "running";
      render();
      intervalId = window.setInterval(function () {
        remaining -= 1;
        if (remaining <= 0) {
          remaining = 0;
          state = "expired";
          stopInterval();
        }
        render();
      }, 1000);
    }

    function pauseTimer() {
      if (state !== "running") return;
      stopInterval();
      state = "paused";
      render();
    }

    function resetTimer() {
      stopInterval();
      remaining = initialSeconds();
      state = "idle";
      render();
    }

    select.addEventListener("change", resetTimer);
    start.addEventListener("click", startTimer);
    pause.addEventListener("click", pauseTimer);
    reset.addEventListener("click", resetTimer);
    window.addEventListener("pagehide", stopInterval);

    render();
  });
})();
