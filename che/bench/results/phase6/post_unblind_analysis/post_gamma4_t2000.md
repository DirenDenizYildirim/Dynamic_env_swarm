# Phase-6 POST-UNBLIND analysis

git `60942fc27168e905dc2401b39113857fb1d30a26` (dirty files: 0) · 2026-09-26T17:49:32+00:00 · sections: gamma4, t2000

Šidák m = 2, z_α = 2.2365, as the family. Every interval is CONDITIONAL on its common eval draw (seed 0, 512 episodes). Nothing here decides or relabels a branch.

## Γ₄ = JOINT − ISO-4 and B̂ = ISO-4 − ISO (§7 proposal 1)

| contrast | a | b | Γ = b − a | sd(Γ) | z | decision | Šidák CI | X (MDE80) |
|---|---|---|---|---|---|---|---|---|
| Γ completion (ISO→JOINT) | 0.7772 (k=72) | 0.7600 (k=72) | -0.0173 | 0.01068 | -1.62 | null | [-0.0412, +0.0066] | 0.0329 |
| Γ₄ completion (ISO-4→JOINT) | 0.7726 (k=20) | 0.7600 (k=72) | -0.0126 | 0.01587 | -0.80 | null | [-0.0481, +0.0228] | 0.0488 |
| B̂ completion (ISO→ISO-4) | 0.7772 (k=72) | 0.7726 (k=20) | -0.0046 | 0.01602 | -0.29 | null | [-0.0405, +0.0312] | 0.0493 |
| Γ survival_rate (ISO→JOINT) | 0.9158 (k=72) | 0.9254 (k=72) | +0.0096 | 0.00216 | +4.43 | REJECT | [+0.0047, +0.0144] | 0.0066 |
| Γ₄ survival_rate (ISO-4→JOINT) | 0.9256 (k=20) | 0.9254 (k=72) | -0.0003 | 0.00294 | -0.09 | null | [-0.0068, +0.0063] | 0.0090 |
| B̂ survival_rate (ISO→ISO-4) | 0.9158 (k=72) | 0.9256 (k=20) | +0.0098 | 0.00289 | +3.39 | REJECT | [+0.0033, +0.0163] | 0.0089 |

- **completion: SECOND_EXCLUSION** — Γ and Γ₄ both null: Γ₄ is quoted as a second exclusion bound, X₄ = 0.0488.
- **survival_rate: DOES_NOT_SURVIVE** — Γ rejects but Γ₄'s CI includes 0 or its sign is opposite: the effect DOES NOT SURVIVE the inert-share correction. Stated in the abstract-level summary; the branch label does not change; A/B text may not call it a composition effect without this qualifier.

No magnitude threshold on B̂ is applied, now or later.

## T = 2000 — DESCRIPTIVE ONLY — UNDERPOWERED (§7 ruling proposal 2); graded by no test; enters no branch decision

| metric | ISO | JOINT | Γ(2000) | sd(Γ) | 95 % CI |
|---|---|---|---|---|---|
| completion | 0.9215 | 0.9218 | +0.0003 | 0.0187 | [-0.0363, +0.0369] |
| survival_rate | 0.9281 | 0.9439 | +0.0159 | 0.0082 | [-0.0002, +0.0319] |

Differential training-surface slope JOINT − ISO, per 100 updates (reference at T = 1000: 0.01209):

- completion: (500,1000] +0.00247, (1000,2000] +0.00384
- survival_rate: (500,1000] +0.00718, (1000,2000] +0.00204

May be cited only for whether the T = 1000 differential drift visibly persists, closes or reverses — never that Γ 'holds' or 'vanishes' at T = 2000. Per-arm curves are in the JSON.
