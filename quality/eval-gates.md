# Eval gates

Every named failure mode has a measurable gate. Nothing ships below its gate.

**Read this first.** The thresholds below are **provisional targets**, set before any
model exists. They are not measurements and must never be quoted as results. Each is
ratified or revised in Phase 2 against a real baseline, and the ratified value is
recorded in the Canonical Numbers block. Until then a threshold's status is
`PROVISIONAL` and it may not appear in a README, a dashboard, or a résumé bullet.

A gate is only real when it runs in CI and can fail the build.

**A statistical threshold without its baseline is not a gate.** G1, G2 and G3 measure
model quality, and for those an absolute number means nothing on its own: the question
is always what a trivial model already scores. Every statistical target below is
therefore expressed as a required improvement over a stated baseline — the constant
predictor, or the best a model can do knowing only one crude fact — and the baseline
travels with the target wherever it is quoted. All three were absolute thresholds until
15 Aug 2026 and all three were passable by a trivial model at the time; the measurements
are recorded in each gate below.

This rule applies to statistical gates only. G4 through G9 are engineering budgets —
latency, attack success rate, freshness lag — where the null model is a broken service
rather than a constant predictor, and an absolute number is the correct form. G8 and
G10 are structural and already state their own coverage boundaries.

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
| Brier reduction vs that population's own constant-predictor baseline | ≥ 25% | PROVISIONAL |
| Brier reported per population, never pooled across judges | required | PROVISIONAL |
| The baseline published beside every Brier figure | required | PROVISIONAL |
| Expected calibration error (10 bins) | ≤ 0.05 | PROVISIONAL |
| Reliability curve | published artefact, every release | PROVISIONAL |

**Why a reduction rather than an absolute number.** The former target was Brier ≤ 0.18.
Measured against the constant-predictor baseline of each population:

| Population | Baseline Brier | Reduction 0.18 demanded |
|---|---|---|
| Codeforces — full response matrix, unmerged | 0.243562 | 26.1% |
| Codeforces — full response matrix, twin-merged | 0.243587 | 26.1% |
| **Codeforces — item bank, twin-merged — what Stage A actually fits** | **0.243166** | **26.0%** |
| CodeNet | 0.181701 | 0.94% |
| pooled | 0.227941 | 21.0% |

**The bank row is the operative one and the other two are shown so nobody grabs
the wrong figure.** Stage A filters the matrix to `in_public_problemset`, which is
11,764 problems of 33,248, so a baseline computed on the full matrix describes a
population the model is not fitted on. That is this document's own argument about
the twin merge — a baseline computed on a different matrix than the fit is
measuring nothing — turned on the filter, which moves the figure by 0.000421
against the merge's 0.000025, close to seventeen times as far. Measured, gated and
reproducible from
`lens`: `python3 -m codrona_lens.responses.matrix --verify-current`, against the
counts in `exports/model/responses.manifest.json`.

**And even the bank figure is not the number the gate compares against.** The split
is temporal, so the constant-predictor baseline is recomputed on the held-out
period itself and published beside the score. 0.243166 is the whole-bank figure and
the sanity check on that recomputation, not a substitute for it.

On the CodeNet half a constant predictor scores 0.181701, so the old gate was cleared by
a model that improved on nothing by one part in a hundred — and pooling hid it, reading
as a respectable 21% while one half went ungated. The 25% figure approximately preserves
the original intent on Codeforces, where 0.18 was a 26.1% reduction, and generalises it
to any population the model is fitted on.

The response definition these baselines assume is the first attempt per (user, problem)
pair. Under an "ever solved" definition the baselines would be 0.064616 and 0.057802, and
a 0.18 target would pass models three times worse than a constant on both halves. See
`analysis/irt-response-definition.md`.

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
| Rating MAE after 10-problem placement, pooled | ≤ 150 | PROVISIONAL |
| MAE within each rating band, vs that band's own-median baseline | ≥ 20% better | PROVISIONAL |
| MAE reported per band, never pooled alone | required | PROVISIONAL |
| Predictions carry an uncertainty interval | required | PROVISIONAL |
| Interval coverage at stated confidence | within ±5pp | PROVISIONAL |

**Why 150 and not 250.** Measured over the 55,484 current rated users:

| Predictor | MAE |
|---|---|
| the cohort median, knowing nothing | 316.0 |
| **a perfect five-band classifier** | **170.8** |
| a perfect 200-point-bin classifier | 44.7 |

The former target of 250 sat above the 170.8 oracle, so **a placement test that did
nothing but sort a user into one of five rating bands passed G2 with 32% headroom.** The
gate could not distinguish an ability estimator from a five-way classifier. 150 sits
below that oracle, so band identification alone cannot clear it, and 44.7 is the floor
that perfect 200-point resolution would reach.

Per-band reporting is required because the cohort is not uniform: 37,783 of 55,484
users — 68.1% — are **newbie**, and that band's own-median baseline is 208.0 against
69.0 for expert. A pooled MAE on this distribution is largely a statement about how
many beginners the cohort contains.

That sentence read "newbie or pupil" until 16 Aug 2026 and the count was never
wrong, only its label: 37,783 is newbie alone, and newbie-or-pupil is 45,960, or
82.8%. The distinction is not cosmetic here, because the band is the unit the gate
reports against, so a reader building five bands from the labels would compute
different baselines than the ones published above.

The five bands the 170.8 oracle assumes, named so the figure can be re-derived
rather than taken on trust — they are `dim_user.rank_name` groupings, not invented
cuts, and every count below comes from Codeforces' own rank boundaries:

| Band | Rating, as observed in the cohort | Users |
|---|---|---|
| newbie | −19 to 1199 | 37,783 |
| pupil and specialist | 1200–1599 | 13,200 |
| expert | 1600–1898 | 3,165 |
| candidate master, master, international master | 1900–2399 | 1,144 |
| grandmaster and above | 2403–3857 | 192 |

The ranges are observed rather than the boundaries themselves, which is why two
of them stop short of the next band's floor: nobody in the cohort sits at 1899 or
between 2400 and 2402. The cut points are Codeforces' own, so the reproduction is
`group by rank_name` rather than any threshold written here.

**A limitation this gate cannot fix.** The held-out users come from a cohort collected
with `activeOnly=true` over rated Codeforces users. A Codrona placement-test user is not
drawn from that population — they will be newer, likelier unrated, and weaker than even
the newbie band. The harness therefore validates against a population the product does
not serve, which is worth stating because cold start is exactly where the model is
weakest.

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
| Content features available for every problem in the serving set | 100% | PROVISIONAL |
| Feature set named per source, since the two sources share none | required | PROVISIONAL |
| Degradation measured per source, never pooled | required | PROVISIONAL |
| Content-only Brier degradation vs full-signal | ≤ 0.05 absolute | PROVISIONAL |

**The former wording was unachievable by construction, not by effort.** It required
"tags + statement embedding" for 100% of problems. Codeforces statement text can never be
stored under link-never-host, and CodeContests supplies statements only for CodeNet-sourced
problems. Measured, the two problem dimensions share no predictive feature at all:

| Source | Tags | Statement | Difficulty label |
|---|---|---|---|
| Codeforces | 38-term vocabulary, 96.5% of the bank | never | rating and `solved_count` |
| CodeNet | none, no tag column from any source | 3,474 of 4,046 | none on any row |

So the feature set is named per source: tags, rating and `solved_count` for Codeforces;
statement embedding and the resource limits for CodeNet. Degradation is measured per
source because pooling would let dense Codeforces coverage hide thin CodeNet coverage —
the same failure the pooled Brier had in G1.

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

## G12 — Response-unit integrity

**Failure guarded:** the matrix every model consumes stops being the thing these
baselines were measured on, and nothing says so. A refactor of the response builder
changes a count; the fit still runs, the calibration report still prints, and every
figure in this document silently describes a different population.

| Metric | Target | Status |
|---|---|---|
| Structural invariants hold on any dataset | no violation | ENFORCED |
| Pinned counts match the real warehouse | 13 counts, exact | ENFORCED |
| Committed manifest matches a fresh build | no differing count or column | ENFORCED |
| Artefact on disk matches the manifest | row count and schema | ENFORCED |

**The gate is split in two, and the split is what makes it runnable.** The pinned
counts are real-data figures — 23,607,105 fact rows, 22,843,153 attempts, 11,176,774
unmerged responses, 11,158,572 merged, 1,182 twin keys carrying evidence, and the
twin rule's own rating classes and excluded populations. Pinned unconditionally they
cannot pass against the synthetic fixtures CI builds, which is the wall G8 already
meets and answers with the `real_data` dbt tag. So the structural invariants run on
every push against any dataset, and the pinned counts run only under `--real-data`.
A test asserts that the pinned half **must** fail on fixtures, because a real-data
gate that passes on invented rows is gating nothing.

**The reconciliation pair is what catches the failure worth catching.** A merge must
move rows between keys and never remove any, so responses fall by exactly the
duplicate count while attempts stay identical. A remap that relabels without
collapsing first attempts passes the attempt assertion and fails the response one; a
remap that drops rows does the reverse. Neither count catches it alone.

**Two of the assertions were wrong when first written**, and both are recorded in
`architecture/phase-2-modelling.md` rather than quietly corrected: one counted a
different quantity than its name claimed, and the twin rule was first implemented
from prose that disagreed with its own reproduction query.

**The schema block exists because counts cannot see shape.** A column added, dropped,
renamed, retyped or reordered leaves every count in the manifest identical. That was
demonstrated on real data rather than argued: the change adding `problem_contest_id`
to the artefact moved none of the thirteen pinned counts. The manifest therefore
records the emitted schema, read back from the engine rather than restated, and the
comparison includes column order.

**What this gate does not cover.** It gates the build, the committed manifest, and the
artefact's row count and schema. It does not gate the emitted Parquet's bytes: the
artefact is uncommitted, so the manifest compares counts and a column list, and
neither depends on row order. The `ORDER BY`
that would make the file byte-reproducible is kept and is deliberately **not** claimed
as a gate — at fixture scale its removal cannot be detected, and at real scale the
negative case is nondeterministic rather than detectable.

**Two commands, two links, neither subsuming the other.** Three things are in play —
the warehouse, the committed manifest, and the Parquet Stage A reads. `--verify-current`
rebuilds from the warehouse and closes both links, at the cost of a full scan of 23.6
million fact rows with two window functions; it is the maintainer command, run before a
fit and before a release rather than on every commit, because a gate slow enough to be
skipped will be skipped. `--verify-artefact` closes only the manifest-to-Parquet link,
from the Parquet footer and a JSON file, with no warehouse and no scan — measured at
0.097s against the real 11,158,572-row artefact, which is cheap enough to hook. A
missing artefact skips loudly under the second, which runs on machines that never built
one, and fails under the first, which runs when there is about to be something to fit.

**Until 16 Aug 2026 neither command opened the artefact at all.** `--verify-current`
compared a fresh build against the manifest and never read the file, so an artefact
deleted, truncated or written by another code path passed clean — while the function's
own docstring claimed to catch precisely that. The gate watched the manifest rather
than the thing the manifest describes.

**G11 and G13 are deliberately absent from this document.** They are specified in
`architecture/phase-2-modelling.md` with status `DESIGNED`: they gate a serving path
that does not exist until Phase 4, so nothing runs them. Listing them here would imply
something does. They arrive when the serving path does.

**Runs:** invariants on every push, in CI, as part of the test suite in `lens`. Pinned
counts and the manifest comparison under `--real-data` and `--verify-current`; the
artefact comparison under `--verify-artefact`, or as part of `--verify-current`. All
against `exports/model/responses.manifest.json`.

---

## Release gate

A release requires, together:

1. G1, G2, G3 at target on the golden set, each reported against its stated baseline and per population or band rather than pooled
2. G4 leakage at zero, with no red-team regression under G5
3. G7 green against staging
4. G8, G10 and G12 green on the publishing run, G12 including its pinned counts and its manifest comparison rather than its invariants alone
5. Every threshold cited in any public artefact traced to Canonical Numbers

Any one failing blocks the release. There is no override; the correct response is to
fix the code or, with an explicit recorded decision, revise the threshold — never to
skip the gate.
