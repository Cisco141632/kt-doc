"""Troubleshooting cases and real-terminal labs, rendered to static HTML."""
ISSUES = [
("command-not-found", "setup", "tmux: command not found",
 "The current host does not have tmux on PATH, or it is installed for a different environment.",
 "Run command -v tmux; check hostname and the OS. A Windows shell and a WSL Linux shell have different executables.",
 "Install with the package manager for this host, then open a new shell if PATH changed. For SSH work, install on the remote host too.",
 "tmux -V prints a version on the machine that will run the job.", "installation"),
("missing-server", "sessions", "no server running / failed to connect to server",
 "There may be no sessions, or you are querying a different host, user or socket.",
 "Check hostname, id -un and whether earlier commands used -L or -S. Inspect tmux processes before assuming work is lost.",
 "Reconnect to the correct host and server. Use tmux -L kt-tmux ls for the course lab server. If no server exists, create a session; attaching cannot create a lost process.",
 "list-sessions shows the intended session, and attaching reveals its expected work.", "sessions"),
("duplicate", "sessions", "duplicate session: api",
 "A session with that name already exists on the selected server.",
 "Inspect tmux list-sessions and list-windows -t api.",
 "Attach to it, use new-session -A -s api deliberately, or choose another name. Do not kill it just to make the error disappear.",
 "The desired workspace is reused without adding duplicate windows.", "sessions"),
("nested", "remote", "sessions should be nested with care",
 "You are starting a new client from inside an existing tmux pane.",
 "Inspect whether TMUX is set and whether you actually need a second host/server.",
 "For a session on the same server, use tmux switch-client -t name. For intentional nesting, understand both prefixes and which server each command controls.",
 "The session changes without an extra prefix layer, or the deliberate inner layer can be detached independently.", "remote"),
("prefix", "input", "Ctrl+b does nothing",
 "The prefix was changed, the terminal intercepts it, or you are in a different nested layer.",
 "From another shell inspect tmux show-options -g prefix and tmux list-keys -T prefix for the correct server.",
 "Press Ctrl+b, release both keys, then the action. Test on a clean isolated server. Use the configured prefix or restore it deliberately.",
 "The current prefix followed by ? opens the key list.", "configuration"),
("frozen", "input", "The terminal looks frozen",
 "Possibilities include copy mode, a busy application, software flow control, or a dead connection.",
 "Look for copy-mode indicators; check another pane or SSH connection. Consider whether Ctrl+s was pressed with terminal flow control enabled.",
 "Leave copy mode with its cancel key. If XOFF flow control is the cause, Ctrl+q resumes output. Check the application and connection before killing anything.",
 "New output appears and ordinary shell input works in the expected pane.", "copy-mode"),
("split", "panes", "The split went the wrong way",
 "The split direction names describe the axis of pane placement, not the divider.",
 "Compare split-window -h with -v in the playground.",
 "Use -h or prefix % for left/right. Use -v or prefix double quote for top/bottom.",
 "The new pane appears beside or below the original as intended.", "panes"),
("space", "panes", "no space for new pane",
 "The target pane or terminal is too small for another split.",
 "Inspect zoom state and terminal dimensions; check other attached clients and the window-size policy.",
 "Enlarge the terminal, unzoom, choose a layout, close a disposable pane or create a new window.",
 "The split succeeds while both panes remain usable.", "panes"),
("lost-pane", "panes", "Other panes disappeared",
 "The current pane may be zoomed, or you may be viewing a different window/session.",
 "Look for Z in the status line and run list-panes for the expected window.",
 "Toggle prefix z, select the correct window, or use the tree chooser. If the pane was killed, re-create its program from saved files/checkpoints.",
 "The existing layout is visible again; do not mistake a recreated process for a resumed one.", "panes"),
("directory", "panes", "A new pane starts in the wrong directory",
 "Default creation paths need not match the directory currently used by the active shell.",
 "Inspect pwd and the pane_current_path format; check the binding that created the pane.",
 "Use split-window -c \"#{pane_current_path}\" or an explicit existing directory. Bind new-window with -c for the same behavior.",
 "pwd in the new pane matches the intended project directory.", "configuration"),
("clipboard", "copy", "Copy works in tmux, but not in another app",
 "The internal paste buffer works, but the OS clipboard bridge is missing or blocked.",
 "Use show-buffer first. Then inspect set-clipboard, the Ms capability, terminal permissions and any copy-pipe tool.",
 "For SSH, configure supported OSC 52 end to end. For a local desktop use pbcopy, wl-copy or xclip as appropriate, with the right display environment.",
 "A harmless test string pastes both inside tmux and into a separate local application.", "copy-mode"),
("selection", "copy", "Space / Enter does not copy",
 "You may have Emacs mode rather than vi mode, or a customized key table.",
 "Inspect show-window-options -v mode-keys and list-keys -T copy-mode or copy-mode-vi.",
 "Use the active table’s selection and copy keys, or explicitly choose vi mode. Enter copy mode before trying selection keys.",
 "show-buffer contains the selected test text.", "copy-mode"),
("history", "copy", "Old output is missing",
 "The pane reached its history limit, the application used an alternate screen, or the pane was recreated.",
 "Check the pane’s creation-time history limit and whether the application manages its own screen.",
 "Increase history-limit before creating future panes and use application logs or pipe-pane for future evidence. Discarded output cannot be recovered by raising the limit.",
 "Newly created panes retain the configured amount; important output is also stored by the application.", "copy-mode"),
("config", "configuration", "Reload did not apply what I expected",
 "A line failed, a local override masks a global value, the wrong file/server was targeted, or a removed setting remains active.",
 "Read source-file errors; inspect global and target-local options plus active key bindings.",
 "Correct the failing line, unset the intended local override or explicitly restore a default. Test a clean server with -f; do not restart important work merely to test config.",
 "show-options and list-keys report the intended effective behavior.", "configuration"),
("version", "configuration", "unknown command / invalid option",
 "The example may target another tmux version, or an old server remains after upgrading the executable.",
 "Compare tmux -V, display-message -p '#{version}', list-commands and the installed manual.",
 "Use syntax supported by the active server, or plan an upgrade when ongoing work can end. Remove unsupported config lines.",
 "The command appears in list-commands and runs on a disposable target.", "advanced"),
("colors", "display", "Broken colors or terminal capabilities",
 "TERM or the available terminfo entry does not describe the terminal at one of the layers.",
 "Compare TERM outside and inside tmux; run infocmp for those values. Check every remote host where applications read terminfo.",
 "Keep the outer TERM accurate. Use a supported tmux/screen entry inside; install missing terminfo rather than forcing xterm-256color inside tmux. Configure RGB support only for terminals that support it.",
 "The same color-capable application renders correctly outside and inside a fresh pane.", "configuration"),
("keys", "display", "Alt, arrows or escape keys behave strangely",
 "The terminal/desktop may intercept a key, or an escape-sequence timing/capability setting is unsuitable.",
 "Check active bindings and reproduce on a clean server with the same terminal. Test the equivalent command from the tmux prompt.",
 "Resolve the terminal key mapping. Adjust escape-time deliberately; an excessively low value over a slow connection can split escape sequences.",
 "Both the direct command and the intended key sequence perform the same operation.", "configuration"),
("resize", "remote", "The screen is too small or resizing is odd",
 "Another attached client or a manual window-size policy may constrain the layout.",
 "Inspect list-clients, client sizes and show-window-options for window-size.",
 "Choose a suitable size policy. Coordinate before detaching other clients; refresh-client can redraw a stale display.",
 "The layout matches the chosen policy and active viewers understand how resizing works.", "remote"),
("agent", "remote", "Git / SSH agent worked before reconnecting",
 "An older shell retains a stale SSH_AUTH_SOCK or another connection-specific environment value.",
 "Compare the new SSH connection’s environment with show-environment for the session and the affected shell.",
 "Verify intentional agent forwarding and update-environment. Create a new pane using refreshed session values or carefully update the old shell.",
 "A harmless agent-backed operation works from the intended shell without copying private keys.", "remote"),
("tty", "remote", "open terminal failed: not a terminal",
 "An interactive tmux client was launched without a usable terminal.",
 "Check whether this is a noninteractive SSH command, redirected stdin or a CI job.",
 "Use ssh -t for an interactive remote attach. Use new-session -d and noninteractive tmux commands for scripts that do not need a display.",
 "Interactive attach has a TTY, while automation completes without trying to take over a nonexistent terminal.", "remote"),
("broadcast", "input", "Typing appears in every pane",
 "synchronize-panes is enabled for the window.",
 "Inspect tmux show-window-options synchronize-panes on the affected window.",
 "Use tmux set-window-option synchronize-panes off. Inspect any commands already broadcast before continuing.",
 "A harmless test string appears only in the active pane.", "configuration"),
("socket", "sessions", "The socket vanished but the server may still exist",
 "A temporary-directory cleanup may have removed the socket file without stopping the server.",
 "Inspect your own tmux server process and verify its socket directory and PID. Do not guess a PID or target an unrelated process.",
 "The tmux manual documents SIGUSR1 to request socket recreation by the running server, provided its directory exists with correct permissions. Use kill -USR1 only with the verified tmux server PID.",
 "A client can connect again. If the server actually died, no signal can restore its process state.", "advanced"),
("reboot", "sessions", "All work vanished after reboot",
 "tmux state and live processes were in memory on the rebooted host.",
 "Confirm the host actually restarted rather than merely changing host/user/socket.",
 "Recreate the workspace, restore saved files and application checkpoints, and rerun recoverable jobs. Use an appropriate service manager for restart guarantees.",
 "The job resumes from its own persisted checkpoint or restarts deliberately; there is no claim of live-process resurrection.", "sessions"),
("sendkeys", "automation", "send-keys succeeded but the job did not",
 "The command only delivered keystrokes; the target may have been busy, wrong, or expecting a different kind of input.",
 "Inspect the pane ID, current foreground program, captured output and application status.",
 "Use a known command in a new pane for deterministic automation; record completion and exit status. Avoid blind sleeps and arbitrary input injection.",
 "You have an application exit code or completion artifact, not merely a zero status from send-keys.", "automation"),
]

# A lab step is a self-reported observation, never an automatic claim of real execution.
LABS = [
dict(id="first-session", title="1 · Prove detach and reattach", topic="sessions", level="Beginner", time="15 min",
 goal="Keep a visible clock running in a disposable session while its client is detached.",
 setup="Run outside tmux. The named kt-tmux server keeps these exercises separate from your normal sessions. If a lab session already exists, attach and inspect it before reusing it.",
 command="""tmux -L kt-tmux -f /dev/null new-session -s kt-clock
# Inside the pane:
while :; do date; sleep 2; done
# Press Ctrl+b, release, then d.
# Back in the outside shell:
tmux -L kt-tmux list-sessions
tmux -L kt-tmux attach-session -t kt-clock""",
 steps=["I can identify the kt-clock session in the status line.", "After detaching, list-sessions still shows kt-clock.", "After attaching, new timestamps appear; the job was not paused.", "I stop the clock with Ctrl+c, then type exit to close this lab shell."],
 predict="Does detaching pause the clock? What happens if the host reboots?",
 solution="Detach only removes the client, so the loop continues. Reboot ends the server and process. Reattaching cannot restore that live loop.",
 problem="If no session is listed, repeat -L kt-tmux and check host/user. If the loop stopped, verify you did not press Ctrl+c or exit.",
 cleanup="After stopping the loop, exit the only shell. Confirm kt-clock is absent from tmux -L kt-tmux ls."),
dict(id="layout", title="2 · Build a three-pane workspace", topic="panes", level="Beginner", time="20 min",
 goal="Create editor, output and scratch areas, then move focus and zoom without stopping programs.",
 setup="Start a fresh lab session outside tmux. Use a terminal large enough for three readable panes.",
 command="""tmux -L kt-tmux -f /dev/null new-session -s kt-layout -n work
# Inside: prefix %, then prefix double quote.
tmux list-panes -F '#{pane_index} #{pane_id} #{pane_current_path}'
tmux select-layout main-vertical
tmux resize-pane -R 5""",
 steps=["I create one side-by-side split, then split the active pane top/bottom.", "I use prefix q and select each displayed pane number.", "I zoom a pane with prefix z and restore all three with prefix z.", "I compare tiled and main-vertical layouts and explain the difference."],
 predict="Does zooming close the hidden panes? Does -h create top/bottom panes?",
 solution="Zoom changes visibility only. -h creates side-by-side panes; -v creates stacked panes.",
 problem="If focus seems wrong, inspect the active border and use prefix q. If splitting fails, enlarge the terminal or use another window.",
 cleanup="Exit the three disposable shells, or detach and run tmux -L kt-tmux kill-session -t '=kt-layout' after inspecting it."),
dict(id="copy", title="3 · Find and capture a useful log", topic="copy-mode", level="Beginner", time="20 min",
 goal="Search a known history, copy a selection and export a snapshot.",
 setup="Start the lab session, then use vi copy-mode keys so the steps are unambiguous.",
 command="""tmux -L kt-tmux -f /dev/null new-session -s kt-copy
tmux set-window-option mode-keys vi
seq 1 200
printf 'ERROR request=42: timeout\\n'
seq 201 250
# Enter copy mode, then ?ERROR and Enter.
# Space starts selection; move, then Enter copies.
tmux show-buffer
tmux capture-pane -p -S -200 > "$HOME/kt-tmux-capture.txt" """,
 steps=["I enter copy mode and search backward to ERROR.", "I copy the error line and verify it with show-buffer.", "I distinguish the tmux buffer from my OS clipboard.", "I inspect the capture file and confirm it contains the test output."],
 predict="Will increasing history-limit recover lines already discarded?",
 solution="No. It helps panes created afterward retain more future output. A capture is limited to output still available.",
 problem="If Space/Enter fails, inspect mode-keys and the copy-mode-vi table. Test internal buffers before clipboard integration.",
 cleanup="Exit the lab shell. Keep or remove only the known ~/kt-tmux-capture.txt exercise file after reviewing it."),
dict(id="config", title="4 · Diagnose a configuration error", topic="configuration", level="Intermediate", time="25 min",
 goal="Observe partial application and fix a deliberately invalid option on an isolated server.",
 setup="Create ~/kt-tmux-test.conf in your editor with: set -g mouse on, then set -g definitely-not-a-tmux-option on. This is a throwaway file; do not replace your real config.",
 command="""tmux -L kt-tmux -f /dev/null new-session -s kt-config
tmux source-file ~/kt-tmux-test.conf
tmux show-options -g mouse
# Fix the invalid line in your editor, then:
tmux source-file ~/kt-tmux-test.conf""",
 steps=["I observe the invalid-option error without killing the server.", "I verify that the valid mouse setting applied despite the later failure.", "I remove the invalid line and reload the corrected file.", "I explain why removing a valid line does not undo an already-applied setting."],
 predict="Is source-file an all-or-nothing transaction?",
 solution="No. It executes commands and reports failures. Previously applied settings remain; explicitly restore or unset the appropriate value.",
 problem="If changes affect another server, inspect TMUX and -L. Startup -f is ignored when that named server already exists.",
 cleanup="Close kt-config and retain/remove only your exercise config. Other lab sessions on kt-tmux may retain this server’s global settings."),
dict(id="remote", title="5 · Recover a remote workspace", topic="remote", level="Intermediate", time="25 min",
 goal="Reconnect to a running job after closing only its SSH client.",
 setup="Requires an SSH host you are authorized to use and tmux installed there. Replace user@host. Use a disposable job, never a production migration for this exercise.",
 command="""ssh user@host
tmux -L kt-remote -f /dev/null new-session -s reconnect
while :; do date; sleep 3; done
# Close this SSH terminal. Reconnect from a new terminal:
ssh user@host
hostname
tmux -L kt-remote list-sessions
tmux -L kt-remote attach-session -t reconnect""",
 steps=["I verify tmux and the loop run on the remote host.", "I close the client terminal and reconnect to the same host/user.", "I reattach on the same named socket and observe continued timestamps.", "I stop the loop with Ctrl+c and exit the disposable remote shell."],
 predict="Would local tmux around an SSH command alone protect a remote process from an SSH drop?",
 solution="No. Place tmux and the job on the remote host. Host/user policies may still terminate processes on logout, so verify your environment.",
 problem="If the session is missing, check host, user, socket, reboot history and logout policy in that order.",
 cleanup="Stop the test loop and exit reconnect. Exit SSH when finished."),
dict(id="script", title="6 · Launch a repeatable project", topic="automation", level="Intermediate", time="30 min",
 goal="Run the provided workspace launcher twice and prove it does not duplicate windows.",
 setup="Use an existing project directory. Download examples/workspace.sh or run it from the repository. Start outside tmux.",
 command="""sh tmux/examples/workspace.sh "$HOME/projects/my-project"
# Detach, then run the SAME command again.
# From an outside shell, inspect:
tmux -L kt-tmux list-windows -t kt-project
tmux -L kt-tmux list-panes -s -t kt-project""",
 steps=["I review the script and choose an existing directory.", "First run creates editor and tests windows with a split editor.", "After detach, a second run reuses the same session and pane IDs.", "I explain the remaining race condition between simultaneous launches."],
 predict="Why does the script capture pane_id rather than select pane 0?",
 solution="Pane indexes and server-global IDs are not guaranteed starting values. Capturing the creation result identifies exactly the pane the launcher made.",
 problem="If the directory is missing, fix the argument. If already inside tmux, detach or use another outside terminal. Inspect partial sessions before retrying after a failure.",
 cleanup="Stop any programs you started. Detach and kill only the inspected kt-project session on -L kt-tmux."),
dict(id="incident", title="7 · Troubleshoot a confusing screen", topic="configuration", level="Intermediate", time="25 min",
 goal="Diagnose two intentionally introduced UI problems without losing the workspace.",
 setup="Use a disposable kt-incident session with two shell panes. Do not run important commands while synchronized input is enabled.",
 command="""tmux -L kt-tmux -f /dev/null new-session -s kt-incident
tmux split-window -h
tmux set-window-option synchronize-panes on
# Type a harmless comment: # hello
# Then turn broadcasting OFF:
tmux set-window-option synchronize-panes off
tmux resize-pane -Z
tmux list-panes""",
 steps=["I observe the harmless comment appearing in both panes.", "I inspect and turn off synchronize-panes before continuing.", "I identify that zoom, not pane deletion, hides the second pane.", "I restore the layout and explain my evidence before naming the fix."],
 predict="Would restarting tmux be the best first diagnosis?",
 solution="No. Inspect the specific option and pane list. Restarting can destroy evidence and terminate work when a reversible view/config change is enough.",
 problem="A command entered while synchronization is on may reach both shells. Clear any unfinished harmless input with Ctrl+c before resuming.",
 cleanup="Ensure synchronization is off, then close only kt-incident and its disposable panes."),
dict(id="capstone", title="8 · Capstone: a recoverable development desk", topic="workflow", level="Advanced", time="45 min",
 goal="Combine project organization, live output, searching, capture, detachment and recovery with a written handoff.",
 setup="Use a harmless project or a scratch directory. The service below is a timestamp loop, so no application installation is required.",
 command="""tmux -L kt-tmux -f /dev/null new-session -s kt-capstone -n editor
tmux new-window -n service
while :; do printf 'service alive '; date; sleep 2; done
# Create a tests window with prefix c, rename it with prefix comma.
# There run:
printf 'PASS smoke-check\\nERROR simulated timeout\\n'
tmux list-panes -a -F '#{pane_id} #{session_name}:#{window_name}'""",
 steps=["I build editor, service and tests windows and identify all pane IDs.", "I search the simulated error and capture only the relevant test output.", "I detach, reattach and confirm service output continued.", "I write a handoff: host, user, socket, session, current issue, evidence path and cleanup plan.", "I stop the loop and close this session without affecting another session."],
 predict="What evidence proves the job is healthy, and what would survive a reboot?",
 solution="Inspect fresh output and application-specific checks; a session existing is insufficient. Saved files and logs survive only on persistent storage. Live tmux processes do not survive reboot.",
 problem="Use the troubleshooting clinic’s symptom → evidence → fix → verification process. Avoid killing the server to solve an individual window issue.",
 cleanup="Stop the service loop with Ctrl+c, save useful files, detach, inspect kt-capstone and kill only that session.")
]
