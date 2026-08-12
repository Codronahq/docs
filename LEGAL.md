# LEGAL — data provenance and licence ledger

**Rule:** free to fetch is not free to use. No dataset, corpus, or feed enters the
pipeline until it has a verified row in this table. A row is verified when the
licence has been read at the source URL on the recorded date — not inferred from a
paper, a blog post, a mirror, or a Hugging Face card.

Rows marked **VERIFY** are blocking. Ingestion code for that source must not merge.

*Not legal advice.*

---

## 1. Training corpora

### IBM Project CodeNet — VERIFIED

| Field | Value |
|---|---|
| Author | IBM Research |
| Dataset licence | CDLA-Permissive-2.0 |
| Tooling licence | Apache-2.0 |
| Licence URL | https://cdla.dev/permissive-2-0/ |
| Source URL | https://developer.ibm.com/exchanges/data/all/project-codenet/ |
| Code repo | https://github.com/IBM/Project_CodeNet |
| Scale | ~13.9M submissions, 4,053 problems, 55 languages |
| Read date | 2026-08-03 |
| Read by | Ayush Gupta |
| Commercial use | Permitted |
| Share-alike | No |
| Obligations | Include the agreement text when redistributing the data |
| Attribution | Required in [`ATTRIBUTION.md`](https://github.com/codronahq/core/blob/main/ATTRIBUTION.md) and the observatory footer |
| Ingested | 2026-08-10 — `metadata/` and `problem_descriptions/` only. The 13.9M-file `data/` tree of submitted source is deliberately not extracted; no Phase 1 feature reads it. Row counts live in codrona.md §6, not here. |

**Notes.** CDLA-Permissive-2.0 was written for exactly this case and imposes no
copyleft on models trained from the data. Submissions were contributed to online
judges by their authors; IBM states the corpus was cleared for public disclosure.
Derived artefacts (features, fitted parameters) are not encumbered.

---

### Aizu Online Judge (AOJ) — PENDING PERMISSION

| Field | Value |
|---|---|
| Author | University of Aizu |
| Licence | **None stated.** No licence or terms appear on the developer site, the guides, or any of the five API documents. |
| API docs | http://developers.u-aizu.ac.jp/ |
| API host | https://judgeapi.u-aizu.ac.jp |
| Published APIs | Core, Analytic, Data (test cases), Resource (descriptions, commentaries), Review — last updated 2025 |
| Rate limit | Not published. Documentation asks callers to be respectful and avoid excessive concurrent requests. |
| Contact | Yutaka Watanobe, yutaka@u-aizu.ac.jp — named on the developer site for archive enquiries |
| Read date | 2026-08-04 |
| Read by | Ayush Gupta |
| Permission requested | 2026-08-05, by email, awaiting reply |
| Follow-up due | 2026-09-05, one polite reminder, once only |
| Decision date | 2026-10-05, after which this row becomes a decline |
| Disposition | **Do not ingest until written permission is received.** Not required for Phase 1. |

**Why this is pending rather than declined.** No licence found is ordinarily a verified
state meaning do not ingest, and that is where this row sits today. What separates AOJ from
the other unlicensed sources in this file is that the rights holder is directly reachable
and has licensed this data permissively before: the Aizu submissions in IBM Project CodeNet,
recorded above as verified under CDLA-Permissive-2.0, came out of a collaboration involving
the same contact named on the AOJ developer site. Asking is a real route here, not a
formality.

**A permission enquiry was sent on 2026-08-05** covering three points: the terms under which
API submission metadata may be used as training data for a statistical model in an
open-source project that may later carry a paid tier; whether the source-code archive files
the site describes as in preparation will be available and under what terms; and what
request rate the operator would like clients to hold to, since the published guidance gives
no figure and this project enforces limits in code rather than by convention. Any reply is
recorded in this file before any adapter is written.

**Codrona does not depend on this.** Historical Aizu submissions already reach the warehouse
through Project CodeNet under a verified licence. AOJ would extend that coverage past
CodeNet's 2021 snapshot and add live problem and test-case data. That is an improvement, not
a prerequisite, and no Phase 1 work is blocked by it.

**Link-never-host applies here too.** The Resource API serves problem descriptions and
commentaries, and no licence covers them. Until permission states otherwise, Codrona stores
and serves no AOJ problem text; problem references link to the judge.

**A pending row needs an expiry, or it becomes a permanent one.** No reply after a week means little: the enquiry was unsolicited, Obon falls 13-16 August and the Japanese academic summer break runs through September. So the wait is dated rather than open. One follow-up on 2026-09-05 - one is professional, two is pestering - and if 2026-10-05 passes in silence the disposition changes from PENDING to CONSIDERED, DECLINED without further deliberation. Nothing waits on this: no Phase 1, 2 or 3 work depends on AOJ.

**What silence actually costs.** AIZU history stops at CodeNet's 2020-10-01 snapshot and ages from there; there is no live AOJ integration, so no user can connect an AOJ handle; and the test-case and source-code archives stay out of reach. What survives is most of the value: 1,955,837 AIZU submissions across 2,534 problems under a verified licence, plus statements and generated tests for the AIZU partition through CodeContests. AOJ supplies no difficulty labels in any case. The corpus headline never counted it. The real consequence is a product one for Phase 5 rather than a data one: with AtCoder bulk-excluded and AOJ declined, Codrona would carry no live Japanese judge, and cross-judge profiles would be Codeforces plus LeetCode, with AtCoder limited to per-user reads of a self-connected handle.

**If permission is refused or never arrives,** this row becomes a decline and Aizu coverage
remains whatever CodeNet provides. No further action is required for that outcome.

*Not legal advice.*

---

### Codeforces open dataset (end-2024) — CONSIDERED, DECLINED

| Field | Value |
|---|---|
| Author | `denk` (Codeforces community member) — **not** Codeforces |
| Licence as published | CC BY 4.0 |
| Licence URL | https://creativecommons.org/licenses/by/4.0/ |
| Source URL | https://huggingface.co/datasets/denkCF/UsersCodeforcesSubmissionsEnd2024 |
| Announcement | https://codeforces.com/blog/entry/136853 |
| Scale | 17,607,999 rows, 135 MB, six columns |
| Read date | 2026-08-04 |
| Read by | Ayush Gupta |
| Disposition | **Declined.** Not ingested. |

**Why this is declined.** This is not a finding that the licence is defective. CC BY
4.0 is stated plainly on the dataset card and in the repository metadata, permits
commercial use, and carries no share-alike clause. Three things make ingestion
unnecessary and therefore unwise.

First, the grant comes from a party who does not hold the underlying rights. The
author collected the data through the Codeforces API and republished it. Codeforces'
Terms restrict sublicensing of Website material, and their Your Content clause vests
a sublicensable licence in Codeforces rather than in any third party. Whether that
renders the CC BY 4.0 grant ineffective over bare factual records is a real question.
It is also a question we do not have to answer.

Second, the same records are reproducible directly from the official API under its
own terms — `user.ratedList` followed by paginated `user.status`. Collecting them
ourselves puts Codrona in the author's position rather than downstream of it, and
removes the third-party grant from the provenance chain entirely.

Third, self-collection returns strictly more: problem tags, programming language,
`participantType` (contest versus practice), time and memory consumed, full verdict
detail, and public handles that are not anonymised. The published file carries six
columns and no tags, which cannot satisfy the content-based-features gate for
previously unseen problems. The convenience copy was never sufficient for the models
we intend to fit.

**Privacy note.** Handles in the published file are anonymised and shuffled, but a
commenter on the announcement demonstrated identifying his own records by matching
submission patterns within narrow rating bands. Codrona does not attempt
re-identification of anonymised data from any source. This applies whether or not a
dataset is ingested.

**Re-open condition.** If direct API collection becomes unavailable, this row may be
revisited — but the sublicensing question must be resolved first, not assumed away.

---

### Codeforces API — VERIFIED

| Field | Value |
|---|---|
| Author | CODEFORCES GLOBAL - FZCO (UAE, reg. DSO-FZCO-51038) |
| Terms URL | https://codeforces.com/terms |
| API documentation | https://codeforces.com/apiHelp |
| Licence | None stated on the API page; the site Terms govern |
| Rate limit | **1 request per 2 seconds** (documented) |
| Governing law | United Arab Emirates |
| Scale | ~8,000+ problems; full public submission metadata; live |
| Read date | 2026-08-04 |
| Read by | Ayush Gupta |
| Role | Primary live integration **and** the Codeforces bulk corpus |
| Disposition | Ingestion permitted under the operating rules below |
| Ingested | 2026-08-06 to 2026-08-09 — `user.ratedList` then paginated `user.status` across the full active rated cohort, at the documented limit. Verdict-level metadata only: the API returns no submitted source, so none was stored. Row counts live in codrona.md §6, not here. |

**Rate limit correction.** The documented limit is one call per two seconds. The
figure of roughly five requests per second, carried in earlier drafts of this file
and in the project documents, is community folklore and is wrong by a factor of ten.
Canonical Numbers records 1 req / 2 s.

**Operating rules — enforced in code, not by convention.**

1. Minimum 2000 ms between calls, through a single global limiter shared by every worker. Parallelism does not multiply the budget.
2. Descriptive `User-Agent` identifying Codrona with a contact URL.
3. Responses cached aggressively; re-fetch only on a freshness miss.
4. On `FAILED` with "Call limit exceeded", on HTTP 429, or on any challenge response: exponential backoff, then stop. Never retry through a block, never route around one.
5. **Link, never host.** Store identifiers, tags, ratings, verdicts, timestamps, language — facts. Never store or serve Codeforces problem statements or editorials. Every problem reference in any Codrona surface deep-links to codeforces.com.
6. Per-user data is fetched only for handles a user has connected themselves. Public problemset metadata is fetched globally.
7. Bulk collection runs `user.ratedList` then paginated `user.status`, resumable, checkpointed. Expect 11-12 hours unattended at the documented limit.

**Note on source code.** The API returns submission metadata only; it does not return
submitted source. Codrona therefore holds and redistributes no Codeforces user code,
which is consistent with the Your Content clause vesting those rights elsewhere.

**Restrictions clause — two live consequences.** The Terms expressly restrict selling,
sublicensing or otherwise commercialising any Website material, and separately
restrict using the Website for advertising or marketing.

- **Before any paid surface ships:** a paid tier built on Codeforces-derived output is not clearly covered by the reading above. Either obtain written permission from CODEFORCES GLOBAL - FZCO, or exclude Codeforces-derived output from the paid surface. This blocks the commercial milestone, not ingestion.
- **At launch:** announcement and marketing material may not be posted to Codeforces. Publish elsewhere and link inward.

**Re-verification.** Codeforces may revise these Terms at any time without notice.
Re-read before each release-train milestone and on the standing re-verification
cadence.

*Not legal advice.*

---

### AtCoder archive (kenkoooo) — VERIFIED, DO NOT INGEST

| Field | Value |
|---|---|
| Author | kenkoooo (community project); data originating from AtCoder Inc. |
| Repo licence | MIT — **covers the project's code only** |
| Repo URL | https://github.com/kenkoooo/AtCoderProblems |
| Data licence | **None stated.** `doc/api.md` declares no licence for the API or datasets. |
| API docs | https://github.com/kenkoooo/AtCoderProblems/blob/master/doc/api.md |
| Bulk dataset | `https://s3-ap-northeast-1.amazonaws.com/kenkoooo/submissions.csv.gz`, refreshed weekly |
| Rate limit | Sleep more than 1 second between accesses (project's own instruction, binding) |
| Upstream rights holder | AtCoder Inc. — Terms at https://atcoder.jp/tos, revised 2026-06-29 |
| Governing law (upstream) | Japan; Tokyo District Court |
| Read date | 2026-08-04 |
| Read by | Ayush Gupta |
| Disposition | **Do not ingest the bulk dataset.** Per-user reads permitted under the narrow conditions below. |

**MIT covers the code, not the data.** The repository carries an MIT licence for the
AtCoder Problems application. The API documentation states no licence for the data served
or the datasets published. Under this file's rule, "no licence found" is a valid verified
state, and it means do not ingest.

**AtCoder changed the underlying position on 2026-06-29, and this is now the decisive
fact.** AtCoder revised its Terms of Use to permit providing third parties such as AI
developers with answer data, log data and metadata as machine-learning training material,
free of charge or for a fee, with user consent. From August 2026 AtCoder licenses
user-submitted source code to AI companies commercially, covering past submissions as well
as new ones. Users were given global and per-submission opt-out settings and a one-month
grace period that closed at the end of July 2026.

Three consequences follow, in increasing order of seriousness.

The republisher does not hold the rights. Same structure as the declined Codeforces bulk
release: a grant made by a party who collected the data rather than owning it.

Taking a free third-party copy of data the rights holder now sells commercially is the
weakest posture available to us, and it is not improved by the copy predating the sale.

**The dataset carries no opt-out signal, and cannot.** It was assembled before the
mechanism existed and has no field to express it. Training on it would necessarily include
submissions from users who have since formally refused AI-training use. That is not a
licensing technicality — it overrides an expressed preference, and no reading of any
licence makes it acceptable. This alone is dispositive.

**No self-collection escape hatch exists.** AtCoder publishes no official public API, so
the route that resolved the Codeforces row is unavailable, and scraping is barred by the
no-circumvention rule regardless of framing.

**Permitted narrow use — per-user reads, on the user's own request.** Fetching a single
connected handle's public submission list through `atcoder-api/v3/user/submissions` is a
different act from bulk corpus building: it is user-initiated, user-scoped, and does not
assemble a training corpus. Conditions: only for a handle the user has connected
themselves; minimum 1000 ms between calls per the project's own instruction; results are
profile data, never training data; treated as cold-path and best-effort, since an
unofficial service may change or disappear without notice. If AtCoder or kenkoooo object,
the adapter is removed rather than worked around.

**Replacement path — Aizu Online Judge.** The cross-judge property this source would
have provided is met instead by AOJ, which publishes an official documented API and is
preparing source-code archives. CodeNet already supplies person-level Aizu and AtCoder
history under CDLA-Permissive-2.0. AtCoder therefore remains present in the corpus through
2021 and Aizu extends to the present. AOJ requires its own verified row in this file,
including the contact request its documentation asks of developers, before any adapter
reads it.

**What is actually lost.** Post-2021 AtCoder submission histories, and the live AtCoder
profile connection. The corpus headline is unaffected: this source was never counted
toward it.

**Re-open condition.** If AtCoder offers a metadata licensing tier and Codrona has revenue
to buy it, this row is revisited through that official channel. Pricing is not published;
the only route is their contact form. Never through a third-party mirror.

*Not legal advice.*

---

### DeepMind CodeContests — VERIFIED (partitioned)

| Field | Value |
|---|---|
| Author | Google DeepMind |
| Code licence | Apache-2.0 |
| Non-code licence | CC BY 4.0 |
| Licence URL | https://github.com/google-deepmind/code_contests/blob/main/LICENSE |
| Source URL | https://github.com/google-deepmind/code_contests |
| Data location | https://huggingface.co/datasets/deepmind/code_contests — DeepMind's own organisation, native Parquet. The `gs://dm-code_contests` Riegeli release is the same data under the same licence from the same rights holder; the HuggingFace channel was taken because the stack already reads Parquet and it adds no new toolchain. The test is authority, not convenience: this is the rights holder's own account, not a third-party mirror. |
| Pinned revision | `802411c3010cb00d1b05bad57ca77365a3c699d6` — recorded in the on-disk filename, in a column on every row, and in a test. |
| Repo state | **Archived 2024-12-06, read-only.** Data remains downloadable. |
| Scale | 13,610 problems across five judges, with tests and human solutions |
| Read date | 2026-08-04 |
| Read by | Ayush Gupta |
| Commercial use | Permitted by DeepMind's own licences |
| Share-alike | No |
| Attribution | DeepMind CC BY 4.0 credit plus the AlphaCode citation (Li et al., Science 378:6624) in [`ATTRIBUTION.md`](https://github.com/codronahq/core/blob/main/ATTRIBUTION.md) and the observatory footer |
| Disposition | **Ingest CodeNet-sourced problems only** (Aizu, AtCoder). All other sources excluded. |
| Ingested | 2026-08-11 — statements and problem metadata for the CodeNet-sourced partition only. Test cases and human solutions stay upstream at the pinned revision until a phase reads them. |

**The licences are not uniform across the dataset, and the row turns on that.** DeepMind
licenses its own contribution — the compilation, structure, and generated test cases
— under Apache-2.0 for code and CC BY 4.0 for everything else. The problems themselves
come from five judges through three upstream chains, and DeepMind states plainly that use
of third-party material may be governed by separate terms and that they make no
representations about rights to use any of it. A CC BY 4.0 grant over a redistributed work
covers the compilation, not the upstream rights.

**Partition, by the `source` field on each `ContestProblem`.** The repository ships
`print_names_and_sources` precisely because this field is queryable, so the filter is a
first-class operation and not a heuristic.

| Upstream | Judges | Stated licence | Decision |
|---|---|---|---|
| CodeNet | Aizu, AtCoder | CDLA-Permissive-2.0 (see the CodeNet row above) | **Ingest** |
| Codeforces (direct) | Codeforces | None stated | **Exclude** |
| description2code | CodeChef, HackerEarth, some Codeforces | MIT, copyright unspecified | **Exclude** |

**The `source` enum was measured, not read from the proto.** Every value was counted across the whole dataset before the filter was written, because the enum recalled from memory put AtCoder and Aizu on the wrong integers. The count also produced a property that settles the partition without trusting the enum at all: sources 5 (AtCoder) and 6 (Aizu) carry a CodeNet `p#####` problem id on 100% of rows, while sources 1, 2 and 3 carry one on 0%. A licence boundary this file depends on is therefore objectively checkable rather than asserted.

**Why Codeforces material is excluded here.** The Codeforces API row commits Codrona to
link-never-host for Codeforces statements, and records that Codrona holds and redistributes
no Codeforces user source code. That commitment does not depend on which party we obtain
the material from. Ingesting Codeforces-sourced problems or solutions through this dataset
would falsify a commitment made elsewhere in this same file.

**Why description2code material is excluded.** Not a licence failure — an absence of
purpose. Codrona integrates Codeforces, LeetCode and AtCoder; no adapter, profile, ladder
or readiness mapping consumes CodeChef or HackerEarth content. The CodeChef material cannot
serve the India observatory, which requires user and submission data this dataset does not
carry. The HackerEarth material cannot serve OA readiness, which derives from assessment
shapes rather than a public contest archive, and the underlying scrape is roughly 2016-era.
Ingesting unused data on the longest provenance chain in this file is exposure without
benefit.

**Note on DeepMind's CodeNet attribution.** Their README records CodeNet as Apache-2.0.
That is the tooling licence; the dataset is CDLA-Permissive-2.0. Codrona relies on its own
verified CodeNet row, not on this restatement. The distinction matters because CodeNet's
licence is the sole basis on which the ingested partition rests.

**What the partition provides.** Statements, paired test cases, and both correct and
incorrect human solutions for Aizu and AtCoder problems under a licence verified at source.
This supplies content-based problem features for the cold-start gate on unseen problems,
and gives the execution sandbox real test cases for problems with no live judge
integration.

**Archived-upstream posture.** The repository is read-only and will receive no corrections.
Snapshot at ingest, record the download date, and treat the corpus as frozen. Absence of an
AtCoder problem here is expected, not a data-quality failure.

**Re-open condition.** If a CodeChef or HackerEarth adapter is ever built, or the Aptitude
Pack requires broader statement diversity, the description2code partition may be revisited
— with a stated purpose recorded here, never silently.

*Not legal advice.*

---

### zerotrac problem ratings — VERIFIED

| Field | Value |
|---|---|
| Author | Shuxin Chen (`zerotrac`) |
| Licence | MIT |
| Licence URL | https://github.com/zerotrac/leetcode_problem_rating/blob/main/LICENSE |
| Source URL | https://github.com/zerotrac/leetcode_problem_rating |
| Data files | `ratings.txt` (raw, rating-descending), `data.json` (structured) |
| Repo state | Active — last push 2026-08-01, not archived |
| Pinned revision | `881a239306ce7a339e32e7825cdb9c00fead00f1` — upstream state of 2026-08-01, recorded in the on-disk filenames, in a column on every row, and in a test asserting the record count. |
| Read date | 2026-08-04 |
| Read by | Ayush Gupta |
| Commercial use | Permitted |
| Share-alike | No |
| Obligations | Retain the copyright notice and permission text |
| Attribution | `Copyright (c) 2021 Shuxin Chen` in [`ATTRIBUTION.md`](https://github.com/codronahq/core/blob/main/ATTRIBUTION.md), the observatory footer, and anywhere a LeetCode difficulty estimate is displayed |
| Role | LeetCode problem-difficulty mapping. **Not corpus** — contributes zero rows to the submission count. |
| Disposition | Ingestion permitted under the conditions below |
| Ingested | 2026-08-11 — `ratings.txt` and `data.json` at the pinned revision, together with the upstream `LICENSE` file, so the copyright notice this row obliges us to retain travels with the snapshot. |

**Why this clears where the Codeforces bulk release did not.** The ratings are not
republished platform records. They are the author's own estimates, computed with an
Elo system and maximum likelihood estimation over contest participant statistics.
That is his work product and his to license. The README states the collection backend
was deliberately withheld from publication so as not to violate any potential terms;
the consequence for us is favourable — the component carrying terms exposure was
never distributed, so consuming this repository involves no collection by Codrona and
no code we could inadvertently run.

**Accuracy is a labelling obligation, not a footnote.** The author states the result is
not fully accurate and is intended for relative difficulty only. Under the honesty
protocol these values must never be rendered as authoritative LeetCode difficulty.
Every surface that displays one labels it as a community estimate, and the model treats
it as a feature with uncertainty rather than ground truth.

**Coverage gap.** Weekly contests 1-62 are excluded — the contest APIs differed at
the time. Those problems carry no zerotrac rating. The pipeline falls back to Codrona's
own IRT estimate rather than emitting a null, and the gap is expected, not a
data-quality failure.

**Freshness and dependency posture.** Updated weekly after contests by a single
maintainer. Treated as cold-path enrichment only, never hot path. Snapshot the file at
ingest and pin the commit SHA so a rewritten upstream cannot silently change historical
ratings. Consistent with the rule that no external platform is load-bearing.

*Not legal advice.*

---

## 2. User-supplied data

| Source | Basis | Notes |
|---|---|---|
| Connected judge handles | User consent at connect time | Public profile data only |
| LeetCode session token (L2) | User consent, local-first | **Never transmitted to Codrona servers.** Stored on device. This is a licensing *and* a security commitment. |
| Browser extension capture (L3) | User consent | Client-side only |
| Manual import (L4) | User-initiated | — |
| First-party telemetry | Privacy policy | Attempts, runs, duels, reviews |

---

## 3. Standing obligations

1. **Attribution.** Every source requiring credit appears in [`ATTRIBUTION.md`](https://github.com/codronahq/core/blob/main/ATTRIBUTION.md),
   the observatory footer, and any published dataset derived from it.
2. **No circumvention.** Official APIs and published datasets only. No proxies, no
   stealth automation, no challenge solving, no scraping through bot protection —
   regardless of how a task is framed. A 403 is an answer, not an obstacle.
3. **Rate limits are code.** Every adapter enforces its source's limit
   programmatically. A limit honoured by convention is a limit that will be broken.
4. **Identifiers are not a loophole.** Using only problem IDs as join keys does not
   waive attribution for the corpus they came from.
5. **Re-verification.** Every row is re-read before each public release. Licences
   change; a read date more than six months old is stale.
6. **Redistribution.** Publishing any derived corpus (Kaggle, Hugging Face) requires
   a fresh check that every input licence permits redistribution. Permission to use
   is not permission to republish.

---

## 4. Verification log

| Date | Source | Action | By |
|---|---|---|---|
| 2026-08-03 | IBM CodeNet | Licence verified — CDLA-Permissive-2.0 | Ayush |
| 2026-08-04 | Codeforces API | Terms and API docs read at source — VERIFIED; rate limit corrected to 1 req / 2s | Ayush |
| 2026-08-04 | Codeforces end-2024 bulk release (denk) | CC BY 4.0 read at source — CONSIDERED, DECLINED; reproducible via official API | Ayush |
| 2026-08-04 | zerotrac problem ratings | MIT LICENSE read at source — VERIFIED | Ayush |
| 2026-08-04 | DeepMind CodeContests | Licences read at source — VERIFIED, partitioned; CodeNet-sourced problems only | Ayush |
| 2026-08-04 | AtCoder archive (kenkoooo) | Repo MIT covers code only; no data licence. AtCoder ToS revised 2026-06-29 — VERIFIED, DO NOT INGEST | Ayush |
| 2026-08-05 | Aizu Online Judge | No licence stated on the developer site; permission enquiry sent to the University of Aizu — PENDING | Ayush |
| 2026-08-06 | Codeforces API | Bulk collection started over the active rated cohort at 1 req / 2 s | Ayush |
| 2026-08-09 | Codeforces API | Collection complete — INGESTED; verdict-level metadata only, no source code | Ayush |
| 2026-08-10 | IBM CodeNet | Archive downloaded and integrity-verified — INGESTED; metadata layer only | Ayush |
| 2026-08-11 | zerotrac problem ratings | Snapshotted at pinned revision `881a2393` — INGESTED | Ayush |
| 2026-08-11 | DeepMind CodeContests | CodeNet-sourced partition taken from DeepMind's own HuggingFace dataset at pinned revision `802411c3` — INGESTED | Ayush |
