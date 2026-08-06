# English Club Interactive Discussion Guide

A bilingual, mobile-first discussion guide for two English Club sessions:

1. Senior Driver License Renewal in Taiwan
2. Mass Tourism in Mallorca

The article summaries and discussion questions are in English. Navigation and controls are bilingual.

## Online use with GitHub Pages

1. Upload the repository contents to GitHub.
2. Open **Settings → Pages**.
3. Select **Deploy from a branch**.
4. Select the `main` branch and `/(root)` folder.
5. Open the published GitHub Pages URL.

## Offline use

1. Download `english-club-guide-offline.zip`.
2. Extract the ZIP completely.
3. Open `index.html`.
4. Keep the `css`, `js`, and `images` folders beside the HTML files.

The discussion website itself does not require an internet connection. Original news-source links require internet access and open in a separate tab.

## Modes

- **Participant／參加者:** article, infographic, and question navigation.
- **Host／主持人:** participant features plus a silent 5, 10, or 15 minute countdown timer.

## Printing

Use the browser’s print command from either topic page. The print layout includes the article, infographic, and all five questions while hiding navigation and timer controls.

## Generated images

The infographics are AI-generated illustrative summaries. They are not official government graphics or original Reuters photographs.

## Development verification

The production site has no runtime package dependency. In the provided development environment, run:

```bash
python scripts/verify_static_site.py
pytest
python scripts/make_offline_zip.py
```
