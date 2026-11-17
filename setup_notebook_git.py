"""One-time git setup for Jupyter notebooks in this repository.

Run once per clone. It can be started from anywhere, e.g.:
- VS Code: open this file and click "Run Python File" (triangle, top right)
- a Jupyter notebook cell in notebooks/:   %run ../setup_notebook_git.py
- a terminal:                              python path/to/setup_notebook_git.py
Use the same Python environment / kernel you run the notebooks with.

It installs nbstripout and nbdime and registers them in this clone's .git/config:
- nbstripout (clean filter): on commit, removes execution counts and cell/notebook
  metadata but KEEPS outputs. Your local .ipynb files are never modified.
- nbdime: notebook-aware `git diff` and `git merge` for .ipynb files.
The matching rules (*.ipynb filter/diff/merge, LF line endings) live in .gitattributes.
"""

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent  # folder containing this script = repository root


def run(*args: str) -> None:
    print("+", " ".join(args))
    subprocess.run(args, check=True, cwd=REPO)


python = sys.executable.replace("\\", "/")
run(python, "-m", "pip", "install", "--quiet", "nbstripout", "nbdime")

# nbstripout filter: strip metadata + execution counts, keep outputs.
run("git", "config", "filter.nbstripout.clean", f'"{python}" -m nbstripout --keep-output')
run("git", "config", "filter.nbstripout.smudge", "cat")
run("git", "config", "filter.nbstripout.required", "true")
run("git", "config", "diff.ipynb.textconv", f'"{python}" -m nbstripout -t --keep-output')

# nbdime: notebook-aware diff/merge drivers (diff=jupyternotebook, merge=jupyternotebook).
run(python, "-m", "nbdime", "config-git", "--enable")

print("\nDone. Notebook commits from this clone are now stripped of metadata.")
