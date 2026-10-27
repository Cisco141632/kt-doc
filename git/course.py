"""Plain-English course. Run python3 git/build.py to make the pages."""
from lesson_parts import section, table, note, flow, compare, filebox
from reference_content import COMMANDS
LESSONS = []


def lesson(id, title, minutes, description, objectives, sections, recap, topic=None):
    LESSONS.append(dict(id=id, title=title, minutes=minutes, description=description,
                        objectives=objectives, sections=sections, recap=recap, topic=topic))


lesson('index', 'Learn Git and GitHub, step by step', 10,
  'Start with one file. See what each command changes, learn how Git keeps your work, and practise fixing mistakes.',
  ['Know where to start, even if you have never used Git.', 'Learn with one small example at a time.', 'Find the lesson and fix you need when something goes wrong.'], [
  section('why', 'Understand what just happened',
    '<p>You save a file, change it, and wish you could get the earlier version back. A friend changes another part of the project. You need a way to keep useful versions, compare changes, and combine your work.</p>' +
    compare(filebox('Without a clear history', 'notes-final.txt\nnotes-final-2.txt\nWhich one had the right change?'), 'Save useful versions with Git', filebox('With Git', 'A · Write the first note\nB · Add a title\nC · Fix the date\nRead or compare each saved version.')) +
    '<p><b>Git</b> keeps the versions you choose to save on your computer. <b>GitHub</b> is a website where people share Git projects, discuss changes, and review work. You can learn local Git before creating a GitHub account.</p><div class="actions"><a class="btn btn-primary" href="why-git.html">Start with a simple story →</a><a class="btn" href="foundations.html">Explain HEAD, staging, and diff</a></div>'),
  section('routes', 'Learn in this order',
    '<div class="learning-route"><a href="why-git.html"><span>01</span><b>Understand the idea</b><small>Why save versions? What is GitHub?</small></a><a href="foundations.html"><span>02</span><b>Follow one file</b><small>Your file → chosen content → commit</small></a><a href="branches-remotes.html"><span>03</span><b>Share and combine</b><small>Branches, GitHub, merge, and conflicts</small></a><a href="undo-recovery.html"><span>04</span><b>Fix and explain</b><small>Undo mistakes and find the cause</small></a></div><p>Stop after a step, predict the next result, then check it. Reading-time labels are rough guides; real practice takes longer.</p>' +
    table(['What you need now', 'Start here'], [
      ['HEAD, index, staging, or diff is confusing.', '<a href="foundations.html#areas">Watch one file change in three places.</a>'],
      ['I want to try commands with buttons first.', '<a href="studio.html#snapshots">Open the file and staging exercise.</a>'],
      ['Git printed an error.', '<a href="troubleshooting.html">Find the message and follow the checks.</a>'],
      ['I want to understand a merge or rebase.', '<a href="playground.html">Step through the history pictures.</a>'],
      ['I am ready to use real Git.', '<a href="practice.html">Create new practice folders and try 12 labs.</a>']
    ])),
  section('scope', 'How to use a lesson',
    flow([('Start with a problem', 'Why would I need this?'), ('Learn the needed words', 'Meaning + example'), ('Try one step', 'Action + expected result'), ('Look inside', 'How Git makes the result'), ('Fix a problem', 'Check, correct, verify')]) +
    '<p>Examples use a Linux or macOS shell; Windows learners can use Git Bash. The first setup lesson explains how to check Git is installed. The practice-folder builder also needs Python 3. Commands using names such as COMMIT or REPOSITORY_URL explain what to replace before running them.</p><p>Pictures and browser exercises do not run Git or change your projects. Real labs use new practice folders and a shared repository stored locally. Progress stays in this browser; you can back it up on the <a href="recap.html#progress">review page</a>.</p>'),
  section('curriculum', 'All lessons and practice pages', '<div class="cards" data-course-cards></div>')
], ['Start with the story, then follow a single file through add and commit.', 'Use pictures to predict the result before trying a command.', 'When a command fails, read the message and check the state before changing more.'])

from beginner_content import add_beginner
add_beginner(lesson, section, table, note)
from core_lessons import add_core
add_core(lesson)
from support_content import add_support
add_support(lesson)
