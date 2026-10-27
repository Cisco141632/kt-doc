#!/usr/bin/env python3
"""Generate static pages. No runtime or build dependency is needed to read them."""
import json
from html import escape
from pathlib import Path
from course import LESSONS, COMMANDS
from questions import QUESTIONS
from practice_content import LABS

ROOT = Path(__file__).resolve().parent
assert len(LESSONS) == 23
assert len(QUESTIONS) == 60
assert len({q["id"] for q in QUESTIONS}) == len(QUESTIONS)
assert all(0 <= q["correct"] < len(q["options"]) for q in QUESTIONS)
assert all(q["topic"] in {m["id"] for m in LESSONS} for q in QUESTIONS)

for index, page in enumerate(LESSONS):
    navigation = ''.join('<li class="' + ('is-active' if m['id'] == page['id'] else '') + '"><a href="' + m['id'] + '.html"' + (' aria-current="page"' if m['id'] == page['id'] else '') + ' data-lesson="' + m['id'] + '"><span class="num">' + str(i+1) + '</span><span class="t">' + escape(m['title']) + '</span><span class="mins">' + str(m['minutes']) + 'm</span></a></li>' for i,m in enumerate(LESSONS))
    for group_index, group_title in ((0, 'Start here'), (5, 'Combine changes'), (11, 'Work with a team'), (16, 'Fix and practise'), (20, 'Review and look up')):
        target = '<li class="' + ('is-active' if LESSONS[group_index]['id'] == page['id'] else '') + '"><a href="' + LESSONS[group_index]['id'] + '.html"'
        navigation = navigation.replace(target, '<li class="nav-group">' + group_title + '</li>' + target, 1)
    content = ''.join(page['sections'])
    cards = ''.join('<a class="card" href="' + m['id'] + '.html"><span class="tag">' + str(i+1).zfill(2) + ' · ' + str(m['minutes']) + ' min</span><b>' + escape(m['title']) + '</b><small>' + escape(m['description']) + '</small></a>' for i,m in enumerate(LESSONS) if i)
    content = content.replace('<div class="cards" data-course-cards></div>', '<div class="cards" data-course-cards>' + cards + '</div>')
    if page['id'] == 'quiz':
        static = ''.join('<details class="reveal"><summary>' + escape(q['prompt']) + '</summary><div><p><b>' + escape(q['options'][q['correct']]['text']) + '</b></p><p>' + escape(q['options'][q['correct']]['why']) + '</p><a href="' + q['topic'] + '.html">Review this topic</a></div></details>' for q in QUESTIONS)
        content = content.replace('<div id="static-questions"></div>', '<div id="static-questions">' + static + '</div>')
    if page.get('topic'):
        content += '<section id="check"><h2>Try two questions</h2><div data-lesson-check="' + page['topic'] + '"></div><noscript><p>Open the <a href="quiz.html">question bank</a> for this topic.</p></noscript></section>'
    prev = '<a class="btn" href="' + LESSONS[index-1]['id'] + '.html">← Previous</a>' if index else ''
    next_link = '<a class="btn btn-primary" href="' + LESSONS[index+1]['id'] + '.html">Next: ' + escape(LESSONS[index+1]['title']) + ' →</a>' if index+1 < len(LESSONS) else '<a class="btn" href="index.html">Back to the course</a>'
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{escape(page['description'], quote=True)}">
  <meta name="color-scheme" content="light dark">
  <title>{escape(page['title'])} · Git &amp; GitHub learning path</title>
  <link rel="icon" href="assets/git.svg" type="image/svg+xml">
  <link rel="stylesheet" href="assets/style.css">
  <script src="assets/data.js" defer></script>
  <script src="assets/app.js" defer></script>
{'  <script src="assets/visuals.js" defer></script>' if page['id'] == 'playground' else ''}
{'  <script src="assets/studio.js" defer></script>' if page['id'] in ('studio','why-git') else ''}
</head>
<body data-module="{page['id']}">
<a class="skip-link" href="#main">Skip to lesson</a>
<div class="layout">
  <aside class="sidebar" id="sidebar">
    <a class="brand" href="index.html"><span class="brand-mark" aria-hidden="true">git</span><span>Git &amp; GitHub<small>Small steps. Clear examples.</small></span></a>
    <div class="toolbar"><a href="../index.html" class="meta">← All learning paths</a><button class="btn btn-small mobile-menu" aria-expanded="false" aria-controls="course-nav">Modules</button></div>
    <div class="progress"><progress id="course-meter" max="{len(LESSONS)}" value="0" aria-label="Lessons marked complete"></progress><span id="course-progress">{len(LESSONS)} modules · learn at your pace</span></div>
    <nav id="course-nav" aria-label="Course modules"><ol class="modules">{navigation}</ol></nav>
    <button class="btn btn-small theme-toggle only-js" type="button">Change theme</button>
  </aside>
  <main class="content" id="main">
    <header class="page-head {'hero' if page['id'] == 'index' else ''}">
      <p class="eyebrow">Lesson {index+1:02d} / {len(LESSONS)} · read at your own pace</p>
      <h1>{escape(page['title'])}</h1><p class="lead">{escape(page['description'])}</p>
    </header>
    <details class="word-help"><summary>Need help with HEAD, index, staging, or diff?</summary><dl><dt>Your file</dt><dd>What you are editing now. Git calls the project files the working tree.</dd><dt>Staging area = index</dt><dd>The file content you chose for the next commit. These are two names for one place.</dd><dt>HEAD</dt><dd>Tells Git which saved commit you are using, usually through your current branch.</dd><dt>Diff</dt><dd>A comparison showing added and removed lines between two versions.</dd></dl><a href="foundations.html#areas">Watch these change with one file →</a></details>
    <div class="objectives"><h2>By the end, you can…</h2><ul>{''.join('<li>' + escape(o) + '</li>' for o in page['objectives'])}</ul></div>
    {content}
    <section class="takeaways" id="remember"><h2>What to remember</h2><ul>{''.join('<li>' + escape(t) + '</li>' for t in page['recap'])}</ul></section>
    <footer class="pager">{prev}<button class="btn only-js" id="mark-done">Mark lesson complete</button>{next_link}</footer>
    <p class="source-foot">Progress stays in this browser · <a href="reference.html#sources">Official manuals and version notes</a> · <a href="recap.html#progress">Back up progress</a></p>
  </main>
</div>
</body></html>
'''
    (ROOT / (page['id'] + '.html')).write_text(html)

payload = dict(
    modules=[{k:m[k] for k in ('id','title','minutes','description')} for m in LESSONS],
    questions=QUESTIONS,
    cards=[dict(id='card'+str(i+1), topic=c[0], prompt=c[1], answer=c[2], why=c[3]) for i,c in enumerate(COMMANDS)],
    exercises=list(range(18)),
    labSteps=[lab['id']+'-'+str(i) for lab in LABS for i in range(len(lab['steps']))],
)
(ROOT/'assets'/'data.js').write_text('/* Generated by build.py. Edit course.py, questions.py or practice_content.py. */\nwindow.GIT_DATA = ' + json.dumps(payload, ensure_ascii=False, indent=2) + ';\n')
print(f"Generated {len(LESSONS)} pages, {len(QUESTIONS)} quiz questions, {len(COMMANDS)} recall cards and {len(LABS)} labs.")
