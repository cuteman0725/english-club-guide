(function () {
  "use strict";

  function renderParagraphs(root, paragraphs) {
    root.replaceChildren(...paragraphs.map(function (text) {
      const paragraph = document.createElement("p");
      paragraph.textContent = text;
      return paragraph;
    }));
  }

  function initializeTabs() {
    const buttons = Array.from(document.querySelectorAll(".tab-button"));
    const panels = Array.from(document.querySelectorAll(".tab-panel"));

    buttons.forEach(function (button) {
      button.addEventListener("click", function () {
        const targetId = button.dataset.tabTarget;
        buttons.forEach(function (item) {
          const active = item === button;
          item.classList.toggle("is-active", active);
          item.setAttribute("aria-selected", String(active));
        });
        panels.forEach(function (panel) {
          panel.hidden = panel.id !== targetId;
        });
      });
    });
  }

  function initialize() {
    const topicId = document.body.dataset.topicId;
    const topic = ClubContent.get(topicId);
    const mode = ClubMode.parse(window.location.search);

    document.title = `${topic.session}: ${topic.title}`;
    document.querySelector("#topicSession").textContent = topic.session;
    document.querySelector("#topicTitle").textContent = topic.title;
    document.querySelector("#topicSubtitle").textContent = topic.subtitle;
    renderParagraphs(document.querySelector("#articleBody"), topic.summaryParagraphs);
    document.querySelector("#factNote").textContent = topic.factNote;

    const sourceLink = document.querySelector("#sourceLink");
    sourceLink.href = topic.sourceUrl;
    sourceLink.textContent = `Open ${topic.sourceLabel}／開啟原始來源 ↗`;

    const backgroundSourceLink = document.querySelector("#backgroundSourceLink");
    if (topic.backgroundSource) {
      backgroundSourceLink.href = topic.backgroundSource.url;
      backgroundSourceLink.textContent = `Open ${topic.backgroundSource.label}／開啟背景文章 ↗`;
      backgroundSourceLink.hidden = false;
    } else {
      backgroundSourceLink.hidden = true;
    }

    const image = document.querySelector("#visualImage");
    image.src = topic.image.src;
    image.alt = topic.image.alt;
    document.querySelector("#visualDisclosure").textContent = topic.image.disclosure;

    const modeSelect = document.querySelector("#topicMode");
    modeSelect.value = mode;
    modeSelect.addEventListener("change", function () {
      window.location.search = `?mode=${encodeURIComponent(modeSelect.value)}`;
    });

    document.querySelector("#homeLink").href = ClubMode.withMode("index.html", mode);
    initializeTabs();

    document.dispatchEvent(new CustomEvent("club:topic-ready", {
      detail: { topic, mode }
    }));
  }

  document.addEventListener("DOMContentLoaded", initialize);
})();
