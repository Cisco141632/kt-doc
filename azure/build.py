#!/usr/bin/env python3
"""Generate the dependency-free Azure Storage course. Run from any directory."""
import json
import re
from html import escape
from pathlib import Path
from course import LESSONS, GLOSSARY, SOURCES
from questions import QUESTIONS
from supplements import LABS, supplements

ROOT = Path(__file__).resolve().parent


def build():
    lesson_ids = {m['id'] for m in LESSONS}
    assert len(LESSONS) == 11 and len(lesson_ids) == 11
    assert len({q['id'] for q in QUESTIONS}) == len(QUESTIONS) >= 32
    assert all(q['topic'] in lesson_ids and 0 <= q['correct'] < len(q['options']) for q in QUESTIONS)
    index, practice, glossary, quiz, reference = supplements(LESSONS, GLOSSARY, SOURCES, QUESTIONS)
    pages = [index, *LESSONS, practice, quiz, glossary, reference]
    assert len({p['id'] for p in pages}) == len(pages) == 16
    (ROOT / 'assets').mkdir(exist_ok=True)
    for position, page in enumerate(pages):
        id = page['id']
        nav = []
        for i, other in enumerate(pages):
            number = f'{i:02d}' if other['id'] in lesson_ids else ('↗' if i else '◉')
            active = other['id'] == id
            nav.append(f'<li class="{"is-active" if active else ""}" data-nav-item="{other["id"]}"><a href="{other["id"]}.html" {"aria-current=page" if active else ""}><span class="num">{number}</span><span class="t">{escape(other["title"].replace(chr(10), " "))}</span><span class="mins">{other["minutes"]}m</span></a></li>')
        content = ''.join(page['sections'])
        if id in lesson_ids:
            content += f'<section class="lesson-section" id="check"><h2>Check what you understand</h2><div data-lesson-check="{id}"></div><noscript><p>Try this topic in the <a href="quiz.html#question-bank">readable question bank</a>.</p></noscript></section>'
        toc = re.findall(r'<section\b[^>]*\bid="([^"]+)"[^>]*>\s*<h2>(.*?)</h2>', content, re.S)
        toc_html = '<nav class="page-toc" aria-label="On this page"><strong>On this page</strong>' + ''.join(f'<a href="#{anchor}">{re.sub("<[^>]+>", "", title)}</a>' for anchor, title in toc) + '</nav>'
        hero_visual = '''<div class="hero-visual" aria-label="One account contains a container, which contains a PDF and its extracted text"><div class="storage-diagram"><div class="storage-building"><span class="hero-pill">AZURE STORAGE ACCOUNT</span><strong>One place for your files</strong><div class="storage-container"><span>CONTAINER / private-files</span><div class="storage-blob"><span aria-hidden="true">▤</span><div><b>complaint.pdf</b><small>The original upload</small></div></div><div class="storage-blob"><span aria-hidden="true">≡</span><div><b>complaint_pages_1-3.md</b><small>The AI's extracted text</small></div></div></div><p class="muted">Account + container + key = one blob</p></div></div></div>'''
        heading = f'<div><p class="eyebrow">{"Start here · learn at your pace" if id == "index" else ("Lesson " + str(position).zfill(2) + " / 11 · " + str(page["minutes"]) + " min" if id in lesson_ids else "Your learning toolkit · " + str(page["minutes"]) + " min")}</p><h1>{escape(page["title"]).replace(chr(10), "<br>")}</h1><p class="lead">{escape(page["description"])}</p></div>'
        header = '<header class="page-head' + (' hero"' if id == 'index' else '"') + '>' + ('<div class="hero-grid">' + heading + hero_visual + '</div>' if id == 'index' else heading) + '</header>'
        objectives = '<div class="objectives"><h2>By the end, you can…</h2><ul>' + ''.join('<li>' + escape(o) + '</li>' for o in page['objectives']) + '</ul></div>' if page['objectives'] else ''
        recap = '<section class="takeaways" id="remember"><h2>Remember in 30 seconds</h2><ul>' + ''.join('<li>' + escape(r) + '</li>' for r in page['recap']) + '</ul></section>' if page['recap'] else ''
        previous = f'<a class="btn" href="{pages[position-1]["id"]}.html">← Previous</a>' if position else ''
        following = f'<a class="btn btn-primary" href="{pages[position+1]["id"]}.html">Next: {escape(pages[position+1]["title"].replace(chr(10), " "))} →</a>' if position + 1 < len(pages) else '<a class="btn" href="index.html">Back to the course →</a>'
        done = '<button class="btn only-js" type="button" id="mark-done" aria-pressed="false">Mark lesson complete</button>' if id in lesson_ids else ''
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{escape(page['description'], quote=True)}">
  <meta name="color-scheme" content="light dark">
  <title>{escape(page['title'].replace(chr(10), ' '))} · Azure Storage learning path</title>
  <link rel="icon" href="assets/storage.svg" type="image/svg+xml">
  <link rel="stylesheet" href="assets/style.css">
  <script src="assets/data.js" defer></script>
  <script src="assets/model.js" defer></script>
  <script src="assets/labs.js" defer></script>
  <script src="assets/app.js" defer></script>
</head>
<body data-module="{id}">
<a class="skip-link" href="#main">Skip to lesson</a>
<div class="layout">
  <aside class="sidebar" id="sidebar">
    <a class="brand" href="index.html"><span class="brand-mark"><img src="assets/storage.svg" width="36" height="36" alt=""></span><span>Azure Storage<small>From one file to the full picture</small></span></a>
    <div class="toolbar"><a class="meta" href="../index.html">← All learning paths</a><button class="btn btn-small mobile-menu only-js" type="button" id="menu-toggle" aria-expanded="false" aria-controls="course-nav">Course menu</button></div>
    <div class="progress"><progress id="course-meter" max="11" value="0" aria-label="Lessons complete"></progress><span id="course-progress">11 lessons · learn at your pace</span></div>
    <nav id="course-nav" aria-label="Course navigation"><label class="field only-js" for="nav-search">Find a lesson<input class="search-nav" type="search" id="nav-search" placeholder="Search lessons…"></label><ol class="modules">{''.join(nav)}</ol><p id="nav-empty" class="muted" hidden>No matching lessons.</p></nav>
    <button class="btn btn-small theme-toggle only-js" type="button" aria-label="Switch color theme">Change theme</button>
    <p class="meta sidebar-note">Read → see → predict → try → explain</p>
  </aside>
  <main class="content" id="main">
    {header}
    <p id="storage-status" class="muted" role="status" hidden></p>
    {toc_html}
    {objectives}
    {content}
    {recap}
    <footer class="pager">{previous}{done}{following}</footer>
    <p class="source-foot">Azure Storage learning path · CrimeOS guide snapshot: 2026-11-06 · <a href="reference.html#sources">Sources</a> · <a href="reference.html#progress">Manage progress</a> · Simulations run in your browser.</p>
  </main>
</div>
</body>
</html>
'''
        html = '\n'.join(line.rstrip() for line in html.splitlines()) + '\n'
        (ROOT / (id + '.html')).write_text(html, encoding='utf-8')
    data = dict(version=1, modules=[{k: m[k] for k in ('id', 'title', 'minutes', 'description')} for m in pages],
                lessonIds=[m['id'] for m in LESSONS], questions=QUESTIONS, labIds=[x[0] for x in LABS])
    (ROOT / 'assets/data.js').write_text('/* Generated by azure/build.py. Edit the Python curriculum sources. */\nwindow.AZURE_DATA = ' + json.dumps(data, ensure_ascii=False, indent=2) + ';\n', encoding='utf-8')
    print(f'Generated {len(pages)} pages, {len(LESSONS)} lessons, {len(LABS)} lab mounts and {len(QUESTIONS)} questions.')


if __name__ == '__main__':
    build()
