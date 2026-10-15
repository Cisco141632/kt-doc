# CI/CD learning path

A static, plain-language CI/CD course with twelve HTML modules, diagrams, current workflow examples, a hands-on Docker pipeline, a scenario quiz and a printable cheat sheet. It has no build step or server-side code.

## Read it locally

Open `index.html`, or serve the repository root:

```sh
python3 -m http.server 8765
# open http://localhost:8765/cicd/
```

Mermaid diagrams load from a CDN. Every lesson and code example remains readable if the diagram library is unavailable.

## Pages

| File | Module |
| --- | --- |
| `index.html` | What is CI/CD? |
| `foundations.html` | Pipeline foundations |
| `continuous-integration.html` | Continuous integration |
| `docker-artifacts.html` | Docker and artifacts |
| `delivery-environments.html` | Delivery and environments |
| `deployment-strategies.html` | Deployment strategies |
| `security.html` | Pipeline security |
| `iac-gitops.html` | Infrastructure as Code, Kubernetes and GitOps |
| `observability.html` | Observe and improve |
| `practice.html` | Hands-on GitHub Actions and Docker pipeline |
| `quiz.html` | Knowledge check |
| `cheatsheet.html` | Cheat sheet |

Navigation, progress, dark mode, code-copy buttons, diagrams and steppers are implemented in `assets/app.js`. Quiz behavior and questions are in `assets/quiz.js`. Shared responsive styles come from the Docker course so the two learning paths stay visually consistent.

## Sources and currency

The workflow examples were checked against the official GitHub Actions, Docker and Kubernetes documentation in October 2026. Third-party actions are shown with major-version tags for readability; production teams should pin them to full commit SHAs and use an automated updater.
