# Architecture overview

Five layers. Data rises, actions descend, telemetry closes the loop.

```
        ┌──────────────────────────────────────────────┐
        │  CLIENTS   web PWA · Tauri desktop · Expo     │
        │            mobile · Go CLI · VS Code ext      │
        └───────┬──────────────────────────▲───────────┘
                │ code runs, attempts      │ predictions, plans
        ┌───────▼──────────────────────────┴───────────┐
        │  MIND      skill model · recommender ·        │
        │            agents · review queue              │
        └───────┬──────────────────────────▲───────────┘
                │                          │ features, training data
        ┌───────▼──────────────────────────┴───────────┐
        │  GRID      API · queue · sandboxed judges ·   │
        │            autoscaling · observability        │
        └───────┬──────────────────────────────────────┘
                │ verdicts, telemetry, COSTS
        ┌───────▼──────────────────────────────────────┐
        │  LENS      lake · warehouse · observatory ·   │
        │            product analytics                  │
        └───────▲──────────────────────────────────────┘
                │
        ┌───────┴──────────────────────────────────────┐
        │  SOURCES   CodeNet · Codeforces · AtCoder ·   │
        │            CodeContests · first-party         │
        └──────────────────────────────────────────────┘
```

## The flywheel

Every solve, duel, and review returns to Lens as training signal, so the models
improve with use. Grid's own operating costs land in Lens as an analytics dataset,
which is what makes the cost-per-judged-run dashboard possible.

Each layer is load-bearing. Remove Lens and the models have no data; remove Grid and
the coach cannot run code; remove Mind and the product is another problem tracker.

## Repository map

| Repo | Contents | Licence |
|---|---|---|
| `mind` | Skill models, recommender, agents, eval harness | AGPL-3.0 |
| `grid` | Judge service, Terraform, k8s, observability | AGPL-3.0 |
| `lens` | Ingestion, dbt project, dashboards | AGPL-3.0 |
| `core` | API, web, desktop, mobile, SDKs, CLI (Turborepo) | AGPL-3.0, MIT per package |
| `docs` | This repository | CC-BY-4.0 |
| `private` | Weights, golden eval set, premium connectors | Not distributed |
| `.github` | Org profile, shared workflows, templates | MIT |

## Sustainability tiers

| Tier | Contents | Guarantee |
|---|---|---|
| 0 — immortal | Local-first apps, bundled ONNX, on-device SQLite, static hosting | Works offline, costs nothing, never sleeps |
| 1 — free-forever | Sync, leaderboards, observatory on Cloudflare Workers + D1/KV; LLM via user's own key | Independent of the maintainer's wallet |
| 2 — credits | AKS, EKS, EMR, Grafana Cloud — for the build and the demos | Teardown is `terraform destroy`; the same stack boots on a laptop |

**The critical path never touches anything that can pause.** Any component that
sleeps on inactivity is disqualified from the hot path, regardless of how convenient
it is.
