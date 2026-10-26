#!/bin/sh
# Sequentially repeatable launcher; not a concurrency-safe deployment tool.
# Invoke from OUTSIDE tmux: sh workspace.sh /existing/project/directory
set -eu
if [ "$#" -ne 1 ] || [ ! -d "$1" ]; then
  printf '%s\n' "Usage: sh workspace.sh /existing/project/directory" >&2
  exit 2
fi
if [ -n "${TMUX:-}" ]; then
  printf '%s\n' "Run this launcher in an outside terminal to avoid nesting clients." >&2
  exit 2
fi
command -v tmux >/dev/null 2>&1 || {
  printf '%s\n' "Install tmux first." >&2
  exit 1
}
project_dir=$(CDPATH= cd -- "$1" && pwd)
session=kt-project
if ! tmux -L kt-tmux has-session -t "=$session" 2>/dev/null; then
  pane=$(tmux -L kt-tmux -f /dev/null new-session -d -P -F '#{pane_id}' \
    -s "$session" -n editor -c "$project_dir")
  tmux -L kt-tmux split-window -h -t "$pane" -c "$project_dir"
  tmux -L kt-tmux new-window -t "$session:" -n tests -c "$project_dir"
  tmux -L kt-tmux select-window -t "$session:editor"
fi
exec tmux -L kt-tmux attach-session -t "=$session"
