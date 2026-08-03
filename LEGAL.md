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

### Codeforces open dataset (end-2024 release) — VERIFY

| Field | Value |
|---|---|
| Author | Codeforces (Mike Mirzayanov) |
| Licence | **VERIFY** at the announcing blog entry |
| Source URL | **VERIFY** — locate the official Codeforces blog release post |
| Scale | ~17.6M submission records |
| Read date | — |
| Commercial use | Unknown |
| Share-alike | Unknown |

**Blocking check.** This is the largest single source after CodeNet and the one
with the least formal licensing. If no explicit licence is stated, treat it as
all-rights-reserved and fall back to the official API under its own terms. Record
the outcome here either way; "no licence found" is a valid verified state and it
means **do not ingest**.

---

### Codeforces API — VERIFY

| Field | Value |
|---|---|
| Author | Codeforces |
| Terms URL | https://codeforces.com/apiHelp |
| Rate limit | ~5 requests/second (hard) |
| Scale | ~8,000+ problems, live |
| Read date | — |
| Role | Primary live integration |

**Operating rules.** One request per 200 ms minimum, enforced in code, not by
convention. Responses cached aggressively; re-fetch only on a freshness miss.
Descriptive `User-Agent` identifying Codrona with a contact URL. On HTTP 429 or any
challenge response, back off exponentially and stop — never retry through a block,
never route around one.

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

### zerotrac problem ratings — VERIFY

| Field | Value |
|---|---|
| Author | zerotrac |
| Licence | **VERIFY** |
| Source URL | **VERIFY** — locate the canonical repository |
| Role | LeetCode problem difficulty mapping |
| Read date | — |

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
