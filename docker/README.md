# Docker learning path

A static, plain-language Docker course: nine pages of lessons, interactive diagrams, a practice lab that checks typed commands, and quizzes. No build step and no server code.

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

| File | Module |
| --- | --- |
| `index.html` | 1. What is Docker? |
| `commands.html` | 2. Everyday commands |
| `dockerfile.html` | 3. Build your own image |
| `storage-network.html` | 4. Data & networking |
| `compose.html` | 5. Docker Compose |
| `real-world.html` | 6. Real-world issues |
| `practice.html` | 7. Practice lab |
| `quiz.html` | 8. Quiz |
| `cheatsheet.html` | 9. Cheat sheet |

## How it is put together

| File | What it holds |
| --- | --- |
| `assets/style.css` | All styling, light and dark theme |
| `assets/app.js` | Navigation (the `MODULES` list), theme, copy buttons, Mermaid, steppers, tabs |
| `assets/widgets.js` | The three interactive diagrams: container lifecycle, build cache, port mapping |
| `assets/exercises.js` | The exercise bank (type the command, fill in the blank, scenario) |
| `assets/practice.js` | Renders the exercises and checks the answers |
| `assets/quiz.js` | The quiz questions and the quiz screen |
| `examples/hello-docker/` | The sample app used in modules 3 to 5 |

## Change or extend it

- **Add a page:** copy an existing page, set `<body data-module="my-id">`, and add one line to `MODULES` in `assets/app.js`. The sidebar, the page number and the previous/next buttons follow from that list.
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
