# GITHUB_AI_INSTRUCTIONS.md

## Goal
You are allowed to update this repo and push changes. Work safely, keep changes small, and produce clear commit history.

---

## Rules
- **Never commit secrets** (API keys, tokens, `.env`, credentials, private URLs).
- **Pull before you start** and **pull/rebase before you push** if needed.
- **Work on a branch**, not directly on `main`.
- Keep commits **small and logical** (1 purpose per commit).
- If unsure, **do the smallest safe thing** and leave a note in the PR/summary.

---

## Standard Workflow (Required)
1. **Check status**
   - `git status`

2. **Sync**
   - `git checkout main`
   - `git pull origin main`

3. **Create a branch**
   - Branch name format:
     - `chore/<short-thing>` (cleanup/structure/tooling)
     - `docs/<short-thing>` (README/docs)
     - `fix/<short-thing>` (bugfix)
     - `feat/<short-thing>` (new feature)
   - Example:
     - `git checkout -b docs/readme-setup`

4. **Make changes**
   - Keep changes focused.
   - Don’t reformat entire files unless needed.

5. **Stage changes**
   - Prefer staging by file:
     - `git add path/to/file`
   - Use `git add -p` for partial staging if mixed edits.

6. **Commit**
   - Always run `git status` first to confirm what’s included.
   - Use the commit message rules below.

7. **Push**
   - `git push -u origin <branch-name>`

8. **PR + Summary**
   - Open a PR from your branch → `main`.
   - In PR description include:
     - What changed (bullets)
     - Why
     - How to test (if applicable)
     - Any risks / follow-ups

---

## Commit Message Rules
Use this format:

`<type>: <short present-tense summary>`

### Allowed types
- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation only
- `chore:` cleanup, tooling, refactors w/out behavior change
- `test:` tests only
- `style:` formatting only (avoid unless requested)

### Message style
- Keep it **under ~60 characters** if possible.
- Don't use any emojis. 
- Sound as human and casual as possible. 
- Use **present tense** (“add”, “fix”, “remove”, “update”).
- Be specific (avoid “stuff”, “changes”, “updates”).

### Examples
- `docs: clarify local setup steps`
- `chore: add gitignore for node and macOS`
- `fix: handle empty response in parser`
- `feat: add basic health check endpoint`

### When to split commits
Split if you’re doing different kinds of work, e.g.:
- One commit for `README` updates
- One commit for adding `.gitignore`
- One commit for moving/renaming files
- One commit for code changes

---

## Push / Sync Conflict Handling
If push is rejected:
1. `git pull --rebase origin main`
2. Resolve conflicts carefully (don’t delete code blindly).
3. `git rebase --continue`
4. `git push`

If rebase gets messy:
- Stop and leave a note explaining what happened and what needs human input.

---

## What NOT to Do
- Don’t force push to `main`.
- Don’t rewrite repo history unless explicitly told.
- Don’t add heavy tooling (Docker, complex CI, new frameworks) for a small build.
- Don’t rename large folders/files without a clear reason.

---

## Final Deliverable
After pushing, provide:
- Branch name
- List of commits
- Short summary of changes
- Any risks/follow-ups