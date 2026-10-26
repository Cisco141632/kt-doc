"""Authored tmux curriculum. Run python3 tmux/build.py after editing."""
from html import escape

def code(text, where="Run in your shell"):
    return '<div class="snippet"><div class="code-caption"><span>' + escape(where) + '</span></div><pre><code>' + escape(text.strip()) + '</code></pre></div>'

def table(headings, rows):
    return '<div class="table-wrap"><table><thead><tr>' + ''.join('<th scope="col">' + h + '</th>' for h in headings) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join('<td class="wrap">' + c + '</td>' for c in row) + '</tr>' for row in rows) + '</tbody></table></div>'

def note(title, body, kind="tip"):
    return '<div class="callout ' + kind + '"><b class="callout-title">' + title + '</b><p>' + body + '</p></div>'

def flow(items):
    return '<div class="flow" role="group" aria-label="Process diagram">' + '<span aria-hidden="true">→</span>'.join('<div><b>' + a + '</b><small>' + b + '</small></div>' for a,b in items) + '</div>'

def section(id, title, body):
    return '<section class="lesson-section" id="' + id + '"><h2>' + title + '</h2>' + body + '</section>'

LESSONS = []
def lesson(id, title, minutes, description, objectives, sections, recap, topic=None):
    LESSONS.append(dict(id=id, title=title, minutes=minutes, description=description, objectives=objectives, sections=sections, recap=recap, topic=topic))

lesson("index", "Make your terminal a workspace.", 10,
    "Learn tmux from your first session to repeatable development and remote workflows. See what each command changes, try it, diagnose failures, then recall it without looking.",
    ["Understand the problem tmux solves.", "Choose a learning route and try the browser playground.", "Know what persistence does—and where it stops."], [
section("why", "The problem: one terminal, too much work",
    """<p>You are editing code, watching a server log, and running tests. Another terminal is connected to a remote machine. Which tab belongs to which project? What happens to a long job if the network drops? tmux gives those programs a named workspace that you can leave and return to.</p>
    <p>A <strong>terminal multiplexer</strong> puts multiple terminal programs inside one terminal interface. It runs a server process on the machine where you start it. Your terminal connects as a client. Detaching disconnects the client while programs inside the server’s panes can keep running.</p>""" +
    flow([("Your terminal", "Keyboard input and a view of your work"), ("tmux client", "Connects or detaches"), ("tmux server", "Keeps sessions, windows and panes"), ("Programs", "Shell, editor, tests, logs")]) +
    note("Persistence has a boundary", "tmux can outlive a terminal or SSH disconnection. It does not keep processes alive through a host reboot, a stopped container, a killed tmux server, or a policy that terminates your user’s processes on logout.", "warn")),
section("route", "Learn by doing, then come back to recall",
    """<div class="stat-grid"><div class="stat"><strong>18</strong><span>connected learning modules</span></div><div class="stat"><strong>48</strong><span>explained quiz questions</span></div><div class="stat"><strong>8</strong><span>real terminal labs</span></div><div class="stat"><strong>6</strong><span>browser missions</span></div></div>""" +
    table(["Your starting point", "Suggested route"], [
    ["Completely new", "Installation → mental model → sessions → windows → panes. Try each shortcut in the playground."],
    ["Already use a few shortcuts", "Copy mode → configuration → everyday workflow → SSH. Use the quiz to discover gaps."],
    ["Want reliable project setup", "Automation → advanced tools → real labs. Build and inspect a repeatable workspace."],
    ["Something broke right now", '<a href="troubleshooting.html">Search the troubleshooting clinic</a>, then check the matching lesson.'],
    ["Need a five-minute refresh", '<a href="recap.html">Review flashcards</a> and keep the <a href="reference.html">command reference</a> open.']]) +
    """<p>Expect roughly 8–10 hours with practice, spread across several sessions. A productive rhythm is: read one section, predict the result, run the example, explain the result aloud, and do a recall check the next day.</p>
    <div class="actions"><a class="btn btn-primary" href="installation.html">Start the learning path →</a><a class="btn" href="playground.html">Try the visual playground</a></div>"""),
section("contract", "What you need and how examples work",
    """<p>You need basic shell skills: entering a command, moving between directories with <code>cd</code>, and interrupting a foreground program with <code>Ctrl+c</code>. Installation is covered next. The browser simulator needs no tmux installation; real labs need tmux on Linux, macOS, or Linux inside WSL.</p>
    <p><strong>Shell command</strong> blocks include the <code>tmux</code> executable. <strong>tmux prompt</strong> examples are entered after <kbd>Ctrl+b</kbd>, release, then <kbd>:</kbd>; do not type an extra <code>tmux</code>. <strong>Configuration</strong> blocks belong in a tmux config file. <strong>Expected output</strong> blocks are observations, not commands.</p>
    <p>The core course targets established tmux 3.2+ behavior. Your installed <code>tmux -V</code>, <code>man tmux</code>, and <code>tmux list-keys</code> are the authority for your version and customization. Optional newer features are labeled. The reference links to the complete manual; this course teaches the full workflow without pretending every version has identical flags.</p>
    <p>Everything runs locally in your browser. Progress, lab checklists and quiz results are stored on this browser when storage is available. No account is required. Clearing browser data removes that progress; the recap page lets you export and import a backup.</p>"""),
section("modules", "Explore the curriculum", '<div class="cards" data-course-cards></div>')
], ["A client is your connection; the server owns the running workspace.", "Practise on disposable sessions before using tmux for important work.", "Use the lesson → exercise → troubleshooting → recall loop."])

lesson("installation", "Install, verify & take the first step", 20,
    "Get a working tmux installation, learn the prefix sequence, and practise leaving and returning without losing your shell.",
    ["Install on Linux, macOS or WSL.", "Tell shell commands, prefix keys and tmux commands apart.", "Create and reattach to a disposable session."], [
section("install", "Install on the machine that will run your work",
    """<p>For remote work, tmux must be installed on the remote host. Installing it only on your laptop does not protect a shell running outside tmux on the server. On Windows, use a Linux environment such as WSL; run the Linux installation commands inside that distribution.</p>""" +
    table(["Environment", "Installation command"], [
    ["Ubuntu / Debian / Ubuntu in WSL", "<code>sudo apt update &amp;&amp; sudo apt install tmux</code>"],
    ["Fedora", "<code>sudo dnf install tmux</code>"],
    ["Arch Linux", "<code>sudo pacman -S tmux</code>"],
    ["macOS with Homebrew already installed", "<code>brew install tmux</code>"],
    ["openSUSE", "<code>sudo zypper install tmux</code>"]]) +
    code("command -v tmux\ntmux -V\nman tmux") +
    """<p><code>command -v</code> should print an executable path. <code>tmux -V</code> prints the version, for example <code>tmux 3.4</code>. Press <kbd>q</kbd> to leave the manual. Distribution packages can be older than upstream. Read the installed manual before adopting examples from newer releases.</p>""" +
    note("If installation fails", "“Command not found” means tmux is missing or absent from PATH. Repository or permission errors belong to the package manager: confirm the OS, repository configuration and administrator access. On a managed host, ask the administrator for the supported package rather than compiling over system files.", "warn")),
section("first", "Your first five minutes",
    code("tmux new-session -s learn") +
    """<p>A shell opens with a status line showing <code>[learn]</code> and its first window. You are now inside tmux. Create a visible marker:</p>""" +
    code("printf 'This shell belongs to my learn session.\\n'\nprintf 'Pane: %s\\n' \"$TMUX_PANE\"") +
    """<div class="keyline"><kbd>Ctrl</kbd> + <kbd>b</kbd> <span>→ release both →</span> <kbd>d</kbd></div>
    <p>You should return to the outside shell with a detached message. Now list the sessions and return:</p>""" +
    code("tmux list-sessions\ntmux attach-session -t learn") +
    """<p>The marker and the same shell should still be there. <code>-s</code> names a new session; <code>-t</code> selects an existing target. If “duplicate session: learn” appears, attach to the existing session or choose another name.</p>"""),
section("keys", "The prefix is a sequence, not one chord",
    """<p>Hold Control and press <kbd>b</kbd>, release both keys, then press the action key. <code>C-b</code> means Control+b; <code>M</code> usually means Alt/Meta. The default prefix is <code>C-b</code>, but someone’s config may change it. Press <kbd>Ctrl+b</kbd> then <kbd>?</kbd> for current bindings; press <kbd>q</kbd> to leave that list.</p>""" +
    table(["Input", "Where", "Meaning"], [
    ["<code>tmux new-session -s learn</code>", "Shell prompt", "Run the tmux program and create a session."],
    ["<kbd>Ctrl+b</kbd> then <kbd>d</kbd>", "An attached tmux client", "Ask tmux to detach the client."],
    ["<kbd>Ctrl+b</kbd> then <kbd>:</kbd>, type <code>list-sessions</code>", "tmux command prompt", "Execute a tmux command without a shell prefix."],
    ["<code>set -g mouse on</code>", "Config file or tmux prompt", "Set a tmux option. From a shell use <code>tmux set -g mouse on</code>."]]) +
    note("Try a clean configuration", 'A separate server keeps experiments away from existing work: <code>tmux -L kt-tmux -f /dev/null new-session -s learn</code>. Use <code>tmux -L kt-tmux …</code> for every outside-shell command to that server. The config selection only applies when that server starts.')),
section("cleanup", "Leave safely and finish deliberately",
    """<p>Detach when you want to return later. Run <code>exit</code> in a shell when you intend to close that shell. When the last pane closes, its window disappears; when the final window in a session disappears, the session ends. The server normally exits once there are no sessions.</p>
    <p>Before practising a close operation, check that you are in the disposable learning session. Avoid <code>kill-server</code> as a troubleshooting reflex: it terminates every session on the targeted server. A stopped program cannot be revived by reattaching.</p>""")
], ["Run tmux where the work runs.", "Prefix means Ctrl+b, release, then the action key.", "Detach leaves work running; exit ends the shell."], "installation")

lesson("mental-model", "See the server, sessions, windows & panes", 20,
    "Build a mental model that makes every later command predictable.",
    ["Trace a key from your terminal to a program.", "Distinguish session, window, pane, client and server.", "Understand indexes, stable IDs and target syntax."], [
section("hierarchy", "One workspace, several layers",
    """<p>Think of the server as an office building, a session as a project room, a window as a desk, and a pane as a workstation running a program. Your client is your view into a room. Leaving the room does not demolish the building.</p>
    <div class="hierarchy"><b>tmux server · one user, one socket</b>
      <div class="nest"><b>Session: project</b><div class="visual-grid">
        <div class="nest"><b>Window 0: editor</b><div class="pane-demo horizontal"><div>Pane %0<br>editor</div><div>Pane %1<br>shell</div></div></div>
        <div class="nest"><b>Window 1: logs</b><div class="pane-demo"><div>Pane %2<br>log viewer</div></div></div>
      </div></div><div class="nest"><b>Session: experiments</b> · separate window list, same server</div>
    </div>
    <p>A pane contains a pseudoterminal and a running program—often a shell which launches other programs. A window arranges panes. A session has a list of linked windows and a current window. Windows can be linked into multiple sessions: this is shared state, not a copy.</p>"""),
section("focus", "Follow the active path",
    flow([("Attached client", "Connected to project"), ("Current window", "0:editor"), ("Active pane", "%1"), ("Foreground program", "Receives your typing")]) +
    """<p>A window remembers its active pane. A session remembers its current window. Clicking another pane (with mouse support) or selecting one with a shortcut changes where subsequent typing goes. Typing in a log viewer is different from typing in a shell; tmux does not interpret normal keystrokes as shell commands.</p>
    <p>Two clients attached to the same session normally see the same current window and active pane. Both may type into the same application. Separate sessions in a session group allow separate current-window selection while sharing windows and the programs inside them.</p>"""),
section("targets", "Names are friendly; IDs are precise",
    code("tmux list-sessions\ntmux list-windows -t project\ntmux list-panes -a -F '#{session_name}:#{window_index}.#{pane_index} #{pane_id} #{pane_current_command}'") +
    table(["Target", "What it selects"], [
    ["<code>project</code>", "A session name; prefer exact session matching with <code>=project</code> where accepted."],
    ["<code>project:1</code>", "Window index 1 in project."],
    ["<code>project:1.0</code>", "Pane index 0 of window index 1 in project."],
    ["<code>%3</code>", "Pane ID 3, stable for that pane’s lifetime on this server."],
    ["<code>@2</code> / <code>$1</code>", "Window ID / session ID. Quote dollar-prefixed IDs so your shell does not expand them."]]) +
    """<p>Indexes may change when you move or renumber objects. IDs are unique within one server and last only as long as that object. A session name is not a Linux process ID. A pane’s PID identifies a process, not a tmux target.</p>
    <p>Without <code>-t</code>, commands use context and defaults that may surprise scripts. Inspect targets first and pass explicit names or IDs for automation. Quote format strings so the shell sends them unchanged.</p>"""),
section("socket", "The missing layer: a server socket",
    """<p>Clients communicate with the server through a Unix socket, normally under a per-user directory such as <code>/tmp/tmux-UID/</code>. The server belongs to the user who starts it. Running <code>sudo tmux ls</code> typically inspects a different user’s server and will not reveal your ordinary sessions.</p>""" +
    code("tmux -L training new-session -d -s demo\ntmux -L training list-sessions") +
    """<p><code>-L training</code> chooses a named socket and therefore a separate server. <code>-S /path/to/socket</code> chooses an explicit path. A missing session can mean the wrong host, user or socket—not that the session has died.</p>""")
], ["Server → session → window → pane → program.", "Input goes to the foreground program in the active pane.", "Use stable pane IDs in scripts, and inspect the correct host, user and socket."], "mental-model")

lesson("sessions", "Sessions & the persistence lifecycle", 25,
    "Create named project workspaces, detach, switch and reattach with confidence.",
    ["Create, inspect, rename and switch sessions.", "Predict which processes survive a disconnection.", "Distinguish detaching a client from ending a workspace."], [
section("lifecycle", "Create → work → detach → return",
    flow([("Create", "tmux new -s api"), ("Work", "Programs run in panes"), ("Detach", "Ctrl+b then d"), ("Return", "tmux attach -t api")]) +
    code("tmux new-session -s api -n editor\n# After detaching:\ntmux list-sessions\ntmux attach-session -t api") +
    """<p><code>-n editor</code> names the first window. Detaching does not pause or freeze the program: it continues consuming CPU, reading files and writing output. If the program finishes while you are away, you return to its shell or to a closed pane, depending on how you launched it.</p>"""),
section("manage", "A small session toolkit",
    table(["Action", "Shell command", "Attached shortcut"], [
    ["Create or attach", "<code>tmux new-session -A -s api</code>", "Use an outside shell; inside use session switching."],
    ["Create without attaching", "<code>tmux new-session -d -s worker</code>", "Command prompt: <code>new-session -d -s worker</code>"],
    ["List", "<code>tmux list-sessions</code> (alias <code>ls</code>)", "<kbd>Ctrl+b</kbd> then <kbd>s</kbd> opens the chooser."],
    ["Rename", "<code>tmux rename-session -t api backend</code>", "<kbd>Ctrl+b</kbd> then <kbd>$</kbd>"],
    ["Switch attached client", "<code>tmux switch-client -t backend</code>", "Choose a session from the session chooser."],
    ["Detach current client", "<code>tmux detach-client</code>", "<kbd>Ctrl+b</kbd> then <kbd>d</kbd>"],
    ["Detach other clients when attaching", "<code>tmux attach-session -d -t backend</code>", "Use only when you intend to disconnect their views."]]) +
    """<p>Inside tmux, <code>switch-client</code> changes the session displayed by your existing client. Running a new tmux client inside a pane creates nesting, which is usually unnecessary for local session switching. <code>new-session -A</code> is convenient but can silently reuse old project state; inspect the workspace after attaching.</p>"""),
section("survival", "Predict what survives",
    table(["Event", "What happens"], [
    ["Close the client terminal / SSH drops", "The server and pane programs generally continue on their host; logout policies can change this."],
    ["Detach with Ctrl+b d", "This client leaves. Other clients may stay attached. Programs keep running."],
    ["Ctrl+c in a pane", "The terminal sends an interrupt to the foreground process group. Often the job stops and the shell remains."],
    ["exit or Ctrl+d at an empty shell prompt", "The shell may exit. The pane normally closes when its main program ends."],
    ["Kill a session", "Its window links disappear; windows with no remaining links close. Programs in closed panes lose their terminals and may terminate."],
    ["Server crash / host reboot / container removal", "tmux does not preserve or resume live processes. Recreate the workspace and restart work from application checkpoints."]]) +
    note("A long job needs its own recovery plan", "Use application checkpoints and persistent logs. For unattended services, use a service manager or job scheduler. tmux provides an interactive workspace; it does not automatically restart failed processes or guarantee successful completion.", "warn")),
section("close", "Close only the intended workspace",
    code("tmux list-windows -t api\ntmux list-panes -s -t api\n# Only after checking that this disposable session can end:\ntmux kill-session -t '=api'") +
    """<p>The equals prefix requests an exact session-name match for this target. Stop applications cleanly first where possible. <code>kill-pane</code>, <code>kill-window</code>, <code>kill-session</code> and <code>kill-server</code> have progressively wider effects; there is no general undo.</p>""")
], ["Name sessions by project or purpose.", "Detach preserves the running workspace, not a durable backup.", "Switch inside tmux; attach from outside; inspect before killing."], "sessions")

lesson("windows", "Windows: organize a project", 20,
    "Give each task a home and move between editor, server, tests and logs without losing context.",
    ["Create, rename, select and reorder windows.", "Read the status line and use the tree chooser.", "Understand linked windows and closing behavior."], [
section("desk", "One window per kind of work",
    """<p>A practical project might have <code>0:editor</code>, <code>1:server</code>, <code>2:tests</code> and <code>3:logs</code>. Each window can contain one or many panes. Switching windows changes what you see; programs in hidden windows continue running.</p>""" +
    flow([("0:editor", "Read and change code"), ("1:server", "Run the development server"), ("2:tests", "Observe test results"), ("3:logs", "Inspect events")]) +
    code("tmux new-window -t api -n tests\ntmux new-window -t api -n logs\ntmux list-windows -t api\ntmux select-window -t api:tests") +
    """<p>Named targets make commands readable, but duplicate window names can be ambiguous. Window IDs such as <code>@4</code> remove ambiguity. Creating a window picks an available index; it does not necessarily append after the highest index if there are gaps.</p>"""),
section("shortcuts", "Move without thinking",
    table(["Prefix, then…", "Effect", "Memory cue"], [
    ["<kbd>c</kbd>", "Create a window", "create"],
    ["<kbd>,</kbd>", "Rename current window", "Give the task a readable name"],
    ["<kbd>n</kbd> / <kbd>p</kbd>", "Next / previous window", "next / previous"],
    ["<kbd>0</kbd> … <kbd>9</kbd>", "Select a window by index", "Read the index in the status line"],
    ["<kbd>l</kbd>", "Last window", "Jump between two tasks"],
    ["<kbd>w</kbd>", "Interactive window/session tree", "Navigate with arrows; Enter selects; q leaves"],
    ["<kbd>.</kbd>", "Move the current window to a new target", "Reorganize deliberately"],
    ["<kbd>&amp;</kbd>", "Confirm killing the current window", "Closes all its panes; save work first"]]) +
    """<p>The default status line marks the current window with <code>*</code>, the last window with <code>-</code>, and a zoomed window with <code>Z</code>. Other flags may signal a bell, activity or a marked pane. Themes may display these differently.</p>"""),
section("arrange", "Reorder and avoid surprising renumbering",
    code("tmux move-window -s api:logs -t api:5\ntmux swap-window -s api:0 -t api:1\ntmux move-window -r -t api") +
    """<p><code>move-window</code> relocates a window; <code>swap-window</code> exchanges two. <code>move-window -r</code> closes index gaps. If the destination is occupied, a move fails unless you explicitly choose behavior that replaces it. Avoid <code>-k</code> here unless destroying the destination is intended.</p>
    <p><code>set -g base-index 1</code> makes new window indexes start at one. <code>set -g renumber-windows on</code> renumbers after windows close. This is convenient for humans but breaks scripts that assume a task always lives at <code>:2</code>; use names or captured IDs.</p>"""),
section("linking", "A linked window is shared, not duplicated",
    code("tmux link-window -s api:logs -t review:3") +
    """<p>This requires a <code>review</code> session and an available destination index. Both sessions now point to the same window and the same panes. Editing or typing in it changes the same programs. <code>unlink-window</code> removes a link; <code>kill-window</code> destroys the window itself and removes it from all linked sessions.</p>
    <p>Use linking for a shared monitoring view. Use a new window if you need independent processes. The advanced lesson explains session groups when several shared windows should stay synchronized.</p>""")
], ["Windows organize tasks; hidden programs keep running.", "Names help navigation; IDs help reliable scripts.", "Linking shares a live window, so killing it affects every linked session."], "windows")

lesson("panes", "Panes, layouts & focus", 30,
    "Split the screen intentionally, understand split direction, and keep track of the pane receiving your input.",
    ["Create side-by-side and stacked panes.", "Select, resize, zoom and rearrange panes.", "Keep working directories and close operations predictable."], [
section("splits", "See the two split directions",
    """<div class="visual-grid"><div><h3>Side by side</h3><div class="pane-demo horizontal"><div>left</div><div>right</div></div><p><kbd>Ctrl+b</kbd> then <kbd>%</kbd><br><code>split-window -h</code></p></div><div><h3>One above another</h3><div class="pane-demo"><div>top</div><div>bottom</div></div><p><kbd>Ctrl+b</kbd> then <kbd>&quot;</kbd><br><code>split-window -v</code></p></div></div>
    <p>The <code>-h</code> direction places panes along the horizontal axis; the divider is vertical. The <code>-v</code> direction places panes along the vertical axis; the divider is horizontal. This vocabulary causes many first-day mistakes.</p>""" +
    code('tmux split-window -h\ntmux split-window -v -c "#{pane_current_path}"') +
    """<p>A split divides the active pane, not necessarily the whole window. <code>-f</code> spans the full window dimension; <code>-b</code> puts the new pane before the current one. <code>-d</code> keeps focus in the existing pane. <code>-c</code> sets the starting directory.</p>"""),
section("focus", "Always know where the next command will go",
    table(["Prefix, then…", "Result"], [
    ["Arrow key", "Move focus to a neighboring pane."],
    ["<kbd>o</kbd>", "Cycle active pane."],
    ["<kbd>q</kbd>, then a displayed number", "Show pane indexes, then select one before the labels disappear."],
    ["<kbd>z</kbd>", "Zoom this pane to fill the window; repeat to restore the layout."],
    ["<kbd>Space</kbd>", "Cycle predefined layouts."],
    ["<kbd>{</kbd> / <kbd>}</kbd>", "Swap with the previous / next pane."],
    ["<kbd>!</kbd>", "Break the current pane out into a separate window."],
    ["<kbd>x</kbd>", "Ask to kill the active pane; inspect its running program before confirming."]]) +
    """<p>The active pane’s border is highlighted. Zoom hides other panes without stopping them. If a pane seems to have vanished, look for the <code>Z</code> status flag and toggle zoom before rebuilding the layout.</p>"""),
section("layout", "Resize and choose a useful arrangement",
    code("tmux resize-pane -R 5\ntmux resize-pane -D 3\ntmux select-layout tiled\ntmux select-layout main-vertical") +
    """<p>Directional resizing changes the selected pane’s boundary when the layout allows it. <code>even-horizontal</code> distributes side-by-side panes; <code>even-vertical</code> stacks them; <code>main-vertical</code> gives a large pane on the left; <code>main-horizontal</code> gives a large pane above; <code>tiled</code> forms a grid.</p>
    <p>Default prefix + Control+arrow resizes in small steps; prefix + Alt+arrow uses larger steps, if the terminal transmits those combinations. Commands from the tmux prompt are a reliable fallback when the terminal or desktop intercepts shortcuts.</p>""" +
    note("A sensible limit", "If a split reports “no space for new pane”, enlarge the terminal, unzoom, close an unneeded pane, or create a new window. Six tiny panes are often less useful than two readable ones.")),
section("move", "Move a pane without restarting its program",
    code("tmux list-panes -a -F '#{pane_id} #{session_name}:#{window_index}.#{pane_index}'\n# Example IDs: substitute IDs from your own output.\ntmux break-pane -s %3\ntmux join-pane -s %3 -t %1 -h") +
    """<p><code>break-pane</code> moves a pane into a window of its own. <code>join-pane</code> moves an existing pane into another window as a split. The program continues running in the same pane. Source and target must be distinct valid panes on the same server.</p>
    <p>To close a shell cleanly, type <code>exit</code>. If it contains a foreground job, first decide whether to stop that job with its normal quit operation. Closing a pane is not equivalent to detaching: it can terminate the work.</p>""")
], ["% / -h = side by side; quote / -v = stacked.", "Focus determines where you type; zoom changes only the view.", "Use -c for a predictable directory and IDs when moving panes."], "panes")

lesson("copy-mode", "Scroll, search, copy & the clipboard", 30,
    "Inspect output without losing your place and understand the difference between tmux buffers and your desktop clipboard.",
    ["Use copy mode with both Emacs and vi keys.", "Search retained output and manage paste buffers.", "Choose and diagnose a clipboard integration."], [
section("history", "There are several different histories",
    """<p>Shell history remembers command lines. tmux pane history remembers terminal output. Your terminal emulator may have its own scrollback. These are separate stores. Pressing the mouse wheel may interact with an application, your terminal, or tmux depending on settings.</p>
    <p>Enter tmux copy mode with <kbd>Ctrl+b</kbd> then <kbd>[</kbd>. The pane stops following new output while you inspect its history; the program itself keeps running. Leave with <kbd>q</kbd> in vi mode or <kbd>Esc</kbd> in Emacs mode. Current bindings are the final authority.</p>""" +
    code("tmux show-window-options -v mode-keys\ntmux list-keys -T copy-mode\ntmux list-keys -T copy-mode-vi") +
    """<p>The <code>mode-keys</code> option chooses Emacs or vi behavior; environment settings can influence its default. Explicitly set it during practice so you know which set you are using.</p>"""),
section("keys", "Copy-mode keys do not need the prefix",
    table(["Action after entering copy mode", "Emacs mode", "vi mode"], [
    ["Move", "Arrow keys", "Arrow keys or h j k l"],
    ["Page up / down", "Alt+v / Ctrl+v", "Ctrl+b / Ctrl+f"],
    ["Start selection", "Ctrl+Space", "Space"],
    ["Copy selection and leave", "Alt+w", "Enter"],
    ["Search backward", "Ctrl+r", "?"],
    ["Search forward", "Ctrl+s", "/"],
    ["Repeat previous search / reverse it", "n / N", "n / N"],
    ["Cancel / leave", "Esc", "q"]]) +
    code("tmux set-window-option -g mode-keys vi", "Choose vi copy-mode keys from a shell") +
    """<ol><li>Generate output with <code>seq 1 200</code> in a practice pane.</li><li>Enter copy mode, press <kbd>?</kbd>, type <code>150</code>, and press Enter to search backward through older output.</li><li>Press Space to start selection, move to extend it, then Enter to copy and leave.</li><li>Paste into a safe editor or an empty prompt using prefix then <kbd>]</kbd>. Inspect pasted text before executing anything.</li></ol>
    <p><code>n</code> invokes search-again and <code>N</code> search-reverse; their direction follows the preceding search. If your terminal captures Ctrl+Space or Alt+w, use vi mode or customize the binding.</p>"""),
section("buffers", "The tmux buffer is not automatically your clipboard",
    flow([("Pane output", "Select in copy mode"), ("tmux paste buffer", "Prefix ] pastes into a pane"), ("Clipboard bridge", "OSC 52 or an external tool"), ("Desktop clipboard", "Paste in another app")]) +
    code("tmux list-buffers\ntmux show-buffer\ntmux save-buffer ~/tmux-selection.txt\ntmux load-buffer ~/tmux-selection.txt\ntmux delete-buffer") +
    """<p>Prefix then <kbd>=</kbd> opens the buffer chooser. A buffer can be named with <code>set-buffer -b name</code> and selected using <code>paste-buffer -b name</code>. <code>save-buffer</code> writes to the machine running the tmux server, which might be remote. Deleting a buffer does not erase copies already written elsewhere.</p>
    <p><code>history-limit</code> limits scrollback per pane. Set it before creating panes; increasing it does not recover discarded lines and existing panes keep their creation-time limit. Full-screen applications can use an alternate screen, so their output may not remain in ordinary scrollback.</p>"""),
section("clipboard", "Choose the bridge that matches your environment",
    table(["Environment", "Common approach", "What must be true"], [
    ["macOS desktop", "<code>copy-pipe-and-cancel 'pbcopy'</code>", "pbcopy runs on the Mac with access to its clipboard."],
    ["Linux Wayland desktop", "<code>copy-pipe-and-cancel 'wl-copy'</code>", "wl-clipboard is installed and the server can reach the Wayland session."],
    ["Linux X11 desktop", "<code>copy-pipe-and-cancel 'xclip -selection clipboard'</code>", "xclip is installed and DISPLAY / X authentication are correct."],
    ["SSH to another machine", "OSC 52 with <code>set-clipboard external</code>", "tmux knows the Ms capability and your local terminal allows clipboard writes."]]) +
    code("set -s set-clipboard external\n# Optional vi-style y binding for a LOCAL macOS tmux server:\nbind -T copy-mode-vi y send-keys -X copy-pipe-and-cancel 'pbcopy'", "Configuration example — choose the command for your OS") +
    """<p><code>external</code> permits tmux to set the outer clipboard while preventing applications inside tmux from creating tmux paste buffers through that mechanism. It does not guarantee every terminal supports OSC 52. Check <code>tmux info</code> for <code>Ms</code> and the terminal’s clipboard settings.</p>
    <p>A remote <code>pbcopy</code> does not magically control your laptop clipboard. First confirm copying works inside tmux with <code>show-buffer</code>, then investigate the bridge separately. When mouse mode is on, the terminal’s own text selection may need a modifier such as Shift; the exact override is terminal-specific.</p>""" +
    note("Copying output can copy secrets", "Scrollback, paste buffers and exported captures may contain tokens, passwords or private records. Review content before sharing or logging it.", "warn"))
], ["Copy mode pauses your view, not the program.", "tmux buffers and the OS clipboard are separate.", "Check mode-keys and the clipboard bridge before changing random bindings."], "copy-mode")

lesson("configuration", "Build a configuration you understand", 35,
    "Add useful settings one at a time and learn how option scope, key tables and reload behavior work.",
    ["Read and safely reload a tmux configuration.", "Distinguish server, session, window and pane settings.", "Customize keys, paths, status and plugins without losing control."], [
section("load", "When configuration is read",
    """<p>tmux reads its configuration when the server starts, not every time you create a session. The usual personal file is <code>~/.tmux.conf</code>; modern versions also support XDG locations. Check FILES in your installed manual for search order. A <code>-f</code> argument chooses a file at server startup.</p>""" +
    code("tmux source-file ~/.tmux.conf", "Reload into an existing server") +
    """<p>Reloading executes the file’s commands in order. It is not a transactional reset: earlier lines may apply even if a later line fails. Removing a setting from the file does not unset its already-loaded value. Use <code>set-option -u</code> for an appropriate local override or explicitly restore the intended global value.</p>
    <p>Test major changes on an isolated server with <code>tmux -L config-check -f /path/to/test.conf new -s check</code>. Opening a new session on an existing server does not retest startup configuration.</p>"""),
section("starter", "A small, commented starting point",
    """<p>Read this before copying. The default prefix stays Ctrl+b so the lesson shortcuts continue to match. The same file is available as a <a href="examples/tmux.conf" download>downloadable starter config</a>.</p>""" +
    code("""# Increase scrollback for panes created after this setting.
set -g history-limit 20000
# Let the mouse select panes, resize borders and enter copy mode.
set -g mouse on
# Choose explicit copy-mode keys.
setw -g mode-keys vi
# Human-friendly indexes for NEW windows and panes.
set -g base-index 1
setw -g pane-base-index 1
set -g renumber-windows on
# Open splits in the current pane's directory.
bind % split-window -h -c "#{pane_current_path}"
bind '"' split-window -v -c "#{pane_current_path}"
bind c new-window -c "#{pane_current_path}"
# Reload the usual personal config; commands are separated by a semicolon.
bind r source-file ~/.tmux.conf \\; display-message "Config reloaded"
# Keep status information simple and readable.
set -g status-left "[#S] "
set -g status-right "#{pane_current_command} | %H:%M"
set -g status-interval 5""", "Configuration — ~/.tmux.conf") +
    """<p><code>set</code> aliases <code>set-option</code>; <code>setw</code> aliases <code>set-window-option</code>. Quoting <code>#{pane_current_path}</code> keeps spaces in paths intact. A command containing semicolons has two parsing layers when entered through a shell; escape the separator as shown in shell/config examples.</p>"""),
section("scope", "Set the right option at the right scope",
    table(["Scope", "Inspect", "Meaning"], [
    ["Server", "<code>tmux show-options -s</code>", "One value for the whole server, such as escape-time or set-clipboard."],
    ["Global session defaults", "<code>tmux show-options -g</code>", "Fallback values for sessions without local overrides."],
    ["One session", "<code>tmux show-options -t api</code>", "Session-specific values. Add -A to include inherited values."],
    ["Global window defaults", "<code>tmux show-window-options -g</code>", "Defaults for window options such as mode-keys."],
    ["One window", "<code>tmux show-window-options -t api:0</code>", "Overrides for the chosen window."],
    ["One pane", "<code>tmux show-options -p -t %3</code>", "Supported pane options; inspect the manual for inheritance rules."]]) +
    """<p>For example, <code>set -w synchronize-panes on</code> affects a window. It copies keyboard input into other panes in that window, so turn it off immediately after a controlled task. A global default can be masked by a local override. Inspect both before concluding that reload failed.</p>"""),
section("bindings", "Key tables and a deliberate prefix change",
    code("""set -g prefix C-a
unbind C-b
bind C-a send-prefix
bind -r H resize-pane -L 5
bind -r L resize-pane -R 5""", "Optional configuration — changes all later prefix sequences") +
    """<p><code>bind</code> uses the prefix table by default. <code>-r</code> allows repetition within the repeat-time interval. <code>bind -n</code> creates a root-table binding with no prefix and can steal keys from applications. <code>bind -T copy-mode-vi</code> affects only that copy-mode table.</p>
    <p>If you choose Ctrl+a, it conflicts with a common shell start-of-line shortcut. Press Ctrl+a twice with the shown binding to send a literal Ctrl+a to the program. Keep a recovery route: from another shell, restore <code>tmux set -g prefix C-b</code> and <code>tmux bind C-b send-prefix</code>.</p>"""),
section("plugins", "Colors, status and plugins: add only what you understand",
    """<p>Check <code>infocmp tmux-256color</code> before choosing <code>set -g default-terminal "tmux-256color"</code>. Programs use TERM to find terminal capabilities; do not force an unrelated TERM in shell startup files. True-color features should describe the actual outer terminal, not a guessed one. The troubleshooting clinic covers the diagnosis.</p>
    <p>The status line uses formats such as <code>#S</code> (session), <code>#I</code> (window index), <code>#W</code> (window name), and <code>#{pane_current_path}</code>. A <code>#(shell command)</code> segment launches a shell command; expensive status commands can slow down refreshes.</p>
    <p>TPM manages third-party plugins; tmux-resurrect saves layout and selected program state; tmux-continuum can automate periodic saves. These tools are optional. Inspect their source and version-specific instructions before installing because plugins execute code as your user. They do not checkpoint arbitrary process memory or resurrect a running transfer after a reboot. Try native features first, then add one plugin and verify what it changes.</p>""")
], ["Reload executes commands; it does not undo removed settings.", "Scope and inheritance explain many configuration surprises.", "Keep a small config, inspect active bindings, and add plugins deliberately."], "configuration")

lesson("workflow", "Everyday development & real work", 25,
    "Turn shortcuts into a repeatable working habit for coding, testing, observing and recovering context.",
    ["Design a useful project layout.", "Capture evidence without confusing logs and scrollback.", "Recognize when a service manager is the better tool."], [
section("project", "A workspace with a purpose",
    """<p>You are debugging an API that sometimes returns 500. Give the editor its own window. Put the development server and its recent logs in a second window. Keep tests in a third. Resist splitting everything into unreadable boxes: only show two tasks together when comparing them helps.</p>""" +
    code("""tmux new-session -s api -n editor -c "$HOME/projects/api"
# Run these from a shell inside the new session.
tmux new-window -n server -c "$HOME/projects/api"
tmux split-window -h -c "#{pane_current_path}"
tmux new-window -n tests -c "$HOME/projects/api"
tmux select-window -t api:editor""") +
    """<p>Replace the path with an existing directory. Run your project’s documented editor, server and test commands in the corresponding panes. A pane is a normal shell; tmux does not install dependencies or configure the application for you.</p>"""),
section("loop", "A practical debugging loop",
    flow([("Reproduce", "Run one failing request"), ("Observe", "Read the matching log and time"), ("Change", "Edit one hypothesis"), ("Verify", "Run focused tests, then repeat")]) +
    """<ol><li>Zoom the log pane when you need to read a long stack trace.</li><li>Enter copy mode and search backward for the error. Copy only the relevant context.</li><li>Return to the editor with the window chooser or the last-window shortcut.</li><li>Run a focused test; do not restart every service unnecessarily.</li><li>Detach for a break. Reattach by session name and inspect whether the job is still running.</li></ol>"""),
section("evidence", "Capture what happened",
    code("tmux capture-pane -p -S -200 -t %3 > ~/tmux-recent-output.txt\n# Start recording NEW pane output; inspect its contents before sharing.\ntmux pipe-pane -o -t %3 'cat >> \"$HOME/tmux-live-output.log\"'\n# Stop this pipe after collecting enough evidence.\ntmux pipe-pane -t %3") +
    """<p>Replace <code>%3</code> with an inspected pane ID. <code>capture-pane</code> captures the rendered pane and available history; it cannot recover output discarded before capture. <code>-S -200</code> begins 200 lines back; <code>-S -</code> starts at the beginning of retained history.</p>
    <p><code>pipe-pane</code> streams new terminal output to a command; it is not retroactive and can include control sequences. <code>-o</code> opens only if there is no existing pipe. Redirection after <code>capture-pane</code> is performed by the shell running the client command; <code>pipe-pane</code> runs its command on the server host.</p>"""),
section("jobs", "Long jobs: know the boundary",
    """<p>Before leaving a long migration, report or model training job, verify that it started in the intended remote pane, has a writable output path, and records useful progress. A tmux status line does not prove the application is healthy. A job can fail while the session remains perfectly alive.</p>""" +
    table(["Need", "Suitable approach"], [
    ["Interactive work you want to revisit", "tmux with named sessions and persistent application logs."],
    ["One detached command", "A carefully understood shell job / nohup workflow may suffice; it has different I/O and lifecycle behavior."],
    ["Service that should restart after failure or reboot", "A service manager, such as systemd where available."],
    ["Recurring or resource-scheduled batch jobs", "A scheduler or platform-native job system with retries, limits and durable outputs."],
    ["Container application", "Let the platform supervise the application; tmux inside a short-lived container shares that container’s lifetime."]]) +
    """<p>End the day by recording the task status, saving edited files, checking running jobs, and detaching. End a project workspace by stopping applications cleanly, inspecting panes, and then closing only the intended session.</p>""")
], ["Organize by task, not by the maximum number of panes.", "Capture-pane is a snapshot; pipe-pane records future output.", "tmux preserves interaction, while applications and supervisors own recovery."], "workflow")

lesson("remote", "SSH, nested tmux & collaboration", 30,
    "Keep remote work reachable, diagnose connection layers and share a terminal intentionally.",
    ["Run tmux on the right host and reconnect after an SSH drop.", "Handle nested prefixes and shared clients.", "Diagnose user, socket, terminal and environment mismatches."], [
section("ssh", "Persistence belongs on the remote host",
    code("ssh user@server.example\n# Now on the server:\ntmux new-session -A -s deploy") +
    flow([("Laptop terminal", "Can close or lose the network"), ("SSH connection", "Carries input and screen updates"), ("Remote tmux server", "Owns the session"), ("Remote job", "Keeps running while its host and server survive")]) +
    """<p>Start the job inside the remote tmux session. After a disconnect, reconnect to the same host as the same user, run <code>tmux ls</code>, and attach by name. If you instead run local tmux and then SSH from one pane, local tmux preserves the local SSH client; it does not automatically protect a remote shell when that SSH connection dies.</p>
    <p>For a direct interactive attach, <code>ssh -t user@server.example 'tmux new-session -A -s deploy'</code> allocates a terminal for tmux. Noninteractive SSH commands do not always have one. A load-balanced hostname may land you on another machine; check <code>hostname</code> before assuming sessions disappeared.</p>"""),
section("nested", "When there are two prefix layers",
    """<p>Sometimes local tmux contains SSH into a second tmux. With Ctrl+b at both layers, the first prefix is consumed by the outer tmux. Its default <code>send-prefix</code> binding lets a second Ctrl+b pass one literal prefix to the inner layer.</p>
    <div class="keyline"><kbd>Ctrl+b</kbd> → <kbd>Ctrl+b</kbd> → <kbd>d</kbd></div>
    <p>With the default binding, that sequence detaches the inner tmux. Prefix then <kbd>d</kbd> detaches the outer one. A distinct outer prefix is another approach. Check <code>list-keys -T prefix</code> if behavior differs.</p>""" +
    note("Nested-session warning", "Inside one tmux server, use switch-client to change sessions. The warning about nesting is useful. Unsetting TMUX just to silence it can hide a mistaken workflow; reserve nesting for a deliberate multi-host or separate-server setup.", "warn")),
section("share", "Attach together, with clear ownership",
    code("tmux list-clients\n# Another terminal, same host/user/socket:\ntmux attach-session -t api\n# Observe with a read-only client:\ntmux attach-session -r -t api") +
    """<p>Two writable clients can type into the same active pane at the same time. Agree who is driving. A read-only client reduces accidental keystrokes but is not a secrecy boundary: its viewer can still see displayed secrets. <code>attach -d</code> detaches the other clients, so do not use it casually during a shared session.</p>
    <p>For separate current-window choices with the same windows, create grouped sessions as shown in the advanced lesson. Pane focus and program state are still shared. For separate users, modern tmux has <code>server-access</code>, but socket path permissions and per-user authorization must both be correct. Do not make a tmux socket world-writable. Use an approved collaboration setup and grant access only to trusted users.</p>"""),
section("environment", "Reconnect does not refresh every existing shell",
    """<p>The server and its sessions hold environment values. On attach, <code>update-environment</code> can refresh selected session variables such as SSH agent or display settings. Existing shell processes keep their inherited environment. A newly created pane may therefore behave differently from an older one.</p>""" +
    code("tmux show-environment -t api\ntmux show-options -g update-environment\nprintf 'Agent socket: %s\\n' \"$SSH_AUTH_SOCK\"\nprintf 'Terminal type: %s\\n' \"$TERM\"") +
    """<p>A stale SSH_AUTH_SOCK can make an agent-backed Git command fail after reconnecting. Inspect the new connection’s environment, confirm forwarding was intentionally enabled, and open a new pane or carefully update the affected shell. Do not blindly evaluate arbitrary environment output. DISPLAY and Wayland clipboard variables have similar lifetime issues.</p>
    <p>If the screen has odd dimensions, inspect <code>list-clients</code> for a small or stale attached client and examine <code>window-size</code>. Modern tmux supports size policies including latest, smallest, largest and manual. Choose intentionally for the team rather than disconnecting someone without explanation.</p>""")
], ["Run remote jobs inside remote tmux.", "Reconnect to the same host, user and socket.", "Sharing a session shares programs; reattaching does not rewrite old shells’ environments."], "remote")

lesson("automation", "Script repeatable workspaces", 40,
    "Turn a fragile list of commands into a repeatable project launcher with explicit targets and observable results.",
    ["Create a workspace without duplicate windows.", "Capture IDs instead of guessing indexes.", "Understand send-keys, quoting, exit status and synchronization."], [
section("recipe", "Start with an inspectable launcher",
    """<p>A launcher should handle both first run and later runs. Check whether the session exists, create it only if missing, capture the created pane ID, and use that ID for the split. The <a href="examples/workspace.sh" download>downloadable workspace script</a> uses a named server and a known config, so it cannot modify your ordinary server.</p>""" +
    code("""#!/bin/sh
set -eu
project_dir="$1"
session="kt-project"
if ! tmux -L kt-tmux has-session -t "=$session" 2>/dev/null; then
  pane=$(tmux -L kt-tmux -f /dev/null new-session -d -P \\
    -F '#{pane_id}' -s "$session" -n editor -c "$project_dir")
  tmux -L kt-tmux split-window -h -t "$pane" -c "$project_dir"
  tmux -L kt-tmux new-window -t "$session:" -n tests -c "$project_dir"
  tmux -L kt-tmux select-window -t "$session:editor"
fi
tmux -L kt-tmux attach-session -t "=$session"
""", "Illustrative shell script — run outside tmux; directory must exist") +
    """<p><code>-d</code> creates detached; <code>-P -F</code> prints the requested format. Capture that output immediately instead of assuming the first pane is <code>%0</code>. The downloadable version also validates the directory and avoids accidental nesting. Run it from another terminal if you are already attached to a different tmux server.</p>
    <p>This is repeatable for sequential runs, not a transactional or race-free deployment system. Two simultaneous launchers can both pass the existence check. Partially created sessions also need inspection before reuse. For concurrency, introduce a lock or synchronize creation explicitly.</p>"""),
section("sending", "Sending text is not a job API",
    code("tmux send-keys -t %3 -l 'printf \"hello from tmux\\n\"'\ntmux send-keys -t %3 Enter") +
    """<p><code>-l</code> sends literal text; the separate Enter submits it. Without <code>-l</code>, key names such as <code>Enter</code> and <code>C-c</code> are interpreted as keys. The target might contain an editor, a password prompt or a busy shell. A successful <code>send-keys</code> means input was sent, not that the intended command ran or succeeded.</p>
    <p>For deterministic jobs, create a pane with a known command, record its exit status, and use a real completion signal. With <code>remain-on-exit</code>, a finished pane stays visible and can expose <code>pane_dead_status</code>. Validate the workflow on your version before using it for important automation.</p>"""),
section("formats", "Formats give you structured observations",
    code("tmux list-panes -a -F '#{pane_id} | #{pane_current_command} | #{pane_current_path}'\ntmux display-message -p -t %3 '#{session_name}:#{window_index}.#{pane_index}'\ntmux display-message -p '#{version}'\ntmux show-hooks -g") +
    """<p>A format expression is expanded by tmux, not your shell. Single-quote it in shell commands. Formats also support conditionals and comparisons; a status example is <code>#{?pane_in_mode,COPY,TYPE}</code>. Inspect actual values before building complex expressions.</p>
    <p><code>if-shell</code> runs a shell test by default. With <code>-F</code> it evaluates a tmux format instead. <code>run-shell</code> executes a command outside a pane; <code>-b</code> runs it in the background. Never interpolate untrusted text into shell commands in status formats, hooks or scripts.</p>"""),
section("sync", "Wait for a signal, not an arbitrary sleep",
    code("""# In one shell:
tmux wait-for task-finished
# In another shell using the SAME server:
tmux wait-for -S task-finished""") +
    """<p><code>wait-for</code> coordinates commands through a channel; <code>-S</code> signals it, and <code>-L</code>/<code>-U</code> lock and unlock a channel. Waiting does not prove success. Your worker should write an exit code and reliably signal on both success and failure. An absent signal can leave a waiter blocked indefinitely, so use your automation environment’s timeout.</p>
    <p>Hooks such as <code>after-new-window</code> run tmux commands after events. They can enforce a layout or notify you, but expensive or recursive hooks create hard-to-explain behavior. Inspect <code>show-hooks</code> while debugging. Command sequences run in order; a launched background job is not automatically finished when the next command runs.</p>""")
], ["Capture IDs and quote paths instead of assuming indexes.", "A successful send-keys call is not a successful job.", "Make completion, failure, concurrency and cleanup explicit."], "automation")

lesson("advanced", "Advanced tools & version boundaries", 35,
    "Understand the less common tools, when they help, and which assumptions need checking before use.",
    ["Use isolated servers, grouped sessions and saved layouts.", "Understand popups, hooks, control mode and recovery limits.", "Locate version-specific capabilities in the manual."], [
section("servers", "Isolation is a useful debugging tool",
    code("tmux -L experiment -f /dev/null new-session -s clean\n# From an outside shell, inspect only this server:\ntmux -L experiment list-sessions") +
    """<p>The server is selected by socket. <code>-L</code> is a socket name; <code>-S</code> supplies a complete path. Isolation separates config, sessions and buffers, but it is not a security sandbox: programs still run with your user permissions and can access your files.</p>
    <p>The same tmux binary can connect to a server started by an older binary after a package upgrade. Compare <code>tmux -V</code> with <code>tmux display-message -p '#{version}'</code>. Do not kill the old server until its work is finished or deliberately moved to a recoverable state.</p>"""),
section("groups", "Share windows, keep separate current-window choices",
    code("tmux new-session -d -t api -s api-review\ntmux attach-session -t api-review") +
    """<p><code>new-session -t api</code> joins a session group based on the existing session. Group members share the window list: creating or removing a linked window is reflected across the group. Their current and previous window choices are independent. Panes and the programs they contain are still shared, including active pane selection within a shared window.</p>
    <p>Use this when two trusted viewers want to inspect different windows of one project. Create independent sessions and independent windows if each person needs isolated programs.</p>"""),
section("layouts", "Save arrangements; understand what is not saved",
    code("tmux display-message -p '#{window_layout}'\n# Later, with a compatible set of panes:\n# tmux select-layout -t api:0 'PASTE_THE_SAVED_LAYOUT_STRING'") +
    """<p>A layout string describes pane geometry. It does not save files, shell variables, application state or live process memory. Layout restoration works with the panes available at restoration time; it is not a full session backup.</p>
    <p><code>remain-on-exit</code> keeps a pane visible after its main program finishes. Inspect <code>pane_dead</code> and <code>pane_dead_status</code>; use <code>respawn-pane</code> only when you intend to restart its command. <code>respawn-pane -k</code> can replace a still-running program and lose unsaved state.</p>"""),
section("toolbox", "Tools worth recognizing",
    table(["Tool", "What it is for", "Important boundary"], [
    ["<code>display-popup -E</code>", "A temporary shell or small tool over the current view (tmux 3.2+).", "A popup is not another ordinary layout pane; closing it may end its command."],
    ["<code>display-menu</code>", "Build a menu of tmux actions.", "Bindings and menu entries execute commands; inspect scripts you import."],
    ["<code>command-prompt</code> / <code>confirm-before</code>", "Ask for input or confirm a risky tmux command.", "Handle shell quoting if that input will reach a shell."],
    ["<code>monitor-activity</code> / <code>monitor-silence</code>", "Notice output or inactivity in another window.", "Activity is not equivalent to job success or service health."],
    ["<code>lock-client</code> / <code>lock-session</code>", "Invoke the configured lock command.", "Not a replacement for OS access control; another authorized client can still have access."],
    ["<code>tmux -C</code>", "Control mode for programs integrating with tmux’s protocol.", "It is a machine interface, not the normal interactive terminal UI."],
    ["<code>set-hook</code>", "Respond to tmux lifecycle events.", "Inspect hooks when behavior happens unexpectedly."],
    ["<code>server-access</code>", "Permit or revoke supported multiuser server access.", "Version-specific; Unix socket permissions also matter. Use least privilege."]]) +
    code("tmux display-popup -E -w 80% -h 70%", "Optional tmux 3.2+ popup from an attached session") +
    """<p>Use <code>exit</code> to close this popup shell. Menus and popups work well for a temporary chooser or help view. Keep long-lived work in an ordinary pane unless you deliberately want the popup lifecycle.</p>"""),
section("versions", "Features evolve; inspect before assuming",
    """<p>Newer tmux documentation may describe floating panes, switch mode, newer client flags and additional format modifiers that an older packaged version does not implement. The upstream getting-started guide labels floating panes and switch mode as 3.8 features. They are optional extensions, not prerequisites for this course’s workflows.</p>
    <p>Before adopting a feature, run <code>tmux -V</code>, inspect the server version, use <code>tmux list-commands</code> for syntax and <code>tmux list-keys</code> for actual bindings, then read the matching installed manual. An “unknown command” or “invalid option” can be a version mismatch rather than a typing error.</p>
    <p>For complete coverage beyond this curriculum’s examples, read the manual sections on command parsing, key bindings, clients and sessions, windows and panes, buffers, options, formats, hooks, styles, mouse support and control mode. The reference page links those primary sources.</p>""")
], ["A separate server isolates tmux state, not user permissions.", "Grouped sessions share windows; layout files do not preserve processes.", "Check both client and server versions before using new features."], "advanced")

from practice_content import ISSUES, LABS

def issues_html():
    return ''.join('<details class="issue" id="' + id + '" data-category="' + category + '"><summary><span class="chip">' + category + '</span> ' + escape(title) + '</summary><h3>Likely cause</h3><p>' + escape(cause) + '</p><h3>Inspect before changing anything</h3><p>' + escape(inspect) + '</p><h3>Fix the cause</h3><p>' + escape(fix) + '</p><h3>Verify</h3><p>' + escape(verify) + '</p><a href="' + link + '.html">Revisit the ' + link.replace("-", " ") + ' lesson →</a></details>' for id,category,title,cause,inspect,fix,verify,link in ISSUES)

def labs_html():
    result = ''
    for lab in LABS:
        result += '<article class="lab" id="' + lab['id'] + '"><p class="eyebrow">' + lab['level'] + ' · ' + lab['time'] + '</p><h3>' + lab['title'] + '</h3><p><b>Outcome:</b> ' + lab['goal'] + '</p><p><b>Before you start:</b> ' + lab['setup'] + '</p>' + code(lab['command'], 'Real terminal lab — read the comments between steps') + '<h4>Observe and check off yourself</h4>'
        result += ''.join('<label class="lab-step"><input type="checkbox" data-lab="' + lab['id'] + '-' + str(i) + '"> ' + step + '</label>' for i,step in enumerate(lab['steps']))
        result += '<details class="reveal"><summary>Predict: ' + lab['predict'] + '</summary><div><p>' + lab['solution'] + '</p></div></details><p><b>If it goes wrong:</b> ' + lab['problem'] + '</p><p><b>Cleanup:</b> ' + lab['cleanup'] + '</p></article>'
    return result

COMMANDS = [
("sessions", "Create named session", "", "tmux new-session -s api", "Run outside tmux; creates and attaches."),
("sessions", "Create or attach", "", "tmux new-session -A -s api", "Inspect old state if the session already exists."),
("sessions", "Detach", "d", "tmux detach-client", "Leaves pane programs running."),
("sessions", "List sessions", "s", "tmux list-sessions", "The shortcut opens the interactive chooser."),
("sessions", "Attach", "", "tmux attach-session -t api", "Use the right host, user and socket."),
("sessions", "Switch session", "", "tmux switch-client -t api", "For an already-attached client."),
("sessions", "Rename session", "$", "tmux rename-session -t api backend", "The shortcut prompts for a name."),
("sessions", "Read-only attach", "", "tmux attach-session -r -t api", "Prevents normal input; contents remain visible."),
("sessions", "Kill one session", "", "tmux kill-session -t '=api'", "Destructive: inspect and stop work first."),
("windows", "Create window", "c", "tmux new-window -n tests", "Starts a program, usually your shell."),
("windows", "Rename window", ",", "tmux rename-window tests", "Gives the current window a useful name."),
("windows", "Next / previous window", "n / p", "tmux next-window / tmux previous-window", "Two alternative commands, not one shell line."),
("windows", "Last window", "l", "tmux last-window", "Jump between two tasks."),
("windows", "Choose a window", "w", "tmux choose-tree -w", "Arrows move; Enter selects; q leaves."),
("windows", "Select by target", "0 … 9", "tmux select-window -t api:2", "Window index or inspected name/ID."),
("windows", "Move / swap", ".", "tmux move-window -s api:2 -t api:5", "Inspect the destination before replacing anything."),
("panes", "Split left / right", "%", "tmux split-window -h", "Horizontal placement, vertical divider."),
("panes", "Split top / bottom", '"', "tmux split-window -v", "Vertical placement, horizontal divider."),
("panes", "Select neighboring pane", "Arrow", "tmux select-pane -L", "Use -L, -R, -U or -D."),
("panes", "Cycle active pane", "o", "tmux select-pane -t :.+", "Focus controls where typing goes."),
("panes", "Display pane numbers", "q", "tmux display-panes", "Press a displayed number before it disappears."),
("panes", "Zoom / unzoom", "z", "tmux resize-pane -Z", "Other panes remain alive."),
("panes", "Cycle layouts", "Space", "tmux next-layout", "Choose tiled or main-vertical explicitly if preferred."),
("panes", "Resize right", "Ctrl+Right", "tmux resize-pane -R 5", "The command moves the boundary by five cells where possible."),
("panes", "Break pane to a window", "!", "tmux break-pane", "Moves the program without restarting it."),
("panes", "Join existing pane", "", "tmux join-pane -s %3 -t %1 -h", "Use inspected distinct source and target pane IDs."),
("panes", "Close pane", "x", "tmux kill-pane -t %3", "Destructive. The shortcut asks for confirmation."),
("copy", "Enter copy mode", "[", "tmux copy-mode", "Program continues; your view stops following output."),
("copy", "Paste latest buffer", "]", "tmux paste-buffer", "Inspect pasted commands before executing."),
("copy", "Choose buffer", "=", "tmux choose-buffer", "Internal tmux buffers, not your OS clipboard."),
("copy", "Inspect buffer", "", "tmux show-buffer", "First check when diagnosing clipboard problems."),
("copy", "Capture retained output", "", "tmux capture-pane -p -S -200 -t %3", "Snapshot, not full historical process logs."),
("configuration", "Open command prompt", ":", "", "Enter tmux commands without the tmux executable prefix."),
("configuration", "Show key bindings", "?", "tmux list-keys", "Actual config may override defaults."),
("configuration", "Reload config", "", "tmux source-file ~/.tmux.conf", "Executes commands; does not undo removed lines."),
("configuration", "Enable mouse", "", "tmux set -g mouse on", "Supports pane selection, resizing and scrolling."),
("configuration", "Disable broadcast", "", "tmux set-window-option synchronize-panes off", "Stops duplicated input to other panes."),
("automation", "List pane IDs", "", "tmux list-panes -a -F '#{pane_id} #{pane_current_command}'", "IDs are stable for the lifetime of each pane."),
("automation", "Send literal text", "", "tmux send-keys -t %3 -l 'text'", "Does not submit Enter or prove application success."),
("advanced", "Inspect server version", "", "tmux display-message -p '#{version}'", "Can differ from tmux -V after a package upgrade."),
("advanced", "Inspect command syntax", "", "tmux list-commands", "Check capabilities of the installed version."),
("advanced", "Create isolated server", "", "tmux -L sandbox -f /dev/null new -s learn", "Use the same -L in later outside-shell commands."),
]

lesson("troubleshooting", "The troubleshooting clinic", 40,
    "Find the symptom, gather evidence, fix the cause and verify the result. Twenty-four cases cover everyday surprises and difficult failures.",
    ["Diagnose before restarting or killing anything.", "Separate input, display, process and connection failures.", "Check the result of each fix."], [
section("method", "A repeatable diagnosis",
    flow([("Symptom", "Describe exactly what changed"), ("Context", "Host, user, socket, version, target"), ("Evidence", "Options, key tables, logs, process state"), ("Small fix", "Change one relevant thing"), ("Verify", "Repeat the failed action safely")]) +
    code("hostname\nid -un\ntmux -V\ntmux list-sessions\ntmux list-clients\ntmux list-panes -a -F '#{pane_id} #{pane_current_command}'") +
    """<p>Use the same <code>-L</code> or <code>-S</code> as the affected server. Not every command succeeds if no server exists; that failure is part of the evidence. A clean server with <code>-f /dev/null</code> helps distinguish a config problem from an application or terminal problem.</p>"""),
section("cases", "Find your symptom",
    """<div class="filters only-js"><label class="field">Search symptoms, causes or fixes<input id="issue-search" type="search" placeholder="clipboard, frozen, SSH, colors…"></label><label class="field">Category<select id="issue-category"><option value="all">All categories</option>""" +
    ''.join('<option>' + x + '</option>' for x in sorted(set(i[1] for i in ISSUES))) +
    """</select></label></div><p id="issue-count" class="meta" aria-live="polite">24 troubleshooting cases</p><div id="issues">""" + issues_html() + '</div><p id="issue-empty" class="empty" hidden>No matching cases. Try a broader term such as “session” or “copy”.</p>'),
section("report", "When you need to report a reproducible bug",
    """<p>Record the client and server version, OS, terminal emulator, TERM inside and outside tmux, minimal config, exact reproduction steps, expected result and actual result. Test whether it occurs on a clean named server. <code>tmux -vv</code> can generate verbose log files in the current directory; use it only in a scratch directory on a disposable server.</p>
    <p>Verbose logs and terminal captures may contain the text you typed or displayed. Review and redact them before sharing. A useful report demonstrates a minimal failure rather than attaching your entire private workspace.</p>""")
], ["Context first: host, user, socket, version, target.", "Prefer a small reversible fix with observable evidence.", "Restarting is a lifecycle decision, not a universal diagnosis."], "troubleshooting")

lesson("practice", "Eight real-world terminal labs", 60,
    "Use an actual tmux installation to turn recognition into skill. Each lab includes an outcome, commands, predictions, common failures and cleanup.",
    ["Complete the setup, workspace, copy, config and remote labs.", "Build a repeatable launcher and diagnose intentional faults.", "Finish a capstone with a clear handoff and cleanup."], [
section("ground-rules", "Practise with a named lab server",
    note("Real terminal, self-reported checklist", "These commands run only when you run them in your terminal. Checkboxes record your observations; the website cannot verify your local or remote machine. The browser playground is a separate simulation.") +
    """<p>Use <code>-L kt-tmux</code> on outside-shell commands for local labs. Inside its panes, ordinary <code>tmux</code> commands normally use the current server through TMUX. The SSH lab uses a separate remote socket named <code>kt-remote</code>. Existing sessions may carry options from earlier labs; inspect them before assuming clean defaults.</p>
    <p>Do not paste an entire lab block without reading its comments: some steps require detaching, switching hosts or stopping a loop first. Example output and predictions are not commands. The full labs take about 3 hours; the 60-minute module estimate is for an initial pass.</p>
    <p id="lab-progress" class="meta" aria-live="polite"></p><progress id="lab-meter" max="1" value="0" aria-label="Self-reported lab steps"></progress>"""),
section("labs", "Work through the labs", labs_html())
], ["Explain your prediction before running a command.", "Check evidence in the actual terminal before ticking a step.", "End only the inspected lab session; leave unrelated work alone."])

lesson("playground", "The visual tmux playground", 25,
    "Try a safe model of sessions, windows, panes and detachment. Every action changes a visible workspace and explains its effect.",
    ["Complete six missions using buttons or supported commands.", "Observe focus, zoom and session lifecycle changes.", "Transfer the practice to the real terminal labs."], [
section("simulator", "Learn by changing the workspace",
    note("A learning simulation", "This is not a shell or a real tmux process. It models a documented subset of commands, defaults and key sequences. It does not run programs, access your files, connect with SSH, or model advanced targeting/configuration. Unsupported commands return an explanation.") +
    '<div id="playground"></div><noscript><p>The simulator needs JavaScript. Use the <a href="practice.html">real-terminal labs</a> instead; every lab remains readable here.</p></noscript>'),
section("supported", "The simulator’s command vocabulary",
    code("""tmux new-session -s api
tmux list-sessions
tmux attach-session -t api
tmux switch-client -t api
tmux detach-client
tmux new-window -n tests
tmux rename-window editor
tmux select-window -t 0
tmux split-window -h
tmux split-window -v
tmux select-pane -t 0
tmux resize-pane -Z
tmux select-layout tiled
tmux next-layout
tmux kill-pane
tmux kill-session -t api
help""", "Supported simulated commands — explicit aliases are listed by help") +
    """<p>Inside the simulator, the visible buttons are equivalent actions. The command field also accepts supported tmux commands without the leading <code>tmux</code>. Targets are limited to the simple names and indexes shown in the model. Shell pipelines, compound commands, arbitrary flags, configuration, full-screen applications and filesystem paths are not interpreted.</p>
    <p>Keyboard practice is scoped to the playground: focus its command input, then press Ctrl+b followed by %, double quote, c, o, n, p, l, z, d, a window digit or Space (cycle layouts). The on-screen buttons provide the same actions if your browser captures a key. Ctrl+b outside the playground is never intercepted.</p>""")
], ["A session groups windows; a window arranges panes.", "Focus, zoom and detach change different parts of the model.", "The simulator teaches state changes; real labs teach your terminal environment."])

lesson("quiz", "Knowledge check: explain your choice", 30,
    "Forty-eight scenario questions cover the complete path. Every answer explains the reasoning, including why a tempting alternative fails.",
    ["Test all topics or focus on one area.", "Review mistakes with links to the relevant lesson.", "Separate a remembered answer from practical confidence."], [
section("assessment", "Test your understanding",
    """<p>Answer before checking the lesson. Your first submitted choice is saved until you choose “Retry missed” or start a fresh attempt. You can navigate back to inspect explanations. Scores reflect this browser’s current attempt, not a certification.</p>
    <div id="quiz"></div><noscript><p>Interactive grading needs JavaScript. Use the printable question bank below, with answers in expandable sections.</p></noscript>
    <details class="reveal"><summary>Open the complete question bank for reading or printing</summary><div id="static-questions"></div></details>""")
], ["A correct explanation matters more than memorizing a key.", "Revisit the lesson behind every missed scenario.", "Repeat the real lab when uncertainty is about behavior, not terminology."])

lesson("recap", "Recall, review & keep your progress", 15,
    "Refresh the high-value commands, reveal answers only after trying, and return to difficult cards later.",
    ["Recall a command from the task it performs.", "Review weak cards instead of rereading everything.", "Export your local learning progress."], [
section("cards", "Active recall cards",
    """<p>Read the task, say the key or command aloud, then reveal. “Know it” schedules this card for tomorrow, then in 3, 7, 14 and 30 days after successive successful reviews. “Again” resets it for immediate review. The review mode includes due and unseen cards; All cards lets you practise at any time.</p><div id="flashcards"></div><noscript><p>Use the <a href="reference.html">command reference</a> as a paper-style recall list: cover the command column and test yourself.</p></noscript>"""),
section("five-minute", "The five-minute mental reset",
    flow([("30 seconds", "Name server → session → window → pane"), ("1 minute", "Recall create, detach and attach"), ("1 minute", "Recall split, focus and zoom"), ("1 minute", "Recall copy mode and paste"), ("90 seconds", "Diagnose one case and verify the fix")]) +
    """<details class="reveal"><summary>Explain: why did my job survive closing the terminal but not a reboot?</summary><div>The client connection ended when the terminal closed, but the server and pane process were still running. Reboot stopped those processes. Saved layouts do not save process memory.</div></details>
    <details class="reveal"><summary>Explain: why did copying into another tmux pane work but desktop paste fail?</summary><div>The tmux paste buffer is separate from the desktop clipboard. The internal copy path worked; diagnose OSC 52 support or a local copy-pipe command and its display environment.</div></details>
    <details class="reveal"><summary>Explain: why did my script type the right command but produce the wrong result?</summary><div>Input goes to the foreground program in the target pane. The pane may be busy, at another prompt or incorrectly targeted. send-keys success is not application success.</div></details>"""),
section("progress", "Your progress belongs to this browser",
    """<p>Completed lessons, lab checkboxes, quiz answers, browser mission completions and recall schedules are saved locally when storage is available. They are learning aids, not evidence of verified terminal work. Export before switching browsers or clearing site data.</p>
    <div class="actions only-js"><button class="btn" id="export-progress">Export progress JSON</button><button class="btn" id="import-trigger">Import progress JSON</button><input type="file" id="import-progress" aria-label="Choose a progress backup" accept=".json,application/json" hidden><button class="btn" id="reset-progress">Reset learning progress</button></div><p id="progress-message" role="status"></p>
    <p id="progress-summary"></p>""")
], ["Retrieve first; reveal second.", "Use Again for uncertain cards and revisit the related real lab.", "Back up browser-local progress before clearing it."])

lesson("reference", "The field reference", 15,
    "A searchable command sheet, practical glossary and primary sources for deeper study.",
    ["Find the right command by task.", "Use defaults without assuming your config matches.", "Know where to check complete, version-specific behavior."], [
section("commands", "Task → shortcut → command",
    """<p>Every shortcut below starts with <kbd>Ctrl+b</kbd>, release, then the listed key. These are default bindings. Commands are shell examples; omit the leading <code>tmux</code> at the tmux command prompt. Replace example names and IDs with inspected targets. A slash between two commands means alternatives, not text to paste.</p>
    <div class="filters only-js"><label class="field">Find a task, key or command<input id="command-search" type="search" placeholder="detach, clipboard, split, ID…"></label><button class="btn" id="print-reference">Print reference</button></div>
    <p id="command-count" class="meta" aria-live="polite"></p>""" +
    '<div id="command-table">' + table(["Task", "Prefix, then", "Shell command", "Remember"], [
        [escape(task), '<kbd>' + escape(key) + '</kbd>' if key else "—", '<code>' + escape(cmd) + '</code>' if cmd else "—", escape(tip)]
        for category,task,key,cmd,tip in COMMANDS
    ]) + '</div><p id="command-empty" class="empty" hidden>No matching commands. Try the troubleshooting clinic for a symptom.</p>'),
section("glossary", "Vocabulary in plain language",
    '<dl class="glossary">' + ''.join('<dt>' + term + '</dt><dd>' + meaning + '</dd>' for term,meaning in [
    ("Client", "A connection from an outside terminal to a tmux server."),
    ("Server", "The process managing sessions, terminal state and pane programs."),
    ("Socket", "A local communication endpoint that identifies a server."),
    ("Session", "A named collection of linked windows, with one current window."),
    ("Window", "An arrangement of panes; may be linked to multiple sessions."),
    ("Pane", "A terminal running a program within a window."),
    ("Prefix", "A key sequence that asks tmux to interpret the next key."),
    ("Key table", "The mapping from keys to actions for a context, such as prefix or copy-mode-vi."),
    ("Copy mode", "A mode for moving through retained output, searching and selecting text."),
    ("Paste buffer", "Text stored inside tmux; distinct from a desktop clipboard."),
    ("Target", "A session, window, pane or client selected by name, index or ID."),
    ("Format", "A tmux-expanded expression such as #{pane_id}, used in status or command output."),
    ("Hook", "A tmux command triggered by a specified event."),
    ("PTY / pseudoterminal", "The terminal interface through which a pane’s programs receive input and produce output."),
    ("TERM / terminfo", "A terminal capability name and its database entry, used by programs to draw correctly."),
    ("OSC 52", "A terminal escape sequence that can transport clipboard text when every layer supports and permits it."),
    ("Control mode", "tmux’s protocol interface for external programs, distinct from its normal terminal UI."),
    ("Session group", "Sessions with a shared window list and independent current-window selection."),
    ]) + '</dl>'),
section("sources", "Primary sources and scope",
    """<p>Core examples use established tmux 3.2+ features. Version-specific sections should be checked against the server actually running your sessions. Documentation reviewed in October 2026; upstream pages can describe features newer than distribution packages.</p>
    <ul class="source-list">
    <li><a href="https://github.com/tmux/tmux/wiki/Getting-Started">Official getting-started guide</a> — concepts, interaction and version-labeled features.</li>
    <li><a href="https://github.com/tmux/tmux/blob/3.5a/tmux.1">Version-pinned tmux 3.5a manual source</a> — stable reference for core command semantics.</li>
    <li><a href="https://man.openbsd.org/tmux">OpenBSD tmux manual</a> — complete reference; may describe a newer version than yours.</li>
    <li><a href="https://github.com/tmux/tmux/wiki/Installing">Official installation guide</a> — packages and source builds.</li>
    <li><a href="https://github.com/tmux/tmux/wiki/Clipboard">Official clipboard guide</a> — OSC 52, terminal capabilities and external clipboard tools.</li>
    <li><a href="https://github.com/tmux/tmux/wiki/FAQ">Official FAQ</a> — TERM, terminal issues and debugging.</li>
    <li><a href="https://github.com/tmux-plugins/tpm">TPM</a>, <a href="https://github.com/tmux-plugins/tmux-resurrect">tmux-resurrect</a>, <a href="https://github.com/tmux-plugins/tmux-continuum">tmux-continuum</a> — optional plugin maintainers’ own documentation.</li>
    </ul><p>This course covers the practical end-to-end workflow and introduces advanced facilities. For every command flag, format operator, hook and version addition, use the installed <code>man tmux</code> and <code>list-commands</code>; an educational reference is not a replacement for the full manual.</p>""")
], ["Inspect the active bindings rather than trusting someone else’s cheatsheet.", "Use explicit targets and understand the scope of close operations.", "The installed manual resolves version-specific details."])
