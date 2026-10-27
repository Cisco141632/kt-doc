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

- 23 modules starting with a school-project introduction for learners with no
  coding knowledge, then covering setup, everyday workflow, ancestry, remotes, merge,
  conflicts, rebase, force pushes, recovery, history investigation, collaboration,
  permissions, rules, automation, advanced tools, practice and recap.
- Plain-English lessons with one action, its purpose, and the result to check.
  HEAD, index, staging, and diff use one text file throughout the explanation.
  Step controls show exactly which file content changes after each action.
- Before/after pictures, deeper explanations of Git storage and commit links,
  and problem tables with checks, fixes, and final verification.
- Eight commit-graph stories with step controls.
- Three scored visual exercises: conflict resolution, concurrent push decisions,
  and a deliberately simplified permission/rules model.
- A first-lesson save/mistake/recovery model, illustrated Git-versus-GitHub
  explanation, and six expandable vocabulary cards before commands.
- A five-station Practice Studio: three snapshot challenges, six branch-pointer
  predictions, three guided incidents, eight intention/command matches, and
  five-question recall rounds that prioritise previously missed questions.
  These contribute 14 studio goals; together with the beginner model and original
  exercises, 18 practice goals can be completed.
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

- course.py: lesson order and the start page
- core_lessons.py: the 14 main Git and GitHub lessons
- lesson_parts.py: shared markup for small steps, before/after pictures, and controls
- support_content.py: problem-solving, real labs, visual tools, quiz, and review pages
- reference_content.py: the command reference, word list, and review-card text
- beginner_content.py and studio_content.py: the illustrated introduction and
  practice-station reading companions
- practice_content.py: incidents and real-lab instructions
- questions.py: quiz questions and explanations
- build.py: static page template and data generator
- assets/app.js: shared learning interactions
- assets/visuals.js: pure exercise models and browser controls
- assets/studio.js: beginner model, snapshot transitions, graph predictions,
  guided decisions, command matching and recall-round selection
- examples/create-labs.py: isolated repository fixture builder

Regenerate from the repository root:

    python3 git/build.py

The stylesheet reuses the tmux/Docker layout with a Git-only blue reading theme,
clearer spacing, and matching light/dark colors. Sibling themes are unchanged.
Keep those sibling folders when moving or serving this module. All assets are
local; no CDN, analytics, font service or third-party script is required.

Progress uses the separate localStorage key git-learning-v1; theme uses
git-learning-theme. It does not modify other learning paths' progress. Storage
can be denied or cleared by the browser, so export a backup for durable records.
Lab checkboxes record the learner's observations, not automatic repository checks.
Studio recall results are separate from the full quiz. The optional studioRecall
field extends the existing version-1 export: older exports still import, and valid
existing lesson/quiz/lab/card records are preserved. Only the most recent
correct/incorrect result per studio question is retained; there is no countdown
or penalty for practising again.

## Create the real labs

Requires Python 3 and Git 2.28+:

    python3 git/examples/create-labs.py /tmp/git-learning-first-run

Choose a new path. Existing destinations are refused. Open practice.html for
the deliberate conflict/failure points, editing steps and expected outcomes.
Examples use a POSIX shell; Windows learners can use Git Bash or WSL.

## Validation

From the repository root:

    python3 git/tests/validate.py
    node --test git/tests/visuals.test.cjs git/tests/studio.test.cjs
    python3 git/tests/labs.py
    node git/tests/browser.mjs

The first check validates local links, anchors, page IDs and content counts.
The model tests cover graph ancestry, resolution requirements, lease races
and permission gates, plus snapshot state transitions, recorded recovery,
pointer ancestry, incident decisions and weak-question recall ordering.
The Git tests execute all twelve labs inside a temporary
directory, including both rejected and accepted lease outcomes against local
remotes; the directory is cleaned afterward.

The browser check requires Node 22+ and Chromium (an optional executable path
can be passed as its argument). It starts its own temporary local server and
browser profile, checks all 23 pages at desktop and 390px mobile widths,
exercises every quiz answer and the visual tools, and verifies no-JavaScript
reading plus denied/malformed storage recovery. It also checks progress imports,
recall scheduling, filtering, persistence, every studio goal, wrong-answer paths,
optional drag input, keyboard activation, and independent studio/full-quiz scores.
It also checks every new step control, including first/last boundaries, restart,
and the full six-step file example without JavaScript.
Screenshots are saved under /tmp/kt-git-*.png, including beginner and studio
desktop/mobile views.
The test closes its owned server and browser when finished.

Validated on Git 2.43.0, Python 3.12, Node 24 and Chromium 156.
References were reviewed in October 2026. GitHub settings and permission models
vary by plan, visibility, organization policy and Enterprise version.
The course links to the current primary documentation for those boundaries.

The browser models do not execute Git or check real GitHub authorization.
This module does not apply GitHub rules, grant access, or configure workflows.
It provides a broad practical curriculum; the linked manuals cover additional
command flags, plumbing details and platform-specific features.
