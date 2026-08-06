# English Club Interactive Discussion Guide Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a bilingual, mobile-first, static English Club discussion website with two independent topic pages, article summaries, offline infographics, five-question navigation, participant/host modes, and a silent host countdown timer.

**Architecture:** Use plain HTML, CSS, and classic deferred JavaScript so the same files work through GitHub Pages and directly from `file://` after ZIP extraction. Store topic copy in a shared `js/content.js` data object, UI behaviour in focused JavaScript files, and use two thin topic HTML entry pages that identify their topic through a `data-topic-id` attribute. Use Playwright only as a development-time test dependency; the deployed site has no runtime dependency or server requirement.

**Tech Stack:** HTML5, CSS3, vanilla JavaScript (ES2020-compatible classic scripts), Node.js 20+, Playwright Test, Python 3 standard-library HTTP server for local test hosting, GitHub Pages.

## Global Constraints

- Online delivery must work through GitHub Pages.
- Offline delivery must work after extracting a ZIP and opening `index.html`.
- The site must contain a home page and one independent page for each topic.
- Navigation and controls are bilingual; article summaries and discussion questions remain in English.
- Each topic provides `Article／文章`, `Visual Summary／圖解`, and `Questions／問題`.
- Participant and Host modes share the same content.
- Host mode provides a 5, 10, or 15 minute silent countdown timer.
- The site must use no server-side code, database, remote JavaScript, remote stylesheet, remote font, `fetch()`, cookies, or browser storage.
- All production CSS, JavaScript, images, and copy must be local.
- Body text must remain readable from 320 CSS pixels upward.
- Printing must hide navigation and timer controls and show the article, infographic, and all five questions.
- Generated visual summaries must be labelled as illustrative summaries rather than original news photographs.
- Timer state and current question are local to one browser tab and are not synchronized between users.
- Do not implement login, voting, chat, analytics, CMS, push notifications, real-time synchronization, or PWA installation.

---

## File Structure

```text
english-club-guide/
├─ index.html
├─ topic-senior-driving.html
├─ topic-mass-tourism.html
├─ README.md
├─ package.json
├─ playwright.config.js
├─ css/
│  ├─ tokens.css
│  ├─ base.css
│  ├─ components.css
│  └─ print.css
├─ js/
│  ├─ content.js
│  ├─ mode.js
│  ├─ topic-page.js
│  ├─ question-navigator.js
│  ├─ timer.js
│  └─ image-dialog.js
├─ images/
│  ├─ senior-driving-summary.png
│  ├─ mass-tourism-article-summary.png
│  └─ mass-tourism-questions.png
├─ scripts/
│  ├─ verify-static-site.mjs
│  └─ make-offline-zip.py
└─ tests/
   ├─ home.spec.js
   ├─ topic-content.spec.js
   ├─ questions.spec.js
   ├─ host-timer.spec.js
   ├─ accessibility.spec.js
   ├─ offline.spec.js
   └─ print.spec.js
```

### File Responsibilities

- `index.html`: mode selection and links to the two independent topic pages.
- `topic-senior-driving.html`: Session I page shell with `data-topic-id="senior-driving"`.
- `topic-mass-tourism.html`: Session II page shell with `data-topic-id="mass-tourism"`.
- `js/content.js`: immutable topic metadata, summaries, sources, image paths, alt text, disclosures, and questions.
- `js/mode.js`: parse and retain `?mode=participant|host`; update mode controls and page visibility.
- `js/topic-page.js`: render article and source data, switch Article/Visual/Questions tabs, and initialize topic components.
- `js/question-navigator.js`: one-at-a-time question navigation and show-all behaviour.
- `js/timer.js`: host-only timer state machine and accessible status updates.
- `js/image-dialog.js`: tap-to-enlarge `<dialog>` interaction and focus restoration.
- `css/tokens.css`: theme variables, spacing, type scale, touch-target constants.
- `css/base.css`: reset, typography, layout, focus states.
- `css/components.css`: cards, tabs, topic screens, question cards, timer and dialog.
- `css/print.css`: printable handout layout.
- `scripts/verify-static-site.mjs`: reject remote production dependencies and missing local assets.
- `scripts/make-offline-zip.py`: produce a ZIP containing only deployable static files.
- `tests/*.spec.js`: browser-level acceptance coverage.

---

### Task 1: Establish the Static Project and Home Navigation

**Files:**
- Create: `package.json`
- Create: `playwright.config.js`
- Create: `index.html`
- Create: `css/tokens.css`
- Create: `css/base.css`
- Create: `css/components.css`
- Create: `js/mode.js`
- Create: `tests/home.spec.js`

**Interfaces:**
- Produces: `window.ClubMode.parse(search: string): "participant" | "host"`
- Produces: `window.ClubMode.withMode(path: string, mode: string): string`
- Produces: home links with IDs `topicSeniorDriving` and `topicMassTourism`
- Produces: mode selector with ID `homeMode`

- [ ] **Step 1: Create the test runner configuration**

Create `package.json`:

```json
{
  "name": "english-club-interactive-guide",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "test": "playwright test",
    "test:headed": "playwright test --headed",
    "verify": "node scripts/verify-static-site.mjs",
    "package:offline": "python scripts/make-offline-zip.py"
  },
  "devDependencies": {
    "@playwright/test": "1.54.2"
  }
}
```

Create `playwright.config.js`:

```js
const { defineConfig, devices } = require("@playwright/test");

module.exports = defineConfig({
  testDir: "./tests",
  fullyParallel: false,
  timeout: 20_000,
  use: {
    baseURL: "http://127.0.0.1:4173",
    trace: "retain-on-failure"
  },
  projects: [
    { name: "mobile-chrome", use: devices["Pixel 5"] },
    { name: "tablet", use: { viewport: { width: 768, height: 1024 } } },
    { name: "desktop", use: { viewport: { width: 1280, height: 800 } } }
  ],
  webServer: {
    command: "python -m http.server 4173",
    port: 4173,
    reuseExistingServer: true
  }
});
```

- [ ] **Step 2: Write failing home-page tests**

Create `tests/home.spec.js`:

```js
const { test, expect } = require("@playwright/test");

test("home displays two topic choices", async ({ page }) => {
  await page.goto("/index.html");
  await expect(page.getByRole("heading", { name: /Choose a discussion topic/i })).toBeVisible();
  await expect(page.locator("#topicSeniorDriving")).toContainText("Senior Driver");
  await expect(page.locator("#topicMassTourism")).toContainText("Mass Tourism");
});

test("selected mode is carried into both topic URLs", async ({ page }) => {
  await page.goto("/index.html");
  await page.locator("#homeMode").selectOption("host");
  await expect(page.locator("#topicSeniorDriving")).toHaveAttribute(
    "href",
    "topic-senior-driving.html?mode=host"
  );
  await expect(page.locator("#topicMassTourism")).toHaveAttribute(
    "href",
    "topic-mass-tourism.html?mode=host"
  );
});

test("unknown mode falls back to participant", async ({ page }) => {
  await page.goto("/index.html?mode=unknown");
  await expect(page.locator("#homeMode")).toHaveValue("participant");
});
```

- [ ] **Step 3: Run the tests and confirm failure**

Run:

```bash
npm install
npx playwright install chromium
npm test -- tests/home.spec.js
```

Expected: FAIL because `index.html` and the expected controls do not yet exist.

- [ ] **Step 4: Implement the mode utility**

Create `js/mode.js`:

```js
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
```

- [ ] **Step 5: Implement base visual tokens**

Create `css/tokens.css`:

```css
:root {
  color-scheme: light;
  --page: #f5f7fb;
  --surface: #ffffff;
  --surface-soft: #eef4ff;
  --text: #182033;
  --muted: #5d6679;
  --border: #cfd7e6;
  --accent: #2457a7;
  --accent-text: #ffffff;
  --danger: #a92f2f;
  --radius: 1rem;
  --content-width: 72rem;
  --reading-width: 46rem;
  --touch-target: 2.75rem;
}

@media (prefers-color-scheme: dark) {
  :root {
    color-scheme: dark;
    --page: #111827;
    --surface: #1f2937;
    --surface-soft: #243552;
    --text: #f5f7fb;
    --muted: #bdc6d7;
    --border: #44516a;
    --accent: #8db7ff;
    --accent-text: #102040;
    --danger: #ff9a9a;
  }
}
```

- [ ] **Step 6: Implement shared base styles**

Create `css/base.css`:

```css
* { box-sizing: border-box; }

html { font-size: 16px; }

body {
  margin: 0;
  min-width: 320px;
  background: var(--page);
  color: var(--text);
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  line-height: 1.65;
}

a { color: inherit; }

button,
select,
a.topic-card {
  min-height: var(--touch-target);
}

button,
select {
  font: inherit;
}

button:focus-visible,
select:focus-visible,
a:focus-visible {
  outline: 3px solid var(--accent);
  outline-offset: 3px;
}

.site-shell {
  width: min(100% - 2rem, var(--content-width));
  margin-inline: auto;
  padding-block: 1.25rem 3rem;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip-path: inset(50%);
  white-space: nowrap;
  border: 0;
}
```

Create the first part of `css/components.css`:

```css
.page-header {
  display: flex;
  flex-wrap: wrap;
  align-items: end;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.mode-control {
  display: grid;
  gap: 0.3rem;
  font-size: 0.9rem;
}

.mode-control select {
  border: 1px solid var(--border);
  border-radius: 0.75rem;
  background: var(--surface);
  color: var(--text);
  padding: 0.65rem 0.8rem;
}

.topic-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
}

.topic-card {
  display: block;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--surface);
  padding: 1.25rem;
  text-decoration: none;
}

.topic-card:hover {
  border-color: var(--accent);
}

.topic-card__session {
  color: var(--accent);
  font-weight: 700;
}

.topic-card h2 {
  margin: 0.6rem 0 0.4rem;
  line-height: 1.25;
}

.topic-card p {
  margin: 0;
  color: var(--muted);
}

@media (max-width: 640px) {
  .topic-grid { grid-template-columns: 1fr; }
}
```

- [ ] **Step 7: Implement the home page**

Create `index.html`:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>English Club Discussion Guide</title>
  <link rel="stylesheet" href="css/tokens.css">
  <link rel="stylesheet" href="css/base.css">
  <link rel="stylesheet" href="css/components.css">
  <script defer src="js/mode.js"></script>
  <script defer>
    document.addEventListener("DOMContentLoaded", function () {
      const modeSelect = document.querySelector("#homeMode");
      const links = {
        senior: document.querySelector("#topicSeniorDriving"),
        tourism: document.querySelector("#topicMassTourism")
      };

      function updateLinks() {
        links.senior.href = ClubMode.withMode("topic-senior-driving.html", modeSelect.value);
        links.tourism.href = ClubMode.withMode("topic-mass-tourism.html", modeSelect.value);
      }

      modeSelect.value = ClubMode.parse(window.location.search);
      modeSelect.addEventListener("change", updateLinks);
      updateLinks();
    });
  </script>
</head>
<body>
  <main class="site-shell">
    <header class="page-header">
      <div>
        <p>English Club／英文俱樂部</p>
        <h1>Choose a discussion topic</h1>
      </div>
      <label class="mode-control" for="homeMode">
        Mode／模式
        <select id="homeMode">
          <option value="participant">Participant／參加者</option>
          <option value="host">Host／主持人</option>
        </select>
      </label>
    </header>

    <section class="topic-grid" aria-label="Discussion topics">
      <a id="topicSeniorDriving" class="topic-card" href="topic-senior-driving.html?mode=participant">
        <span class="topic-card__session">Session I</span>
        <h2>Senior Driver License Renewal</h2>
        <p>Should older drivers face stricter license renewal requirements?</p>
      </a>

      <a id="topicMassTourism" class="topic-card" href="topic-mass-tourism.html?mode=participant">
        <span class="topic-card__session">Session II</span>
        <h2>Mass Tourism in Mallorca</h2>
        <p>Is mass tourism destroying the places we love?</p>
      </a>
    </section>
  </main>
</body>
</html>
```

- [ ] **Step 8: Run home-page tests**

Run:

```bash
npm test -- tests/home.spec.js
```

Expected: 3 tests PASS in all configured projects.

- [ ] **Step 9: Commit Task 1**

```bash
git add package.json playwright.config.js index.html css js/mode.js tests/home.spec.js
git commit -m "feat: add bilingual topic home page"
```

---

### Task 2: Define Verified Topic Content and Render Independent Article Pages

**Files:**
- Create: `js/content.js`
- Create: `js/topic-page.js`
- Create: `topic-senior-driving.html`
- Create: `topic-mass-tourism.html`
- Modify: `css/components.css`
- Create: `tests/topic-content.spec.js`

**Interfaces:**
- Consumes: `window.ClubMode.parse()` and `window.ClubMode.withMode()`
- Produces: `window.ClubContent.get(topicId: string): Topic`
- Produces Topic shape:
  - `id: string`
  - `session: string`
  - `title: string`
  - `subtitle: string`
  - `summaryParagraphs: string[]`
  - `factNote: string`
  - `sourceLabel: string`
  - `sourceUrl: string`
  - `image: { src: string, alt: string, disclosure: string }`
  - `questions: string[]`
- Produces DOM IDs used by later tasks:
  - `topicSession`, `topicTitle`, `topicSubtitle`
  - `articleBody`, `factNote`, `sourceLink`
  - `visualImage`, `visualDisclosure`
  - `questionsRoot`, `timerRoot`
  - `topicMode`, `homeLink`

- [ ] **Step 1: Write failing topic-content tests**

Create `tests/topic-content.spec.js`:

```js
const { test, expect } = require("@playwright/test");

for (const fixture of [
  {
    path: "/topic-senior-driving.html?mode=participant",
    heading: "Senior Driver License Renewal in Taiwan",
    source: /thb\.gov\.tw/,
    phrase: "May 31, 2026"
  },
  {
    path: "/topic-mass-tourism.html?mode=participant",
    heading: "Mass Tourism in Mallorca",
    source: /reuters\.com/,
    phrase: "July 26, 2026"
  }
]) {
  test(`${fixture.heading} renders verified summary and source`, async ({ page }) => {
    await page.goto(fixture.path);
    await expect(page.getByRole("heading", { name: fixture.heading })).toBeVisible();
    await expect(page.locator("#articleBody")).toContainText(fixture.phrase);
    await expect(page.locator("#sourceLink")).toHaveAttribute("href", fixture.source);
  });
}

test("topic page retains host mode on home link", async ({ page }) => {
  await page.goto("/topic-senior-driving.html?mode=host");
  await expect(page.locator("#topicMode")).toHaveValue("host");
  await expect(page.locator("#homeLink")).toHaveAttribute("href", "index.html?mode=host");
});
```

- [ ] **Step 2: Run the topic-content tests and confirm failure**

Run:

```bash
npm test -- tests/topic-content.spec.js
```

Expected: FAIL because topic pages and shared content do not yet exist.

- [ ] **Step 3: Add the shared topic content**

Create `js/content.js`:

```js
(function () {
  "use strict";

  const topics = Object.freeze({
    "senior-driving": Object.freeze({
      id: "senior-driving",
      session: "Session I",
      title: "Senior Driver License Renewal in Taiwan",
      subtitle: "Should older drivers face stricter license renewal requirements?",
      summaryParagraphs: Object.freeze([
        "Starting on May 31, 2026, Taiwan lowers the mandatory senior driver license renewal age from 75 to 70.",
        "Drivers aged 70 to 74 must pass a physical examination and complete a road-safety course. Their renewed license remains valid until age 75.",
        "Drivers aged 75 or above must also complete a cognitive assessment, or provide medical evidence showing that they do not have moderate or severe dementia. They must renew their licenses every three years."
      ]),
      factNote: "The policy does not automatically require every older driver to retake an actual road test. Whether a road test should be added is a discussion question.",
      sourceLabel: "Taiwan Directorate General of Highways",
      sourceUrl: "https://www.thb.gov.tw/en/News_Content_Table.aspx?n=10868&s=300330",
      image: Object.freeze({
        src: "images/senior-driving-summary.png",
        alt: "Illustrated English summary of Taiwan's senior driver license renewal rules for ages 70 to 74 and age 75 or older.",
        disclosure: "AI-generated illustrative summary based on the official policy. It is not an official government graphic."
      }),
      questions: Object.freeze([
        "Do you agree that drivers should be required to renew their licenses after the age of 70? Is 70 an appropriate age, or should the requirement begin earlier or later?",
        "Should older drivers be required to retake an actual road test, or are physical examinations, cognitive assessments and road-safety courses enough?",
        "Is it fair to judge driving ability mainly by age? Should a driver’s health, accident history and driving record be considered more important than age?",
        "If you felt that an elderly family member or friend was no longer able to drive safely, would you ask that person to stop driving? Who should make the final decision—the driver, the family, a doctor or the government?",
        "If older people give up driving, what transportation services or financial support should the government provide?"
      ])
    }),

    "mass-tourism": Object.freeze({
      id: "mass-tourism",
      session: "Session II",
      title: "Mass Tourism in Mallorca",
      subtitle: "Is mass tourism destroying the places we love?",
      summaryParagraphs: Object.freeze([
        "On July 26, 2026, residents marched in Mallorca, Spain, to protest against mass tourism.",
        "Protesters said that excessive visitor numbers were damaging the island’s culture and environment and making everyday life more difficult for local residents.",
        "Wider reporting on overtourism in Spain has focused on rising housing costs, crowded streets, pressure on transportation and public services, and heavy demand for water and other natural resources.",
        "Tourism also provides jobs, business income and tax revenue. The central conflict is how to preserve these benefits without making residents and the environment bear most of the costs."
      ]),
      factNote: "The Reuters link is a short news-video page. This summary clearly separates the video's core report from broader background reporting on overtourism in Spain.",
      sourceLabel: "Reuters video report",
      sourceUrl: "https://www.reuters.com/video/watch/idRW109027072026RP1/",
      image: Object.freeze({
        src: "images/mass-tourism-article-summary.png",
        alt: "Illustrated English news summary of residents protesting mass tourism in Mallorca and its effects on housing, services, culture and the environment.",
        disclosure: "AI-generated illustrative summary based on Reuters reporting. The people and scenes are not original Reuters photographs."
      }),
      questions: Object.freeze([
        "Do you think mass tourism brings more benefits or more problems to a popular destination? Who benefits the most from tourism, and who suffers the most?",
        "Have you ever visited a place that was so crowded that it affected your travel experience? Did the crowds make you enjoy the trip less?",
        "Should popular destinations limit the number of visitors by requiring reservations, restricting tour buses or cruise ships, or charging higher entrance fees and tourism taxes?",
        "Is it fair for local residents to blame tourists, or should governments and tourism businesses take more responsibility?",
        "Would you be willing to travel during the off-season, visit a less famous destination or pay more money to reduce the negative effects of tourism? Why or why not?"
      ])
    })
  });

  function get(topicId) {
    const topic = topics[topicId];
    if (!topic) {
      throw new Error(`Unknown topic: ${topicId}`);
    }
    return topic;
  }

  window.ClubContent = Object.freeze({ get });
})();
```

- [ ] **Step 4: Add the shared topic-page renderer**

Create `js/topic-page.js`:

```js
(function () {
  "use strict";

  function renderParagraphs(root, paragraphs) {
    root.replaceChildren(
      ...paragraphs.map(function (text) {
        const paragraph = document.createElement("p");
        paragraph.textContent = text;
        return paragraph;
      })
    );
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
    sourceLink.textContent = `Open ${topic.sourceLabel}／開啟原始來源`;

    const image = document.querySelector("#visualImage");
    image.src = topic.image.src;
    image.alt = topic.image.alt;
    document.querySelector("#visualDisclosure").textContent = topic.image.disclosure;

    const modeSelect = document.querySelector("#topicMode");
    modeSelect.value = mode;
    modeSelect.addEventListener("change", function () {
      const newMode = modeSelect.value;
      window.location.search = `?mode=${encodeURIComponent(newMode)}`;
    });

    document.querySelector("#homeLink").href = ClubMode.withMode("index.html", mode);

    document.dispatchEvent(new CustomEvent("club:topic-ready", {
      detail: { topic, mode }
    }));
  }

  document.addEventListener("DOMContentLoaded", initialize);
})();
```

- [ ] **Step 5: Create the shared topic-page HTML shell**

Create `topic-senior-driving.html` and copy it to `topic-mass-tourism.html`, changing only the `<title>` and `data-topic-id`.

`topic-senior-driving.html`:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Session I: Senior Driver License Renewal</title>
  <link rel="stylesheet" href="css/tokens.css">
  <link rel="stylesheet" href="css/base.css">
  <link rel="stylesheet" href="css/components.css">
  <link rel="stylesheet" href="css/print.css" media="print">
  <script defer src="js/mode.js"></script>
  <script defer src="js/content.js"></script>
  <script defer src="js/question-navigator.js"></script>
  <script defer src="js/timer.js"></script>
  <script defer src="js/image-dialog.js"></script>
  <script defer src="js/topic-page.js"></script>
</head>
<body data-topic-id="senior-driving">
  <main class="site-shell">
    <nav class="topic-nav" aria-label="Topic navigation">
      <a id="homeLink" class="button-link" href="index.html?mode=participant">← Home／首頁</a>
      <label class="mode-control" for="topicMode">
        Mode／模式
        <select id="topicMode">
          <option value="participant">Participant／參加者</option>
          <option value="host">Host／主持人</option>
        </select>
      </label>
    </nav>

    <header class="topic-header">
      <p id="topicSession"></p>
      <h1 id="topicTitle"></h1>
      <p id="topicSubtitle"></p>
    </header>

    <nav class="tab-list" aria-label="Topic sections">
      <button type="button" class="tab-button is-active" data-tab-target="articlePanel"
              aria-controls="articlePanel" aria-selected="true">Article／文章</button>
      <button type="button" class="tab-button" data-tab-target="visualPanel"
              aria-controls="visualPanel" aria-selected="false">Visual Summary／圖解</button>
      <button type="button" class="tab-button" data-tab-target="questionsPanel"
              aria-controls="questionsPanel" aria-selected="false">Questions／問題</button>
    </nav>

    <section id="articlePanel" class="tab-panel reading-panel">
      <div id="articleBody"></div>
      <aside class="fact-note">
        <strong>Important note:</strong>
        <span id="factNote"></span>
      </aside>
      <a id="sourceLink" class="button-link" href="#" target="_blank" rel="noopener"></a>
    </section>

    <section id="visualPanel" class="tab-panel" hidden>
      <button id="visualOpenButton" class="image-button" type="button">
        <img id="visualImage" src="" alt="">
        <span>Tap to enlarge／點一下放大</span>
      </button>
      <p id="visualDisclosure" class="disclosure"></p>
    </section>

    <section id="questionsPanel" class="tab-panel" hidden>
      <div id="questionsRoot"></div>
      <div id="timerRoot" hidden></div>
    </section>
  </main>

  <dialog id="imageDialog">
    <form method="dialog">
      <button class="dialog-close" aria-label="Close enlarged image">Close／關閉</button>
    </form>
    <img id="dialogImage" src="" alt="">
  </dialog>
</body>
</html>
```

In `topic-mass-tourism.html`, set:

```html
<title>Session II: Mass Tourism in Mallorca</title>
<body data-topic-id="mass-tourism">
```

- [ ] **Step 6: Add article and tab styles**

Append to `css/components.css`:

```css
.topic-nav,
.topic-header,
.tab-list,
.tab-panel {
  width: min(100%, var(--reading-width));
  margin-inline: auto;
}

.topic-nav {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.button-link {
  display: inline-flex;
  align-items: center;
  border: 1px solid var(--border);
  border-radius: 0.75rem;
  background: var(--surface);
  padding: 0.65rem 0.9rem;
  text-decoration: none;
}

.topic-header {
  margin-bottom: 1rem;
}

.topic-header h1 {
  margin: 0.25rem 0;
  line-height: 1.2;
}

.topic-header p {
  margin: 0;
  color: var(--muted);
}

.tab-list {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.tab-button {
  border: 1px solid var(--border);
  border-radius: 0.75rem;
  background: var(--surface);
  color: var(--text);
  padding: 0.7rem 0.45rem;
}

.tab-button.is-active {
  border-color: var(--accent);
  background: var(--accent);
  color: var(--accent-text);
}

.tab-panel {
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--surface);
  padding: clamp(1rem, 4vw, 2rem);
}

.reading-panel p {
  margin: 0 0 1rem;
}

.fact-note {
  margin-block: 1.25rem;
  border-inline-start: 0.3rem solid var(--accent);
  background: var(--surface-soft);
  padding: 1rem;
}

.disclosure {
  color: var(--muted);
  font-size: 0.9rem;
}
```

- [ ] **Step 7: Implement tab switching inside `topic-page.js`**

Add before the `club:topic-ready` dispatch:

```js
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
```

- [ ] **Step 8: Run topic-content tests**

Run:

```bash
npm test -- tests/topic-content.spec.js
```

Expected: all tests PASS.

- [ ] **Step 9: Commit Task 2**

```bash
git add js/content.js js/topic-page.js topic-*.html css/components.css tests/topic-content.spec.js
git commit -m "feat: render independent topic article pages"
```

---

### Task 3: Add Responsive Question Navigation

**Files:**
- Create: `js/question-navigator.js`
- Modify: `css/components.css`
- Create: `tests/questions.spec.js`

**Interfaces:**
- Consumes: `club:topic-ready` event detail `{ topic, mode }`
- Produces:
  - `#questionProgress`
  - `#questionText`
  - `#previousQuestion`
  - `#nextQuestion`
  - `#toggleAllQuestions`
  - `#allQuestions`
- Produces custom event: `club:question-change` with `{ index, total }`

- [ ] **Step 1: Write failing question-navigation tests**

Create `tests/questions.spec.js`:

```js
const { test, expect } = require("@playwright/test");

test.beforeEach(async ({ page }) => {
  await page.goto("/topic-senior-driving.html?mode=participant");
  await page.getByRole("button", { name: /Questions/ }).click();
});

test("shows one question and advances through five questions", async ({ page }) => {
  await expect(page.locator("#questionProgress")).toHaveText("Question 1 of 5");
  await expect(page.locator("#questionText")).toContainText("renew their licenses");
  await page.locator("#nextQuestion").click();
  await expect(page.locator("#questionProgress")).toHaveText("Question 2 of 5");
  await expect(page.locator("#questionText")).toContainText("actual road test");
});

test("previous and next buttons stop at boundaries", async ({ page }) => {
  await expect(page.locator("#previousQuestion")).toBeDisabled();
  for (let index = 0; index < 4; index += 1) {
    await page.locator("#nextQuestion").click();
  }
  await expect(page.locator("#nextQuestion")).toBeDisabled();
  await expect(page.locator("#questionProgress")).toHaveText("Question 5 of 5");
});

test("show all reveals exactly five numbered questions", async ({ page }) => {
  await page.locator("#toggleAllQuestions").click();
  await expect(page.locator("#allQuestions > li")).toHaveCount(5);
  await expect(page.locator("#allQuestions")).toBeVisible();
});
```

- [ ] **Step 2: Run the tests and confirm failure**

Run:

```bash
npm test -- tests/questions.spec.js
```

Expected: FAIL because question controls do not exist.

- [ ] **Step 3: Implement the question navigator**

Create `js/question-navigator.js`:

```js
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
```

- [ ] **Step 4: Add question layout styles**

Append to `css/components.css`:

```css
.question-toolbar,
.question-controls {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
}

.question-toolbar button,
.question-controls button {
  border: 1px solid var(--border);
  border-radius: 0.75rem;
  background: var(--surface);
  color: var(--text);
  padding: 0.7rem 0.8rem;
}

.question-controls {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.question-card {
  margin-block: 1rem;
  border-radius: var(--radius);
  background: var(--surface-soft);
  padding: clamp(1.1rem, 5vw, 2rem);
}

.question-card p {
  margin: 0;
  font-size: clamp(1.2rem, 4.7vw, 1.65rem);
  line-height: 1.5;
}

#allQuestions {
  margin: 1.25rem 0 0;
  padding-inline-start: 1.5rem;
}

#allQuestions li {
  margin-bottom: 1rem;
  padding-inline-start: 0.4rem;
}

button:disabled {
  cursor: not-allowed;
  opacity: 0.45;
}
```

- [ ] **Step 5: Run the question tests**

Run:

```bash
npm test -- tests/questions.spec.js
```

Expected: all tests PASS.

- [ ] **Step 6: Commit Task 3**

```bash
git add js/question-navigator.js css/components.css tests/questions.spec.js
git commit -m "feat: add five-question discussion navigator"
```

---

### Task 4: Add the Host-Only Silent Countdown Timer

**Files:**
- Create: `js/timer.js`
- Modify: `css/components.css`
- Create: `tests/host-timer.spec.js`

**Interfaces:**
- Consumes: `club:topic-ready` event detail `{ mode }`
- Produces:
  - `#timerMinutes`
  - `#timerDisplay`
  - `#timerStart`
  - `#timerPause`
  - `#timerReset`
  - `#timerStatus`
- Timer states: `"idle" | "running" | "paused" | "expired"`

- [ ] **Step 1: Write failing host-timer tests**

Create `tests/host-timer.spec.js`:

```js
const { test, expect } = require("@playwright/test");

test("timer is hidden in participant mode", async ({ page }) => {
  await page.goto("/topic-senior-driving.html?mode=participant");
  await page.getByRole("button", { name: /Questions/ }).click();
  await expect(page.locator("#timerRoot")).toBeHidden();
});

test("host can choose, start, pause and reset the timer", async ({ page }) => {
  await page.goto("/topic-senior-driving.html?mode=host");
  await page.getByRole("button", { name: /Questions/ }).click();

  await expect(page.locator("#timerRoot")).toBeVisible();
  await page.locator("#timerMinutes").selectOption("5");
  await expect(page.locator("#timerDisplay")).toHaveText("05:00");

  await page.locator("#timerStart").click();
  await expect(page.locator("#timerDisplay")).not.toHaveText("05:00", { timeout: 2500 });

  await page.locator("#timerPause").click();
  const pausedValue = await page.locator("#timerDisplay").textContent();
  await page.waitForTimeout(1200);
  await expect(page.locator("#timerDisplay")).toHaveText(pausedValue);

  await page.locator("#timerReset").click();
  await expect(page.locator("#timerDisplay")).toHaveText("05:00");
});

test("timer expiry shows a silent visible alert", async ({ page }) => {
  await page.addInitScript(() => {
    window.__CLUB_TIMER_TEST_SECONDS__ = 1;
  });
  await page.goto("/topic-senior-driving.html?mode=host");
  await page.getByRole("button", { name: /Questions/ }).click();
  await page.locator("#timerStart").click();
  await expect(page.locator("#timerStatus")).toHaveText("Time is up／時間到！", {
    timeout: 2500
  });
});
```

- [ ] **Step 2: Run the tests and confirm failure**

Run:

```bash
npm test -- tests/host-timer.spec.js
```

Expected: FAIL because the timer UI does not exist.

- [ ] **Step 3: Implement the timer state machine**

Create `js/timer.js`:

```js
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
    [
      ["5", "5 minutes"],
      ["10", "10 minutes"],
      ["15", "15 minutes"]
    ].forEach(function ([value, text]) {
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

    const start = document.createElement("button");
    start.id = "timerStart";
    start.type = "button";
    start.textContent = "Start／開始";

    const pause = document.createElement("button");
    pause.id = "timerPause";
    pause.type = "button";
    pause.textContent = "Pause／暫停";

    const reset = document.createElement("button");
    reset.id = "timerReset";
    reset.type = "button";
    reset.textContent = "Reset／重設";

    controls.append(start, pause, reset);

    const status = document.createElement("p");
    status.id = "timerStatus";
    status.setAttribute("aria-live", "assertive");

    root.replaceChildren(label, select, display, controls, status);

    let state = "idle";
    let intervalId = null;
    let remaining = initialSeconds();

    function initialSeconds() {
      if (Number.isFinite(window.__CLUB_TIMER_TEST_SECONDS__)) {
        return window.__CLUB_TIMER_TEST_SECONDS__;
      }
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
```

- [ ] **Step 4: Add timer styles**

Append to `css/components.css`:

```css
.timer-panel {
  margin-top: 1.25rem;
  border-top: 1px solid var(--border);
  padding-top: 1.25rem;
}

.timer-panel label {
  display: block;
  margin-bottom: 0.35rem;
}

.timer-panel select {
  width: 100%;
  border: 1px solid var(--border);
  border-radius: 0.75rem;
  background: var(--surface);
  color: var(--text);
  padding: 0.7rem;
}

#timerDisplay {
  display: block;
  margin-block: 1rem;
  font-variant-numeric: tabular-nums;
  font-size: clamp(2rem, 12vw, 4rem);
  font-weight: 750;
  text-align: center;
}

.timer-controls {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.5rem;
}

.timer-controls button {
  border: 1px solid var(--border);
  border-radius: 0.75rem;
  background: var(--surface);
  color: var(--text);
  padding: 0.7rem 0.35rem;
}

#timerStatus {
  min-height: 1.7rem;
  margin-bottom: 0;
  color: var(--danger);
  font-weight: 750;
  text-align: center;
}
```

- [ ] **Step 5: Run timer tests**

Run:

```bash
npm test -- tests/host-timer.spec.js
```

Expected: all tests PASS without audio or notification permission requests.

- [ ] **Step 6: Commit Task 4**

```bash
git add js/timer.js css/components.css tests/host-timer.spec.js
git commit -m "feat: add silent host discussion timer"
```

---

### Task 5: Integrate Infographics with Accessible Tap-to-Enlarge Viewing

**Files:**
- Copy: `/mnt/data/台灣高齡駕照換發政策視覺指南.png` → `images/senior-driving-summary.png`
- Copy: `/mnt/data/a_wide_infographic_news_style_poster_about_a_prote.png` → `images/mass-tourism-article-summary.png`
- Copy: `/mnt/data/大眾旅遊會摧毀我們珍愛的地方嗎.png` → `images/mass-tourism-questions.png`
- Create: `js/image-dialog.js`
- Modify: `css/components.css`
- Create: `tests/accessibility.spec.js`

**Interfaces:**
- Consumes: `#visualOpenButton`, `#visualImage`, `#imageDialog`, `#dialogImage`
- Produces accessible `<dialog>` open/close behaviour
- Restores focus to `#visualOpenButton` after closing

- [ ] **Step 1: Copy and normalize image filenames**

Run:

```bash
mkdir -p images
cp "/mnt/data/台灣高齡駕照換發政策視覺指南.png" "images/senior-driving-summary.png"
cp "/mnt/data/a_wide_infographic_news_style_poster_about_a_prote.png" "images/mass-tourism-article-summary.png"
cp "/mnt/data/大眾旅遊會摧毀我們珍愛的地方嗎.png" "images/mass-tourism-questions.png"
```

Verify:

```bash
python - <<'PY'
from pathlib import Path
from PIL import Image

for path in Path("images").glob("*.png"):
    with Image.open(path) as image:
        print(path, image.size, image.mode)
PY
```

Expected: all three PNG files open without corruption.

- [ ] **Step 2: Write failing image and accessibility tests**

Create `tests/accessibility.spec.js`:

```js
const { test, expect } = require("@playwright/test");

test("topic image has meaningful alt text and disclosure", async ({ page }) => {
  await page.goto("/topic-mass-tourism.html?mode=participant");
  await page.getByRole("button", { name: /Visual Summary/ }).click();

  await expect(page.locator("#visualImage")).toHaveAttribute("alt", /Mallorca/i);
  await expect(page.locator("#visualDisclosure")).toContainText("AI-generated");
  await expect(page.locator("#visualDisclosure")).toContainText("not original Reuters photographs");
});

test("image can be enlarged and closed with focus restored", async ({ page }) => {
  await page.goto("/topic-senior-driving.html?mode=participant");
  await page.getByRole("button", { name: /Visual Summary/ }).click();

  await page.locator("#visualOpenButton").click();
  await expect(page.locator("#imageDialog")).toHaveJSProperty("open", true);
  await page.getByRole("button", { name: /Close enlarged image/i }).click();
  await expect(page.locator("#visualOpenButton")).toBeFocused();
});

test("all interactive controls are keyboard reachable", async ({ page }) => {
  await page.goto("/topic-senior-driving.html?mode=host");
  await page.keyboard.press("Tab");
  await expect(page.locator("#homeLink")).toBeFocused();
});
```

- [ ] **Step 3: Run the tests and confirm failure**

Run:

```bash
npm test -- tests/accessibility.spec.js
```

Expected: dialog/focus test FAIL because `image-dialog.js` does not yet exist.

- [ ] **Step 4: Implement the image dialog**

Create `js/image-dialog.js`:

```js
(function () {
  "use strict";

  document.addEventListener("club:topic-ready", function () {
    const openButton = document.querySelector("#visualOpenButton");
    const sourceImage = document.querySelector("#visualImage");
    const dialog = document.querySelector("#imageDialog");
    const dialogImage = document.querySelector("#dialogImage");

    dialogImage.src = sourceImage.src;
    dialogImage.alt = sourceImage.alt;

    openButton.addEventListener("click", function () {
      dialog.showModal();
    });

    dialog.addEventListener("close", function () {
      openButton.focus();
    });

    dialog.addEventListener("click", function (event) {
      if (event.target === dialog) {
        dialog.close();
      }
    });
  });
})();
```

- [ ] **Step 5: Add responsive image and dialog styles**

Append to `css/components.css`:

```css
.image-button {
  width: 100%;
  border: 0;
  background: transparent;
  color: var(--text);
  padding: 0;
}

.image-button img {
  display: block;
  width: 100%;
  height: auto;
  border-radius: 0.75rem;
}

.image-button span {
  display: inline-block;
  margin-top: 0.65rem;
}

dialog {
  width: min(96vw, 80rem);
  max-height: 94vh;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--surface);
  color: var(--text);
  padding: 0.75rem;
}

dialog::backdrop {
  background: rgb(0 0 0 / 0.7);
}

dialog img {
  display: block;
  max-width: 100%;
  max-height: 82vh;
  margin-inline: auto;
  object-fit: contain;
}

.dialog-close {
  display: block;
  margin: 0 0 0.75rem auto;
  border: 1px solid var(--border);
  border-radius: 0.75rem;
  background: var(--surface);
  color: var(--text);
  padding: 0.6rem 0.85rem;
}
```

- [ ] **Step 6: Run accessibility tests**

Run:

```bash
npm test -- tests/accessibility.spec.js
```

Expected: all tests PASS.

- [ ] **Step 7: Commit Task 5**

```bash
git add images js/image-dialog.js css/components.css tests/accessibility.spec.js
git commit -m "feat: add accessible infographic viewer"
```

---

### Task 6: Add Print Handouts and Verify 320 px–Tablet Responsiveness

**Files:**
- Create: `css/print.css`
- Create: `tests/print.spec.js`
- Modify: `tests/accessibility.spec.js`

**Interfaces:**
- Print output must show:
  - topic header
  - article text
  - fact note
  - infographic
  - all five questions
- Print output must hide:
  - mode selector
  - topic tabs
  - previous/next controls
  - show-all button
  - timer
  - dialog
- Mobile output must have no horizontal overflow at 320 px

- [ ] **Step 1: Write failing print and viewport tests**

Create `tests/print.spec.js`:

```js
const { test, expect } = require("@playwright/test");

test("320px layout has no horizontal overflow", async ({ page }) => {
  await page.setViewportSize({ width: 320, height: 700 });
  await page.goto("/topic-mass-tourism.html?mode=host");

  const sizes = await page.evaluate(() => ({
    scrollWidth: document.documentElement.scrollWidth,
    clientWidth: document.documentElement.clientWidth
  }));

  expect(sizes.scrollWidth).toBeLessThanOrEqual(sizes.clientWidth);
});

test("print mode shows all questions and hides interactive controls", async ({ page }) => {
  await page.goto("/topic-senior-driving.html?mode=host");
  await page.emulateMedia({ media: "print" });

  await expect(page.locator("#articlePanel")).toBeVisible();
  await expect(page.locator("#visualPanel")).toBeVisible();
  await expect(page.locator("#questionsPanel")).toBeVisible();
  await expect(page.locator("#allQuestions")).toBeVisible();
  await expect(page.locator("#topicMode")).toBeHidden();
  await expect(page.locator("#timerRoot")).toBeHidden();
  await expect(page.locator(".tab-list")).toBeHidden();
});
```

Append to `tests/accessibility.spec.js`:

```js
test("routine text is at least 16px on a 320px viewport", async ({ page }) => {
  await page.setViewportSize({ width: 320, height: 700 });
  await page.goto("/topic-senior-driving.html?mode=participant");

  const fontSize = await page.locator("#articleBody p").first().evaluate(
    element => Number.parseFloat(getComputedStyle(element).fontSize)
  );

  expect(fontSize).toBeGreaterThanOrEqual(16);
});
```

- [ ] **Step 2: Run tests and confirm print failure**

Run:

```bash
npm test -- tests/print.spec.js tests/accessibility.spec.js
```

Expected: print test FAIL because hidden panels and interactive controls are not overridden for print.

- [ ] **Step 3: Implement print styles**

Create `css/print.css`:

```css
@page {
  size: A4;
  margin: 14mm;
}

body {
  background: #ffffff;
  color: #000000;
  font-size: 11pt;
}

.site-shell {
  width: 100%;
  padding: 0;
}

.topic-nav,
.tab-list,
.question-toolbar,
.question-controls,
.timer-panel,
dialog,
.image-button span {
  display: none !important;
}

.tab-panel,
.tab-panel[hidden] {
  display: block !important;
  width: 100%;
  border: 0;
  padding: 0;
  margin-top: 1rem;
}

#questionText {
  display: none;
}

#allQuestions,
#allQuestions[hidden] {
  display: block !important;
}

.image-button {
  display: block;
}

.image-button img {
  max-height: 210mm;
  object-fit: contain;
  break-inside: avoid;
}

.fact-note,
#allQuestions li {
  break-inside: avoid;
}

a::after {
  content: " (" attr(href) ")";
  overflow-wrap: anywhere;
}
```

- [ ] **Step 4: Run print and responsiveness tests**

Run:

```bash
npm test -- tests/print.spec.js tests/accessibility.spec.js
```

Expected: all tests PASS at 320 px and under print media.

- [ ] **Step 5: Manually inspect all required widths**

Run:

```bash
npm run test:headed -- tests/home.spec.js tests/topic-content.spec.js
```

Inspect at:

- 320 × 700
- 375 × 812
- 430 × 932
- 768 × 1024
- 1024 × 768

Expected:

- no horizontal scroll
- all controls at least 44 CSS px high
- tab labels remain readable
- infographic scales to the available width
- question card uses visibly larger text than article body

- [ ] **Step 6: Commit Task 6**

```bash
git add css/print.css tests/print.spec.js tests/accessibility.spec.js
git commit -m "feat: add responsive printable handout layout"
```

---

### Task 7: Enforce Offline Safety and Produce the Offline ZIP

**Files:**
- Create: `scripts/verify-static-site.mjs`
- Create: `scripts/make-offline-zip.py`
- Create: `tests/offline.spec.js`
- Create: `README.md`

**Interfaces:**
- `npm run verify` exits `0` only when:
  - every local `src` and `href` target exists
  - no production HTML contains remote script/style/font dependencies
  - no production JavaScript contains `fetch(`, `localStorage`, `sessionStorage`, or service-worker registration
- `npm run package:offline` creates `dist/english-club-guide-offline.zip`
- ZIP root contains `index.html`, not an extra enclosing directory

- [ ] **Step 1: Write the failing offline browser test**

Create `tests/offline.spec.js`:

```js
const { test, expect } = require("@playwright/test");

test("all primary interactions work while external network requests are blocked", async ({ page }) => {
  await page.route(/^https?:\/\/(?!127\.0\.0\.1:4173)/, route => route.abort());

  await page.goto("/index.html");
  await page.locator("#homeMode").selectOption("host");
  await page.locator("#topicMassTourism").click();

  await expect(page.locator("#topicTitle")).toHaveText("Mass Tourism in Mallorca");
  await page.getByRole("button", { name: /Visual Summary/ }).click();
  await expect(page.locator("#visualImage")).toBeVisible();

  await page.getByRole("button", { name: /Questions/ }).click();
  await expect(page.locator("#questionProgress")).toHaveText("Question 1 of 5");
  await expect(page.locator("#timerRoot")).toBeVisible();
});
```

- [ ] **Step 2: Run the offline test**

Run:

```bash
npm test -- tests/offline.spec.js
```

Expected: PASS only after all prior production assets are local. If it fails, inspect the aborted request and remove that external dependency.

- [ ] **Step 3: Implement static-site verification**

Create `scripts/verify-static-site.mjs`:

```js
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const htmlFiles = [
  "index.html",
  "topic-senior-driving.html",
  "topic-mass-tourism.html"
];
const jsFiles = fs.readdirSync(path.join(root, "js"))
  .filter(name => name.endsWith(".js"))
  .map(name => path.join("js", name));

const errors = [];
const externalPattern = /(?:src|href)=["']https?:\/\//gi;
const localAssetPattern = /(?:src|href)=["'](?!#|mailto:|tel:|https?:)([^"'?]+)(?:\?[^"']*)?["']/gi;

for (const relativePath of htmlFiles) {
  const source = fs.readFileSync(path.join(root, relativePath), "utf8");

  if (externalPattern.test(source)) {
    errors.push(`${relativePath}: contains a remote production dependency`);
  }
  externalPattern.lastIndex = 0;

  for (const match of source.matchAll(localAssetPattern)) {
    const target = path.resolve(root, path.dirname(relativePath), match[1]);
    if (!fs.existsSync(target)) {
      errors.push(`${relativePath}: missing local asset ${match[1]}`);
    }
  }
}

const forbiddenJs = [
  ["fetch(", "fetch is forbidden"],
  ["localStorage", "localStorage is forbidden"],
  ["sessionStorage", "sessionStorage is forbidden"],
  ["serviceWorker.register", "service workers are out of scope"]
];

for (const relativePath of jsFiles) {
  const source = fs.readFileSync(path.join(root, relativePath), "utf8");
  for (const [needle, message] of forbiddenJs) {
    if (source.includes(needle)) {
      errors.push(`${relativePath}: ${message}`);
    }
  }
}

if (errors.length > 0) {
  console.error(errors.join("\n"));
  process.exit(1);
}

console.log("Static-site verification passed.");
```

- [ ] **Step 4: Implement deterministic offline ZIP creation**

Create `scripts/make-offline-zip.py`:

```python
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
OUTPUT = DIST / "english-club-guide-offline.zip"

INCLUDED = [
    ROOT / "index.html",
    ROOT / "topic-senior-driving.html",
    ROOT / "topic-mass-tourism.html",
    ROOT / "README.md",
    *sorted((ROOT / "css").glob("*.css")),
    *sorted((ROOT / "js").glob("*.js")),
    *sorted((ROOT / "images").glob("*.png")),
]

missing = [path for path in INCLUDED if not path.exists()]
if missing:
    raise SystemExit("Missing package files:\n" + "\n".join(map(str, missing)))

DIST.mkdir(exist_ok=True)

with ZipFile(OUTPUT, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
    for source in INCLUDED:
        archive.write(source, source.relative_to(ROOT).as_posix())

print(OUTPUT)
```

- [ ] **Step 5: Write the user README**

Create `README.md`:

```md
# English Club Interactive Discussion Guide

## Online use

Upload the repository root to GitHub and enable GitHub Pages from the main
branch root. Open `index.html` through the published Pages URL.

## Offline use

1. Download `english-club-guide-offline.zip`.
2. Extract the ZIP completely.
3. Open `index.html`.
4. Keep the `css`, `js`, and `images` folders beside the HTML files.

The discussion website does not require an internet connection. Original
news-source links require internet access and open in a separate tab.

## Modes

- Participant／參加者: article, infographic, and question navigation.
- Host／主持人: participant features plus a silent countdown timer.

## Generated images

The infographics are AI-generated illustrative summaries. They are not
official government graphics or original Reuters photographs.
```

- [ ] **Step 6: Verify and package**

Run:

```bash
npm run verify
npm run package:offline
python - <<'PY'
from pathlib import Path
from zipfile import ZipFile

zip_path = Path("dist/english-club-guide-offline.zip")
with ZipFile(zip_path) as archive:
    names = set(archive.namelist())
    assert "index.html" in names
    assert "topic-senior-driving.html" in names
    assert "topic-mass-tourism.html" in names
    assert "images/senior-driving-summary.png" in names
    assert "images/mass-tourism-article-summary.png" in names
    print(f"{zip_path}: {len(names)} files")
PY
```

Expected:

- `Static-site verification passed.`
- ZIP is created.
- ZIP inspection prints a positive file count without assertion errors.

- [ ] **Step 7: Run the full browser suite**

Run:

```bash
npm test
```

Expected: all tests PASS in mobile, tablet, and desktop projects.

- [ ] **Step 8: Commit Task 7**

```bash
git add scripts tests/offline.spec.js README.md package.json
git commit -m "build: verify and package offline discussion site"
```

---

### Task 8: Perform Final Cross-Browser and GitHub Pages Acceptance Verification

**Files:**
- Modify only if verification finds a concrete defect:
  - `README.md`
  - relevant HTML, CSS, JavaScript, or test file
- Generate: `dist/english-club-guide-offline.zip`

**Interfaces:**
- Final deliverables:
  - deployable repository root
  - `dist/english-club-guide-offline.zip`
  - passing Playwright suite
  - verified GitHub Pages URL

- [ ] **Step 1: Run all automated gates from a clean install**

Run:

```bash
rm -rf node_modules playwright-report test-results dist
npm ci
npx playwright install chromium
npm run verify
npm test
npm run package:offline
```

Expected: every command exits `0`.

- [ ] **Step 2: Test the extracted ZIP using `file://`**

Run:

```bash
rm -rf /tmp/english-club-guide-offline
mkdir -p /tmp/english-club-guide-offline
python - <<'PY'
from pathlib import Path
from zipfile import ZipFile

source = Path("dist/english-club-guide-offline.zip")
target = Path("/tmp/english-club-guide-offline")
with ZipFile(source) as archive:
    archive.extractall(target)
print((target / "index.html").resolve().as_uri())
PY
```

Open the printed `file://` URL manually in Chrome or Edge and verify:

1. Home page loads with both topic cards.
2. Host mode is retained when opening either topic.
3. Article tabs render without network.
4. Both infographics render without network.
5. All five questions can be navigated.
6. Host timer starts, pauses, resets, and expires silently.
7. Browser back returns to the home page.

- [ ] **Step 3: Test on real mobile and tablet devices**

Using the local-network URL or temporary GitHub Pages URL, test:

- Android Chrome, current stable
- iPhone Safari, current stable
- iPad Safari or Android tablet browser

Verify:

- no horizontal overflow
- tap targets are comfortable
- text does not require pinch zoom
- tabs remain visible and understandable
- the enlarged infographic can be closed
- source links open in a new tab
- timer remains readable when the screen rotates

Record any defect with device, browser version, viewport orientation, and reproduction steps before changing code.

- [ ] **Step 4: Deploy to GitHub Pages**

Repository settings:

```text
Settings
→ Pages
→ Build and deployment
→ Source: Deploy from a branch
→ Branch: main
→ Folder: /(root)
→ Save
```

After deployment, open:

```text
https://<github-username>.github.io/<repository-name>/
```

Verify the browser console contains no 404 errors for CSS, JavaScript, or images.

- [ ] **Step 5: Run the print acceptance check**

From each topic page:

1. Open browser print preview.
2. Confirm Article, Visual Summary, and all five questions appear.
3. Confirm timer, tabs, and navigation do not appear.
4. Confirm no question is split so badly that its number appears on a separate page.
5. Save one topic as PDF and inspect every page.

- [ ] **Step 6: Update README with the final Pages URL**

Add:

```md
## Published website

<final GitHub Pages URL>
```

Do not add the URL until deployment succeeds and the page is manually opened.

- [ ] **Step 7: Re-run final evidence commands**

Run:

```bash
npm run verify
npm test
npm run package:offline
git status --short
```

Expected:

- verification PASS
- all Playwright tests PASS
- ZIP regenerated successfully
- only intentionally generated or documented files appear in `git status`

- [ ] **Step 8: Commit final acceptance fixes and documentation**

```bash
git add .
git commit -m "docs: finalize English Club guide deployment"
```

If there were no changes after the previous commit, do not create an empty commit.

---

## Plan Self-Review

### Spec Coverage

- Home page and two independent topic pages: Tasks 1–2.
- Bilingual controls with English content: Tasks 1–3.
- Concise summaries and original links: Task 2.
- Participant and host modes: Tasks 1, 2, and 4.
- Magazine article, infographic, and large question cards: Tasks 2, 3, and 5.
- Five-question navigation: Task 3.
- Silent 5/10/15 minute timer: Task 4.
- Tap-to-enlarge local infographics and disclosure: Task 5.
- 320 px mobile, tablet, accessibility, and print: Tasks 5–6.
- Offline file use and GitHub Pages: Tasks 7–8.
- ZIP delivery: Task 7.
- Runtime-dependency prohibition: Task 7.
- Scope exclusions remain unimplemented: enforced by architecture and verifier.

### Placeholder Scan

The plan contains no `TBD`, `TODO`, “implement later”, unspecified error-handling step, or ungrounded test instruction.

### Interface Consistency

- `ClubMode.parse` and `ClubMode.withMode` are defined in Task 1 and consumed in Task 2.
- `ClubContent.get` and the Topic shape are defined in Task 2.
- `club:topic-ready` is emitted in Task 2 and consumed by Tasks 3–5.
- All selectors used by tests are created in the corresponding implementation task.
