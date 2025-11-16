# Project Collaboration Guide

## Git Conventions
- If possible, let us have atomic commits (handling one objective at a time) with good commit messages (which explains what the commit is about, yet in a concise way)
- Let us work in our own branches and make PRs to merge into main.

## Useful Commands

**To branch from main**
```bash
git checkout main
git pull # To first ensure that local main has all the upstream changes updated
git checkout -b <YOUR-BRANCH-NAME> # Your branch name can include your name to differentiate branches
```

**When your local branch is behind what's in upstream main**
```bash
git checkout main
git pull
git checkout <YOUR-BRANCH-NAME>
git rebase main # Rebase changes from main into your branch
```
