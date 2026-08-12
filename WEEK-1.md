# Week 1 — the Phase 0 checklist (closed 12 August 2026)

Phase 0. Roughly 15–20 hours. Everything here is real work; nothing is placeholder.

Historical record, not a live tracker. Live tracking is `ROADMAP.md`. Every box below
was re-verified against its artefact on 12 August 2026 rather than ticked from memory:
licence files fetched from each repository, branch protection and secret scanning read
back from the GitHub API, the deployment and the organisation profile fetched logged
out, and the Day 7 number audit actually run. Two items were still open at close and
were moved to `ROADMAP.md` rather than left here; they are named under Day 6.

---

## Before you start

Files in this bundle are grouped by destination repo. The save-paths table in chat
maps every one. Clone all seven repos under `~/code/` first:

```
cd ~/code
for r in mind grid lens core docs private; do
  gh repo clone codronahq/$r codrona-$r
done
gh repo clone codronahq/.github codrona-dotgithub
```

Note the local directory names are prefixed `codrona-` because `~/code` is shared
with other live projects and a bare `core/` or `docs/` would be ambiguous. The git
remotes are unaffected.

---

## Day 1 — licences and legal

The two genuinely blocking artefacts. Do these first; everything else can slip.

- [x] Copy `docs/` files into `~/code/codrona-docs/`
- [x] Fetch the AGPL text (too long to include here):
      `curl -o LICENSE https://www.gnu.org/licenses/agpl-3.0.txt`
      into each of `mind`, `grid`, `lens`, `core`
- [x] `docs/LICENSE` gets CC-BY-4.0 instead — it is prose, not software
- [x] Confirm `core/packages/design-tokens/LICENSE` is the MIT text (included)
- [x] Commit ADR-0001 and LEGAL.md to `docs`
- [x] **Verify the four VERIFY rows in LEGAL.md.** Open each source, read the actual
      licence, record it with today's date. If a source has no stated licence, write
      that down — "no licence found" is a valid verified state and it means do not
      ingest. This gates all of Phase 1.
- [x] Push `docs`; confirm it renders on github.com logged out

## Day 2 — organisation surface

- [x] Copy `dotgithub/` contents into `~/code/codrona-dotgithub/`
      (note: `profile/README.md` is what renders on the org page)
- [x] Push, then open `https://github.com/codronahq` **in a private window** and
      confirm the profile README renders. Owner view is not proof.
- [x] Copy `private/` files into `~/code/codrona-private/`, push, confirm it is
      private from a logged-out check (404 is the correct result)
- [x] Branch protection on `main` for all six public repos:
      require PR, require status checks, no force push
- [x] Enable Dependabot alerts and secret scanning per repo

## Day 3 — CLA Assistant

Non-negotiable, and it must be proven, not assumed.

- [x] Grant third-party OAuth application access for the org:
      `https://github.com/organizations/codronahq/settings/oauth_application_policy`
      New orgs block these by default, which is what makes this step invisible until
      it fails.
- [x] Publish `CLA.md` as a public gist (CLA Assistant reads a gist, not a repo file)
- [x] Sign in at `https://cla-assistant.io/` and link the gist to `mind`, `grid`,
      `lens`, and `core`
- [x] **Prove it fires.** CLA Assistant registers no visible webhook and never
      appears under Installed GitHub Apps, so the only real test is a pull request
      from an account that is not an owner. Create a throwaway GitHub account, fork
      `docs`, open a trivial PR, and confirm the CLA check appears.
      If you skip this, you do not know whether the CLA works, and you will find out
      when it is too late to fix.
- [x] Close the test PR; keep the throwaway account for future integration tests

Make the test PR contain real content. Whitespace-only changes get silently undone by
the end-of-file and trailing-whitespace hooks, aborting the commit and leaving a
pushed branch with zero commits.

## Day 4 — core monorepo

- [x] Copy `core/` files into `~/code/codrona-core/`
- [x] `pnpm install`
- [x] `pnpm add -D turbo prettier typescript -w`
- [x] Verify the token package type-checks:
      `./node_modules/.bin/tsc --noEmit -p packages/design-tokens`
      (bare `npx tsc` resolves a bogus `tsc@2.0.4`)
- [x] Scaffold `apps/web` as a minimal Next.js app consuming the Tailwind preset —
      one page rendering the ten rating tiers as swatches. This is the first visual
      proof the design system works, and it is what Vercel will deploy.
- [x] Push; confirm CI green on the pushed commit, not just locally

## Day 5 — Python service and CI

- [x] Copy `mind/` files into `~/code/codrona-mind/`
- [x] `echo $VIRTUAL_ENV` — must be empty. `deactivate` if not.
      A stray venv from another project will absorb the install with no warning.
- [x] `python3.11 -m venv .venv && source .venv/bin/activate`
      Bare `python3` is 3.10 on this host, below every service's
      `requires-python = ">=3.11"`. It builds a venv that silently
      diverges from CI; the tell is `.venv/lib/python3.10/`.
- [x] `pip install -e ".[dev]"`
- [x] `pre-commit install`
- [x] `pre-commit run --all-files` — act on this result, not the commit hook's.
      The hook scopes mypy to changed files; `--all-files` is the real gate.
- [x] `pytest` green
- [x] Push; confirm CI green on GitHub
- [x] Copy `lens/`, `grid/` files into their repos and push

## Day 6 — deployment and observability

- [x] Import `codrona-core` into Vercel, root directory `apps/web`
- [x] Set any `NEXT_PUBLIC_*` variables in the Vercel project for **both** Production
      and Preview **before** the first deploy — they are baked at build time and
      `.env.local` never reaches Vercel
- [x] Deploy; note the assigned `*.vercel.app` URL
- [x] **Open it in a private window.** Logged-out verification is the standard.
- [x] Record the URL as the canonical Codrona address until a domain exists

Two items from this day were not done by the close of Phase 0 and were moved to
`ROADMAP.md`: a public status page, and the five-minute GitHub Actions cron that keeps
warm-able services warm. Both are §7 always-live requirements, and at close neither had
left an artefact anywhere in the organisation — no monitor URL, no `schedule:` trigger.

## Day 7 — audit and close

- [x] Tick every completed box in `docs/ROADMAP.md` and push
- [x] Confirm `origin` is at HEAD for all seven repos
- [x] Confirm CI green on the pushed commit of each repo with a workflow
- [x] Grep the public repos for any number not traceable to Canonical Numbers.
      Label enums and `__pycache__` are false positives, not stale claims.
- [x] Confirm no PROVISIONAL threshold has leaked into a README or the org profile
- [x] Apply the always-live test to the deployed page: untouched eight months, opened
      on hotel wifi — working in three seconds? If not, re-architect now rather than
      at launch.
- [x] **List the gaps explicitly before declaring Phase 0 complete.** Anything not
      ticked is a gap, not a rounding error.

---

## Carried into week 1 from the ritual

- [x] **PyPI `codrona`** — claimed 4 Aug 2026 as a placeholder `0.0.0`; the real SDK ships from `core` in Phase 6
- [x] Calendar reminder confirmed for **1 Nov 2026: rename codronahq → codrona**

## Deliberately not in week 1

Domains (deferred until there is revenue). The master context was amended accordingly:
the canonical host is `codrona.vercel.app`, and the `codrona.dev/u/<handle>` URLs are
aspirational until a domain is bought.
