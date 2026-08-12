# Roadmap

Eight phases. Every phase ends with something real.

**Done means two things:** the box is ticked **and** the gate in
`quality/eval-gates.md` is passing. A ticked box with a failing gate is not done.

Progress: **Phase 0 in progress.**

---

## Phase 0 — Foundation (week 1)

- [x] Organisation and seven repositories created
- [x] ADR-0001 committed (licensing and open-core)
- [x] `LEGAL.md` committed; CodeNet verified; remaining sources marked VERIFY
- [x] CLA Assistant configured and proven with a real pull request
- [x] Turborepo + pnpm workspace in `core`
- [x] `@codrona/design-tokens` with the rating ladder
- [x] ADR and RFC templates, CODEOWNERS, issue and PR templates
- [x] CI on every repo that has something to check: lint, type-check and tests in `core`, `mind` and `lens`; repository hygiene (YAML validity, internal link resolution) in `grid`, `docs` and `.github`. `private` runs no workflow by design — it holds weights and the golden eval set, not code.
- [x] Branch protection and conventional commits
- [x] `docs` published with architecture, warehouse, ingestion, eval gates
- [x] Organisation profile README

## Phase 1 — Data spine (weeks 2–3)

- [ ] Adapter interface and verdict mapping table
- [ ] CodeNet adapter — metadata ingest
- [ ] Codeforces adapter — API, token-bucket rate limiting, resumable cursor
- [ ] AtCoder adapter (blocked on LEGAL verification)
- [ ] Lake layout: raw → staged, idempotent partition replacement
- [ ] PySpark normalisation to canonical schema
- [ ] dbt project: staging, intermediate, marts
- [ ] SCD-2 snapshots on `dim_problem` and `dim_user`
- [ ] Custom tests: validity overlap, single-current, as-of correctness
- [ ] Airflow DAGs — crawl, stage, dbt, publish
- [ ] Databricks EDA notebook over the full corpus
- [ ] 5M sample → 30M full cutover, with the quality report
- [ ] G8 enforced in CI
- [ ] First observatory charts

## Phase 2 — The science (weeks 4–6)

- [ ] IRT 2PL over the corpus
- [ ] Per-topic Elo
- [ ] GBM stack on top of IRT and Elo features
- [ ] Survival model for time-to-solve, censored attempts included
- [ ] Calibration report: Brier, ECE, reliability curves
- [ ] Difficulty and tag drift analysis
- [ ] Contextual bandit recommender
- [ ] Placement test design
- [ ] G1, G2, G3 ratified against baselines and enforced
- [ ] Calibration writeup published

## Phase 3 — The grid (weeks 7–9)

- [ ] Judge service, Judge0 CE core
- [ ] nsjail/gVisor hardened sandboxes
- [ ] Queue: Redis plus Redpanda
- [ ] KEDA on queue depth, HPA on the API
- [ ] AKS: API and judge plane; EKS: data and ML plane
- [ ] Terraform, values-driven, no cloud hard-coding
- [ ] Azure DevOps pipeline for one service
- [ ] Key Vault via External Secrets Operator
- [ ] OpenTelemetry end-to-end traces to Grafana Cloud
- [ ] Multi-burn-rate SLOs and alerting
- [ ] k6 spike tests as a CI gate; G7 enforced
- [ ] infracost in CI; cost exports into Lens
- [ ] Trivy, non-root, read-only containers
- [ ] `MIGRATION.md` and laptop teardown proven

## Phase 4 — The coach (weeks 10–12)

- [ ] LangGraph agents: Coach, Post-mortem, Contest Scout
- [ ] Tool layer: profile, predict, run, similar, editorial, schedule
- [ ] pgvector in production, FAISS for offline eval
- [ ] FSRS × IRT review queue
- [ ] Integrity mode with contest-clock checking
- [ ] Leak classifier; G4 enforced
- [ ] Red-team suite, 200+ cases; G5 enforced
- [ ] Dogfooding begins

## Phase 5 — Core and launch, v1.0 (weeks 13–16)

- [ ] OAuth2, JWT rotation, TOTP 2FA
- [ ] Versioned REST API, OpenAPI, per-key rate limiting
- [ ] Hybrid search: OpenSearch plus pgvector
- [ ] Public profiles and dynamic OG share cards
- [ ] Weekly report-card emails
- [ ] Observatory published
- [ ] GA4 and PostHog, verified at the provider
- [ ] Live A/B: bandit vs ladder order, with CUPED
- [ ] Postgres performance documented, before and after
- [ ] Status page live
- [ ] **Rename `codronahq` → `codrona` and sweep every surface**
- [ ] Public launch

## Phase 6 — Arena, v1.5 (weeks 17–20)

- [ ] 1v1 duels, IRT-matched, WebSockets, Redis pub/sub
- [ ] Reconnection and race-condition handling
- [ ] Sorted-set leaderboards, cursor pagination
- [ ] Rope Squads: shared goals, presence, streaks
- [ ] Virtual contests with ghost leaderboards
- [ ] Event-driven contest debrief
- [ ] Signed webhooks: retries, DLQ, outbox, idempotency keys
- [ ] SDKs published: npm, PyPI, Maven Central
- [ ] Spring Boot notification service, Java 21 virtual threads
- [ ] gRPC judge orchestrator; GraphQL BFF with dataloader
- [ ] VS Code extension

## Phase 7 — Apps and institutions, v2.0+ (weeks 21–24)

- [ ] Tauri v2 desktop, optional local sandbox
- [ ] Expo mobile
- [ ] Go CLI
- [ ] Bundled ONNX, on-device SQLite, offline operation
- [ ] WebAssembly sample testing via Pyodide
- [ ] College multi-tenant: orgs, invites, RBAC
- [ ] OA-readiness dashboards
- [ ] Aptitude pack: quantitative, logical, verbal
- [ ] Stripe test-mode supporter tier

---

## Release train

`v0.1` data and models → `v0.5` grid and agents → `v1.0` public launch →
`v1.5` arena and aptitude → `v2.0+` apps and institutions.
