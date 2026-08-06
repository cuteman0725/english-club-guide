# English Club Interactive Discussion Guide — Design Specification

Date: 2026-08-06

## 1. Goal

Build a mobile- and tablet-first interactive website for an English club meeting. Participants should be able to switch between two topics, read a concise article summary, view a visual summary, and browse discussion questions. The same site must work online through GitHub Pages and offline after downloading the site files.

## 2. Confirmed Product Decisions

- Delivery:
  - Online via GitHub Pages
  - Offline as a downloadable ZIP
- Information architecture:
  - Home page
  - One independent page for each topic
- Interface language:
  - Bilingual navigation and controls
  - Article summaries and discussion questions remain in English
- Article presentation:
  - Concise English summary
  - Original source link
- User modes:
  - Participant mode
  - Host mode
- Visual style:
  - Magazine-style article layout
  - Infographic visual-summary section
  - Large question cards
- Host tools:
  - One question at a time
  - Previous and Next controls
  - Show-all option
  - 5, 10, or 15 minute countdown
  - Start, pause, and reset
  - Silent “Time is up” alert

## 3. Site Structure

```text
english-club-guide/
├─ index.html
├─ topic-senior-driving.html
├─ topic-mass-tourism.html
├─ css/
│  └─ styles.css
├─ js/
│  ├─ app.js
│  └─ timer.js
├─ images/
│  ├─ senior-driving-summary.png
│  ├─ mass-tourism-article-summary.png
│  └─ mass-tourism-questions.png
└─ README.md
```

## 4. Home Page

The home page displays:

- English Club title
- Mode selector:
  - Participant／參加者
  - Host／主持人
- Two topic cards:
  - Session I: Senior Driver License Renewal in Taiwan
  - Session II: Mass Tourism in Mallorca

Selecting a topic opens its independent topic page while retaining the selected mode in the URL.

Example:

```text
topic-senior-driving.html?mode=participant
topic-mass-tourism.html?mode=host
```

## 5. Topic Page Layout

Each topic page contains three main tabs:

1. Article／文章
2. Visual Summary／圖解
3. Questions／問題

A persistent navigation area provides:

- Home／首頁
- Topic title
- Current mode
- Mode switcher

## 6. Article Section

Each article section includes:

- Topic title
- Concise English summary
- Important factual clarification
- Original source button
- Readable paragraph width and spacing for mobile devices

### Session I

Focus:

- Taiwan lowers the senior-driver renewal threshold from age 75 to age 70
- Requirements for ages 70–74
- Additional requirements for ages 75 and older
- Clarification that the policy does not automatically require a new road test

Source:

- Taiwan Directorate General of Highways

### Session II

Focus:

- Mallorca residents protested mass tourism
- Cultural and environmental concerns
- Wider pressures involving housing, transportation, public services, and natural resources
- Tourism’s economic benefits and the conflict over who bears its costs

Source:

- Reuters video report
- Supporting Reuters background reporting where needed

## 7. Visual Summary Section

- Displays the generated infographic for the current topic
- Supports tap or click to enlarge
- Includes a short disclosure that generated visuals are illustrative summaries, not original Reuters photographs
- Works without a network connection

## 8. Questions Section

### Participant Mode

- One question shown at a time
- Previous／上一題
- Next／下一題
- Show all／全部顯示
- Current position shown as “Question 2 of 5”

### Host Mode

Includes all participant controls plus:

- Large question text
- 5, 10, or 15 minute timer
- Start／開始
- Pause／暫停
- Reset／重設
- Silent “Time is up／時間到” notice

The timer runs only in the current browser and does not synchronize between users.

## 9. Responsive Behaviour

### Mobile

- Single-column layout
- Large tap targets
- Body text at least 16 px
- Question text larger than article text
- No horizontal scrolling

### Tablet

- Wider reading column
- Question and timer controls may sit side by side where space allows

### Print

- Clean white background
- Navigation and timer controls hidden
- Article and all questions printed in sequence
- Infographic scaled to fit the page

## 10. Accessibility

- Semantic buttons and headings
- Visible focus states
- Sufficient text contrast
- Alt text for every infographic
- ARIA live region for timer status and question changes
- No important interaction dependent on colour alone

## 11. Offline and Deployment Requirements

- No server-side code
- No database
- No remote JavaScript dependency
- All CSS, JavaScript, images, and content stored locally
- Site works by opening `index.html` after ZIP extraction
- Same folder can be uploaded directly to GitHub Pages

## 12. Scope Exclusions

The first version will not include:

- Real-time synchronization between host and participants
- Login or member accounts
- Online voting
- Comments or chat
- Analytics
- Content-management backend
- Push notifications
- PWA installation

These can be considered in a later version if the basic meeting workflow proves useful.

## 13. Acceptance Criteria

The implementation is accepted when:

1. Both topics can be opened from the home page.
2. Mode selection is retained when moving between pages.
3. Each topic provides Article, Visual Summary, and Questions sections.
4. All five questions are available for each topic.
5. Host mode provides a working silent countdown timer.
6. The layout works at widths from 320 px upward.
7. The site is usable on Android Chrome, iPhone Safari, and tablets.
8. Printing produces a readable article-and-questions handout.
9. The site works offline after extracting the ZIP.
10. The same files deploy successfully on GitHub Pages.

## 14. Verification Plan

- Manual mobile test at 320 px, 375 px, and 430 px widths
- Tablet test at 768 px and 1024 px widths
- Keyboard navigation test
- Timer start, pause, reset, and expiry test
- Offline test with network disabled
- Print-preview test
- GitHub Pages deployment smoke test
- Link verification for both original sources
