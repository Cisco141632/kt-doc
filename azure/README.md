# Azure Storage and CrimeOS learning path

An interactive, dependency-free course integrated into the KT docs homepage. All twelve parts and the glossary of the supplied `azure-storage-learning-guide.html` are represented in sixteen pages: eleven lessons, 41 explained scenario questions, seven browser labs, 40 glossary terms and a reference.

Serve the repository root with `python3 -m http.server 8765`, then open **http://localhost:8765/azure/**. Generated HTML is included; readers do not need Python, Node, an Azure account or a build step. Direct file viewing supports reading; serving locally gives consistent browser storage across pages.

The course covers accounts, containers, blob names, virtual folders, authorization, customer ownership, routed keys, saved versus built paths, storage grants, the PDF lifecycle, migrations, safe implementation, debugging and the code map. It distinguishes Azure concepts from the November 6, 2026 CrimeOS guide snapshot. It does not claim to audit current application branches. Azure facts link to official documentation. The course is focused on Blob Storage and this guide; other Azure Storage services and operational topics are linked as further study.

The labs simulate storage identity, SAS permissions and expiry, key routing, path behavior, PDF processing, migration and debugging. They use fictional data, make no cloud calls, generate no usable credentials and execute no database queries. Lab completion records an explored milestone, not proof of live Azure proficiency.

## Maintenance

| File | Purpose |
| --- | --- |
| `course.py` | Eleven authored lessons, glossary and primary source list |
| `questions.py` | Scenario questions and per-option explanations |
| `supplements.py` | Course home, practice hub, glossary, assessment and reference |
| `build.py` | Generates the sixteen shipped HTML pages and `assets/data.js` |
| `assets/model.js` | Pure, tested simulation rules |
| `assets/labs.js` | Interactive controls and lab visualizations |
| `assets/app.js` | Progress, quiz, theme, navigation, search and backups |
| `assets/style.css` | Responsive course styles, dark mode and print layout |

After editing curriculum sources, run `python3 azure/build.py`. Do not edit generated HTML or `assets/data.js` directly.

## Validation

Run from the repository root:

```sh
python3 azure/build.py
python3 azure/tests/validate.py
node --test azure/tests/model.test.cjs
node azure/tests/browser.mjs
```

Browser checks use Node 22+ and an existing Chromium executable; supply its path as the final argument if needed. They start their own temporary server and browser profile and clean up both. Screenshots go to the system temporary directory. No dependencies are installed.

Learning records use `azure-storage-learning-v1`; the theme uses `azure-storage-learning-theme`. Browser-local progress can be exported, imported or reset from the reference page. Imports validate the course/version and retain only recognized identifiers and valid answer indices. Reading still works without JavaScript; interactive labs and saved progress require it. Export before clearing browser data.
