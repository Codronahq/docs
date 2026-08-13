# Eval gates

Every named failure mode has a measurable gate. Nothing ships below its gate.

**Read this first.** The thresholds below are **provisional targets**, set before any
model exists. They are not measurements and must never be quoted as results. Each is
ratified or revised in Phase 2 against a real baseline, and the ratified value is
recorded in the Canonical Numbers block. Until then a threshold's status is
`PROVISIONAL` and it may not appear in a README, a dashboard, or a résumé bullet.

A gate is only real when it runs in CI and can fail the build.

---

## Status legend

| Status | Meaning |
|---|---|
| `PROVISIONAL` | Target set by judgement; no baseline yet |
| `RATIFIED` | Measured against real data; value is now canonical |
| `ENFORCED` | Wired into CI and capable of blocking |

---

## G1 — Skill model calibration

**Failure guarded:** the model is confident and wrong, so recommendations sit at the
wrong difficulty and the ladder stops adapting.

| Metric | Target | Status |
|---|---|---|
| Brier score, held-out submissions | ≤ 0.18 | PROVISIONAL |
| Expected calibration error (10 bins) | ≤ 0.05 | PROVISIONAL |
| Reliability curve | published artefact, every release | PROVISIONAL |

Calibration matters more than raw accuracy here. A recommender that maximises
learning at the ability edge needs P(solve) ≈ 0.6–0.7 to mean what it says. AUC can
be excellent while calibration is useless.

Held-out split is **temporal**, not random — train on submissions before a cutoff,
evaluate after. A random split leaks, because a user's later submissions inform their
earlier ones.

**Runs:** on every change to `mind/models/**`. Blocks model release.

---

## G2 — Cold start

**Failure guarded:** a new user with no history gets nonsense recommendations and
leaves in the first session.

| Metric | Target | Status |
|---|---|---|
| Rating MAE after 10-problem placement | ≤ 250 | PROVISIONAL |
| Predictions carry an uncertainty interval | required | PROVISIONAL |
| Interval coverage at stated confidence | within ±5pp | PROVISIONAL |

The uncertainty requirement is a product commitment, not just a metric: the interface
says when it does not know. An honest wide interval passes; a confident wrong point
estimate fails.

**Runs:** simulated cold-start harness over held-out users.

---

## G3 — New problems, no history

**Failure guarded:** a problem published yesterday has no submission signal and
falls out of the recommender entirely.

| Metric | Target | Status |
|---|---|---|
| Content-only prediction (tags + statement embedding) available for every problem | 100% | PROVISIONAL |
| Content-only Brier degradation vs full-signal | ≤ 0.05 absolute | PROVISIONAL |

Enforced structurally: the feature pipeline fails if any problem in the serving set
lacks content features.

---

## G4 — Hint quality and solution leakage

**Failure guarded:** the coach hands over an answer, which destroys both the learning
value and the integrity claim.

| Metric | Target | Status |
|---|---|---|
| Leak-classifier positive rate on the golden hint set | 0 | PROVISIONAL |
| LLM-as-judge hint usefulness | ≥ 4.0 / 5 | PROVISIONAL |
| Integrity mode: solution-level help during a live contest | 0 instances | PROVISIONAL |

Zero is the right target for leakage and it is achievable because the golden set is
fixed and adversarial. The set lives in the private repo; the harness is public.

**Runs:** on every change to agent prompts, tools, or graph. Blocks agent release.

---

## G5 — Prompt injection

**Failure guarded:** a user's submitted code or a problem statement contains
instructions the agent obeys.

| Metric | Target | Status |
|---|---|---|
| Attack success rate over the red-team suite | ≤ 2% | PROVISIONAL |
| Suite size | ≥ 200 cases at Phase 4 | PROVISIONAL |
| Regression vs previous release | 0 new successes | PROVISIONAL |

User code and problem statements are untrusted input by definition. The zero-regression
clause is the operative one — a rising rate blocks merge even if it stays under target.

**Runs:** every merge to `mind/agents/**`.

---

## G6 — Data freshness

**Failure guarded:** the warehouse silently stops updating and recommendations decay
without anyone noticing.

| Metric | Target | Status |
|---|---|---|
| Judge → warehouse lag | ≤ 24h | PROVISIONAL |
| Alert on breach | required | PROVISIONAL |

**Runs:** continuous, as an SLO with alerting rather than a CI check.

---

## G7 — Contest-day load

**Failure guarded:** the judge plane collapses at the exact moment it matters, which
is the only moment anyone will remember.

| Metric | Target | Status |
|---|---|---|
| p99 verdict latency under k6 spike | ≤ 3000 ms | PROVISIONAL |
| Error rate under spike | ≤ 0.5% | PROVISIONAL |
| Queue drain after spike | ≤ 120 s | PROVISIONAL |

Spike profile models a contest start: near-idle to peak in under 60 seconds.

**Runs:** k6 in CI against a staging deployment. Blocks release.

---

## G8 — Warehouse data quality

**Failure guarded:** a bad transform publishes to the dashboards.

| Metric | Target | Status |
|---|---|---|
| dbt tests at `error` severity | 100% pass | ENFORCED |
| Orphan rate, submissions → problems | ≤ 0.5% | ENFORCED |
| SCD-2 invariants (no overlap, one current, as-of correctness) | 100% pass | ENFORCED |

**Runs:** every push, in CI. `dbt build` executes against synthetic fixtures built by `scripts/make_ci_fixtures.py` in `lens`, so a failing test blocks rather than being noticed later on a laptop. It will additionally run before `publish_marts` once the Airflow DAG exists; that is an extra trigger, not the thing that makes this gate real.

Three qualifications, so the status is not read as more than it is. The orphan rate is enforced at **zero** rather than at 0.5% — `relationships` tests plus `assert_dim_problem_covers_corpus` admit no orphan at all, which is stricter than the target and is why the target itself has never been exercised. The SCD-2 invariants are **vacuously true today**, since one collection snapshot means one version per key; they were written before the second snapshot deliberately, and each was proven to fail against an injected defect rather than merely observed to pass. And the tests that pin counts of the real world carry the `real_data` tag and are excluded in CI — `dbt list --select tag:real_data` names them — so CI gates every data test but those.

---

## G9 — Cost

**Failure guarded:** credits burn out mid-build and the cloud story dies unfinished.

| Metric | Target | Status |
|---|---|---|
| Cost per 1,000 judged runs | tracked and published | PROVISIONAL |
| Credit burn-down vs plan | alert at 60% and 85% | PROVISIONAL |
| infracost delta on infra PRs | reported, blocking above threshold | PROVISIONAL |

---

## G10 — Host-dependent derived values

**Failure guarded:** a published figure derived from the machine rather than from the
data — the session time zone, `$HOME`, the locale — differs between the laptop that
publishes it and the container that recomputes it, while every row count stays identical.

| Metric | Target | Status |
|---|---|---|
| Engines whose session zone is pinned *and asserted* | 3 of 3: dbt, Spark, DuckDB | ENFORCED |
| DuckDB connections opened outside the pinned helper | 0 | ENFORCED |
| Warehouse path resolved from the environment rather than `$HOME` | required | ENFORCED |

Separate from G8 rather than a line inside it, because G8 gates what the warehouse
contains and this gates the processes that read and write it. `dim_user.registered_at` is
TIMESTAMP WITH TIME ZONE, so `year()` resolves against the session zone: 2020 read 814
registrations under UTC against 812 under Asia/Kolkata, the observatory's cumulative
`registered_by_then` carried the shift into every later year, and G8 stayed green
throughout because no count changed — only which year each count was filed under. The
third-engine reproduction on Databricks did not catch it either, since the two columns it
moved are the two that comparison deliberately excludes. A container found it and a laptop
never could, which is the general point: a second machine is a test.

The rules are written to be capable of failing, which is the part that is easy to get
wrong. Two tests already named UTC and neither could have caught this: each configured UTC
in its own fixture and neither called the constructor it claimed to gate, so both asserted
a property of Spark rather than of this code and would have passed unchanged with the pin
deleted. Every rule here first poisons the live session or connection with a non-UTC zone,
then invokes the production path, then asserts the poison is gone — which fails on a CI
runner that is already UTC exactly as it fails on a laptop that is not. Each was shown to
fail against its own mutation before being trusted to pass, and the boundary value is
itself asserted, since a value that stopped straddling the year would quietly make every
other rule vacuous.

One rule is structural rather than behavioural: nothing outside the connection helper may
open DuckDB directly. The other rules gate the helper and none of them gates whether
anything uses it, so a new caller would be unpinned and unnoticed. That rule found three
connections on the day it was written.

The boundary is the session time zone and the warehouse path. Locale-dependent collation,
filesystem ordering, and any other value derived from the environment are **not** covered.
Naming what a gate does not cover is what separates it from a claim.

**Runs:** every push, in CI, as part of the test suite in `lens`.

---

## Release gate

A release requires, together:

1. G1, G2, G3 at target on the golden set
2. G4 leakage at zero, with no red-team regression under G5
3. G7 green against staging
4. G8 and G10 green on the publishing run
5. Every threshold cited in any public artefact traced to Canonical Numbers

Any one failing blocks the release. There is no override; the correct response is to
fix the code or, with an explicit recorded decision, revise the threshold — never to
skip the gate.
