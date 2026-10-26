# Git & GitHub learning path

Open [index.html](index.html), or follow the Git & GitHub card on the repository's
main learning-path page. These are static documents: no package installation,
API keys, account access or application backend is required.

For a consistent local browser origin, serve the **repository root**:

    python3 -m http.server 8000 --bind 127.0.0.1

Then open http://127.0.0.1:8000/git/.
Core lessons, commands, navigation and the readable question bank work without
JavaScript. JavaScript adds the exercises, filters, recall cards and local progress.

## Included

- 21 modules covering setup, everyday workflow, ancestry, remotes, merge,
  conflicts, rebase, force pushes, recovery, history investigation, collaboration,
  permissions, rules, automation, advanced tools, practice and recap.
- Eight commit-graph stories with step controls.
- Three scored visual exercises: conflict resolution, concurrent push decisions,
  and a deliberately simplified permission/rules model.
- 60 questions across 15 topics, with explanations for every answer choice,
  topic filters, missed-answer retries and lesson-level checks.
- 48 recall cards, review scheduling and a searchable command reference.
- 30 searchable development incidents with evidence, resolution and verification.
- 12 real Git labs created in fresh local directories, including a local bare
  remote and Alice/Bob clones. No network remote or credential is needed.
- An adaptable team policy worksheet and primary Git/GitHub references.
- Responsive layouts, keyboard controls, light/dark themes, print support,
  and browser-local progress export/import.

## Content and regeneration

Edit the authored sources rather than the generated HTML/data:

- course.py: lessons, diagrams, reference commands and page markup
- practice_content.py: incidents and real-lab instructions
- questions.py: quiz questions and explanations
- build.py: static page template and data generator
- assets/app.js: shared learning interactions
- assets/visuals.js: pure exercise models and browser controls
- examples/create-labs.py: isolated repository fixture builder

Regenerate from the repository root:

    python3 git/build.py

The stylesheet intentionally reuses the existing tmux/Docker style foundation.
Keep those sibling folders when moving or serving this module. All assets are
local; no CDN, analytics, font service or third-party script is required.

Progress uses the separate localStorage key git-learning-v1; theme uses
git-learning-theme. It does not modify other learning paths' progress. Storage
can be denied or cleared by the browser, so export a backup for durable records.
Lab checkboxes record the learner's observations, not automatic repository checks.

## Create the real labs

Requires Python 3 and Git 2.28+:

    python3 git/examples/create-labs.py /tmp/git-learning-first-run

Choose a new path. Existing destinations are refused. Open practice.html for
the deliberate conflict/failure points, editing steps and expected outcomes.
Examples use a POSIX shell; Windows learners can use Git Bash or WSL.

## Validation

From the repository root:

    python3 git/tests/validate.py
    node --test git/tests/visuals.test.cjs
    python3 git/tests/labs.py
    node git/tests/browser.mjs

The first check validates local links, anchors, page IDs and content counts.
The model tests cover graph ancestry, resolution requirements, lease races
and permission gates. The Git tests execute all twelve labs inside a temporary
directory, including both rejected and accepted lease outcomes against local
remotes; the directory is cleaned afterward.

The browser check requires Node 22+ and Chromium (an optional executable path
can be passed as its argument). It starts its own temporary local server and
browser profile, checks all 21 pages at desktop and 390px mobile widths,
exercises every quiz answer and the visual tools, and verifies no-JavaScript
reading plus denied/malformed storage recovery. It also checks progress imports,
recall scheduling, filtering, persistence and keyboard activation.
Screenshots are saved under /tmp/kt-git-{desktop,playground,mobile}.png.
The test closes its owned server and browser when finished.

Validated on Git 2.43.0, Python 3.12, Node 24 and Chromium 156.
References were reviewed in October 2026. GitHub settings and permission models
vary by plan, visibility, organization policy and Enterprise version.
The course links to the current primary documentation for those boundaries.

The browser models do not execute Git or check real GitHub authorization.
This module does not apply GitHub rules, grant access, or configure workflows.
It provides a broad practical curriculum; the linked manuals cover additional
command flags, plumbing details and platform-specific features.
