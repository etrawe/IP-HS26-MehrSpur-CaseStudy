"""One-time git setup for Jupyter notebooks in this repository.

Run once per clone, from the repository root, with the Python you use for the notebooks:

    python setup_notebook_git.py

It installs nbstripout and nbdime and registers them in this clone's .git/config:
- nbstripout (clean filter): on commit, removes execution counts and cell/notebook
  metadata but KEEPS outputs. Your local .ipynb files are never modified.
- nbdime: notebook-aware `git diff` and `git merge` for .ipynb files.
The matching rules (*.ipynb filter/diff/merge, LF line endings) live in .gitattributes.
"""

import subprocess
import sys


def run(*args: str) -> None:
    print("+", " ".join(args))
    subprocess.run(args, check=True)


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
