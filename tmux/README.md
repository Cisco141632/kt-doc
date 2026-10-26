# tmux learning path

An 18-module learning path integrated into the KT docs home page. It uses static HTML, CSS and JavaScript, with no package installation or runtime network dependency. Shared base styling comes from the existing Docker module.

## Read locally

Serve the repository root:

    python3 -m http.server 8765

Open http://localhost:8765/tmux/. Directly opening [index.html](index.html) also works, but browser storage behavior for file URLs varies; use the local server for consistent progress across pages.

## Included

- Installation on Linux, macOS and WSL; prefix syntax and first-session practice.
- Client/server architecture, sockets, targets, sessions, windows, panes and layouts.
- Copy mode, searches, paste buffers, OS clipboard integration and scrollback limits.
- Configuration, option scope, key tables, terminal capabilities and optional plugins.
- Development workflows, SSH recovery, collaboration, scripting and advanced features.
- 24 searchable troubleshooting cases with cause, evidence, fix and verification.
- Eight real-terminal labs with predictions, solutions, self-reported steps and cleanup.
- A visual simulator with six checked missions and free practice.
- 48 scenario questions across 12 topics, with feedback for every answer, topic filters, missed-question retry and saved attempts.
- 24 additional in-lesson practice checks using questions from the same bank.
- 42 recall cards with due dates and a searchable, printable command reference.
- Browser-local progress, export/import, dark mode, mobile navigation, keyboard support and no-JavaScript reading.

The simulator executes no shell commands. It implements the subset described on its page and rejects unsupported syntax. Real lab checkboxes record the learner's observations; the website cannot inspect the learner's terminal. tmux does not preserve live processes across host reboot.

## Content and maintenance

The generated HTML pages and assets/data.js are included so readers need no build step.

| File | Purpose |
| --- | --- |
| course.py | Lesson prose, diagrams, command reference and page definitions |
| practice_content.py | Troubleshooting cases and real-terminal labs |
| questions.py | Quiz questions and per-answer explanations |
| build.py | Generates all 18 pages and the browser data file |
| assets/app.js | Progress, quizzes, flashcards, filters, backup, theme and navigation |
| assets/simulator.js | Pure state model plus browser playground |
| assets/style.css | Course styling layered over the existing shared stylesheet |
| examples/tmux.conf | Commented optional starter config |
| examples/workspace.sh | Sequentially repeatable launcher on a named lab server |

After changing curriculum source:

    python3 tmux/build.py

Do not edit generated lesson HTML or assets/data.js directly. Authored sections, navigation, diagrams, labs, troubleshooting entries and the expandable question bank remain in the static HTML.

## Validation

Run from the repository root:

    node --test tmux/tests/model.test.cjs
    python3 tmux/tests/validate.py
    python3 tmux/tests/validate.py --tmux
    node tmux/tests/browser.mjs

The optional tmux checks require an installed tmux executable. They use a unique disposable socket and clean up only their own server. They cover the actual starter config, pane operations, buffers, targeted session cleanup and sequential workspace creation. The launcher test verifies detached setup and reuse; its final interactive attach intentionally lacks a TTY in that check.

Browser tests require Node 22+ and local Chromium; pass its path as a final argument if it is not named chromium. They start and stop their own temporary HTTP server and browser profile, without installing dependencies. Checks cover all pages at desktop and mobile widths, all six missions, keyboard prefix input, quiz behavior, filters, progress, validated imports, flashcards, malformed/blocked storage and reading without JavaScript. Screenshots are written to the system temporary directory.

Verified on tmux 3.4 and Chromium 156. Remote SSH, platform-specific clipboard tools and third-party plugins require the learner's actual environment and are not claimed as executed here.

## Sources and versions

Core lessons target established tmux 3.2+ behavior. Newer optional features are labeled, and the installed manual and active bindings remain the authority for each environment. Documentation was reviewed in October 2026; primary sources are linked on [the reference page](reference.html#sources).

Learning data is stored under tmux-learning-v1; the theme uses tmux-learning-theme. No accounts, analytics or external scripts are used. Export a backup before clearing browser storage. Import validates the format and retains only recognized lesson, question, card, mission and lab identifiers.
