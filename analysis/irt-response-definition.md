# What counts as one response: the IRT unit measurement

**Status: measurement complete, no warehouse change.** This document records what
the corpus says about the unit an item-response model consumes. It is an input to
Phase 2 modelling and changes nothing in `lens`.

**Scope: both halves, measured separately, and they must stay separate.** The body of
this document measures the Codeforces half from `main_marts.fct_submission`. The
CodeNet half is measured in its own section below, from
`main_staging.stg_codenet_submissions`. The two share no user space, no problem key
space and no verdict vocabulary, so no figure here is ever a sum across them unless it
says so explicitly.

## The question

Item response theory takes one response per person per item. The warehouse holds
submissions, and a person submits to one problem many times. So before any model is
fitted, two things have to be decided from the data rather than from convenience:
how many submissions collapse into one response, and what that response's value is.

Getting this wrong is not a modelling inefficiency. It sets the base rate, and the
base rate sets what every calibration number in `quality/eval-gates.md` means.

## The population

Filtered to `is_evidence and is_person_level`, which is the settled evidence policy.

| Quantity | Value |
|---|---|
| Person-level evidence rows | 22,843,153 |
| Distinct (user, problem) pairs | 11,176,774 |
| Users appearing in those pairs | 55,235 |
| Problems appearing in those pairs | 34,430 |
| Mean attempts per pair | 2.0438 |
| Maximum attempts on one pair | 723 |
| Matrix density | 0.5877% |

The attempt distribution is concentrated but has a real tail.

| Attempts on a pair | Pairs |
|---|---|
| 1 | 6,547,447 |
| 2 | 2,162,721 |
| 3 | 1,024,020 |
| 4–5 | 859,236 |
| 6–10 | 472,060 |
| 11–20 | 96,583 |
| more than 20 | 14,707 |

58.58% of pairs are a single attempt, so the collapse from submissions to responses
is real but not extreme: 22,843,153 attempts become 11,176,774 responses, leaving
11,666,379 attempts that are not the first on their pair.

**That second number is not waste.** It is the survival model's entire dataset.

## What each candidate response definition showed

**"Ever solved" — the obvious choice, and the one that must not be used.** 10,400,680
of 11,176,774 pairs end in an accepted verdict, a positive rate of 93.0562%. People
choose their own problems, so almost nobody attempts what they cannot eventually do.
There is very little variance left for a latent ability parameter to explain, and a
model that predicts the base rate and nothing else already looks excellent.

**"First attempt on the pair" — near-balanced.** 6,485,190 of 11,176,774 first
attempts are accepted, a positive rate of 58.0238%. Attempt two is taken with judge
feedback in hand, so it is not an independent response to the same item; it is a
learning observation, and treating it as a second response both violates local
independence and inflates apparent difficulty for exactly the problems people grind
at hardest.

The split by the participant type of that first attempt:

| Participant type of first attempt | Pairs | Accepted | Rate |
|---|---|---|---|
| PRACTICE | 7,038,888 | 3,994,171 | 56.74% |
| CONTESTANT | 3,289,161 | 1,949,569 | 59.27% |
| VIRTUAL | 647,865 | 396,652 | 61.22% |
| OUT_OF_COMPETITION | 200,860 | 144,798 | 72.09% |
| all | 11,176,774 | 6,485,190 | 58.02% |

## The finding that settles it

**The choice of response definition decides whether the calibration gate can fail
at all.** A constant predictor at the base rate scores a Brier of `p(1-p)`:

| Definition | Base rate | Baseline Brier | G1 target 0.18 |
|---|---|---|---|
| ever solved | 0.930562 | 0.064616 | passes models three times worse than a constant |
| first attempt | 0.580238 | 0.243562 | requires a 26.1% reduction on baseline |

Under "ever solved" the existing G1 threshold is looser than doing nothing. Under
"first attempt" it is a real bar. This is not an argument from statistical taste; it
is the difference between a gate and a decoration.

## The rule this supports

**One response is the first person-level evidence submission on a (user, problem)
pair, ordered by `submission_key`, valued by `is_accepted`.**

Three consequences, each stated rather than implied:

- The IRT response matrix is 11,176,774 responses over 55,235 users and 34,430 problems, not 23,607,105 submissions. Any sizing claim written against the submission count is against the wrong number.
- The remaining 11,666,379 attempts are the survival model's input, censored where the pair never reaches an accepted verdict. Nothing is discarded; it is routed.
- The baseline a calibration report must beat is 0.243562, and that figure belongs beside every Brier score Codrona publishes.

## Ordering: `submission_key`, never `submitted_at`

`submitted_at` has **332 tied groups** on (user, problem, timestamp), so `arg_min`
over it is non-deterministic and the first-attempt figure is not reproducible under
it. Measured directly: the same query returned 6,485,189 accepted first attempts
under `submitted_at` and 6,485,190 under `submission_key`.

`submission_key` is unique across all 23,607,105 fact rows, so `row_number()` over
it is a total order. **Uniqueness is the whole of the justification.**

**Codeforces submission ids are NOT monotonic in submission time, measured.** An
earlier draft of this document claimed they were and used that to argue the id
ordering is also chronologically correct. It is not. Over 11,684,581 consecutive
attempt pairs there are **27 inversions on a single problem key** — a higher id
carrying an earlier timestamp — spread across 23 users and 26 problems, in both
PRACTICE and VIRTUAL rows, from 2010 to 2026. The mildest is 2 seconds and the worst
is 245 days. Rare enough that no spot check would find it, persistent enough that it
is a property of the source rather than a historical artefact.

The consequence is bounded and stated rather than assumed: ordering by id instead of
by time selects a different first attempt for 27 of 11,158,572 pairs. That is
immaterial to every figure in this document, and it is immaterial by measurement, not
by hope.

**One row of difference is the entire signal here.** A figure that moves under a
re-run is not a measurement, and a tie-break that happens to be stable today is not
a total order. The 332 timestamp ties are why `submitted_at` cannot be the key; the
27 inversions are why the id is not defended as chronological truth either.

## What this does to the item bank

Item counts at each response threshold, under three pooling definitions. "Administered"
means CONTESTANT plus VIRTUAL — the row classes where the participant was shown the
whole problem set rather than choosing one problem from the archive.

| Definition | ≥30 | ≥100 | ≥200 | ≥500 |
|---|---|---|---|---|
| all first attempts | 13,821 | 8,299 | 6,244 | 3,779 |
| administered (contestant + virtual) | 6,514 | 3,641 | 2,557 | 1,361 |
| contestant only | 5,277 | 3,107 | 2,148 | 1,145 |

Of 34,430 problems, 8,299 carry 100 or more first attempts — 24.10%. Under the
administered definition it is 3,641, and contestant-only 3,107, which is 9.02% of
the bank.

**Evidence density collapses monotonically as difficulty rises**, which is the
opposite of what a recommender aimed at the ability edge needs.

| Rating band | Problems | Median responses, all | Median, administered | all ≥200 | admin ≥200 | Has `solved_count` |
|---|---|---|---|---|---|---|
| 800–1199 | 2,396 | 1028.5 | 246.0 | 2,189 | 1,302 | 2,283 |
| 1200–1599 | 2,122 | 458.5 | 74.5 | 1,494 | 643 | 1,861 |
| 1600–1999 | 2,603 | 205.0 | 33.0 | 1,315 | 392 | 2,066 |
| 2000–2399 | 2,264 | 117.0 | 16.0 | 814 | 153 | 1,829 |
| 2400–2799 | 1,841 | 67.0 | 8.0 | 279 | 13 | 1,525 |
| 2800+ | 1,652 | 33.0 | 4.0 | 23 | 0 | 1,487 |
| unrated | 21,552 | 6.0 | 2.0 | 130 | 54 | 713 |

Three readings, none of them optional for Phase 2:

- **Not one problem rated 2800 or above has 200 administered responses**, and 2400–2799 has thirteen. The cohort policy in the master document took the upper rating bands whole specifically to identify hard-problem difficulty; measured against administered responses, it did not achieve that. It bought volume in the practice column, which is the self-selected one.
- **`solved_count` survives where responses fail.** 3,012 of the 3,493 problems rated 2400 or above carry it — 86.2%. It is measured over every Codeforces user rather than our cohort, so it is the only difficulty signal in the warehouse that does not thin out with our sampling. Any model for the hard bands rests on it.
- **The unrated 21,552 have nothing.** Median 6 responses, median 2 administered, and `solved_count` on 713 of them, which is 3.3%. No rating, no population signal, no responses. These are overwhelmingly gym, and this is the measurement that makes filtering on `in_public_problemset` a modelling requirement rather than a convention.

## Two counts that did not match, both closed

Both were chased because a count that should match another and does not is a lead,
and a user or problem silently missing from the response matrix is a sampling-bias
symptom.

**249 users.** `dim_user` holds 55,484 current rows; 55,235 appear in the pair set.
All 249 missing users do have fact rows — 2,160 of them, **every one non-evidence and
none team-submitted**. They submitted and nothing was judgeable. The sampled handles
are 2026 registrations rated 375–496 with roll-number-shaped names, consistent with
mass college signups. Benign, and now recorded rather than assumed.

**1,136 problems.** `dim_problem` holds 35,566 current rows; 34,430 appear. All 1,136
have fact rows — 6,034 total, of which 6,032 are not person-level. These are problems
attempted in our cohort only by teams. They are outside the person-level item bank by
the evidence policy working correctly, not by accident.

A third gap reconciles and is not a lead: 22,981,576 person-level submissions less
22,843,153 person-level evidence rows is 138,423, against the 140,298 unjudged rows in
the corpus, the difference being unjudged rows that are not person-level.

## The CodeNet half

Measured over `main_staging.stg_codenet_submissions`, filtered to `is_evidence`. There
is no `is_person_level` filter because CodeNet has no team concept.

| Quantity | Value |
|---|---|
| Evidence rows | 13,916,561 |
| Distinct (user, problem) pairs | 6,764,548 |
| Users | 154,178 |
| Problems | 4,046 |
| Mean attempts per pair | 2.0573 |
| Matrix density | 1.0844% |
| First-attempt accepted | 5,150,128 — 76.13% |
| Ever accepted | 6,347,880 — 93.84% |

`submission_id` is unique across all 13,916,868 rows, so the same
`row_number()` ordering is a total order here too.

**The ever-solved rate is 93.84% against Codeforces' 93.06%** — near-identical, from
two unrelated populations on different judges. Mean attempts are 2.0573 against
2.0438. Self-selection produces the same shape wherever people pick their own
problems, which is mild evidence the first-attempt rule generalises rather than
fitting one dataset.

**The first-attempt rate does not generalise, and that is the finding.**

| Population | Pairs | First-attempt AC | Baseline Brier |
|---|---|---|---|
| Codeforces | 11,176,774 | 58.02% | 0.243562 |
| CodeNet — AtCoder | 5,907,806 | 75.74% | 0.183728 |
| CodeNet — AIZU | 856,742 | 78.83% | 0.166893 |
| CodeNet — both | 6,764,548 | 76.13% | 0.181701 |
| pooled, all | 17,941,322 | 64.85% | 0.227941 |

A single absolute Brier threshold cannot mean the same thing on both halves. The
consequence for the calibration gate is in `architecture/phase-2-modelling.md`.

### The item banks are complementary in the worst way

| | Problems | Pairs | Mean responses per problem | Difficulty label |
|---|---|---|---|---|
| Codeforces | 34,430 | 11,176,774 | 324.6 | rating and `solved_count` |
| CodeNet | 4,046 | 6,764,548 | 1,671.9 | none, on any row |

CodeNet response counts per problem: median 225.5, maximum 18,899, with 2,110 problems
at 200 or more and 1,521 at 500 or more. Only 720 sit below 30.

So the half carrying difficulty labels has items too thinly observed to identify from
responses alone, and the half whose items are five times more densely observed has no
label to anchor a scale to — CodeNet's `rating`, `tags` and `complexity` columns are
empty on all 4,053 rows. Neither half can do what the other does, and no linking
design exists between them.

### One lead, closed

4,048 problems carry submissions; 4,046 carry evidence rows. The two absent are
`p02849` and `p03002`, both AtCoder, one row each, both `Judge Not Available` — an
unjudged status correctly excluded. The evidence policy working, not a sampling gap.

## Reproduction

Every figure re-derives from the local warehouse through
`codrona_lens.warehouse.connect`, which pins the session timezone. No figure here is
timezone-sensitive, but the pinned helper is the only sanctioned route to the
warehouse.

```sql
-- the response matrix and its base rates
with ranked as (
    select user_key, problem_key, is_accepted, participant_type,
           row_number() over (partition by user_key, problem_key
                              order by submission_key) as rn,
           max(is_accepted::int) over (partition by user_key, problem_key) as ever_ok
    from main_marts.fct_submission
    where is_evidence and is_person_level
)
select count(*)                        as pairs,
       sum(is_accepted::int)           as first_attempt_accepted,
       sum(ever_ok)                    as ever_accepted
from ranked
where rn = 1;
```

```sql
-- responses per problem, and the band collapse
with ranked as (
    select user_key, problem_key, participant_type,
           row_number() over (partition by user_key, problem_key
                              order by submission_key) as rn
    from main_marts.fct_submission
    where is_evidence and is_person_level
),
per_problem as (
    select problem_key,
           count(*) as n_all,
           count(*) filter (where participant_type in ('CONTESTANT', 'VIRTUAL')) as n_adm
    from ranked where rn = 1 group by 1
)
select p.problem_rating is null as unrated,
       count(*), median(pp.n_all), median(pp.n_adm),
       count(*) filter (where pp.n_adm >= 200) as adm_200,
       count(*) filter (where p.solved_count is not null) as has_solved
from per_problem pp
join main_marts.dim_problem p
  on p.problem_key = pp.problem_key and p.is_current
group by 1;
```

## What this document does not claim

It does not say the practice rows are unusable. It says they are self-selected, that
99.41% of the matrix is unobserved for the same reason being estimated, and that
pooling them with administered responses without recording which is which would hide
that. The modelling response to it is in `architecture/phase-2-modelling.md`.

It says nothing about how the two halves might be placed on one scale, because
nothing in the corpus supports doing so. Three conditions were checked and all three
fail: no common persons, since CodeNet users are anonymised; no common items, since the
364 shared problem names are all AIZU generic-title collisions of the kind
`analysis/div1-div2-twins.md` measured and rejected; and no shared predictive feature,
since Codeforces carries tags and never statements while CodeNet carries statements and
no tags. That is a modelling constraint and it lives in
`architecture/phase-2-modelling.md`.

### Two documented counts that disagreed, both reconciled

`stg_codenet_submissions` records 54 problems with a null name over 79,337 rows;
`dim_problem_codenet` holds 56 nulls. Both are right and they count different
populations: 54 of the null-named problems carry submissions and 2 do not, and the
dimension is built from the problem index rather than the fact side precisely so the
five submission-less problems survive. The 79,337 figure matches to the row.

Likewise 4,048 CodeNet problems carry submissions against 4,046 in the evidence
matrix. The two absent are `p02849` and `p03002`, one row each, both `Judge Not
Available`.

Neither was a defect. Both are recorded because a documented count that disagrees with
the artefact is a lead until it is closed, and closing it costs one query.
