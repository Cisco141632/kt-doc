"""Static reading companion and launch points for the interactive practice studio."""

def add_studio(lesson, section, note, table):
    lesson("studio", "Practice Studio: make Git stick", 40,
      "Move snapshots, place branch pointers, investigate incidents and retrieve what you know. A visual practice session with room to experiment.",
      ["Predict which content a command will record.", "Read a commit graph and place the resulting branch pointer.", "Choose a recovery action from evidence and practise weak recall topics."], [
      section("choose", "Choose a practice station", """
<div class="studio-intro">
  <div><p class="eyebrow">Learn by changing the picture</p><h3>Predict. Try. Explain. Repeat.</h3><p>Start with one station. Notice what moves and what stays. Say why the result makes sense before moving on.</p><p class="meta">No timer, no lost lives. Every mistake comes with a reason.</p><p id="studio-progress" role="status">Five stations · fourteen practice goals</p></div>
  <svg viewBox="0 0 340 230" role="img" aria-labelledby="studio-map-title"><title id="studio-map-title">Your learning path branches into practice and rejoins with stronger recall</title><path d="M35 115H105L185 45H290M105 115L185 185H290M105 115H290" fill="none" stroke="currentColor" stroke-width="3"/><g fill="var(--surface)" stroke="currentColor" stroke-width="3"><circle cx="35" cy="115" r="12"/><circle cx="105" cy="115" r="12"/><circle cx="185" cy="45" r="12"/><circle cx="185" cy="115" r="12"/><circle cx="185" cy="185" r="12"/><circle cx="290" cy="45" r="12"/><circle cx="290" cy="115" r="12"/><circle cx="290" cy="185" r="12"/></g><g fill="var(--text)" font-size="13" font-family="system-ui"><text x="15" y="150">learn</text><text x="159" y="22">predict</text><text x="169" y="151">try</text><text x="157" y="218">explain</text></g></svg>
</div>
<nav class="station-menu" aria-label="Practice stations">
 <a href="#snapshots"><span class="station-number">01</span><b>Snapshot lab</b><small>Move file versions · 6 min</small></a>
 <a href="#pointers"><span class="station-number">02</span><b>Place the pointer</b><small>Predict six histories · 8 min</small></a>
 <a href="#incidents"><span class="station-number">03</span><b>Incident room</b><small>Evidence → decision · 10 min</small></a>
 <a href="#match"><span class="station-number">04</span><b>Connect the command</b><small>Match eight intentions · 5 min</small></a>
 <a href="#sprint"><span class="station-number">05</span><b>Five-minute recall</b><small>Retrieve, then retry · 5 min</small></a>
</nav>""" + note("Practice model", "The studio changes browser models only. It does not run Git or touch a repository. The <a href=\"practice.html\">real Git labs</a> let you verify the same ideas in a terminal. Completed goals and recall results use your existing exportable learning progress.")),
      section("snapshots", "01 · Watch a snapshot move",
        '<p>One file, three versions of reality. Change the working file, stage its current content, then commit. Each lane shows the actual content held in that part of this model.</p><div id="snapshot-studio" class="studio-tool"></div><noscript><p>Example: HEAD has base text. Edit to version A, stage A, then edit to B. The index still holds A. Commit records A and leaves B as an unstaged edit. Unstaging copies HEAD into the index; it does not discard the working file.</p></noscript>'),
      section("pointers", "02 · Where does the branch go?",
        '<p>Read the operation and move the branch badge to its resulting commit. Dragging is optional: tap or keyboard-select a commit, then check. Dashed circles are possible new commits for this prediction.</p><div id="pointer-studio" class="studio-tool"></div><noscript><p>Fast-forward moves to an existing descendant. A true merge moves to a new two-parent commit. Rebase moves the replayed branch to replacement commits. Revert adds an inverse change. Soft reset moves the branch but retains staged and working content. Fetch normally updates remote-tracking refs, not your checked-out local branch.</p></noscript>'),
      section("incidents", "03 · You are on call for the repository",
        '<p>Open the evidence cards, choose the next step, and explain the outcome. A wrong choice stays at the current step so you can learn from its consequence.</p><div id="incident-studio" class="studio-tool"></div><noscript><p>Rejected push: fetch and inspect the divergence, integrate the teammate’s change, then test and push normally. Lost committed work: inspect reflog, protect the identified tip with a rescue branch, then choose integration. Rebase conflict: inspect the replayed patch and all available stages, preserve intended behavior, stage, test and continue.</p></noscript>'),
      section("match", "04 · Connect an intention to a command",
        '<p>Choose one intention and its matching command. Work from the effect you need. Both columns stay visible: the challenge is understanding the match, not guessing where a card was hidden.</p><div id="match-studio" class="studio-tool"></div><noscript><p>Use the <a href="reference.html">task-to-command table</a>: cover the command column, say your answer, then uncover it.</p></noscript>'),
      section("sprint", "05 · A small recall round",
        '<p>Five questions, about five minutes, without a countdown. Previously missed studio questions come first. Make a prediction before reading the explanation, then retry the questions you missed. These answers are separate from your full quiz attempt.</p><div id="recall-studio" class="studio-tool"></div><noscript><p>Choose five prompts from the <a href="quiz.html">readable question bank</a>. Write your answers, check the explanations, then repeat the missed prompts without looking.</p></noscript>'),
      section("transfer", "Turn the picture into a lasting explanation",
        table(["Picture", "Say this from memory", "Verify in a real lab"], [
          ["Three snapshot lanes", "Add copies current content into the index. Commit records the index.", '<a href="practice.html#staging">Staging lab</a>'],
          ["A two-parent node", "Merge preserves both ancestry lines; the final behavior still needs tests.", '<a href="practice.html#three-way">Three-way merge lab</a>'],
          ["A moved branch badge", "A reference moved. Ask what stayed reachable and what happened to the files.", '<a href="practice.html#reflog">Reflog recovery lab</a>'],
          ["A rejected lease", "The live tip differs from my explicit expectation. Inspect the new work.", '<a href="practice.html#lease">Alice/Bob push race</a>']
        ]) + '<p>Tomorrow, return for another recall round. Later, use the <a href="recap.html">scheduled recall cards</a> and explain one incident to a teammate. A completed badge records practice, not a guarantee of real-world proficiency.</p>')
    ], ["Name the layer before choosing the command.", "Predict the new tip and parent relationships.", "Use mistakes as a shortlist for your next recall session."])
