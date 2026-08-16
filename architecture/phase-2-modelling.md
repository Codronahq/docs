# Phase 2 modelling blueprint

**Status: blueprint, nothing built.** This is the phase-entry design document for
the science chapter. It fixes the decisions that are expensive to reverse and names
the measurements still owed. It does not specify hyperparameters, which are an
outcome rather than an input.

Two inputs it rests on, both measurement documents rather than plans:
`analysis/irt-response-definition.md` and `analysis/div1-div2-twins.md`.

---

## 1. What is settled before any code

**The response unit.** One response is the first person-level evidence submission on
a (user, problem) pair, ordered by `submission_key`, valued by `is_accepted`.
`submission_key` rather than `submitted_at` because the latter has 332 tied groups and
is therefore not a total order. Derivation, and the reason the alternative definition
breaks the existing gate: `analysis/irt-response-definition.md`.

**Two matrices, and Stage A fits the merged one.** Twin conforming (section 4) collapses
1,182 problem keys before any parameter is estimated, so the figures the model sees are
not the figures the warehouse holds:

| | Responses | Users | Problems | First-attempt AC | Baseline Brier |
|---|---|---|---|---|---|
| full matrix, unmerged | 11,176,774 | 55,235 | 34,430 | 58.0238% | 0.243562 |
| full matrix, twin-merged | 11,158,572 | 55,235 | 33,248 | 58.0079% | 0.243587 |
| **item bank, twin-merged - the population Stage A fits** | **10,817,555** | 55,231 | **11,764** | **58.2670%** | **0.243166** |

**The bottom row is the one every calibration figure is measured against, and it
was not in this table until 16 Aug 2026.** The marker sat on the merged full
matrix, which is not what Stage A fits — the `in_public_problemset` filter in this
same section removes 21,484 problems before a parameter is estimated. The
correction is this document's own argument about the merge, that a baseline
computed on a different matrix than the fit is measuring nothing, applied to the
filter: it moves the figure by 0.000421 against the merge's 0.000025, close to
seventeen times as far. `quality/eval-gates.md` G1 carried the same error against
the same figure and was corrected first.

Measured and gated in `lens`, not asserted here: `exports/model/responses.manifest.json`,
checked by `python3 -m codrona_lens.responses.matrix --verify-current`.

The baseline moves by +0.000025, which is immaterial to the gate but is quoted from the
merged matrix regardless, because a baseline computed on a different matrix than the fit
is measuring nothing. That the shift is negligible was measured rather than assumed: twin-
touching pairs run 47.37% accepted against 58.59% elsewhere, an 11.2-point gap that
suggested the merge would move the base rate materially. It does not, because the merge
removes only the 18,202 duplicated responses rather than reweighting the 562,680 twin-
touching ones.

**The corpus is two disconnected matrices and IRT cannot join them.** The Codeforces
half and the CodeNet half share zero items by construction, since one is Codeforces
problems and the other AIZU and AtCoder. They share zero persons, since CodeNet users
are anonymised and cannot be identified with a Codeforces handle even in principle.
Item response theory places two populations on one scale through common items or
common persons. With neither, two independent fits produce two arbitrary latent
metrics, and a CodeNet difficulty of 1.2 is not the same quantity as a Codeforces
difficulty of 1.2.

Both matrices are now measured, and they are complementary in the way that hurts most.

| | Problems | Pairs | Mean responses per problem | Difficulty label | First-attempt AC |
|---|---|---|---|---|---|
| Codeforces | 34,430 | 11,176,774 | 324.6 | rating and `solved_count` | 58.02% |
| CodeNet | 4,046 | 6,764,548 | 1,671.9 | none on any row | 76.13% |

The labelled half is thinly observed per item; the densely observed half is unlabelled.
2,110 of 4,046 CodeNet problems carry 200 or more responses, against 3,641 of 34,430
Codeforces problems at 100 or more under the administered definition. This is the
Phase 2 problem stated completely.

The master document says cross-judge equivalence is something IRT must produce rather
than something the warehouse assumes. That is right about the warehouse and wrong
about IRT: **no linking design exists, so IRT cannot produce it.**

**Nor does a content bridge exist.** The obvious fallback — regress Codeforces tags
onto Codeforces ratings, apply the model to CodeNet items — requires a feature the two
dimensions share. Measured, they share none that predicts difficulty:

| | Tags | Statement | Difficulty label |
|---|---|---|---|
| `dim_problem` (Codeforces) | 38-term vocabulary, 96.5% of the bank | never, under link-never-host | rating and `solved_count` |
| `dim_problem_codenet` | no tag column, from any source | 3,474 of 4,046, via CodeContests | none on any row |

A model trained on Codeforces tags cannot score a CodeNet problem, which has no tags.
A model trained on CodeNet statements has no label to fit against. CodeContests was
checked at the raw Parquet rather than the staging projection, in case a tag column had
simply not been carried forward: all 17 raw columns, no tag field of any name. The
absence is licence-shaped, not effort-shaped — Codeforces statement text can never be
stored, and tags were never published for AIZU or AtCoder.

**And there are no common items.** 364 problem names appear in both dimensions, out of
29,440 Codeforces and 3,882 CodeNet names. Every one is AIZU; AtCoder contributes zero.
They are generic-title collisions of exactly the kind `analysis/div1-div2-twins.md`
measured and rejected — `a + b`, `add`, `area`, `ball`, `auction` — and `alice and bob`
draws six Codeforces candidates against one CodeNet problem. Worse than the twins case,
because there is no rating on the CodeNet side to disqualify a false match. 452 CodeNet
problems collapse into those 364 names, so CodeNet reuses titles internally too.

**What remains is one route, and it is a product feature rather than a data asset:**
first-party users who solve on both judges. That is Phase 4 and it starts at zero.

**The claim this narrows.** At Phase 2, with this corpus, Codrona can produce two
independent, well-calibrated, within-judge skill models. It cannot place a CodeNet
ability on a Codeforces scale, and no amount of fitting changes that. The master
document's cross-judge profile claim has to be narrowed on the surfaces that render it
before it renders, not after.

**This narrows a product claim.** "Cross-judge profiles" as stated in the master
document's moat section is, at Phase 2, a content-model estimate bridging two
unlinked scales. It stays honest by being labelled, in the same way `community_rating`
carries `rating_source`.

**The item bank is filtered, not the warehouse.** `in_public_problemset` is a LEFT
enrichment on `dim_problem` and filtering it at the warehouse would drop 23,802
problems and their submissions through a failed lookup. The filter belongs at the
model input, where it is a stated modelling scope with the 21,552 unrated problems
excluded for a measured reason.

---

## 2. The four model-shaping constraints

**Constraint 1 — self-selection, and the administration subset that partly escapes
it.** Matrix density is 0.5877%, and the 99.41% unobserved is missing for the reason
being estimated: nobody attempts what they cannot do. Inside a contest, every
participant was shown every problem, so CONTESTANT and VIRTUAL rows are an
administration rather than a selection. That subset covers 3,641 problems at 100 or
more responses against 8,299 for all first attempts.

There is a residual gap even there: `contest_id` records who submitted, never who
registered. A participant who read a problem and submitted nothing is invisible.
Closing it needs `contest.standings`, which has never been collected — section 5.

**Constraint 2 — evidence density collapses as difficulty rises.** Zero problems
rated 2800 or above have 200 administered responses; 2400–2799 has thirteen. A freely
estimated 2PL discrimination on single-digit responses is noise with a decimal point.

**Constraint 3 — `solved_count` survives where responses do not.** It covers 3,012 of
the 3,493 problems rated 2400 or above, and it is measured over every Codeforces user
rather than our cohort. With `problem_rating` it forms a difficulty prior available
precisely in the bands the responses cannot carry.

**Constraint 4 — `problem_rating` is today's rating applied retroactively.** Zero
problems show more than one rating across the corpus, so a rating is a current
estimate placed on historical rows. Usable as a prior. Not usable as ground truth for
a drift analysis over time, which needs the problemset snapshot series and therefore
at least a second snapshot.

---

## 3. The stack, in build order

Each stage names what it consumes, what it emits, and the gate it must clear. Nothing
proceeds on a stage whose gate has not been proven capable of failing.

### Stage A — Hierarchical IRT 2PL

**Not a free 2PL.** Difficulty is drawn from a prior conditioned on `problem_rating`
and `log(solved_count)`, so a thin item shrinks toward its prior instead of fitting
noise, and a dense item overrides it. This is the only structure under which the hard
bands are estimable at all.

**The second covariate carries publication date, and this changes what the prior is
allowed to be.** Measured 16 Aug 2026 over the bank: with rating removed as a factor,
`ln(solved_count)` still correlates with contest id at 0.4444 in 1200-1599 and 0.4353
in 1600-1999 — a fifth of the residual variance the covariate exists to explain — and
the sign crosses zero between rating 2700 and 2800. Three things bind this stage as a
result. A single global date term is provably wrong, so any date term must vary with
rating. `log(solved_count)` needs a guard, because 31 bank problems carry
`solved_count = 0` and this document specified no such guard. And the fit must emit a
post-fit diagnostic correlating the fitted difficulty residual against contest id per
band: that is the only thing separating a contaminated covariate from genuine drift in
Codeforces' own calibration, and neither this document nor the measurement decides
between them. Derivation in `analysis/solved-count-and-release-date.md`.

**The ability side gets a population prior and no covariate, and that is a decision
rather than an omission.** Hierarchical already means ability is drawn from a
population distribution whose parameters are estimated, and that is what shrinks a
thin person toward the mean — a newbie carrying a median of 12 administered responses
is not left to a free estimate. The open question was only whether to *condition* that
prior on `dim_user.rating`. It is not conditioned. The G1 split is temporal and the
rating is a 2026-08-06 snapshot, so a prior carrying it puts post-cutoff information
into every training row and the held-out Brier would partly read out outcomes that
happen after the cutoff. **A temporal split with a rating-conditioned prior is not a
temporal split.** The same leak reaches G2, which validates placement against rating;
`analysis/person-margin-and-selection.md` records the G2 half of this and not the G1
half, which is the larger one. A rating-conditioned variant may be fitted as a
diagnostic and must never score G1 or G2. The decision is reconsiderable only if
`user.rating` history is collected, since a rating as of the response date is not
future information — section 9.

- Consumes: the twin-merged matrix filtered to `in_public_problemset` — **10,817,555 responses over 11,764 problems**. Not the 11,176,774-response unmerged matrix: conforming happens before this stage (section 4), so filtering the unmerged one would fit 10,626,688, and this line named that population until 16 Aug 2026 while the table in section 1 named the correct one.
- Emits: per-problem difficulty and discrimination with posterior intervals, per-user ability with intervals.
- Fit: marginal maximum likelihood or variational inference in PyTorch, mini-batched. CPU-viable at this size; a free T4 is a convenience, not a requirement.
- **The administered subset is fitted first and is the reference.** The practice rows are then added as a second fit, and the two difficulty vectors are compared on the problems both cover. Agreement is evidence the practice rows carry usable signal; systematic divergence is the self-selection bias appearing, and it is reported rather than averaged away.
- **Practice responses far above the responder are kept, not excluded, and the effect is estimated.** Measured 16 Aug 2026 in `analysis/person-margin-and-selection.md`: excluding them at a gap of 800 rating points costs 1.5% of the bank globally but **37.56% of the 2800+ band** even anchored on peak rating, on items whose per-item median depth is 38 responses. That halves the thinnest evidence in the bank to remove a confound, in the one band where `person-margin-and-selection.md` already establishes the posterior is the prior. Instead the practice effect is fitted as an offset varying with the gap between the problem's rating and the responder's, reported **per band and never pooled** — self-selection reverses sign at 1200, so a pooled offset cancels toward agreement and reads as no effect at all. Any rule of this shape anchors on `max_rating`, never current rating: peak rating is a lifetime bound that does not decay backwards across sixteen years, and it drops 106,022 responses against 159,507 for a contamination measurably more concentrated under it.
- **This procedure does not exist for CodeNet.** Its staging model carries no participant type, no contest context and no roster, so every CodeNet row is self-selected and there is no administered reference to check the practice fit against. The two halves therefore cannot be fitted by the same procedure, which is a second reason beyond the missing linking design that they cannot share a scale. What CodeNet offers instead is density: a per-item response count high enough that difficulty is identifiable from responses without a prior, which is exactly what Codeforces cannot offer.
- Items below a response floor are emitted as prior-only estimates with a flag, never silently. The floor is set from the measured distribution once the first fit exists, not now.

### Stage B — Topical ability: confirmatory MIRT supplying loadings, Elo supplying time

**Per-topic Elo over raw tags is not well-posed, and this was measured rather than
argued.** 9,298 of 11,764 bank problems carry two or more tags, covering 8,980,827 of
10,817,555 bank responses — 83.0%. On those, one solve is evidence about several topics
at once and nothing in the data says which. Elo is a two-player update rule assuming one
contest and one outcome; applied to a multi-tagged problem it must either update every
tag fully, which double-counts, or split the update by an invented weighting.

**Credit assignment is a loadings problem, so it is estimated rather than assumed.**
Multidimensional IRT fits how strongly each problem loads on each latent skill. Those
fitted loadings then weight the Elo updates. Tags stop being ground truth and become the
initial loading structure — which is also more honest, since Codeforces tags are
crowd-assigned and the roadmap already commits to detecting tag-quality drift.

**Elo is not replaced.** MIRT is static and gives one ability per user forever; Elo is
sequential and tracks ability changing over time, which is what a coach needs and what
IRT structurally cannot express. The two do different jobs and only one of them was
broken.

**Confirmatory, not exploratory, and that choice is load-bearing.** Exploratory MIRT
loadings are identified only up to rotation, so the dimensions come out uninterpretable
and unlabelable. Anchoring the loading structure resolves rotation and labelling together.

**What the anchor can and cannot be.** Tag co-occurrence was measured over the bank and
does not decompose into K coarse groups:

- **One genuine family:** `dfs and similar`, `graphs`, `trees`, `dsu`, `shortest paths`, at Jaccard 0.155 to 0.330. This is the anchor the data supports.
- **Two specialist pairs too small to be dimensions alone:** `flows` with `graph matchings` (44 problems), `hashing` with `string suffix structures` (46 problems).
- **The rest are hub artefacts.** `greedy` co-occurs with six partners at Jaccard 0.14 to 0.18 and sits on 3,549 problems; `math` on 3,475. Jaccard against a hub tag measures the hub's size, not topical affinity. **A hub tag that loads on every dimension is the correct fitted answer, not a failure**, so hub tags load freely rather than being forced into one group.

K is chosen by held-out likelihood over a small candidate range, never read off a
dendrogram.

**`*special` is excluded from the latent structure entirely.** 745 problems carry it and
52.3% carry it alone — the highest solo rate of any tag by a factor of three. It is
Codeforces' marker for non-standard interaction: interactive problems, unusual I/O,
special judges. It describes a submission format, not a skill. Left in, MIRT would fit a
dimension that is a protocol and it would look legitimate because 745 problems load on
it. It is kept as a problem attribute.

**Topical ability is real but small, and the effect size caps what any surface may
claim.** Comparing each user's accepted rate on graph-family problems against non-graph
problems within the same 400-point difficulty band, over cells with at least ten
responses on each side:

| Quantity | Value |
|---|---|
| Comparable cells | 21,272 |
| Users contributing | 9,781 of 55,231 |
| Mean gap | +2.65pp |
| Standard deviation | 13.22pp |
| Cells more than 15pp stronger at graphs | 3,409 — 16.0% |
| Cells more than 15pp weaker | 1,697 — 8.0% |

The mean is nearly nothing; the spread is five times the mean and asymmetric. So per-user
topical variation exists and is worth modelling, but **most topic deltas a profile would
render are indistinguishable from sampling noise on a ten-response cell.** The interface
may say "notably stronger at graphs than your rating predicts" for the 16% where it is
true. It may not render a 38-bar chart, which would show noise at the same visual weight
as signal.

**The comparison covers only the deepest 17.7% of users**, since it requires ten
responses on each side within one band. Thin users have noisier topic estimates, not
necessarily flatter ones, and nothing available settles whether the effect generalises.

**Depth, and why coarse grouping cannot fix it.** Over the merged bank there are
1,107,069 (user, topic) cells with a median of 5 responses. The median user has 6 topics
at 10 or more responses and 2 at 30 or more; **12,364 users — 22.4% — have no topic
reaching ten.** Grouping tags into coarse buckets would raise those counts, but the
measurement above says the buckets do not exist outside the graph family. Depth is
therefore handled at the surface, not by grouping.

**The serving rule.** Every dimension is shown. A cell below the response floor renders
as an explicit unmeasured state rather than a number with a caveat, because a flagged
number is still read as a number. For a user with no cell above the floor, that state
routes to the placement test — cold start as a designed path rather than a degradation.
The 22.4% is a floor rather than a ceiling: it is measured over Codeforces-active rated
users averaging 195.9 bank responses each, and real users will arrive with far fewer.

### Stage C — Survival model on attempt count, not wall-clock time

**The time axis in the master document's spec does not survive measurement.** Over
merged keys, on multi-attempt solved pairs, elapsed time from first to accepted
attempt runs:

| Quantile | Elapsed |
|---|---|
| median | 15 minutes |
| p90 | 3,180 minutes — 53 hours |
| maximum | 5,423 days |
| pairs spanning over a year | 50,617 — 1.2% |

**One in ten multi-attempt solved pairs spans more than two days.** That is not
time-to-solve, it is time-until-the-person-came-back. A model fitted on it would call
a user who returned after a year slow at a problem they may have solved in twenty
minutes on the second sitting, and it would be measuring scheduling rather than
ability.

**Attempt count is the axis.** Discrete, bounded by the submission sequence, nothing
to interpret in the gaps, and it is what a coach can act on: "this usually takes you
four attempts" is useful where "this usually takes you 53 hours" is noise.

- Consumes: the **11,684,581** attempts that are not first on their pair over merged keys, plus the first attempt as the origin. The unmerged figure was 11,666,379; the difference is exactly the 18,202 duplicate first attempts that become non-first under the merge, which reconciles three ways.
- Emits: expected attempts to solve, conditioned on ability and difficulty.
- Censoring: **770,806 pairs — 6.91%** — never reach an accepted verdict and are right-censored. That is the commitment in the master document and it stands unchanged.
- Mean attempts 2.0471, maximum 723. Heavy-tailed, so a negative binomial or discrete-time hazard, never a Poisson.

**Wall-clock survives in one narrow form, and the boundary is measured rather than
chosen.** The consecutive-attempt gap distribution has a sharp elbow:

| Gap | Pairs | Reading |
|---|---|---|
| under 1 min | 1,424,036 | contiguous |
| 1–5 min | 4,696,385 | contiguous |
| 5–30 min | 3,651,267 | contiguous |
| 30–60 min | 488,590 | the trough |
| 1–4 hours | 408,450 | return |
| 4–24 hours | 399,993 | return |
| 1–7 days | 232,418 | return |
| over a week | 383,442 | return |

83.6% of consecutive attempts fall within 30 minutes and 12.2% beyond an hour, with
the 30–60 minute bucket a trough between them rather than a peak split down the
middle. The percentiles agree: p75 is 870 seconds, p90 is 7,329, and p99 is 173 days.

**So a pair is a sequence of sessions at a 30-minute boundary.** Within-session
elapsed time is a real covariate; between-session time is dropped rather than
modelled, because it measures when someone had a free evening.

### Stage D — GBM stack

- Consumes: IRT ability and difficulty, Elo topic vectors, survival hazards, `solved_count`, tags, contest context.
- Emits: the served P(solve | user, problem).
- **Held-out split is temporal, and the cutoff is a stated date.** A random split leaks: a user's later submissions inform their earlier ones. The existing gate document already requires this and it is inherited unchanged.

### Stage E — Contextual bandit recommender

- Consumes: the calibrated P(solve) and its interval.
- Target band for the ability edge is a product decision recorded in the master document; the bandit optimises within it rather than choosing it.
- Cannot be evaluated offline in any way that means much. Off-policy estimates are the Phase 2 deliverable; the real evaluation is the Phase 5 live experiment with CUPED.

### Stage F — Placement test design

- Consumes: the fitted item bank, selecting maximum-information items at each ability level.
- The cold-start gate targets a rating MAE of **150** after ten problems, not 250. This bullet said 250 and said it would be "revised upward without embarrassment" until 16 Aug 2026; `quality/eval-gates.md` had already revised it, and downward, because 250 sat above the 170.8 five-band oracle and was cleared by sorting alone. Ten binary responses is roughly 10 bits before any adaptivity, so 150 is a stronger claim than it looks and stays unratified until the harness exists.
- **The harness design is settled, and the premise this bullet carried was false.** It said a held-out newbie carries a median of 40 bank responses against an 11,764-problem bank, so an adaptive selector would almost never choose an item that user actually attempted. Measured 16 Aug 2026, a median newbie has **33 observed bank items within 400 rating points of their rating** — constrained, not starved. `quality/eval-gates.md` G2 now specifies real responses on observed items and never simulation from fitted parameters, because the circular branch reports a good number and a gate that cannot report a bad one is not a gate. Two constraints neither branch had named: the pool is all responses contamination-filtered rather than administered only, since administered only leaves a median newbie ten items for a ten-item test; and spread binds before size, because a newbie covers a median of two rating bins of six, so that band's figure is labelled as ability estimated from the user's own near-level responses and never as a demonstration of adaptive selection. Coverage share is published per band beside the MAE.

---

## 4. Twins conforming

The rule from `analysis/div1-div2-twins.md` is settled: contest ids differing by one,
equal names, ratings agreeing or neither side rated. **1,183 pairs qualify** — 1,174
where the ratings agree and 9 where neither side carries a rating. No pair at gap 1 has
exactly one side rated; the twins document said otherwise until 15 Aug 2026 and was
corrected against the data.

**Conforming happens before Stage A, not alongside it.** Fitting first and merging
later invalidates every parameter, and a wrong merge is undetectable afterwards
because pooled responses carry no record of having come from two problems.

**Measured at pair level, which is what the model consumes.** The 523,813 figure in the
twins document is a submission count and predates the response definition.

| Quantity | Value |
|---|---|
| Twin pairs qualifying | 1,183 |
| Absent keys drawing more than one partner | 0 |
| First-attempt pairs on absent keys | 209,069 |
| First-attempt pairs on present keys | 353,611 |
| **Same user on both sides of a twin** | **18,202** |
| Problem keys actually merged | 1,182 |

**The 18,202 are why a naive key remap is wrong.** Those users would each hold two
first-attempt responses to what becomes one item — a direct local-independence violation
of exactly the kind the response definition exists to prevent. **The collapse rule is
therefore: first attempt across both keys by `submission_key`, later side discarded.**
Merged twin-touching pairs fall from 562,680 to 544,478.

1,182 keys merge rather than 1,183 because one absent twin key carries no person-level
evidence row at all and never enters the matrix.

**The merge grows the item bank rather than shrinking it.** Absent twin keys are excluded
by `in_public_problemset`, so their responses were outside the bank entirely; merging
routes them to their present partners. Bank responses rise from 10,626,688 to
**10,817,555** over an unchanged 11,764 problems.

The merge is applied at the model input as a key-mapping table, not as a warehouse
mutation. That keeps it reversible, which is the property the twins document argued
for.

The 9 pairs where neither side is rated pass the rule and are handled explicitly. They
are the weakest members of the set, not a corroborated middle: with no rating on either
side, the name-and-gap match is the whole of the evidence.

---

## 5. Data additions, and the one that needs a decision

**`contest.standings` collection — scope now measured, and the recommendation is
withdrawn pending a decision.** The fact table holds 4,612 distinct contests, 2,537 of
them carrying CONTESTANT rows, so the scoped collection is 2,537 contests rather than
"a collection night" — a phrase this document used twice without measuring it.

Two objections, both found after the recommendation was written:

- **"Who was shown the problem set" overstates it.** Being shown a set is not reading problem F. Educational measurement treats a not-reached item as missing rather than incorrect, precisely because coding it as wrong biases ability downward in proportion to contest speed rather than to the item. A roster does not distinguish "read it and could not do it" from "never opened it".
- **The defensible part is already on disk.** The usable rule is that every index below a participant's highest attempted index was reached, and `dim_problem.problem_index` plus `fct_submission.contest_id` and `participant_type` supply exactly that at zero API calls. What standings adds beyond it is (user, contest) pairs with no submission at all, which under the same rule contribute all-missing rows.

**`user.rating` is the stronger target for the same rate-limited night**, and this
document currently defers it in section 8. It is one request per user, the shape of the
pass that built the corpus, and it is the only external criterion available for
validating fitted ability at more than one point in time — Stage A's central output
currently has none, and Stage B's Elo supplies a time dimension with nothing to calibrate
against.

Binding conditions, all inherited: 1 request per 2 seconds at 2.1s spacing, a
checkpoint per contest so an interruption costs one item, a `LEGAL.md` row before the
first request, no second caller against the API while it runs, and files-on-disk
compared against files-read with a hard failure on a gap.

**The CodeNet response matrix — measured, no ingest needed.** It was one query, not the
job this blueprint first assumed: `stg_codenet_submissions` is a view over silver
Parquet carrying `user_id`, `problem_id`, `is_accepted` and `submission_id`, which is a
complete response matrix. 6,764,548 pairs over 154,178 users and 4,046 problems.
Figures and the judge split are in `analysis/irt-response-definition.md`.

**A second problemset snapshot — required for drift, not for the models.** The
difficulty and tag drift item on the roadmap needs at least two snapshots to compare.
One exists.

---

## 6. Gate revisions

The existing gates are provisional targets set before any model existed. Two are not
merely unratified but structurally wrong, and both are found by the measurement rather
than by opinion.

**G1 — the absolute threshold has to go.** Brier ≤ 0.18 does not mean the same thing on
the two halves of the corpus, and measured against each it is nearly vacuous on one:

| Population | Baseline Brier | Reduction that 0.18 demands |
|---|---|---|
| Codeforces | 0.243562 | 26.1% |
| CodeNet | 0.181701 | 0.94% |
| pooled | 0.227941 | 21.0% |

On CodeNet a constant predictor scores 0.181701, so the gate is passed by a model
that improves on nothing by one part in a hundred. Pooling hides it: the pooled figure
reads as a respectable 21% and one half of it is unmeasured by the gate entirely. The
same threshold under the "ever solved" response definition would sit against a
baseline of 0.064616 on Codeforces and 0.057802 on CodeNet, passing models three times
worse than a constant on both.

**The revision: G1 becomes a required percentage reduction against a per-population
baseline, reported per population, never pooled and never absolute.** The baseline is a
published figure in every calibration artefact, and a model that cannot beat its own
population's constant predictor fails regardless of what the other half scores.

**G3 — unachievable as written.** It requires content-only prediction from "tags plus
statement embedding" for 100% of problems. Codeforces statements can never be stored
under link-never-host, and CodeContests supplies statements for 3,474 CodeNet problems
only. No Codeforces problem will ever have a statement embedding. The gate is revised
to require content features for 100% of problems and to name what they are per source:
tags, rating and `solved_count` for Codeforces; tags and statement embedding for
CodeNet. The degradation target is then measured per source rather than pooled, since
pooling would let dense Codeforces coverage hide thin CodeNet coverage.

**New gate, G11 — item-bank honesty.** No served prediction may present a prior-only
difficulty estimate as an observed one. Enforced structurally: every problem in the
serving set carries its response count and an estimate-source flag, and the serving
pipeline fails if either is absent. This is the same shape as `rating_source` on
community ratings and exists for the same reason.

**New gate, G13 — topic-cell honesty.** No surface may render a topical ability estimate
for a (user, topic) cell below the response floor as though it were measured. Enforced
structurally: every served topic cell carries its response count and an estimate-source
flag, and the serving pipeline fails if either is absent. Same shape as G11 and the same
reason — with a median cell holding 5 responses and 22.4% of users holding no cell above
ten, a chart that renders all dimensions identically is rendering mostly noise.

**New gate, G12 — response-unit integrity.** The response builder asserts that
responses equal distinct pairs, that attempts equal person-level evidence rows, and
that the ordering key is unique. All three were measured this chapter and all three
are the kind of thing that changes silently under a refactor.

Every one of these is proven against a mutation before it is trusted. A gate that has
not been watched to go red is not a gate.

**And a gate with no named trigger is not a gate either.** G11, G12 and G13 were stated
above as requirements and nothing said what runs them or what artefact they read, which
is the failure `quality/eval-gates.md` G10 names directly: naming what a gate does not
cover is what separates it from a claim. Specified:

| Gate | Runs | Mechanism | Status |
|---|---|---|---|
| G11 item-bank honesty | serving-set build | schema requirement on the served payload | DESIGNED |
| G12 response-unit integrity | invariants on every push; pinned counts under `--real-data` | `codrona_lens.responses.matrix`, gated against `exports/model/responses.manifest.json` | **ENFORCED** |
| G13 topic-cell honesty | serving-set build | schema requirement on the served payload | DESIGNED |

**`DESIGNED` is a new status and it is deliberately not `PROVISIONAL`.** A provisional
gate has a target nobody has ratified; a designed gate has no runnable trigger at all,
because the serving pipeline it inspects does not exist until Phase 4. Recording them as
provisional would imply something runs them. Nothing does. They become `ENFORCED` when
the serving path exists, and until then they are a design commitment.

**G12 is specifiable now, and these are its assertions.** The response builder is Phase 2
work, so every expected value below is already measured:

| Assertion | Expected | Mutation that must make it fail |
|---|---|---|
| ordering key unique | 23,607,105 rows = 23,607,105 distinct `submission_key` | duplicate one key |
| attempts = person-level evidence rows | 22,843,153 | drop the `is_person_level` filter |
| unmerged responses = distinct pairs | 11,176,774 | order by `submitted_at`, which has 332 ties |
| twin remap key count | 1,182 merged keys | admit gap-2 matches |
| merged responses | 11,158,572 = 11,176,774 − 18,202 | apply the remap without collapsing first attempts |
| merged attempts unchanged | 22,843,153 | drop rows during the remap rather than relabel them |

The last two are the pair that matters. A merge must move rows between keys and never
remove any, so responses fall by exactly the duplicate count while attempts stay
identical — and a naive remap that fails to collapse first attempts passes the attempt
assertion while failing the response one. That is the reconciliation-pair discipline the
master document already requires: a count nothing compares against is a count nothing can
catch.

**Settled: `lens`, and the reason is G10 rather than preference.** The builder reads
`main_marts.fct_submission` through `codrona_lens.warehouse.connect`, which G10 makes
the only sanctioned route to DuckDB. In `mind` it would either open DuckDB itself,
violating that gate, or depend on `lens` anyway. The boundary between the two
repositories is the emitted artefact: `lens` writes the matrix, `mind` reads a file and
never sees the warehouse. The gate shipped in the same commit as the builder, because a
builder without its assertions is how 11,176,774 quietly becomes something else.

**Two of the six assertions above were wrong when built, and both are recorded rather
than quietly corrected.** `twin remap key count` measured 1,180 against the 1,182 here,
because the first implementation counted absent keys supplying a surviving *first
attempt* rather than absent keys carrying at least one evidence row — two keys have
evidence yet never win the ordering against the same user's earlier present-key attempt.
Different quantity, wrong one. Separately, the rule was first implemented from
`analysis/div1-div2-twins.md`'s prose rather than its reproduction query, and the two
differ; see that document. The built gate carries thirteen counts rather than six, adding
the twin rule's own rating classes and the populations its scope excludes.

**G12 is split, and the split is what makes it runnable.** Pinned unconditionally, the
counts above cannot pass against the synthetic fixtures CI builds — the wall G8 already
meets and answers with the `real_data` dbt tag. So the structural invariants run on any
dataset and the pinned counts run only under `--real-data`, with a test asserting the
pinned half *must* fail on fixtures. A gate that executes on one laptop is not in CI, and
a gate CI skips is not a gate.

---

## 7. Sequencing

| Order | Item | Blocks |
|---|---|---|
| 1 | ~~CodeNet response matrix measured~~ — DONE, see the analysis doc | nothing |
| 2 | ~~Tag coverage and co-occurrence measured~~ — DONE, section 3 Stage B | nothing |
| 3 | ~~Twins yield re-measured at pair level~~ — DONE, section 4 | nothing |
| 4 | ~~Twin key-mapping applied at model input~~ — DONE, built in `lens` with G12 enforced | nothing |
| 5 | Stage A on the administered subset | everything downstream |
| 6 | Stage A on all first attempts, compared | the self-selection report |
| 7 | Stages B and C — both respecified in section 3 against measurement | Stage D |
| 8 | Stage D, temporal split | G1 ratification |
| 9 | G1 ratified against the measured baseline | any published metric |
| 10 | Stages E and F | Phase 4 and 5 |

`contest.standings` collection runs parallel to items 1 through 4 if approved. If it
is declined, the administered fit proceeds on submit-only rosters and the blueprint
records that as a stated limitation rather than an unknown.

---

## 8. Deliberately not in this phase

- Cross-judge difficulty equivalence as a fitted quantity. It is a content-model estimate and is labelled as one.
- Any warehouse mutation. Twins conforming is a model-input mapping.
- Hyperparameters, learning rates and architecture sizes. These come out of the first fit.
- The live experiment. Off-policy estimates only until Phase 5.
- Rating history per user, **unless section 9's decision approves collecting it**. `user.ratedList` gives today's rating only, so absent that collection, ability trajectories are inferred from responses rather than validated against a rating curve. This bullet read as an unconditional exclusion until 16 Aug 2026, contradicting section 9's recommendation to approve.

---

## 9. Decisions owed by the founder

- **`contest.standings` collection: approve or decline.** Recommendation changed to **decline**, on measurement rather than on cost: the scope is 2,537 contests, and the reached-item structure it is wanted for is already derivable from `problem_index` at zero API calls. See section 5.
- **`user.rating` history collection: approve or decline.** Still recommended, and the recommendation now rests on two grounds rather than four. It is the only route to validating fitted ability against an external criterion over time, and it is the only thing that would make a rating-conditioned ability prior admissible under a temporal split (Stage A). Two things that were argued to need it do **not**: the practice-response rule, since 71.3% of bank responses fall within one year of the 2026-08-06 snapshot and 94.3% within four, and `max_rating` anchors that rule with no collection at all; and the non-monotone newbie share, which `max_rank_name` separated on 16 Aug 2026 without it. One request per user, a `LEGAL.md` row before the first request, and roughly 32 hours of request spacing alone at the documented 1-request-per-2-seconds limit — the shape of the pass that built the corpus rather than a single night.
- **Whether the ability prior is ever conditioned on rating.** Recommendation: not now, and this is downstream of the `user.rating` decision rather than parallel to it. On today's data the answer is no on leakage grounds alone; if rating history is collected the answer changes, because a rating as of the response date is not future information. Settling it before the collection decision would settle it on the wrong evidence.
- **Response floor for prior-only items.** A number set after the first fit, not now, but the policy question is whether prior-only items are served at all or withheld until they have responses. Recommendation: served, flagged, and excluded from the calibration report's headline figure.
- **Whether the cross-judge claim is narrowed in the master document now or after the content model is measured.** Recommendation: now, because the claim is currently stronger than anything that can be built.
