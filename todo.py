#!/usr/bin/env python3
"""A small command-line to-do list manager.

Tasks are stored in ``todo.json`` next to this script. Each task has
an ``id``, a ``text``, a ``done`` flag and a ``created`` timestamp.

Usage:
    python todo.py add "Buy milk"
    python todo.py list
    python todo.py done 1
    python todo.py delete 1
    python todo.py clear-done
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / "todo.json"


def load_tasks():
    """Load the task list from todo.json, or return an empty list."""
    if not DATA_FILE.exists():
        return []
    try:
        data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


def save_tasks(tasks):
    """Save the task list to todo.json."""
    DATA_FILE.write_text(json.dumps(tasks, indent=2), encoding="utf-8")


def next_id(tasks):
    """Return the next free task id."""
    return max((task["id"] for task in tasks), default=0) + 1


def find_task(tasks, task_id):
    """Return the task with the given id, or None."""
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def cmd_add(args):
    """Add a new task."""
    tasks = load_tasks()
    task = {
        "id": next_id(tasks),
        "text": " ".join(args.text),
        "done": False,
        "created": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Added #{task['id']}: {task['text']}")


def cmd_list(args):
    """List tasks, pending first."""
    tasks = load_tasks()
    if not tasks:
        print("No tasks yet.")
        return
    for task in sorted(tasks, key=lambda t: (t["done"], t["id"])):
        mark = "x" if task["done"] else " "
        created = task.get("created", "")
        print(f"[{mark}] {task['id']:>3}  {task['text']}  ({created})")


def cmd_done(args):
    """Mark a task as done."""
    tasks = load_tasks()
    task = find_task(tasks, args.id)
    if task is None:
        print(f"No task with id {args.id}.", file=sys.stderr)
        sys.exit(1)
    task["done"] = True
    save_tasks(tasks)
    print(f"Done #{task['id']}: {task['text']}")


def cmd_delete(args):
    """Delete a task."""
    tasks = load_tasks()
    task = find_task(tasks, args.id)
    if task is None:
        print(f"No task with id {args.id}.", file=sys.stderr)
        sys.exit(1)
    tasks.remove(task)
    save_tasks(tasks)
    print(f"Deleted #{task['id']}: {task['text']}")


def cmd_clear_done(args):
    """Delete all completed tasks."""
    tasks = load_tasks()
    remaining = [task for task in tasks if not task["done"]]
    removed = len(tasks) - len(remaining)
    save_tasks(remaining)
    print(f"Removed {removed} completed task(s).")


def build_parser():
    """Build the argument parser."""
    parser = argparse.ArgumentParser(
        prog="todo.py",
        description="A small command-line to-do list manager.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_add = subparsers.add_parser("add", help="Add a new task")
    parser_add.add_argument("text", nargs="+", help="Text of the task")
    parser_add.set_defaults(func=cmd_add)

    parser_list = subparsers.add_parser("list", help="List all tasks")
    parser_list.set_defaults(func=cmd_list)

    parser_done = subparsers.add_parser("done", help="Mark a task as done")
    parser_done.add_argument("id", type=int, help="Id of the task")
    parser_done.set_defaults(func=cmd_done)

    parser_delete = subparsers.add_parser("delete", help="Delete a task")
    parser_delete.add_argument("id", type=int, help="Id of the task")
    parser_delete.set_defaults(func=cmd_delete)

    parser_clear = subparsers.add_parser(
        "clear-done", help="Delete all completed tasks"
    )
    parser_clear.set_defaults(func=cmd_clear_done)

    return parser


def main():
    """Parse arguments and run the chosen command."""
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
