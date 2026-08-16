# The person margin, and what selection does to it

**Status: measurement complete, no warehouse change and no model change.** This
document records what the corpus says about the *user* side of the response matrix.
It is an input to Phase 2 Stage A and changes nothing in `lens` beyond the
measurements themselves.

**Why it exists.** `analysis/irt-response-definition.md` measured the item margin
exhaustively — threshold counts at 30, 100, 200 and 500 under three pooling
definitions, and a per-band density collapse. The person margin got a headcount and
one mean. A 2PL fit has two margins and only one of them had ever been looked at.

**Scope: the merged item bank, which is the matrix Stage A fits.** 10,817,555
responses over 55,231 users and 11,764 problems, after twin conforming and after the
`in_public_problemset` filter. Every figure here is measured on that population and
not on the full matrix, because a margin measured on a population the model is not
fitted on describes something else. An earlier draft of this measurement ran on the
unmerged bank and reported a median of 73 and a mean of 192.41; those are real
numbers about the wrong matrix and are superseded by the ones below.

## The person margin

| Bank responses per user | all | administered |
|---|---|---|
| mean | 195.86 | 69.16 |
| p10 | 6 | 3 |
| p25 | 21 | 8 |
| **median** | **74** | **23** |
| p75 | 225 | 66 |
| p90 | 507 | 168 |
| max | 11,118 | 3,848 |
| users at zero | 0 | 166 |
| users under 10 | 7,864 — 14.2% | 16,122 — 29.2% |
| users under 30 | 17,163 — 31.1% | **30,944 — 56.0%** |
| users at 100 or more | 23,959 — 43.4% | 9,662 — 17.5% |

"Administered" is CONTESTANT plus VIRTUAL, the row classes where the participant was
shown a whole problem set rather than choosing one problem from the archive. It is
3,819,560 responses, **35.3% of the bank**.

**The mean is not a description of this distribution.** 195.86 falls between the median of 74 and the
75th percentile of 225, so it describes a user in the top third of the cohort by
volume. `architecture/phase-2-modelling.md` quotes it correctly and it is the
right number; it is simply not a summary, and the median is 74.

## The thinness is one band, not the cohort

| Rank | Users | Median all | Median administered | Administered under 30 |
|---|---|---|---|---|
| newbie | 37,532 | 40 | 12 | 28,456 |
| pupil | 8,175 | 180 | 61 | 1,696 |
| specialist | 5,023 | 261 | 96 | 551 |
| expert | 3,165 | 348 | 144 | 213 |
| candidate master | 670 | 438 | 188 | 24 |
| master | 368 | 578 | 257 | 3 |
| international master | 106 | 586 | 295.5 | 1 |
| grandmaster | 114 | 624 | 263.5 | 0 |
| international grandmaster | 60 | 1,108 | 604.5 | 0 |
| legendary grandmaster | 18 | 2,290.5 | 1,232.5 | 0 |

**Of the 30,944 users with fewer than 30 administered responses, 28,456 — 92.0% — are
newbies.** For the 17,699 users rated 1200 or above, the figure is 14.1%. The pooled
median of 23 is a mixture statistic dominated by the 68.0% of the cohort sitting in
one band, and quoting it pooled is the error `quality/eval-gates.md` G1 was revised
to prevent, in a different place.

**Two consequences for Stage A, neither of them in the blueprint before this.**

- Ability needs a prior for the same reason difficulty does. Stage A draws difficulty from a prior conditioned on `problem_rating` and `log(solved_count)`; nothing conditions ability, though `dim_user.rating` and `max_rating` are the exact external analogue. At a newbie median of 12 administered responses a free ability estimate is noise with a decimal point.
- That prior creates a circularity G2 has to handle. G2 validates a placement test against rating. An ability prior conditioned on rating means the model is partly predicting rating from rating, and the harness has to hold that out or report the prior-only baseline beside the score.

## The information budget

Administered responses by problem difficulty, over the merged bank.

| Problem band | Administered | Share | Problems | Median responder depth | CM and above |
|---|---|---|---|---|---|
| under 1200 | 2,400,578 | 62.85% | 2,282 | 164 | 7.6% |
| 1200–1599 | 782,183 | 20.48% | 1,859 | 278 | 14.7% |
| 1600–1999 | 334,956 | 8.77% | 2,045 | 440 | 30.6% |
| 2000–2399 | 119,260 | 3.12% | 1,768 | 595 | 53.5% |
| 2400–2799 | 39,893 | 1.04% | 1,440 | 922 | 73.5% |
| 2800+ | 14,456 | 0.38% | 1,285 | 1,177 | 80.1% |
| unrated | 128,234 | 3.36% | 284 | 51 | 5.7% |

**98.6% of the administered evidence sits below 2400, and 62.85% below 1200.** The
sub-1200 band carries 166 times the responses of 2800+.

**But the thin bands are anchored by deep users, and that is the finding that makes
them estimable at all.** Median responder depth rises monotonically with difficulty,
164 to 1,177 administered responses, and the CM-and-above share rises 7.6% to 80.1%.
A 2800+ problem has few responses and they come from people whose own ability is
precisely estimated. An earlier reading of this document's own author predicted both
margins would be thin *simultaneously* in the administered fit; measured, they are
thin in different populations, and the population that makes hard items thin is the
deepest in the cohort.

**801 of the bank's 11,764 problems carry no administered response at all**, so the
administered fit's item bank is 10,963 problems, not 11,764.

**What this costs Stage A, stated plainly.** At a committed median of 4 administered
responses per 2800+ problem, the posterior for a hard item is essentially its prior,
and the prior is `problem_rating` and `log(solved_count)`. In the hard bands the
fitted difficulty is therefore close to a smooth transform of the rating Codeforces
already publishes. That is the correct engineering choice and it is also a limit on
what any surface may claim: the model earns its difficulty estimate in the dense
low and middle bands, not at the top, which is where `codrona.md` section 0 promises
most. G11 exists for exactly this and its response floor is still unset.

## Self-selection reverses sign at 1200

First-attempt accepted rate, administered against practice, over the merged bank.

| Problem band | Administered AC | Practice AC | Practice − administered |
|---|---|---|---|
| under 1200 | 67.94% | 63.65% | **−4.29** |
| 1200–1599 | 49.16% | 53.04% | +3.88 |
| 1600–1999 | 40.77% | 48.83% | +8.06 |
| 2000–2399 | 36.26% | 44.53% | +8.27 |
| 2400–2799 | 33.26% | 40.76% | +7.50 |
| 2800+ | 29.59% | 37.26% | +7.67 |
| unrated | 55.55% | 52.19% | **−3.36** |

`architecture/phase-2-modelling.md` Stage A plans to fit the administered subset
first and compare its difficulty vector against a practice fit, reading agreement as
evidence the practice rows carry signal and divergence as the self-selection bias
appearing. **Pooled, the sign flip partly cancels and that comparison would report
near-agreement.** Per band it points opposite ways.

The confound is population composition rather than selection. An easy problem inside
a contest is answered by everyone present, including masters; the same problem in
practice is attempted mostly by the weakest users grinding. Nothing about that is
self-selection bias, and it dominates the two bands where administered beats
practice. **The comparison is therefore only interpretable per band, and it needs a
noise floor**: split the administered responses at random, fit both halves, and
compare their difficulty vectors. That is what pure estimation noise looks like at
this sample size, and administered-versus-practice divergence means something only
where it exceeds it.

## Practice responses on far-above-rating problems are not clean

Newbie-ranked users, on problems rated 2000 and above.

| Problem band | Mode | Responses | Accepted | Rate |
|---|---|---|---|---|
| 2000–2399 | practice | 24,442 | 9,288 | 38.00% |
| 2000–2399 | administered | 4,534 | 704 | 15.53% |
| 2400–2799 | practice | 8,025 | 2,644 | 32.95% |
| 2400–2799 | administered | 1,812 | 157 | 8.66% |
| 2800+ | practice | 5,016 | 1,277 | 25.46% |
| 2800+ | administered | 1,142 | 53 | **4.64%** |

The administered rates are what a genuinely weak person shown a hard problem looks
like: 4.64% on 2800+. Those responses are consistent evidence and the model should
have them.

The practice rates are not. **A user rated under 1200 accepting a quarter of the
2800+ problems they touch is not a description of ability**, and the gap on the same
rank and the same band is 20.82pp at 2800+, 24.28pp at 2400–2799 and 22.47pp at
2000–2399. Retroactive rating, editorial lookup in practice mode, and alternate
accounts all produce this shape and nothing here separates them.

**Why this is worse than self-selection.** Self-selection biases *which* items get a
response. This biases *the response value itself*: a positive response that does not
reflect the person's ability on that item. Item response theory assumes it does. The
blueprint's choice of the administered subset as the reference is right, and for a
stronger reason than it gives — and whether practice responses far above the
responder's rating are excluded, downweighted or kept is a Stage A decision the
blueprint does not yet contain.

## A caveat that touches every rank figure here

`dim_user.rating` is a single 2026-08-06 snapshot applied retroactively to responses
spanning 2010 to 2026 — the person-side analogue of the blueprint's Constraint 4 for
`problem_rating`, and worse, because ability genuinely changes over sixteen years
while a problem's difficulty does not.

The split matters and is stated rather than left for a reader to work out. **Response
counts and depth figures are time-invariant** and survive: a user with 1,232.5 median
administered responses has them regardless of when. **Rank attributions do not.**
"80.1% CM and above on 2800+" assigns responses from across sixteen years by 2026
rank.

The non-monotone newbie share is where this shows. Newbies are 33.5% of administered
responses under 1200, falling to 3.8% at 2000–2399, then **rising to 4.5% and 7.9%**
in the two hardest bands. Two readings fit — Div. 2 rounds administering a 2800+
final problem to everyone registered, which is benign and informative, or today's
rank misdescribing who those people were — and this document does not separate them.
`user.rating` history is the collection that would; it is a decision owed in
`architecture/phase-2-modelling.md` section 9.

## What this document does not claim

It does not say the practice rows are unusable. It says they carry a confound whose
sign depends on the band, and a contamination concentrated in responses far above the
responder's rating, and that both are reported rather than averaged away.

It does not set a response floor for ability estimates. That is a number set after
the first fit, as G11's item-side floor is. It says only that no floor currently
exists on the person side, while items have one and topic cells have G13.

It says nothing about CodeNet, which has no participant type, no contest context and
no roster, so none of the administered-versus-practice structure here exists there at
all.

## Reproduction

Every figure derives from the committed response matrix and the warehouse, through
`codrona_lens.warehouse.connect`, which pins the session timezone. The matrix itself
is gated: `python3 -m codrona_lens.responses.matrix --verify-current`, against
`exports/model/responses.manifest.json` in `lens`.

```sql
-- the person margin, on the merged bank
with bank as (
    select r.user_key,
           r.participant_type in ('CONTESTANT', 'VIRTUAL') as adm
    from read_parquet('~/codrona-data/model/responses.parquet') r
    where r.in_public_problemset
),
per_user as (
    select user_key,
           count(*) as n_all,
           count(*) filter (where adm) as n_adm
    from bank group by 1
)
select count(*) as users,
       median(n_all), median(n_adm),
       count(*) filter (where n_adm < 30) as adm_under_30
from per_user;
```

```sql
-- the information budget and responder depth
with bank as (
    select r.user_key, r.problem_key, r.problem_rating,
           r.participant_type in ('CONTESTANT', 'VIRTUAL') as adm
    from read_parquet('~/codrona-data/model/responses.parquet') r
    where r.in_public_problemset
),
depth as (
    select user_key, count(*) filter (where adm) as n_adm
    from bank group by 1
)
select b.problem_rating >= 2400 as hard,
       count(*) as adm_responses,
       count(distinct b.problem_key) as problems,
       median(d.n_adm) as median_responder_depth
from bank b join depth d on d.user_key = b.user_key
where b.adm group by 1;
```
