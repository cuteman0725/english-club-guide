(function () {
  "use strict";

  function createButton(id, text) {
    const button = document.createElement("button");
    button.id = id;
    button.type = "button";
    button.textContent = text;
    return button;
  }

  document.addEventListener("club:topic-ready", function (event) {
    const questions = event.detail.topic.questions;
    const root = document.querySelector("#questionsRoot");
    let currentIndex = 0;
    let showAll = false;

    const toolbar = document.createElement("div");
    toolbar.className = "question-toolbar";

    const progress = document.createElement("p");
    progress.id = "questionProgress";
    progress.setAttribute("aria-live", "polite");

    const toggleAll = createButton("toggleAllQuestions", "Show all／全部顯示");
    toolbar.append(progress, toggleAll);

    const card = document.createElement("article");
    card.className = "question-card";
    const text = document.createElement("p");
    text.id = "questionText";
    card.append(text);

    const controls = document.createElement("div");
    controls.className = "question-controls";
    const previous = createButton("previousQuestion", "← Previous／上一題");
    const next = createButton("nextQuestion", "Next／下一題 →");
    controls.append(previous, next);

    const allQuestions = document.createElement("ol");
    allQuestions.id = "allQuestions";
    allQuestions.hidden = true;
    questions.forEach(function (question) {
      const item = document.createElement("li");
      item.textContent = question;
      allQuestions.append(item);
    });

    function render() {
      progress.textContent = `Question ${currentIndex + 1} of ${questions.length}`;
      text.textContent = questions[currentIndex];
      previous.disabled = currentIndex === 0;
      next.disabled = currentIndex === questions.length - 1;
      allQuestions.hidden = !showAll;
      toggleAll.textContent = showAll ? "Hide all／收合" : "Show all／全部顯示";
      document.dispatchEvent(new CustomEvent("club:question-change", {
        detail: { index: currentIndex, total: questions.length }
      }));
    }

    previous.addEventListener("click", function () {
      if (currentIndex > 0) currentIndex -= 1;
      render();
    });
    next.addEventListener("click", function () {
      if (currentIndex < questions.length - 1) currentIndex += 1;
      render();
    });
    toggleAll.addEventListener("click", function () {
      showAll = !showAll;
      render();
    });

    root.replaceChildren(toolbar, card, controls, allQuestions);
    render();
  });
})();
