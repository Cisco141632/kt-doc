# Docker learning path

A static, plain-language Docker course: thirteen pages of lessons, interactive diagrams, a practice lab that checks typed commands, and quizzes. No build step and no server code.

Live site (GitHub Pages): https://cisco141632.github.io/kt-doc/docker/

## Read it locally

Open `index.html` in a browser, or serve the folder:

```sh
cd docker
python3 -m http.server 8765
# then open http://localhost:8765
```

Diagrams are drawn with Mermaid, which is loaded from a CDN, so they need an internet connection. Everything else works offline.

## Pages

In reading order. The order, the numbering in the sidebar and the previous/next buttons all come from the `MODULES` list in `assets/app.js`.

| File | Module |
| --- | --- |
| `index.html` | What is Docker? |
| `visual-tour.html` | Visual Docker journey |
| `commands.html` | Everyday commands |
| `dockerfile.html` | Build your own image |
| `rebuild.html` | Change, build, run |
| `storage-network.html` | Data & networking |
| `compose.html` | Docker Compose |
| `pipeline.html` | From laptop to production |
| `real-world.html` | Real-world issues |
| `interview.html` | Interview questions & best practices |
| `practice.html` | Practice lab |
| `quiz.html` | Quiz |
| `cheatsheet.html` | Cheat sheet |

## How it is put together

| File | What it holds |
| --- | --- |
| `assets/style.css` | All styling, light and dark theme |
| `assets/app.js` | Navigation (the `MODULES` list), theme, copy buttons, Mermaid, steppers, tabs |
| `assets/widgets.js` | The interactive diagrams: container lifecycle, build cache, volume lifecycle, bind mounts, request routing, port mapping, code/image/container |
| `assets/visual-tour.js` | The visual lifecycle walkthrough and live `docker run` command builder |
| `assets/interview.js` | Filterable interview question bank, mock-question picker and confidence tracking |
| `assets/exercises.js` | The exercise bank (type the command, fill in the blank, scenario) |
| `assets/practice.js` | Renders the exercises and checks the answers |
| `assets/quiz.js` | The quiz questions and the quiz screen |
| `examples/hello-docker/` | The sample app used from "Build your own image" onwards |

## Change or extend it

- **Add a page:** copy an existing page, set `<body data-module="my-id">`, and add one line to `MODULES` in `assets/app.js`. Do not write module numbers in the text; refer to other pages by name, so nothing has to be renumbered.
- **Add an exercise:** add an object to `assets/exercises.js`. The comment at the top of that file explains the three kinds. An exercise appears on its module page and in the practice lab.
- **Add a quiz question:** add an object to a test in `assets/quiz.js`. The first option is the correct one; options are shuffled when shown.
- **Add a diagram:** put Mermaid text inside `<pre class="mermaid">`. Write `<br/>` as `&lt;br/&gt;`.

## Run the sample app

```sh
cd docker/examples/hello-docker
cp .env.example .env
docker compose up -d
curl http://localhost:8000
docker compose down
```
