# Design language

Dark-first. The rating ladder is the palette. Numbers never move.

## The thesis

Competitive programming already has a colour system its audience reads without
thinking — a red handle means something specific to everyone in the room. Codrona
adopts that system rather than inventing a brand palette on top of it, because the
product's whole subject is the climb through those colours.

The raw Codeforces values are tuned for a white page and fail on a dark surface, so
the ladder uses the Radix step-9 dark scale, which holds each tier's hue identity at
accessible contrast. The scale lands on `#e5484d` at grandmaster — the same crimson
already used as the brand mark. The summit of the climb and the mark are the same
colour. That coincidence is the reason this system was chosen over any alternative.

Source of truth: `core/packages/design-tokens/src/tokens.ts`. Nothing downstream
defines its own colour.

## The ladder

| Tier | Rating | Token |
|---|---|---|
| Newbie | 0–1199 | `rating-newbie` |
| Pupil | 1200–1399 | `rating-pupil` |
| Specialist | 1400–1599 | `rating-specialist` |
| Expert | 1600–1899 | `rating-expert` |
| Candidate Master | 1900–2099 | `rating-candidate-master` |
| Master | 2100–2299 | `rating-master` |
| International Master | 2300–2399 | `rating-international-master` |
| Grandmaster | 2400–2599 | `rating-grandmaster` |
| International Grandmaster | 2600–2999 | `rating-international-grandmaster` |
| Legendary Grandmaster | 3000+ | `rating-legendary-grandmaster`, first character in foreground |

A user's accent colour is their tier. It propagates to the profile, the OG share
card, the duel arena, and the CLI. Levelling up changes the interface, which is the
point.

## What the ladder is not for

Verdicts have their own narrow set. A green "accepted" badge must never be mistaken
for pupil-tier green in a submissions table, so `verdict.*` tokens are separate and
deliberately do not reuse ladder values.

Difficulty tints on problem links use `difficulty.*`, a four-step scale, not the
ten-step ladder — a link colour that encodes ten states encodes none.

## Type

**Archivo** for UI and display. A real grotesque with usable range at heavy display
weights, technical without being cute, and not the interface default that every other
product reaches for.

**JetBrains Mono** for code — and for every number in the interface. Ratings,
timings, memory, leaderboard columns and standings all use tabular figures. A rating
that changes width when it ticks from 1499 to 1500 is a bug, and in a product about
watching a number go up it is the worst possible bug.

## Motion

150–250 ms, spring-weighted (`cubic-bezier(0.22, 1, 0.36, 1)`). One exception:
`duration.climb` at 600 ms, reserved exclusively for a rating increase. Spending the
longest animation in the product on the single moment the product exists to produce
is the whole motion budget, deliberately concentrated.

`prefers-reduced-motion` is honoured everywhere including the climb.

## Voice

Loading states are pulsing code brackets. Empty states invite an action rather than
apologise for emptiness. Errors say what happened and what to do, in the interface's
voice — never a person's, never an apology.

No portfolio framing anywhere a user can see. Codrona is a product.

## Quality floor

Responsive to mobile, visible keyboard focus, reduced motion respected, contrast
verified against the dark surfaces at small sizes. Not announced — just met.

## Cross-surface parity

A colour, label, or metric rendered by the UI is applied to **every** surface in the
same change: web, desktop, mobile, API serialisers, CLI, observatory, status page. A
gap on one surface triggers an audit of all of them.
