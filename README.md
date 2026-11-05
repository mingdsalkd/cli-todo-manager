# cli-todo-manager

A small command-line to-do list manager in Python. Add tasks, list them,
mark them as done, delete them, and clear all completed tasks — all from
the terminal.

## What it does

- Add a task with a short text description.
- List all tasks, pending tasks first, marked `[ ]` for pending and `[x]`
  for completed.
- Mark a task as done by its id.
- Delete a task by its id.
- Remove all completed tasks at once with `clear-done`.

## Requirements

- Python 3.8 or later.
- No dependencies — only the Python standard library
  (`argparse`, `json` and `pathlib`).

## Usage

```bash
# Add a task
python todo.py add "Buy milk"

# List all tasks (pending first)
python todo.py list

# Mark task 1 as done
python todo.py done 1

# Delete task 1
python todo.py delete 1

# Remove all completed tasks
python todo.py clear-done

# Show help for a command
python todo.py --help
python todo.py add --help
```

Example output of `python todo.py list`:

```text
[ ]   1  Buy milk  (2026-11-05T09:54:00+00:00)
[x]   2  Take out the trash  (2026-11-05T09:55:00+00:00)
```

## Data storage

Tasks are stored in `todo.json`, a local JSON file next to `todo.py`.
Each task has an `id`, a `text`, a `done` flag and a `created`
timestamp. No account, server or database is needed — the data lives
only in that file.
