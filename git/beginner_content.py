"""A school-project introduction before commands and repository internals."""

def add_beginner(lesson, section, table, note):
    lesson("why-git", "What is Git, and why do we need it?", 20,
      "Start with a school project. Learn why saving useful versions matters, how Git helps a team, and how GitHub fits in. No coding knowledge needed.",
      ["Explain Git in your own words.", "Save a version, make a mistake and recover earlier content in a visual model.", "Tell Git apart from GitHub, autosave and a backup."], [
      section("story", "Imagine you are making a science-project website", """
<div class="story-strip" aria-label="A project changes over time">
 <article><span class="story-icon" aria-hidden="true">01</span><h3>Monday: a good start</h3><p>You write a title and two facts about the solar system.</p><div class="paper-preview"><b>Our solar system</b><span>Eight planets orbit the Sun.</span><span>Earth is our home.</span></div></article>
 <article><span class="story-icon" aria-hidden="true">02</span><h3>Tuesday: an accidental edit</h3><p>You replace the correct fact while trying a new idea. You want the earlier work back.</p><div class="paper-preview mistake"><b>Our solar system</b><del>Eight planets orbit the Sun.</del><ins>Two planets orbit the Sun.</ins></div></article>
 <article><span class="story-icon" aria-hidden="true">03</span><h3>Wednesday: a teammate joins</h3><p>Your friend improves the title while you add a fact. How do you keep both changes?</p><div class="paper-preview"><b>Our amazing solar system</b><span>Eight planets orbit the Sun.</span><span>Earth is our home.</span><span>The Sun is a star.</span></div></article>
</div>
<p>Renaming files to <code>project-final</code>, <code>project-final-2</code> and <code>project-really-final</code> quickly becomes confusing. You need a clear record of useful versions and a way to compare changes.</p>"""),
      section("meaning", "Git is a version-control tool",
        """<div class="big-idea"><span class="eyebrow">The idea in one sentence</span><p><strong>Git keeps a history of versions you deliberately record, so you can understand changes, recover recorded work and combine a team’s contributions.</strong></p></div>
<p>A <strong>version</strong> is the project as it looked at one point. A <strong>snapshot</strong> is a way to think about that recorded state, like a photograph of the project. A <strong>commit</strong> is a recorded snapshot with a message and links to its earlier history.</p>
<p>You decide when to record a commit. Saving a file in your editor and making a Git commit are different actions. Git does not automatically remember every keystroke.</p>""" +
        table(["Your problem", "What Git helps you do", "Why it matters"], [
          ["“What changed?”", "Compare two recorded versions.", "Find the exact change instead of guessing."],
          ["“The project worked yesterday.”", "Inspect and recover previously recorded content.", "Repair a mistake with evidence."],
          ["“Can I try a different idea?”", "Make a branch: a separate line of development.", "Experiment before combining the idea with the main work."],
          ["“We both changed the project.”", "Combine changes and identify conflicting edits.", "Keep useful contributions from more than one person."],
          ["“Why did we change this?”", "Read commit messages and review history.", "Help your future self and teammates understand the decision."]
        ])),
      section("time-machine", "Try it: save, make a mistake, recover",
        """<p>This small project has one sentence. First record the mistake, then recover the correct sentence from version A and record the correction. Watch the saved history grow.</p><div id="beginner-lab" class="studio-tool"></div>
<noscript><div class="memory-strip"><b>A: correct fact</b><span>→</span><b>B: mistaken fact</b><span>→</span><b>C: correction</b></div><p>Restoring the correct content and recording a new commit keeps a visible history of the mistake and its correction. Git also has other recovery operations; you will learn their differences later.</p></noscript>""" +
        note("What the buttons represent", "This browser model simplifies the steps. In real Git you edit a file, select content for the next commit by staging it, then commit. “Use this version” here changes the working sentence; it does not delete the saved history. “Record a snapshot” creates a new saved version.")),
      section("words", "Six words, introduced through the project", """
<div class="word-cards">
 <details><summary><span aria-hidden="true">▤</span> Repository</summary><p>The project together with its Git history and metadata. Think “project + recorded story,” not just a folder of latest files.</p></details>
 <details><summary><span aria-hidden="true">●</span> Commit</summary><p>A deliberately recorded project state with a message and parent history. “Add the planet facts” is a useful message.</p></details>
 <details><summary><span aria-hidden="true">⑂</span> Branch</summary><p>A name for a line of development. You can try a new title on a branch before combining it with the main work. Git stores a branch as a reference, not a full extra project copy.</p></details>
 <details><summary><span aria-hidden="true">⇄</span> Diff</summary><p>A comparison showing what changed between two states. Removed and added lines help you inspect the change.</p></details>
 <details><summary><span aria-hidden="true">⋈</span> Merge</summary><p>Combine lines of development. If you changed the title and your friend added a fact, both changes may fit together.</p></details>
 <details><summary><span aria-hidden="true">!</span> Conflict</summary><p>Git needs your decision because it cannot automatically combine an edit. If you and your friend choose different titles, you decide the intended final title.</p></details>
</div><p>Do not memorize every command now. First say what problem each word describes. The later lessons show the exact commands and their effects.</p>"""),
      section("github", "Git and GitHub are related, but different", """
<div class="git-github-map">
 <article><span class="station-number" aria-hidden="true">01</span><h3>Your computer: Git</h3><p>Record and inspect project history locally. You can make commits without an internet connection.</p><div class="mini-timeline" aria-label="Local commits A, B and C"><span>A</span><i></i><span>B</span><i></i><span>C</span></div></article>
 <div class="transport-label"><b>push →</b><small>send commits</small><b>← fetch</b><small>download updates</small></div>
 <article><span class="station-number" aria-hidden="true">02</span><h3>A hosting service: GitHub</h3><p>Host a remote repository, discuss changes, review pull requests and control access. Others can work with that shared repository.</p><div class="review-bubbles"><span>Your change</span><span>Teammate review</span><span>Checks</span></div></article>
</div>
<p><strong>Git</strong> is the version-control tool. <strong>GitHub</strong> is one service that hosts Git repositories and adds collaboration features. You can use Git without GitHub. A local commit is not on GitHub until you send it to the remote, normally with a push.</p>
<p>A <strong>pull request</strong> asks to combine proposed changes with a base branch and gives people a place to review them. Opening a pull request does not automatically merge or publish your project.</p>
<details class="reveal"><summary>Quick check: I committed while offline. Can my friend see it on GitHub?</summary><p>No. The commit exists locally. You must later send it to the intended remote, with the required access. Commit and push are separate steps.</p></details>
<details class="reveal"><summary>Quick check: Git found a conflict. Has it decided whose answer is correct?</summary><p>No. You inspect both intentions, choose or combine the correct content, and test the result. Git cannot decide the project’s requirements for you.</p></details>"""),
      section("limits", "What Git does not promise",
        table(["Common assumption", "More accurate idea"], [
          ["“Git saves every edit automatically.”", "A commit records selected content when you create it. Unsaved or never-recorded work may be lost."],
          ["“Git is my complete backup.”", "History in one local repository is still on that computer. Keep appropriate remote copies and backups; do not rely on Git for everything."],
          ["“Git checks whether my answer or code is correct.”", "It records and compares content. People and tests check correctness."],
          ["“GitHub is required to use Git.”", "Local Git works independently. Hosting adds sharing and collaboration."],
          ["“A merge always combines everything correctly.”", "Some edits conflict. Even a clean text merge needs review and tests."]
        ]) +
        '<p>Next, follow the project into <a href="foundations.html">working files, staging and commits</a>. Then try the <a href="studio.html#snapshots">visual snapshot lab</a>. A good first goal is to explain “edit → stage → commit → push” in your own words.</p><p class="source-note">Continue reading: <a href="https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control">Pro Git: About Version Control</a> and <a href="https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F">What is Git?</a>.</p>')
    ], ["Git helps you understand and manage recorded project changes.", "A commit is a deliberate record, not automatic saving.", "Git is the tool; GitHub adds remote hosting and collaboration."])
