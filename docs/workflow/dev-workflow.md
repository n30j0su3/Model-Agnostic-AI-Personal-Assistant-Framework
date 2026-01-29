# Dev HQ Workflow

This repository is the exclusive development HQ for the Framework.
All private data lives here and syncs only to the private remote.

## Remotes
- origin = private repo (dev)
- upstream = public repo (release)

## Branches
- main: private development branch
- public-release: sanitized public branch

## Daily Development Flow
1. Start a feature session:
   - Windows: `dev.bat`
   - macOS/Linux: `./dev.sh`
2. Work on `main` and commit normally.
3. Push to private:
   - `git push origin main`

## Publish to Public (Sanitized)
1. Ensure working tree is clean.
2. Run publish script:
   - `python scripts/publish-release.py --push`
3. This updates `public-release` and pushes to `upstream`.

## Rules
- Never push `main` to `upstream`.
- Keep `sessions/`, `workspaces/`, and `logs/` private.
- `docs/backlog.md` and `docs/backlog.view.md` are private-only.
