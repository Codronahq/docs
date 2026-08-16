# One problem, two keys: the Div. 1 / Div. 2 twin measurement

**Status: measurement complete, conforming deliberately not done.** This document
records what the corpus says about problems that appear under two contest ids. It
is an input to Phase 2 modelling, not a change to the warehouse.

## The question

Codeforces runs some events as a Div. 1 and a Div. 2 round simultaneously, and the
same problem appears in both under different contest ids. The public problemset
publishes only one of the pair.

That matters to IRT and to nothing else. If one problem occupies two keys, its
responses split across them, and each key's difficulty is estimated from half the
evidence — producing two under-determined estimates instead of one good one. So
the question is whether the model gets one latent difficulty per *problem* or per
*problem key*, and the answer has to come from the data rather than from
convenience.

## The population

Measured over `dim_problem` filtered to `is_current`, which matters: the dimension
is SCD-2 and an unfiltered count will double as soon as a second snapshot lands.

| Family | In the public archive | Problems | Rated | Named |
|---|---|---|---|---|
| mainline | yes | 11,347 | 11,051 | 11,347 |
| mainline | no | 1,921 | 1,761 | 1,921 |
| gym | no | 21,881 | 106 | 21,881 |
| acmsguru | yes | 417 | 0 | 417 |

Only the 1,921 absent mainline problems are candidates. Gym is out of scope — the
archive's own boundary, not a gap — and acmsguru has no contest id at all.

Those 1,921 problems carry **628,205 submissions, of which 601,233 are evidence
rows**. That is 2.7% of the corpus riding on ids the public problemset omits.

## What each candidate rule showed

**Name alone is not sufficient.** 1,852 of the 1,921 match at least one archived
problem by name, but 151 of them draw two or more candidates and one draws ten.
Codeforces reuses titles.

**Name plus rating is much tighter.** 1,734 resolve to exactly one candidate and
only 11 stay ambiguous. Compare the tags route, which left 156 ambiguous.

**The contest gap is the real signal.** Div. 1 and Div. 2 rounds of one event get
consecutive contest ids, and matched pairs concentrate hard at a gap of 1 — 1,211
pairs, against a long thin tail spread over gaps up to 1,825.

**The index shift confirms the mechanism rather than a coincidence of titles.**
Among gap-1 pairs, the absent problem's index maps onto the archived one in a
consistent offset:

| Absent index | Archive index | Pairs |
|---|---|---|
| C | A | 261 |
| D | B | 260 |
| E | C | 259 |
| F | D | 84 |

Three near-identical counts at C→A, D→B, E→C is the Div. 2 A/B/C to Div. 1 C/D/E
offset showing up in the data. A string coincidence does not produce that shape.

**The full offset distribution is wider than those four rows, measured 16 Aug 2026.**
Over the 1,112 map entries carrying a single-character index on both sides — 68 have a
multi-character absent index and 3 a multi-character published one, which reconciles
to 1,183 — the offsets run **+2 at 879**, −2 at 81, +3 at 73, **0 at 43**, +1 at 21,
−1 at 8, and 9 pairs spread over ten further offsets. The four rows above name 864 of
the 879. So +2 holds 79% and the rest of the population is not at +2 at all: 43 pairs
share an index outright and **81 run the opposite way**, with the archived side
indexed higher. The Div. 2 to Div. 1 shift is the dominant mechanism and not the only
one. An offset of +2 is therefore evidence *for* a pair, while its absence is not
evidence against — a distinction this document did not previously support, and one
that matters immediately below.

## The finding that settles it

**At a contest gap of 1, and in the rule's direction, no name-matched pair disagrees
on rating.** Of 1,183 name-matched pairs: 1,174 agree, 9 have **neither** side rated,
and zero differ. Not one pair has exactly one side rated.

**The direction is load-bearing in that sentence, and was left implicit until
16 Aug 2026.** The reversed population sits at gap 1 too, and is the mirror image: of
its 74 name matches, 37 agree, **zero** have neither side rated, **6** have exactly
one, and **31 differ**. So rating disagreement does occur at gap 1 — just never in the
direction the rule looks — and the two populations' unrated profiles are exact
opposites, 9-and-0 against 0-and-6. Every claim on this page scoped to "gap 1" means
gap 1 in the rule's direction. The reversed figures are below.

That distinction was recorded wrongly here until 15 Aug 2026 and matters to the
model rather than to the prose. A pair with one side rated carries a corroborating
signal; a pair with neither carries a name match at gap 1 and nothing else. The nine
are the *weakest* members of the set, not a partially-corroborated middle.

Across all gaps, 290 pairs share a name and carry different ratings — and every
one of them sits at a gap other than 1. So rating disagreement is not evidence
that twins can hold two difficulties; it is the signature of a name collision
between unrelated problems. `Wrong Subtraction` at a gap of 235, `Graph Cutting`
at 1,825, `Queue`, `Elections`, `Balance`, `Labyrinth` — Codeforces reuses generic
titles across years, and merging on those would pool responses from genuinely
different problems into one difficulty estimate. That is the corruption this
exercise exists to prevent, and it is the opposite of the one it set out to find.

The contest-pair shape supports the same reading. Grouping matches by contest
pair, the bulk sits at three to five shared problems per pair — 210 pairs share 3,
84 share 4, 24 share 5 — which is what a Div. 1 / Div. 2 split looks like. Only 8
contest pairs share one or two problems, and those are the weak cases.

## The rule this supports

A candidate twin requires all three:

1. The two contest ids differ by exactly one, **and the unpublished side is the higher of the two**. This clause read as symmetric until 16 Aug 2026, while the reproduction query below has always been directional (`p.problem_contest_id = a.problem_contest_id - 1`). The query is what produced every yield on this page, so the query is the rule and the prose was wrong. What the direction excludes is measured below.
2. The problem names are equal, **and no contest publishes that name twice**. This was never stated because nothing tested it; the reversed-direction set below contains two absent keys that each draw two published partners, so the assumption is real and it is not universal.
3. The ratings agree, or neither side is rated — **in the prose. The query admits a pair where EITHER side is unrated.** Over the rule's own directional population the two readings pick out the same 1,183 pairs, because no pair there has exactly one side rated, so the divergence is vacuous **in scope**. It is **not** vacuous outside it: six of the reversed direction's 74 name matches have exactly one side rated, and all six sit inside the 43 that pass, so that audited count is 37 agreeing plus 6 half-rated and a reader applying the prose rule to it computes 37. This clause claimed the divergence was vacuous outright until 16 Aug 2026. The implementation follows the query, carries a counter that fails if the in-scope count ever leaves zero, and now carries the reversed class split so the 43 reconciles to either reading without anyone recomputing it.

**Yield: 1,174 rating-agreeing problems carrying 523,813 submissions, or 1,183
including the nine unrated-on-both-sides pairs, which carry 523,997 between them.**
The three-part rule as written
admits all 1,183, which is what the reproduction query at the foot of this document
returns; the 1,174 figure names the rating-agreeing subset alone. Quote whichever is
meant and say which. Those are the responses
that would otherwise be split across two keys.

## What the rule cannot see

Measured when the rule was implemented, by running it without the direction
constraint and without the gym predicate. None of these change the yield above;
all three are recorded because a population dropped silently is how nobody knew
about the first one.

**43 gap-1 mainline pairs sit in the reversed direction** — 74 name matches of
which 43 pass the rating clause — where the *published* side carries the higher
contest id. The directional query never looks there. They are not simply 43 more
twins: contest 206/207 dominates the set and breaks clause 2, since
`The Beaver's Problem - 3` occupies 206D1 and 206D2 on one side and 207D1, 207D2,
207D3 and 207D9 on the other, at two different ratings. That is a subtask-indexed
round, where a name match resolves nothing and merging on it would pool problems of
genuinely different difficulty. Admitting the reversed direction is therefore a
modelling decision with its own evidence to gather, not a widened predicate.

**It is now costed, and the cost closes it.** Of the 43 pairs only **30** absent keys
carry any evidence at all, totalling **161 responses**, with **9 users** on both
sides. The rule's own merge routed 190,867 responses into the item bank; admitting
the reversed direction would route 161, roughly **1,185 times less**, in exchange for
the 206/207 subtask hazard above and the 31 rating disagreements the direction
currently filters out. **Decision: not admitted, and not deferred again.** The number
is recorded so the question is answered rather than left open.

**Four gap-1 mainline pairs have both keys published, and one of them passes every
clause of the rule.** Three are themed-round name reuse that the rating clause
rejects outright — `Mr. Kitayuta's Gift` at 1100 against 3000, `Mr. Kitayuta's
Colorful Graph` at 1400 against 2400, `Drazil and His Happy Friends` at 1300
against 3100. The fourth is **`420C` / `421D`, `Bug in Code`, rated 1900 on both
sides** — the one case the absent-versus-present framing cannot express, since both
keys are already in the item bank. **Measured 16 Aug 2026, and decided: not merged,
and no longer an open item.** `420C` carries 71 responses and `421D` 31, with **18
users holding both**, so the split is real and small. Three things say they are two
problems rather than one.

Codeforces publishes exactly one problemset entry per problem: every one of the 1,183
canonical twins appears once, which is the entire reason the rule is shaped as absent
versus present. It gave these two entries. That is the platform's own statement, and
it is the strongest evidence available here.

Their tags overlap at a Jaccard of **0.167** — `data structures, graphs,
implementation, two pointers` against `binary search, data structures, sortings`,
one tag shared of six. That is the joint-lowest of the four, while `505B` / `506D`,
a pair nobody disputes is two different problems, sits at **0.600**. A duplicate
should top that column; this one bottoms it.

Of the 18 users holding both, **8 solved one and failed the other** — weak on its own,
since a first attempt in contest and one in practice years later differ legitimately,
and it points the same way as the rest.

Equal ratings are the single clause it satisfies, and the rating clause is a filter
against collisions rather than positive evidence of identity: it rejected the other
three by a mechanism — wildly divergent difficulty — that has nothing to do with
both-published pairs, and on the one pair where ratings coincide it gave no answer at
all. The index offset of +1 is **not** among the reasons: 21 confirmed twins sit at
+1, as the distribution above records.

**606 gap-1 name pairs sit in gym.** Out of the archive's scope and out of the item
bank, so they cannot affect any yield here. They are counted anyway because the
response matrix is deliberately *not* bank-filtered, so a mirrored gym contest would
split one problem's responses inside it.

**The query's `problem_contest_id < 100000` predicate is inert.** A gym problem is
never in the public problemset, so it can never be the published side, and a gym
absent problem can only match a published partner that is by definition not gym.
Removing it changes nothing. It documents intent and filters nothing, which is worth
knowing before anyone treats it as load-bearing.

## The merge, as built

Applied at model input in `codronahq/lens`, never to the warehouse. The map holds
**1,183 entries**; **1,182** of those absent keys carry at least one person-level
evidence row, the remaining one carrying none and never entering the matrix.
Collapsing first attempts across both sides removes **18,202** duplicate responses,
and **202,102** surviving responses are attributed to an absent source key.

That last figure reconciles against this document rather than standing alone:
190,867 pairs touch an absent key only, and 11,235 of the 18,202 users who touched
both sides submitted to the absent side first, which sums to exactly 202,102.
**61.7% attempting the unpublished side first** is the Div. 2 round being played
live and the Div. 1 mirror met later in practice — the same mechanism the index
shift above infers from structure, visible here in the ordering.

Reproducible from `exports/model/responses.manifest.json` in `lens` via
`python3 -m codrona_lens.responses.matrix --verify-current`.

Explicitly excluded, and each for a stated reason rather than by omission:

- Matches at any contest gap other than 1 — the rating disagreements live entirely here, so these are name collisions rather than twins.
- Matches resolved only by tags — superseded, and the tags route left 156 ambiguous against 11 for rating.
- Gym and acmsguru — out of the archive's scope, and acmsguru carries no contest id to compare. The gym exclusion is stated intent rather than an active filter; see above.
- The reversed direction, both-published pairs, and gym name matches — measured above rather than merely asserted, and each excluded for a reason of its own.
- The 9 pairs where neither side is rated pass the rule but should be handled explicitly by the model rather than silently, since nothing corroborates them at all — no rating on either side means the name-and-gap match is the whole of the evidence. They carry **184 submissions between them, every one an evidence row**, averaging 20 per problem: obscure enough that neither side ever earned a rating, which is the same fact seen from the other side. 523,997 − 523,813 = 184 and 520,639 − 520,455 = 184, so the two yields reconcile against each other rather than each standing alone.

## Why the warehouse is not changed

Conforming two problem keys into one is a merge, and a wrong merge is undetectable
afterwards: once responses are pooled, nothing in the data records that they came
from two problems. The measurement is reversible and the merge is not, so the
measurement is the deliverable. Phase 2 decides what to do with it, with these
numbers in hand.

Nothing in the current warehouse assumes one problem is one key, and nothing
should be added that does.

## Reproduction

Every figure above comes from the local warehouse and can be re-derived. The
session timezone should be pinned to UTC, as `profiles.yml` does, though no figure
here depends on it — the timezone-sensitive columns live on `dim_user`.

```sql
-- the confident twins, and the evidence they carry
with cur as (
    select * from main_marts.dim_problem
    where is_current and problem_contest_id is not null and problem_contest_id < 100000
),
absent as (select * from cur where not in_public_problemset),
present as (select * from cur where in_public_problemset)
select count(distinct a.problem_key) as twin_problems
from absent a
join present p
  on p.problem_name = a.problem_name
 and p.problem_contest_id = a.problem_contest_id - 1
 and (p.problem_rating = a.problem_rating
      or p.problem_rating is null or a.problem_rating is null);
```

The reversed population's rating classes and the offset distribution, both added
16 Aug 2026. The first is also emitted by `lens` into
`exports/model/responses.manifest.json` under `twin_excluded`, so the query and the
gate can be compared rather than trusted separately.

```sql
-- reversed direction: name matches by rating class
with cur as (
    select * from main_marts.dim_problem
    where is_current and problem_contest_id is not null
      and problem_contest_id < 100000 and problem_name is not null
),
absent as (select * from cur where not in_public_problemset),
present as (select * from cur where in_public_problemset)
select case
         when a.problem_rating is null and p.problem_rating is null then 'both unrated'
         when a.problem_rating is null or p.problem_rating is null then 'one unrated'
         when a.problem_rating = p.problem_rating then 'agree'
         else 'differ'
       end as rating_class,
       count(*) as pairs
from absent a
join present p
  on p.problem_name = a.problem_name
 and p.problem_contest_id = a.problem_contest_id + 1
group by 1 order by 2 desc;
```

The offset distribution needs the derived map rather than a single query; it is
`twins.derive` joined back to `dim_problem` on both keys, differencing
`ascii(problem_index)` and restricted to single-character indices on both sides.

## A note on earlier figures

Previous work recorded 1,852 problems matching by name, 447 once tags had to
agree, 156 ambiguous, and 591,295 submissions on absent ids. Those came from a
different rule and are not comparable line for line. This document's figures
supersede them: 1,921 absent mainline problems carrying 628,205 submissions, of
which 1,174 problems and 523,813 submissions meet the three-part rule. Any figure
quoted from here should travel with the rule that produced it.
