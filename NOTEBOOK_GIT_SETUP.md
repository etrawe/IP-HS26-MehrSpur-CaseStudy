# Notebook git setup (avoid notebook merge conflicts)

Running a notebook rewrites execution counts and cell metadata, so two people running the
same notebook used to conflict even without changing any code. This repo now strips that
noise automatically on every commit. **Outputs are kept**, and your local `.ipynb` files
are never changed — only what gets committed is cleaned.

## First-time setup (everyone, once per clone)

1. **Commit or stash your own work first**, then pull:
   ```bash
   git add -A && git commit -m "WIP before notebook setup"   # or: git stash
   git pull
   ```
   If the pull conflicts on a notebook, see "Resolving a notebook conflict" below.

2. From the repository root, with the Python environment you use for the notebooks:
   ```bash
   python setup_notebook_git.py
   ```
   This installs `nbstripout` and `nbdime` and registers them in your `.git/config`
   (git never shares this config, which is why every person must run it once).

3. Check that it worked:
   ```bash
   git config --get filter.nbstripout.clean
   ```
   It should print a line ending in `-m nbstripout --keep-output`.

4. If `git status` now lists notebooks as modified although you did not edit them, that is
   only the one-time cleanup. Commit it:
   ```bash
   git add --renormalize notebooks
   git commit -m "Normalize notebooks"
   ```

## Daily use

Nothing changes: run notebooks, `git add`, `git commit`, `git pull`, `git push` as usual.

- `git diff` on a notebook shows a readable, cell-by-cell diff (nbdime).
- Browser view of a notebook diff: `nbdiff-web notebooks/02_system_modeling.ipynb`

## Resolving a notebook conflict

Keep one whole version:
```bash
git checkout --theirs notebooks/03_uncertainty_modeling.ipynb   # incoming version
# or
git checkout --ours   notebooks/03_uncertainty_modeling.ipynb   # your version
git add notebooks/03_uncertainty_modeling.ipynb
git commit
```

Or merge cell by cell in the browser:
```bash
nbdime mergetool
```

Tip: to reduce conflicts further, agree who edits which notebook, and pull before you start
working.

## Troubleshooting

- **`error: external filter ... nbstripout failed`** — the Python path stored in your git
  config no longer exists (e.g. new virtual environment). Re-run `python setup_notebook_git.py`.
- **Commits from a clone without setup** still work, but they include metadata again.
  Make sure every teammate has run the setup script.
