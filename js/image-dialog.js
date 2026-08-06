(function () {
  "use strict";

  document.addEventListener("club:topic-ready", function () {
    const openButton = document.querySelector("#visualOpenButton");
    const sourceImage = document.querySelector("#visualImage");
    const dialog = document.querySelector("#imageDialog");
    const dialogImage = document.querySelector("#dialogImage");

    if (!openButton || !sourceImage || !dialog || !dialogImage) return;

    dialogImage.src = sourceImage.src;
    dialogImage.alt = sourceImage.alt;

    openButton.addEventListener("click", function () {
      dialog.showModal();
    });

    dialog.addEventListener("close", function () {
      openButton.focus();
    });

    dialog.addEventListener("click", function (event) {
      if (event.target === dialog) dialog.close();
    });
  });
})();
