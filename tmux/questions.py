"""Scenario questions with feedback for every answer."""
QUESTIONS = []
def q(topic, prompt, right, wrong1, wrong2):
    choices = [right, wrong1, wrong2]
    shift = len(QUESTIONS) % 3
    choices = choices[shift:] + choices[:shift]
    QUESTIONS.append(dict(id="q" + str(len(QUESTIONS)+1), topic=topic, prompt=prompt,
        options=[dict(text=a, why=b) for a,b in choices], correct=(3-shift)%3))

q("installation", "You installed tmux on your laptop. Where must it run to protect a job on an SSH server?",
 ("On the remote server, with the job inside its pane", "The tmux server and job need to share the remote host so the SSH client can disconnect without removing their terminal."),
 ("Only on the laptop, around the SSH command", "That preserves the local SSH client, but a broken SSH connection can still end a remote shell that is not protected remotely."),
 ("In the browser playground", "The playground models behavior; it does not execute or host real processes."))
q("installation", "How do you use the default detach shortcut?",
 ("Hold Ctrl and press b, release both, then press d", "tmux first enters its prefix key table; d is then interpreted as detach-client."),
 ("Hold Ctrl, b and d together", "The action key follows the prefix chord. Holding everything can send a different key."),
 ("Type the letters Ctrl+b d at the shell prompt", "Those are key-sequence notation, not a shell command."))
q("installation", "You opened the tmux command prompt with prefix :. What do you enter to list sessions?",
 ("list-sessions", "The prompt already interprets tmux commands. The executable name is needed at a shell prompt."),
 ("tmux list-sessions", "The tmux command prompt does not use the shell executable prefix in this command."),
 ("$ list-sessions", "A dollar sign in documentation often marks a shell prompt; it is not part of a tmux command."))
q("installation", "Which check tells you the installed tmux executable version?",
 ("tmux -V", "Capital V prints the client executable version. Compare the running server version separately after upgrades."),
 ("tmux -v", "Lowercase v enables verbose logging; case matters."),
 ("echo $TERM", "TERM names terminal capabilities. It is not a tmux version."))

q("mental-model", "You type a command while two panes are visible. Who receives normal input?",
 ("The foreground program in the active pane", "The selected session, current window and active pane determine the input destination."),
 ("Every pane in every window", "That is not normal routing. synchronize-panes can broadcast within a specific window when explicitly enabled."),
 ("The tmux server as a shell command", "tmux forwards ordinary input; only its prefix bindings and command prompt interpret tmux commands."))
q("mental-model", "A script needs to keep targeting a pane after rearranging its layout. Which target is best?",
 ("The captured pane ID, such as %7", "Pane IDs stay with a pane for its lifetime on one server. Capture the ID when creating it."),
 ("Always pane index 0", "Indexes describe positions and can change. The intended pane may never have been at index 0."),
 ("The pane’s screen title alone", "Titles can change and may not uniquely identify a pane."))
q("mental-model", "tmux ls shows nothing, but you created work using -L training. What should you check first?",
 ("tmux -L training ls", "A different socket name selects a different server. Inspect the server where the session was created."),
 ("Run tmux kill-server", "This targets the current server and can destroy unrelated work without diagnosing the missing session."),
 ("Reinstall tmux immediately", "A socket mismatch is a context problem, not evidence that the executable is broken."))
q("mental-model", "Two sessions link to the same window. Are its programs duplicated?",
 ("No, both links refer to the same window and programs", "Linking changes which sessions can reference a live window; it does not clone processes."),
 ("Yes, each session gets its own independent copy", "That would require new panes/programs, not link-window."),
 ("Only the scrollback is copied", "The entire live window is shared, including panes, focus and programs."))

q("sessions", "A long job is running in tmux. You detach. What changes?",
 ("The client disconnects; the job keeps running on its host", "Detaching changes attachment, not process execution. Host and logout policy still determine lifetime."),
 ("The job pauses until you attach", "Detachment does not suspend the process."),
 ("The job is saved to disk and can survive reboot", "tmux does not checkpoint process memory or make jobs reboot-persistent."))
q("sessions", "You are already inside tmux and want another existing session on the same server.",
 ("Use tmux switch-client -t target", "This changes the session displayed by your existing client without nesting another client."),
 ("Unset TMUX and start a nested client every time", "That hides the nesting warning and adds unnecessary prefix layers."),
 ("Close your current session before switching", "Sessions can coexist. Ending one is unnecessary and can stop its programs."))
q("sessions", "A host rebooted. What can tmux itself restore?",
 ("No live processes; recreate the workspace and recover application data", "Process memory and the tmux server ended. Recovery needs saved files, checkpoints or appropriate supervision."),
 ("Every running process exactly where it stopped", "tmux is not a process checkpointing system."),
 ("Everything if the session had been detached", "Detached and attached sessions both depend on the same running server and host."))
q("sessions", "You want to end only the disposable session api after inspecting it.",
 ("tmux kill-session -t '=api'", "This explicitly targets the exact session name. Stop important applications cleanly first."),
 ("tmux kill-server", "That ends all sessions on the targeted server, a much larger scope."),
 ("Press prefix d", "Detaching leaves the session and its programs running; it does not clean it up."))

q("windows", "Which default sequence creates a new window?",
 ("Prefix then c", "c creates a new-window; its first pane normally starts a shell."),
 ("Prefix then %", "Percent splits the current pane side by side inside the current window."),
 ("Prefix then z", "z zooms the current pane; it does not create a window."))
q("windows", "A window is hidden while you view another one. What happens to its program?",
 ("It continues running", "Window selection affects the view. Background windows retain live panes."),
 ("It automatically pauses", "tmux does not suspend programs just because their window is hidden."),
 ("It becomes a screenshot with no live program", "Ordinary windows remain interactive workspaces, not saved images."))
q("windows", "You want to jump repeatedly between the current and previous window.",
 ("Prefix then l", "Lowercase l selects the last window. This is useful for an editor/test loop."),
 ("Prefix then L", "Uppercase and lowercase bindings differ. Inspect list-keys rather than assuming case is interchangeable."),
 ("Prefix then x", "x asks to kill the active pane and can terminate work."))
q("windows", "A shared window is linked in two sessions. What does kill-window do?",
 ("Destroys that window and removes its links from both sessions", "Use unlink-window when you only intend to remove a session’s link, accounting for last-link behavior."),
 ("Only hides it in the current client", "Killing is a lifecycle operation, not a display operation."),
 ("Creates an independent copy in the other session", "Killing does not duplicate or preserve process state."))

q("panes", "You want two panes next to each other, left and right.",
 ("split-window -h, or prefix %", "Horizontal placement means panes along the horizontal axis; the dividing line is vertical."),
 ("split-window -v, or prefix double quote", "That creates one pane above another."),
 ("new-window -n right", "A new window is a separate view, not a split in the current window."))
q("panes", "You zoomed a pane and now only one is visible. How do you restore the arrangement?",
 ("Prefix then z again", "Zoom toggles the view while preserving the other panes and their programs."),
 ("Recreate every hidden pane", "The existing panes still exist, so recreating them duplicates work."),
 ("Restart the tmux server", "Restarting destroys live state and is unnecessary for a zoomed view."))
q("panes", "New splits should start in the current pane’s directory. What should the split command include?",
 ('-c "#{pane_current_path}"', "The format is expanded by tmux; quoting preserves directories containing spaces."),
 ("-n current", "Naming a window does not set its working directory."),
 ("-t /your/project", "-t selects a tmux target; -c selects a working directory."))
q("panes", "You need to move a running pane into a window of its own.",
 ("break-pane", "This changes the pane’s container without restarting its program."),
 ("kill-pane then new-window", "Killing may terminate the running program; creating a window does not restore it."),
 ("capture-pane", "Capture reads displayed output, not the live pane’s placement."))

q("copy-mode", "After entering vi copy mode, what selects and copies text using default bindings?",
 ("Space starts selection; Enter copies and leaves", "These are vi-table keys after entering copy mode. No prefix is needed for these mode actions."),
 ("Ctrl+b before every character selection movement", "Copy-mode movement keys are interpreted directly inside their table."),
 ("Ctrl+c always copies to the desktop clipboard", "Ctrl+c normally interrupts a foreground program outside copy mode; desktop clipboard integration is separate."))
q("copy-mode", "show-buffer contains the right text, but the desktop paste is old. Where is the likely problem?",
 ("The clipboard bridge between tmux and the outer terminal/desktop", "Internal copying succeeded. Inspect OSC 52 support or the local clipboard command and environment."),
 ("The session name must be changed", "Session naming does not control clipboard transport."),
 ("The text never entered a tmux buffer", "show-buffer is evidence that the internal buffer already has it."))
q("copy-mode", "You increased history-limit after important lines were discarded. Can it recover them?",
 ("No; it cannot recreate discarded output", "Set the limit before creating future panes and use persistent logs for important evidence."),
 ("Yes, tmux retrieves them from the application automatically", "There is no general mechanism for reconstructing past output from an arbitrary application."),
 ("Yes, if you detach and reattach", "Client attachment does not restore discarded history."))
q("copy-mode", "What is the difference between capture-pane and pipe-pane?",
 ("capture-pane snapshots retained content; pipe-pane can stream future output", "Choose capture for current evidence and a pipe or application logs for ongoing recording."),
 ("Both recover all output since boot", "Both have limits. A capture sees retained history; a newly opened pipe is not retroactive."),
 ("Both restart the program in the pane", "They observe output rather than restart programs."))

q("configuration", "You removed a setting from the config and ran source-file. Why is its value still active?",
 ("Reload executes remaining commands but does not undo deleted lines", "Explicitly restore the intended value or unset the relevant override; test clean startup separately."),
 ("The file is always ignored after startup", "source-file explicitly executes a file in a running server."),
 ("All settings require killing every session", "Many settings apply live. Destroying work is unnecessary for routine configuration changes."))
q("configuration", "The global value looks right but one session behaves differently.",
 ("Inspect a local override and inherited effective values", "A target-local option can mask the global fallback. Check both scopes."),
 ("Change the host’s clock", "Clock settings do not explain tmux option inheritance."),
 ("Assume show-options is randomly incorrect", "Scope and inheritance explain this deterministically."))
q("configuration", "Typing is duplicated into every pane of a window. What should you inspect?",
 ("synchronize-panes", "This window option broadcasts input. Turn it off and inspect any commands already sent."),
 ("history-limit", "History limits affect retained output, not input routing."),
 ("base-index", "Index numbering does not broadcast keystrokes."))
q("configuration", "A new prefix binding works, but an application shortcut stopped working after bind -n.",
 ("The root-table binding may consume the key without a prefix", "bind -n installs a root binding; choose a prefix binding when applications need the raw key."),
 ("The application must be uninstalled", "The symptom follows a key-routing change, not evidence of application corruption."),
 ("A bigger pane is required", "Pane geometry does not resolve key-table interception."))

q("workflow", "The tmux session exists after your break. Does that prove the long job succeeded?",
 ("No; inspect application output, status and results", "The shell/session can remain alive after a failed job. Workspace existence is not health evidence."),
 ("Yes, tmux only keeps successful jobs", "tmux does not enforce application success."),
 ("Yes, if the status line is green", "Status-line colors are presentation and can be customized."))
q("workflow", "Your service needs restart-on-failure and restart-after-reboot.",
 ("Use an appropriate service manager or scheduler", "tmux helps with interaction but does not automatically supervise or restart arbitrary services."),
 ("Detach from tmux twice", "Detachment does not add supervision or reboot persistence."),
 ("Enable mouse mode", "Mouse support changes interaction, not process recovery."))
q("workflow", "You captured a pane on a remote tmux server using a remote shell. Where is the redirected file?",
 ("On the remote shell’s filesystem at the chosen path", "Shell redirection occurs where that shell runs. Transfer or share it deliberately after inspection."),
 ("Automatically in your laptop Downloads folder", "SSH does not automatically redirect remote file creation to local Downloads."),
 ("Only in the tmux paste buffer", "capture-pane -p prints output; the shell redirects it to a file."))
q("workflow", "You are debugging a production-looking error in a practice environment. What is the best first step?",
 ("Reproduce a small case and collect relevant evidence", "A narrow reproduction plus timestamps and logs helps distinguish causes before changes."),
 ("Kill the whole tmux server to clear the screen", "That destroys evidence and can terminate unrelated work."),
 ("Enable synchronized input across all panes", "Broadcasting can run unintended commands and does not diagnose the error."))

q("remote", "After reconnecting, tmux cannot find your session. What context should you verify first?",
 ("Host, user and socket", "The same session name on another machine, account or socket refers to different state."),
 ("Your terminal font", "Font choice does not select the tmux server."),
 ("Whether your local editor is open", "A local editor does not control remote session lookup."))
q("remote", "Two default Ctrl+b tmux layers are nested. How do you detach the inner layer?",
 ("Ctrl+b, Ctrl+b, then d", "The outer default send-prefix binding forwards the inner prefix; d then reaches the inner table."),
 ("Ctrl+b, then d", "That detaches the outer layer."),
 ("Ctrl+d in the running program", "Ctrl+d is application/terminal input and may end a shell; it is not tmux detach."))
q("remote", "You want a second terminal to observe a session without sending normal typing.",
 ("tmux attach-session -r -t name", "A read-only client reduces accidental input. It still displays the session’s contents and is not a secrecy boundary."),
 ("tmux attach-session -d -t name", "-d detaches other clients. It does not make this client read-only."),
 ("Make the socket world-writable", "That unnecessarily exposes control of user processes; it is not a safe observation mechanism."))
q("remote", "Git’s SSH agent access broke only in an old pane after reconnecting.",
 ("Compare SSH_AUTH_SOCK in the old shell and refreshed session environment", "Existing processes retain their environment. A new pane may inherit an updated agent socket while the old shell keeps a stale one."),
 ("The pane must have fewer columns", "Terminal width does not select an SSH agent socket."),
 ("Copy your private key into the status line", "That exposes credentials and does not repair environment propagation."))

q("automation", "send-keys returned zero. What does that actually prove?",
 ("The input was sent to the targeted pane", "It does not verify that a shell was ready, the intended command ran, or the command succeeded."),
 ("The application passed all tests", "Application success requires application evidence or an exit status."),
 ("The input cannot have gone to an editor", "The current foreground application receives input; it may be an editor or another prompt."))
q("automation", "A launcher runs twice. How can it avoid duplicating windows during sequential use?",
 ("Check for the exact session and create its layout only when absent", "This supports sequential reuse. Handle partial state and concurrent creation separately."),
 ("Always issue new-window four times", "That duplicates the layout on every run."),
 ("Assume window index 0 means setup is complete", "A single window index does not prove the expected session and layout exist."))
q("automation", "Why use new-session -P -F '#{pane_id}' in a launcher?",
 ("To capture the identity of the pane just created", "The returned ID avoids assumptions about server-global counters or customized pane indexes."),
 ("To print a screenshot", "-P prints formatted information, not a bitmap capture."),
 ("To make every command succeed", "Formatting output does not alter downstream command success."))
q("automation", "A worker signals a wait-for channel. What else should a robust script check?",
 ("The worker’s recorded result/exit status and a timeout policy", "A signal coordinates progress but does not itself encode success. A missing signal must not block forever."),
 ("Nothing; every signal means success", "Workers can fail and still signal completion."),
 ("The status-bar background color", "Presentation is not a completion contract."))

q("advanced", "What does a saved window_layout string preserve?",
 ("Pane arrangement, not live process memory", "Restoring geometry is distinct from restoring files, environments or running applications."),
 ("Every process and open network connection", "A layout string contains no process checkpoint."),
 ("All server passwords", "Layouts do not store application secrets as a backup mechanism."))
q("advanced", "Two sessions are in one group. What can be independent?",
 ("Their current window selection", "Grouped sessions share their window list but can view different current windows. Programs and pane state remain shared."),
 ("Every program’s memory and files", "The linked windows still contain the same live programs."),
 ("Which windows exist in the group", "The shared window list is the point of grouping."))
q("advanced", "After upgrading the tmux package, a new command still fails in an existing session.",
 ("Check the running server version as well as tmux -V", "An existing server can still be the old version. Plan any restart around its running work."),
 ("Change your session name to the version number", "Names do not change the server executable."),
 ("Use the new command repeatedly until it is accepted", "An unsupported command will not become supported through repetition."))
q("advanced", "What does a separate -L experiment server isolate?",
 ("tmux state such as sessions and options, but not filesystem permissions", "Its programs still run as your user. A separate socket is not an OS security sandbox."),
 ("All files and network access in a security container", "tmux does not provide container-style isolation."),
 ("Only the color scheme", "A separate server has its own sessions, options, buffers and other state."))

q("troubleshooting", "A screen stopped updating after Ctrl+s. Software flow control is enabled. What can resume it?",
 ("Ctrl+q", "With XON/XOFF flow control active, Ctrl+q resumes output. Also distinguish copy mode, a busy app and a dead connection."),
 ("Delete the socket directory", "That can break connections to a running server and does not address flow control."),
 ("Reboot immediately", "A reversible terminal state should be diagnosed before destructive recovery."))
q("troubleshooting", "Inside tmux, an app has broken colors. Someone hardcoded TERM=xterm-256color in shell startup.",
 ("Remove the override and use an installed tmux/screen terminfo entry inside", "TERM should describe the terminal interface the application actually sees. Verify terminfo on each relevant host."),
 ("Force the same override on every host", "Spreading a mismatched terminal description can reproduce the problem everywhere."),
 ("Increase history-limit", "Scrollback retention does not correct terminal capabilities."))
q("troubleshooting", "An interactive tmux attach launched by noninteractive SSH reports 'not a terminal'.",
 ("Allocate a TTY with ssh -t, or use detached commands for automation", "Interactive clients need a terminal. Automated setup can use new-session -d instead."),
 ("Always send SIGKILL to the tmux server", "That terminates work and cannot supply a missing terminal."),
 ("Rename the window to tty", "A window name is not a terminal allocation."))
q("troubleshooting", "What makes a troubleshooting fix complete?",
 ("Verify the intended behavior and check for unintended effects", "A diagnosis should connect symptom, evidence, cause, correction and an observable result."),
 ("The error message temporarily disappears", "A hidden message does not prove the underlying workflow is working."),
 ("You changed several options at once", "Many simultaneous changes make it harder to know which cause was real."))
