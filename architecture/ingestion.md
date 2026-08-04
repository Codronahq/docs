# Ingestion — three judges, one contract

**Status:** Design, Phase 1 (weeks 2–3)
**Prerequisite:** every source has a verified row in `LEGAL.md`. Rows marked VERIFY block the adapter that reads them.

---

## 1. Principle: no judge is load-bearing

Every source sits behind an adapter implementing the same interface. Adding
LeetCode, CodeChef, or SPOJ later is a new adapter, not a schema change. Losing a
source degrades the corpus; it never breaks the pipeline.

This is the structural expression of the denial plan: the models train on
CodeNet + Codeforces + AtCoder, none of which can revoke access, and no adapter's
failure is allowed to propagate past the staging layer.

```
                  ┌─────────────┐
   CodeNet ──────▶│             │
   Codeforces ───▶│   Adapter   │──▶ raw/ ──▶ staged/ ──▶ dbt ──▶ marts/
   AtCoder ──────▶│  interface  │   (bronze)  (silver)          (gold)
                  └─────────────┘
```

## 2. The adapter interface

Each adapter lives at `lens/ingest/adapters/<judge>.py` and implements:

```python
class JudgeAdapter(Protocol):
    judge_id: str                    # "codenet" | "codeforces" | "atcoder"
    min_interval_ms: int             # enforced in code, not by convention

    def discover(self, since: date | None) -> Iterator[EntityRef]: ...
    def fetch(self, ref: EntityRef) -> RawRecord: ...
    def normalise(self, raw: RawRecord) -> CanonicalSubmission | CanonicalProblem: ...
```

`normalise` is pure and unit-tested against fixtures. Fetching is retried with
exponential backoff; a 403, 429, or any challenge response aborts the run and
raises. The pipeline never routes around a block.

## 3. Lake layout

Medallion, on S3 in the cloud story and on local disk for the ₹0 dev path.

```
s3://codrona-lake/
  raw/{judge}/{entity}/ingest_date=YYYY-MM-DD/part-*.jsonl.zst
  staged/{judge}/{entity}/ingest_date=YYYY-MM-DD/part-*.parquet
  warehouse/                     # dbt target
```

- **raw** is immutable and byte-faithful. Never edited, never backfilled in place.
  It is the only thing that makes a bad transform recoverable.
- **staged** is typed Parquet in the canonical schema, partitioned by
  `ingest_date`, Zstandard-compressed. This is what dbt reads.
- Re-running an ingest for a date **replaces** that partition rather than appending,
  which makes the whole pipeline idempotent by construction.

**Dev path:** the same layout under `~/code/codrona-lake/` with dbt-duckdb reading
Parquet directly. No cloud account required to develop. LocalStack when exercising
the S3 code paths specifically.

## 4. Canonical schemas

### `canonical_submission`

| Column | Type | Notes |
|---|---|---|
| `submission_key` | string | `{judge}:{native_id}` — globally unique |
| `judge` | string | enum |
| `native_id` | string | as issued by the source |
| `user_handle` | string | source-native, case preserved |
| `problem_key` | string | FK to `canonical_problem` |
| `contest_key` | string? | null for practice submissions |
| `verdict` | string | canonical enum, see §5 |
| `language_raw` | string | source string, unmodified |
| `language_family` | string | `cpp` \| `python` \| `java` \| `c` \| `other` |
| `submitted_at` | timestamp | UTC, always |
| `execution_time_ms` | int? | null where the source omits it |
| `memory_kb` | int? | |
| `source_length_bytes` | int? | |
| `is_contest_submission` | bool | derived |
| `ingest_date` | date | partition key |
| `source_uri` | string | provenance back to the raw record |

### `canonical_problem`

| Column | Type | Notes |
|---|---|---|
| `problem_key` | string | `{judge}:{native_id}` |
| `judge` | string | |
| `title` | string | |
| `rating_official` | int? | CF-style difficulty where published |
| `tags` | array\<string\> | source-native tags |
| `time_limit_ms` | int? | |
| `memory_limit_kb` | int? | |
| `statement_uri` | string? | for later embedding |
| `first_seen_at` | date | |
| `observed_at` | date | drives SCD-2 change detection |

**`observed_at` is the field that makes drift detection possible.** Difficulty
ratings and tags are revised by judges over time; capturing the observation date on
every crawl is what lets the warehouse reconstruct what a problem's rating *was*
when a given submission was made, rather than what it is today. Training on
present-day difficulty for a 2019 submission is a subtle and serious leak.

## 5. Verdict normalisation

The three sources disagree on both vocabulary and granularity. The mapping table
lives at `lens/ingest/mappings/verdicts.yml` and is version-controlled, because it
is a modelling decision, not a detail.

| Canonical | CodeNet | Codeforces | AtCoder |
|---|---|---|---|
| `AC` | Accepted | OK | AC |
| `WA` | Wrong Answer | WRONG_ANSWER | WA |
| `TLE` | Time Limit Exceeded | TIME_LIMIT_EXCEEDED | TLE |
| `MLE` | Memory Limit Exceeded | MEMORY_LIMIT_EXCEEDED | MLE |
| `RE` | Runtime Error | RUNTIME_ERROR | RE |
| `CE` | Compile Error | COMPILATION_ERROR | CE |
| `OLE` | Output Limit Exceeded | IDLENESS_LIMIT_EXCEEDED | OLE |
| `OTHER` | (residual) | (residual) | (residual) |

Any source value not in the table lands in `OTHER` **and raises a warning with the
unmapped literal**. Silent bucketing into `OTHER` would hide a source changing its
vocabulary, which is exactly the failure that shows up as unexplained model drift
six weeks later.

`AC` is the label the skill model predicts. Everything else is a distinct failure
signature and stays distinguishable.

## 6. Per-judge notes

**CodeNet** — a one-time bulk download, not a crawl. ~13.9M submissions across
4,053 problems. The metadata CSVs are the fast path; individual source files are
only needed for the length feature and later embedding work. Ingest metadata first,
defer the source tree.

**Codeforces** — one channel. The official API serves both history and live data;
the third-party end-2024 bulk release is declined in LEGAL.md and is not ingested.
The documented limit is one request per two seconds, enforced as a 2000 ms minimum
interval through a single global limiter shared by every worker — parallelism does
not multiply the budget. History is collected by `user.ratedList` followed by
paginated `user.status`; checkpoint the cursor so an interrupted crawl resumes
rather than restarts. Expect 11-12 hours for a full unattended pass.

**AtCoder** — the community archive, with the project's own published limits
honoured. Two licences apply here and both must clear LEGAL before the adapter merges.

## 7. Orchestration

Airflow, one DAG per judge plus a shared downstream:

```
discover ──▶ fetch ──▶ stage ──▶ dbt_run ──▶ dbt_test ──▶ publish_marts
```

- Fetch tasks are partitioned by date and independently retryable.
- `dbt_test` failing at `error` severity halts the DAG before `publish_marts`.
  The marts a dashboard reads are never updated by a run whose tests failed.
- A judge's DAG failing does not block the others. The shared downstream runs on
  whatever staged successfully and records which sources contributed.

## 8. Scale discipline

Develop against a **5M-row sample**, cut over to the full 30M once green. The
cutover is expected to surface two classes of failure that clean samples hide:

1. **Referential-integrity orphans** — submissions referencing problems absent from
   the problem crawl. Filter these at the staging boundary and count them as a
   quality metric. Never mutate operational tables to make a join succeed.
2. **Range tests tripping on real edge cases** — genuine 0 ms executions, absurd
   memory figures, timestamps predating a judge's founding. Loosen the test to
   `warn` and investigate. Never clamp real signal to satisfy a threshold.

Both outcomes get recorded in the run's data-quality report rather than fixed
silently.

## 9. Cost and cache discipline

Expensive deterministic work — statement embeddings, feature extraction — is
cache-read on re-run and only recomputed behind an explicit flag:

```bash
REEMBED=1 python -m lens.features.embed
```

A scale-up must never turn a 30-second iteration into a 30-minute one.
