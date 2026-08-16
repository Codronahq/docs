# `solved_count` carries release date, and the sign reverses at 2700

**Status:** Measured 16 Aug 2026. An input to Phase 2 Stage A. Changes nothing in
`lens` beyond the `problem_contest_id` column the reproduction below reads.

Stage A does not fit a free 2PL. `architecture/phase-2-modelling.md` draws item
difficulty from a prior conditioned on `problem_rating` and `log(solved_count)`, so
that a thin item shrinks toward its prior instead of fitting noise. `solved_count` is
the only cohort-independent difficulty signal the warehouse holds: it is measured over
every Codeforces user rather than over our 55,484, which is why `codrona.md` §6 calls
it the sole independent check on cohort sampling bias.

**It is also a cumulative counter with no denominator.** Nothing in this project had
asked what else it counts. This document asks.

**Scope: the 11,764-problem item bank, read from the gated response matrix.** Not the
warehouse and not `dim_problem` — every figure below comes from
`~/codrona-data/model/responses.parquet` filtered to `in_public_problemset`, which is
the artefact Stage A fits and which `--verify-artefact` checks against
`exports/model/responses.manifest.json` in `lens`.

---

## The prediction that was wrong, recorded rather than quietly dropped

The hypothesis this document set out to test was that **older problems accumulate more
solvers**, so `log(solved_count)` would read a 2011 problem as easier than an
identically-rated 2024 one purely through fifteen extra years of exposure.

The direction is wrong in six of seven bands. Exposure is time multiplied by
population, and Codeforces' growth swamps the extra years: **newer problems carry
higher `solved_count` everywhere below rating 2800.** The reasoning that produced the
prediction held time constant in the wrong place. It is recorded here because a
measurement that merely confirms what was expected teaches less than one that reverses
it, and because the project's standing rule is that a stated number is measured or it
is not stated.

---

## Population, and three coverage facts nobody had counted

| Quantity | Value |
|---|---|
| Bank problems | 11,764 |
| Rated | 11,051 |
| Unrated | 713 |
| Carrying `solved_count` | **11,764 — all of them** |
| `solved_count = 0` | **31** |
| No `problem_contest_id` | **417** |

**`solved_count` coverage is exactly co-extensive with bank membership.**
`analysis/irt-response-definition.md` reports it as 3,012 of 3,493 problems rated 2400
or above, which reads as 86% partial coverage. Measured over the bank the same 3,012 is
every 2400+ bank problem there is; the missing 481 are outside the public problemset
entirely. The column arrives with the problemset snapshot, so a problem has it if and
only if the snapshot covers it. The rated count of 11,051 matches `codrona.md` §6's
problemset figure to the row, which is an independent reconciliation of the bank
against a number measured a different way in a different phase.

**31 problems carry `solved_count = 0`** — 15 rated 2800+, 16 unrated. `log(0)` is
undefined. The blueprint's prior specification has no guard for this and would produce
a negative infinity for 31 items, so a guard is owed before the first fit. It is a
small population and a silent one: nothing currently fails.

**417 bank problems carry no `problem_contest_id`**, all of them unrated. These are the
acmsguru/SGU archive, which `codrona.md` §6 records as keying on `problemset_name` plus
a numeric index with no contest id at all. Any covariate derived from contest id needs a
stated policy for them rather than a null.

---

## Contest id is publication order, and that is measured too

Contest ids increase with time, but "increase with time" is an assumption until
something checks it. Against the earliest first-attempt observed for each problem:

| n | `corr(contest_id, first_seen)` |
|---|---|
| 11,347 | **0.9882** |

The 417 without a contest id are the difference between 11,347 and 11,764. Contest id
is used throughout rather than a date because it is an intrinsic property of the
problem: it inherits none of the `activeOnly=true` cohort bias that makes `first_seen`
date an old problem later than its release. `first_seen` here is the earliest evidence
first-attempt in the response matrix, which is a slightly different quantity from the
earliest row in `fct_submission`; the two agree to 0.988 either way.

---

## Median `solved_count` by age tercile, within band

Tercile 1 is the oldest third of each band by contest id.

| Band | oldest | middle | newest | ratio | ln gap |
|---|---|---|---|---|---|
| under 1200 | 14,449 | 23,755 | 26,157 | 1.810 | +0.593 |
| 1200–1599 | 6,845 | 12,198 | 15,967 | 2.333 | +0.847 |
| 1600–1999 | 3,019 | 5,740 | 7,358 | 2.437 | +0.891 |
| 2000–2399 | 1,334 | 2,546 | 2,615 | 1.960 | +0.673 |
| 2400–2799 | 753 | 1,152 | 1,104 | 1.466 | +0.383 |
| **2800+** | **514** | **488** | **274** | **0.533** | **−0.629** |
| unrated | 314 | 388 | 971 | 3.092 | +1.129 |

Two identically-rated problems in 1600–1999 differ by a factor of 2.4 in
`solved_count` according to nothing but which decade they were published in.

---

## Rating removed as a factor

Bands still leave rating variance inside them. Centring `ln(solved_count)` on its mean
within each **exact** rating value removes rating entirely, with no functional form
assumed, and leaves precisely the residual the second covariate exists to explain.

| Band | n | `corr(resid, contest_id)` | sd of residual | gap ÷ sd | variance explained |
|---|---|---|---|---|---|
| under 1200 | 2,283 | 0.1346 | 0.6837 | 0.87 | 1.8% |
| 1200–1599 | 1,861 | **0.4444** | 0.8021 | 1.06 | **19.7%** |
| 1600–1999 | 2,066 | **0.4353** | 0.8886 | 1.00 | **18.9%** |
| 2000–2399 | 1,829 | 0.3419 | 0.8333 | 0.81 | 11.7% |
| 2400–2799 | 1,525 | 0.1978 | 0.6863 | 0.56 | 3.9% |
| 2800+ | 1,472 | −0.1793 | 0.7647 | −0.82 | 3.2% |
| **pooled** | 11,036 | **0.2581** | 0.7816 | — | 6.7% |

**The pooled figure hides it, which is this project's recurring shape.** Pooled, 0.2581
is a nuisance worth ignoring. Per band it reaches 0.4444, and the prior conditions on
rating *first* — so the residual is the only thing the second covariate ever sees, and
in 1200–2000 a fifth of it is publication date. The `gap ÷ sd` column is the same
statement without a correlation: in 1600–1999 the oldest and newest terciles sit a full
residual standard deviation apart.

This is the same failure mode as G1's pooled Brier, which read as a respectable 21%
reduction while one corpus half went ungated, and as the self-selection sign flip in
`analysis/person-margin-and-selection.md`, which cancels to agreement when pooled.
Three findings, one lesson: **on this corpus a pooled statistic is a statement about
population composition.**

---

## The sign crosses zero between 2700 and 2800

Per exact rating value, with no rating variance left to confound anything:

| Rating | n | corr | oldest | newest | Rating | n | corr | oldest | newest |
|---|---|---|---|---|---|---|---|---|---|
| 800 | 1,087 | −0.0798 | 21,981 | 28,287 | 2200 | 472 | 0.3380 | 1,274 | 2,251 |
| 900 | 350 | 0.2208 | 13,448 | 25,879 | 2300 | 412 | 0.3082 | 1,017 | 1,967 |
| 1000 | 402 | 0.2136 | 13,840 | 24,202 | 2400 | 462 | 0.2620 | 955 | 1,526 |
| 1100 | 444 | 0.4475 | 10,716 | 21,836 | 2500 | 415 | 0.2426 | 817 | 1,138 |
| 1200 | 455 | 0.4631 | 8,694 | 20,079 | 2600 | 340 | 0.1456 | 700 | 934 |
| 1300 | 471 | 0.4256 | 6,824 | 16,514 | **2700** | 308 | **0.1082** | 610 | 676 |
| 1400 | 460 | 0.4149 | 6,734 | 14,643 | **2800** | 254 | **−0.1328** | 599 | 565 |
| **1500** | 475 | **0.4835** | 5,085 | 13,914 | 2900 | 239 | −0.0695 | 503 | 397 |
| 1600 | 522 | 0.4702 | 4,432 | 12,125 | 3000 | 198 | −0.1655 | 594 | 392 |
| 1700 | 516 | 0.4371 | 3,771 | 8,649 | 3100 | 170 | −0.1990 | 484 | 333 |
| 1800 | 491 | 0.4736 | 2,432 | 6,843 | 3200 | 145 | −0.2130 | 452 | 397 |
| 1900 | 537 | 0.3663 | 2,498 | 5,166 | 3300 | 136 | −0.3611 | 470 | 198 |
| 2000 | 494 | 0.3638 | 1,728 | 4,276 | 3400 | 90 | −0.2222 | 269 | 242 |
| 2100 | 451 | 0.3535 | 1,687 | 3,092 | **3500** | 240 | **−0.4363** | 312 | 112 |

The approach to zero is monotone from both directions across four rating values on each
side, so the crossing is structure rather than noise. Peaks: **1500 at 0.4835**, 23.4%
of the residual variance; **3500 at −0.4363**, 19.0%.

**A reading, not a measurement.** Below the crossing the pool able to solve a problem
grows with the platform, so a newer problem gathers solvers faster than an old one ever
did. Above it the capable pool is small and roughly fixed, so accumulation time
dominates instead and the old problem wins. Both are age effects with opposite signs.
This document does not separate the mechanisms and nothing here depends on which is
right.

**Rating 800 is the one cell where the linear statistic and the medians disagree** —
correlation −0.0798 against a tercile ratio of 1.287, over the largest cell in the
bank. 800 is the floor, so it absorbs every problem that would otherwise rate lower and
holds a wide range of true difficulties. At the floor even the *sign* of a linear term
is unreliable.

---

## What this does to Stage A, including the part that de-escalates it

**A single global date term in the prior is provably wrong.** Whatever the cause, one
coefficient cannot represent a relationship that is +0.44 at 1500 and −0.44 at 3500. If
a date term is added it must be allowed to vary with rating.

**But the confound is anti-correlated with where the prior binds.** Hierarchical
shrinkage matters in proportion to how little evidence an item carries, and the two
columns run opposite ways:

| Band | administered responses per item | variance explained by date |
|---|---|---|
| under 1200 | 1,051.5 | 1.8% |
| 1200–1599 | 420.3 | **19.7%** |
| 1600–1999 | 162.1 | **18.9%** |
| 2000–2399 | 65.2 | 11.7% |
| 2400–2799 | 26.2 | 3.9% |
| 2800+ | 9.7 | 3.2% |

Where date contamination peaks, items carry hundreds of responses and the prior is
overridden. Where the prior dominates — 2800+, at a committed median of 4 administered
responses per problem, where `analysis/person-margin-and-selection.md` establishes that
the posterior *is* the prior — the contamination is at its weakest. The right-hand
column is a mean rather than a median and the prior's weight is not yet specified, so
this bounds the problem rather than dismissing it.

**The premise survives.** `corr(ln(solved_count), problem_rating)` is **−0.8697** over
11,036 problems. The covariate carries real difficulty and dropping it would lose
signal that the 100-point rating grid cannot express. The defect is that it carries
publication date on top and the prior has no term to separate them.

---

## The fork, which cannot be settled before the fit

Two readings fit every number above and no measurement in this document distinguishes
them:

1. **The covariate is contaminated** by platform growth, and date should be removed.
2. **Difficulty at a given published rating genuinely drifted** over sixteen years, and
   `solved_count` is correctly reporting it.

Codeforces assigns `problem.rating` once and it never varies within a snapshot
(`codrona.md` §6), so nothing in the rating itself can adjudicate. If reading 2 holds,
residualising date away would delete a true signal.

**Only Stage A's own output separates them.** Fit without a date term, then correlate
the fitted difficulty residual against contest id. If the residual still tracks date
after the responses have spoken, difficulty drifted; if it does not, the prior was
injecting date. That diagnostic is cheap, it is the reason `problem_contest_id` is
carried in the response matrix, and it belongs in Stage A's specification rather than
in a later analysis.

**One route is already closed.** Normalising `solved_count` by the contemporaneous
solver population would remove the confound directly, and it cannot be built: the
exposure denominator would have to come from a platform-size time series, and
`codrona.md` §6 settles that our activity-per-year curve is left-truncated by
`activeOnly=true` and is not a growth curve. The denominator does not exist in our data.

---

## What this document does not claim

It does not claim the covariate is contaminated. It claims the covariate carries
publication date, that this is large within the residual the prior operates on, that
the sign reverses, and that the cause is undetermined.

It does not set the prior's functional form, its variance, or a date term. Those follow
the first fit.

It says nothing about CodeNet, whose problems carry no difficulty label from any source
(`codrona.md` §6) and therefore have no rating to residualise against.

It does not establish that `solved_count` is a *worse* covariate than an alternative,
because no alternative was measured. It was compared against rating and against
publication order, and against nothing else.

---

## Reproduction

Every figure comes from the response matrix, through `codrona_lens.warehouse`, which
pins the session timezone. The artefact is gated first:

    python3 -m codrona_lens.responses.matrix --verify-artefact

Bank, publication order, and the two coverage counts:

```sql
create temp table bank as
select distinct problem_key, problem_rating, solved_count,
       problem_contest_id as cid
from read_parquet('~/codrona-data/model/responses.parquet')
where in_public_problemset;

select count(*) as bank_problems,
       count(problem_rating) as rated,
       count(solved_count) as has_solved,
       count(*) filter (where solved_count = 0) as solved_zero,
       count(*) filter (where cid is null) as no_cid
from bank;
```

Contest id against observed publication, and the contrast with rating:

```sql
with seen as (
    select problem_key, min(submitted_at) as first_seen
    from read_parquet('~/codrona-data/model/responses.parquet')
    where in_public_problemset group by problem_key
)
select count(*) as n,
       round(corr(b.cid, epoch(seen.first_seen)), 4) as corr_cid_seen
from bank b join seen using (problem_key)
where b.cid is not null;

select count(*) as n,
       round(corr(ln(solved_count), problem_rating), 4) as corr_ln_rating
from bank
where solved_count > 0 and problem_rating is not null and cid is not null;
```

Rating removed as a factor — the table this document turns on:

```sql
with c as (
    select cid, problem_rating,
           ln(solved_count)
             - avg(ln(solved_count)) over (partition by problem_rating) as resid
    from bank
    where solved_count > 0 and cid is not null and problem_rating is not null
)
select round(corr(resid, cid), 4) as corr_resid_cid,
       round(stddev_samp(resid), 4) as sd_resid,
       count(*) as n
from c;
```

Per exact rating value, including the crossing:

```sql
with t as (
    select problem_rating as rating, solved_count, cid,
           ntile(3) over (partition by problem_rating order by cid) as age3
    from bank
    where solved_count > 0 and cid is not null and problem_rating is not null
)
select rating, count(*) as n,
       round(corr(ln(solved_count), cid), 4) as corr_age,
       cast(median(solved_count) filter (where age3 = 1) as bigint) as med_old,
       cast(median(solved_count) filter (where age3 = 3) as bigint) as med_new
from t group by rating order by rating;
```

Band terciles use the same `ntile(3)` partitioned by the band rather than by the exact
rating; bands are the six cuts named in the tables above plus `unrated`.

The ratios, log gaps, `gap ÷ sd` and variance-explained columns are arithmetic on the
figures beside them and are not separately measured: ratio is newest ÷ oldest, ln gap is
its natural log, `gap ÷ sd` divides that by the residual standard deviation in the same
row, and variance explained is the correlation squared.
