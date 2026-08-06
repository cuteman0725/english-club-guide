(function () {
  "use strict";

  const VALID_MODES = new Set(["participant", "host"]);

  function parse(search) {
    const value = new URLSearchParams(search).get("mode");
    return VALID_MODES.has(value) ? value : "participant";
  }

  function withMode(path, mode) {
    const safeMode = VALID_MODES.has(mode) ? mode : "participant";
    return `${path}?mode=${encodeURIComponent(safeMode)}`;
  }

  window.ClubMode = Object.freeze({ parse, withMode });
})();
