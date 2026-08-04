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
| Commercial use | Permitted |
| Share-alike | No |
| Obligations | Include the agreement text when redistributing the data |
| Attribution | Required in `docs/ATTRIBUTION.md` and the observatory footer |

**Notes.** CDLA-Permissive-2.0 was written for exactly this case and imposes no
copyleft on models trained from the data. Submissions were contributed to online
judges by their authors; IBM states the corpus was cleared for public disclosure.
Derived artefacts (features, fitted parameters) are not encumbered.

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

### AtCoder archive (kenkoooo) — VERIFY

| Field | Value |
|---|---|
| Author | kenkoooo (community project), data originating from AtCoder |
| Licence | **VERIFY** — the API repo licence and AtCoder's own terms are separate questions |
| Source URL | https://github.com/kenkoooo/AtCoderProblems |
| Read date | — |

**Blocking check.** Two licences apply here and they are independent: the community
tool's own licence, and AtCoder's terms governing the underlying submission data.
Verify both. Rate limits published by the project are binding.

---

### DeepMind CodeContests — VERIFY

| Field | Value |
|---|---|
| Author | Google DeepMind |
| Licence | **VERIFY** — check both the dataset card and the repo; these have differed |
| Source URL | https://github.com/google-deepmind/code_contests |
| Scale | 13,610 problems, multi-judge, labelled |
| Read date | — |

**Blocking check.** Confirm whether any component carries a non-commercial or
research-only restriction. A NC clause anywhere in this corpus excludes it from
Codrona entirely given §13 commercial intent — it cannot be quarantined to
"research only" use inside a product that may be sold.

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
| Read date | 2026-08-04 |
| Read by | Ayush Gupta |
| Commercial use | Permitted |
| Share-alike | No |
| Obligations | Retain the copyright notice and permission text |
| Attribution | `Copyright (c) 2021 Shuxin Chen` in `docs/ATTRIBUTION.md`, the observatory footer, and anywhere a LeetCode difficulty estimate is displayed |
| Role | LeetCode problem-difficulty mapping. **Not corpus** — contributes zero rows to the submission count. |
| Disposition | Ingestion permitted under the conditions below |

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

1. **Attribution.** Every source requiring credit appears in `docs/ATTRIBUTION.md`,
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
