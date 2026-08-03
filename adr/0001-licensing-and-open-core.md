# ADR-0001: Licensing and open-core boundary

- **Status:** Accepted
- **Date:** 2026-08-03
- **Deciders:** Ayush Gupta
- **Supersedes:** —
- **Superseded by:** —

## Context

Codrona is built as open source and may later be commercialised. Those two facts
pull in opposite directions, and the licence chosen on day one is the hardest
decision to reverse: every contributor who merges code under a licence acquires a
say in whether that licence can ever change.

Three risks shape the decision.

1. **The SaaS loophole.** Under a permissive licence (MIT, Apache-2.0) a
   well-funded competitor may take the codebase, improve it privately, run it as a
   hosted service, and return nothing. Codrona's value is concentrated in a hosted,
   networked product, so this is the realistic attack, not a theoretical one.
2. **Integration friction.** The opposite failure is licensing so aggressively that
   nobody can embed a Codrona client. An SDK under a copyleft licence is an SDK
   nobody imports, which forfeits the ecosystem moat.
3. **The relicensing trap.** Without a Contributor Licence Agreement, copyright in
   merged contributions is held by their authors. Relicensing then requires the
   permission of every past contributor, in perpetuity. This becomes unfixable the
   moment the first external pull request merges.

## Decision

### 1. AGPL-3.0 on the engine and server

`mind` (skill models, coaching engine) and `core` (API and applications) are
licensed **AGPL-3.0-or-later**.

AGPL extends copyleft across the network boundary: anyone who runs a modified
Codrona as a network service must publish their modifications. A fork cannot
privately out-develop the original, and improvements flow back.

`grid` and `lens` also take AGPL-3.0 — both are operational surfaces of the same
service, and a uniform default is simpler to reason about than a per-repo argument.

### 2. MIT on the integration surface

The following are **MIT**, declared per package rather than per repo:

| Package | Repo | Rationale |
|---|---|---|
| `packages/design-tokens` | `core` | Design values must be freely embeddable |
| `packages/sdk-ts` | `core` | Published to npm; copyleft would prevent adoption |
| Python SDK | `mind` | Published to PyPI; same reasoning |
| Go CLI, VS Code extension | `core` | Client-side tools; friction must be zero |

Every MIT package carries its own `LICENSE` file and an SPDX `license` field in its
manifest. The repository-root `LICENSE` is AGPL-3.0 and governs everything not
explicitly carved out.

**Applications are not carved out.** `apps/web`, `apps/desktop`, and `apps/mobile`
stay AGPL. They are the product surface, not an integration surface; MIT there would
hand a competitor the finished interface. "Clients stay permissive" in the master
context means *SDKs and client libraries*, not *the applications themselves*. This
ADR is the authoritative reading of that line.

### 3. Crown jewels stay private

The `private` repository is not licensed for distribution and holds:

- Trained model weights and fitted parameters
- The golden evaluation dataset and its labels
- Premium connector implementations
- Institutional and OA-readiness assets

The training recipe, feature definitions, model architecture, and evaluation
harness are public. The fitted artefacts are not. Anyone can reproduce the method;
nobody inherits the result.

The hosted synchronisation, multiplayer, matchmaking, and institutional backends
are likewise not published. Codrona runs locally for anyone; the live networked
service is the commercial product.

### 4. CLA before the first external contribution

CLA Assistant is configured on the organisation **before any outside pull request
merges**. This is non-negotiable and time-sensitive: it cannot be applied
retroactively to contributions already merged.

### 5. BSL documented as the fallback

If AGPL proves insufficient against commercial free-riding, the Business Source
Licence (source-available, free except for running a competing commercial service,
converting to open source after a fixed term) is the escape hatch. Codrona does not
start there. It is recorded so that the option is a decision rather than a scramble.

## Consequences

**Positive**

- A hosted fork must publish its modifications, so forks cannot privately out-develop.
- The integration surface stays frictionless, protecting the ecosystem moat.
- Dual-licensing and relicensing remain available because contributor copyright is assigned.
- The commercial path is unobstructed at every layer.

**Negative**

- AGPL deters some corporate contributors whose employers prohibit it. Accepted.
- Mixed licensing within `core` demands discipline: every new package declares its
  licence explicitly, and the CI licence check enforces it.
- A CLA adds friction to first-time contributors. Mitigated by CLA Assistant's
  one-click signature flow.

**Neutral**

- AGPL constrains nothing for individual users running Codrona for themselves.

## Compliance notes

- SPDX identifiers: `AGPL-3.0-or-later` and `MIT`.
- Every source file in an AGPL repo carries a short header pointing to the root `LICENSE`.
- Third-party dependency licences are audited in CI; a copyleft dependency inside an
  MIT package fails the build.
- Dataset licensing is tracked separately in `LEGAL.md` and is not governed by this ADR.

*Not legal advice. Obtain professional counsel before commercialisation.*
