# Week 1 — the literal checklist

Phase 0. Roughly 15–20 hours. Everything here is real work; nothing is placeholder.

At the end of week 1 the organisation is public, licensed, documented, and CI-gated,
and Phase 1 can start without any setup detour.

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

- [ ] Copy `docs/` files into `~/code/codrona-docs/`
- [ ] Fetch the AGPL text (too long to include here):
      `curl -o LICENSE https://www.gnu.org/licenses/agpl-3.0.txt`
      into each of `mind`, `grid`, `lens`, `core`
- [ ] `docs/LICENSE` gets CC-BY-4.0 instead — it is prose, not software
- [ ] Confirm `core/packages/design-tokens/LICENSE` is the MIT text (included)
- [ ] Commit ADR-0001 and LEGAL.md to `docs`
- [ ] **Verify the four VERIFY rows in LEGAL.md.** Open each source, read the actual
      licence, record it with today's date. If a source has no stated licence, write
      that down — "no licence found" is a valid verified state and it means do not
      ingest. This gates all of Phase 1.
- [ ] Push `docs`; confirm it renders on github.com logged out

## Day 2 — organisation surface

- [ ] Copy `dotgithub/` contents into `~/code/codrona-dotgithub/`
      (note: `profile/README.md` is what renders on the org page)
- [ ] Push, then open `https://github.com/codronahq` **in a private window** and
      confirm the profile README renders. Owner view is not proof.
- [ ] Copy `private/` files into `~/code/codrona-private/`, push, confirm it is
      private from a logged-out check (404 is the correct result)
- [ ] Branch protection on `main` for all six public repos:
      require PR, require status checks, no force push
- [ ] Enable Dependabot alerts and secret scanning per repo

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

- [ ] Copy `mind/` files into `~/code/codrona-mind/`
- [ ] `echo $VIRTUAL_ENV` — must be empty. `deactivate` if not.
      A stray venv from another project will absorb the install with no warning.
- [ ] `python3 -m venv .venv && source .venv/bin/activate`
- [ ] `pip install -e ".[dev]"`
- [ ] `pre-commit install`
- [ ] `pre-commit run --all-files` — act on this result, not the commit hook's.
      The hook scopes mypy to changed files; `--all-files` is the real gate.
- [ ] `pytest` green
- [ ] Push; confirm CI green on GitHub
- [ ] Copy `lens/`, `grid/` files into their repos and push

## Day 6 — deployment and observability

- [ ] Import `codrona-core` into Vercel, root directory `apps/web`
- [ ] Set any `NEXT_PUBLIC_*` variables in the Vercel project for **both** Production
      and Preview **before** the first deploy — they are baked at build time and
      `.env.local` never reaches Vercel
- [ ] Deploy; note the assigned `*.vercel.app` URL
- [ ] **Open it in a private window.** Logged-out verification is the standard.
- [ ] Record the URL as the canonical Codrona address until a domain exists
- [ ] Set up a status page (UptimeRobot or Better Stack free tier) pointing at it
- [ ] GitHub Actions cron pinging every 5 minutes

## Day 7 — audit and close

- [ ] Tick every completed box in `docs/ROADMAP.md` and push
- [ ] Confirm `origin` is at HEAD for all seven repos
- [ ] Confirm CI green on the pushed commit of each repo with a workflow
- [ ] Grep the public repos for any number not traceable to Canonical Numbers.
      Label enums and `__pycache__` are false positives, not stale claims.
- [ ] Confirm no PROVISIONAL threshold has leaked into a README or the org profile
- [ ] Apply the always-live test to the deployed page: untouched eight months, opened
      on hotel wifi — working in three seconds? If not, re-architect now rather than
      at launch.
- [ ] **List the gaps explicitly before declaring Phase 0 complete.** Anything not
      ticked is a gap, not a rounding error.

---

## Carried into week 1 from the ritual

- [ ] **PyPI `codrona`** — rate-limited on 3 Aug. Retry once; do not loop.
      `cd /tmp/codrona-pypi-claim && source .venv/bin/activate && twine upload dist/*`
- [ ] Calendar reminder confirmed for **1 Nov 2026: rename codronahq → codrona**

## Deliberately not in week 1

Domains (deferred until there is revenue). The `codrona.dev/u/<handle>` profile URLs
in the master context are aspirational until then and the doc needs amending to say
so.
