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

## The finding that settles it

**At a contest gap of 1, no name-matched pair disagrees on rating.** Of 1,183
name-matched pairs at gap 1: 1,174 agree, 9 have **neither** side rated, and zero
differ. Not one pair has exactly one side rated.

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

1. The two contest ids differ by exactly one.
2. The problem names are equal.
3. The ratings agree, or neither side is rated. No pair at gap 1 has exactly one side rated, so that case is vacuous rather than admitted.

**Yield: 1,174 rating-agreeing problems carrying 523,813 submissions, or 1,183
including the nine unrated-on-both-sides pairs, which carry 523,997 between them.**
The three-part rule as written
admits all 1,183, which is what the reproduction query at the foot of this document
returns; the 1,174 figure names the rating-agreeing subset alone. Quote whichever is
meant and say which. Those are the responses
that would otherwise be split across two keys.

Explicitly excluded, and each for a stated reason rather than by omission:

- Matches at any contest gap other than 1 — the rating disagreements live entirely here, so these are name collisions rather than twins.
- Matches resolved only by tags — superseded, and the tags route left 156 ambiguous against 11 for rating.
- Gym and acmsguru — out of the archive's scope, and acmsguru carries no contest id to compare.
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

## A note on earlier figures

Previous work recorded 1,852 problems matching by name, 447 once tags had to
agree, 156 ambiguous, and 591,295 submissions on absent ids. Those came from a
different rule and are not comparable line for line. This document's figures
supersede them: 1,921 absent mainline problems carrying 628,205 submissions, of
which 1,174 problems and 523,813 submissions meet the three-part rule. Any figure
quoted from here should travel with the rule that produced it.
