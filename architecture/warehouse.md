# Warehouse — star schema and SCD-2

**Status:** Design, Phase 1 (weeks 2–3)
**Engine:** dbt. DuckDB locally, BigQuery sandbox / Databricks Free Edition at scale.
**Downstream mart:** MS SQL Server in Docker, for the BI consumption layer.

---

## 1. Why SCD-2 here is load-bearing, not decorative

Two facts about this domain force slowly-changing dimensions:

- **Problem difficulty is revised.** Codeforces re-rates problems. Tags are added
  and corrected. A problem rated 1400 in 2019 may read 1600 today.
- **User rating is the target variable.** A user's rating at the moment of a
  submission is the thing the skill model is trying to reason about.

Type-1 dimensions would overwrite both. Training a model on *today's* problem
difficulty against a *2019* submission leaks future information into the past —
the model learns from a rating that was assigned partly because of that very
submission. SCD-2 is what makes the corpus temporally honest.

## 2. Layers

```
models/
  staging/        one model per source entity, light typing, no joins
  intermediate/   cross-judge unification, deduplication
  marts/
    core/         dimensions and facts
    observatory/  aggregates for the public dashboards
```

Staging models are views. Marts are tables. Intermediate is ephemeral except where
a materialisation measurably helps.

This document describes the intended shape and names models that are planned as
well as models that exist. It is not the inventory: `dbt ls --resource-type model`
in `lens` is, and a list repeated here would drift from it within a phase.

## 3. Staging

```
staging/
  codenet/     stg_codenet__submissions.sql,  stg_codenet__problems.sql
  codeforces/  stg_cf__submissions.sql, stg_cf__problems.sql,
               stg_cf__users.sql, stg_cf__contests.sql
  atcoder/     stg_atcoder__submissions.sql, stg_atcoder__problems.sql
  _sources.yml
```

Staging does exactly four things: read the Parquet partition, cast types, rename to
canonical column names, apply the verdict mapping. No joins, no business logic, no
filtering other than structurally malformed rows. Keeping this layer thin is what
makes a source's quirks debuggable in isolation.

## 4. Intermediate

| Model | Purpose |
|---|---|
| `int_problems__unified` | Union all judges' problems on `problem_key`; resolve tag vocabularies to a shared taxonomy |
| `int_submissions__unified` | Union all judges' submissions; drop orphans whose `problem_key` has no match, counting them |
| `int_users__rating_history` | Reconstruct rating timelines from contest results |
| `int_problems__change_detect` | Hash the mutable attributes of each problem to drive SCD-2 |

The orphan drop happens **here**, at the staging boundary, and emits a count into
the data-quality report. It never happens by mutating an upstream table.

## 5. Dimensions

### `dim_problem` — SCD-2

| Column | Notes |
|---|---|
| `problem_sk` | surrogate key, hash of (`problem_key`, `valid_from`) |
| `problem_key` | natural key, `{judge}:{native_id}` |
| `judge`, `title`, `time_limit_ms`, `memory_limit_kb` | |
| `rating_official` | **tracked** — changes open a new version |
| `tags` | **tracked** — changes open a new version |
| `valid_from`, `valid_to` | `valid_to` is `9999-12-31` for the current row |
| `is_current` | boolean convenience flag |
| `version` | monotonic per `problem_key` |

Implemented with `dbt snapshot`, strategy `check`, on the tracked columns only.
Cosmetic changes (title whitespace, statement URI) must not open a version — version
churn destroys the usefulness of the drift analysis.

### `dim_user` — SCD-2

Tracks `rating`, `max_rating`, `tier`. A new version per rating change, which for an
active competitor is one row per contest. This table is the spine of the "climb"
narrative and the rating-color UI.

### `dim_contest`, `dim_date`, `dim_language`

Type-1. Contests and dates do not change; language is a small conformed lookup.

## 6. Facts

### `fct_submission` — grain: one row per submission

| Column | Notes |
|---|---|
| `submission_key` | degenerate dimension |
| `problem_sk` | **resolved as-of `submitted_at`**, not to the current version |
| `user_sk` | same |
| `contest_sk`, `date_sk`, `language_sk` | |
| `verdict` | canonical enum |
| `is_accepted` | the model's label |
| `execution_time_ms`, `memory_kb`, `source_length_bytes` | |
| `attempt_ordinal` | nth attempt by this user on this problem |
| `seconds_since_first_attempt` | feeds the survival model |

The as-of join is the entire point of the SCD-2 work. Written carelessly this
becomes a join to `is_current = true` and the temporal honesty evaporates. It gets a
dedicated dbt test.

Partitioned by `date_sk`, clustered on `problem_sk` — ~30M rows is small for a
warehouse and large for a laptop, and the local DuckDB path relies on partition
pruning to stay interactive.

### `fct_attempt_sequence` — grain: one row per (user, problem)

Collapses a user's attempts on a problem into a solve trajectory: attempt count,
first and last verdict, time to solve, and a censoring flag for problems never
solved. Censored rows are data, not missing values — the survival model needs them.

## 7. Observatory marts

Five aggregates feed the public "State of Competitive Programming" surfaces.

| Model | Content |
|---|---|
| `obs_rating_distribution` | Cohort users per rating band, with share of cohort |
| `obs_activity_by_year` | Submissions, active users and participation rate per year |
| `obs_tag_landscape` | Per-tag problem counts, Codeforces ratings, population-wide solve counts |
| `obs_country_participation` | Cohort users by self-declared country, undeclared emitted as its own row |
| `obs_organization_participation` | Cohort users by declared organisation, free text and unnormalised |

Two figures in this set are not what an earlier draft of this document promised, and the difference is worth stating. `obs_rating_distribution` is a single-snapshot distribution, not a histogram over time: `user.ratedList` returns today's rating only, so rating inflation cannot be measured until a rating-history source exists, which is Phase 2 work. And the activity series is left-truncated by construction — the cohort was collected with `activeOnly=true`, so the final year reads as fully active because it cannot read otherwise. The volume curve is the cohort's registration curve, not the growth of competitive programming. Participation rate is the figure that survives, and it is flat.

**Aggregation is not anonymisation, so two guards enforce the boundary rather than assuming it.** `assert_observatory_holds_no_identities` reads `information_schema`, so an identifying column fails when it is *added* rather than when someone notices what a chart renders. `assert_observatory_no_small_cells` enforces a minimum cell size of five people, recomputing the count from the output instead of trusting either model's own flag.

The two person-counting tables suppress differently, and the asymmetry was measured rather than assumed. Organisations collapse below the threshold into a single `(below reporting threshold)` row carrying only a count. Countries keep their name and count and publish no rating statistics, because 64 of 158 country rows hold fewer than five users and the smallest holds one — where a mean equals a max equals that person's exact current rating, beside a country that `user.ratedList` is filterable by. An organisation name at two users identifies a cohort; a country name at one user identifies a country, and the coverage figure is information a reader is owed.

### The export

The aggregates live in a DuckDB file outside the repository, so nothing off the maintainer's machine can read them. `codrona_lens.observatory.export` serialises them to committed JSON under `lens/exports/observatory/`, which is the Tier 0 answer from the sustainability architecture: a static file cannot pause and puts no service on the hot path.

The published column set is an allowlist, and a warehouse column absent from it aborts the export rather than being dropped quietly — quiet dropping is how a new identifying field would reach a chart with nobody deciding. Caveats are read from the dbt schema rather than retyped, so a figure cannot ship without the warning that makes it honest. The output carries no timestamp, so regenerating an unchanged warehouse produces identical bytes and any diff means something moved. Two separate gates cover it: a test that reads only the written files, and a pre-commit hook that regenerates and byte-compares. They are non-overlapping by design — a corrupted count passed the first and was caught only by the second.

`obs_topic_trends`, `obs_difficulty_drift`, `obs_language_share` and `obs_india_vs_world` were named in the Phase 0 design and are not built. `obs_college_readiness` is **excluded from the public set**: it is institutional and belongs to the private open-core layer under ADR-0001.

## 8. Tests

Severity is deliberate: `error` halts the DAG before marts publish, `warn` records
and continues.

| Test | Model | Severity |
|---|---|---|
| `unique` + `not_null` on every `_sk` | all dims | error |
| `relationships` fact → dim | `fct_submission` | error |
| `accepted_values` on `verdict` | staging | error |
| No overlapping validity windows | SCD-2 dims | error |
| Exactly one `is_current` per natural key | SCD-2 dims | error |
| As-of join correctness (no fact joined to a version postdating it) | `fct_submission` | error |
| `submitted_at` within judge's plausible range | staging | warn |
| `execution_time_ms` within limits | staging | warn |
| Orphan rate below threshold | intermediate | warn |
| Row count within expected band | marts | warn |

The three custom tests — validity overlap, single-current, and as-of correctness —
are the ones worth writing carefully. Generic dbt tests will not catch a broken
SCD-2 implementation, and a broken SCD-2 implementation produces a model that looks
excellent in backtest and fails in production.
