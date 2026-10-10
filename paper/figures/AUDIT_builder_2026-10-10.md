# Builder's audit of the figure agents' outputs (2026-10-10)

Held for the owner's batched decisions (owner: "bring me the decisions after
all the agents are done").

## Restyled GIFs (`paper/renders/2026-10-10/`)

- Independent check: re-running `che.scripts.render_episode` for the
  random-policy episode reproduced the committed 2026-09-27 GIF byte for byte
  (sha256 ef64f923…b7ad). The agent's per-frame digest chains match for all
  three episodes (`provenance/identity_check.json`).
- Metadata clean (GIF: graphic-control + NETSCAPE2.0 only; PNG:
  IHDR/PLTE/IDAT/IEND); no identifying strings.
- Reading rule added by the agent: random and JOINT share fire and structure
  for all 257 frames; ISO diverges at t = 16 through a load-triggered
  collapse (no ledger row yet).

## Slot figures (`paper/figures/`)

- No identifying strings; the only URL in the HTML is the SVG namespace.
- **Fig 8: "REJECT" on B̂ is not a recorded verdict** (UNBLIND RESULT gives
  only the estimate, z and CI; no test is registered for B̂). Verdict words
  are recorded for Γ (k = 72 and the k = 60 prefix), Γ₄, Γ₄′ and Γ_H.
  Passed to the Opus agent.
- Inconsistencies the agent reported, checked:
  1. METH-1: confirmed, the floor pair also differs in config (R_comm).
     Ledger note updated.
  2. CB-5: confirmed, "pooled 1.41×" is the 2-seed estimate over the floor;
     the three-replicate mean gives ≈ 1.19×. Ledger note updated.
  3. T_X: confirmed, `env.py` agent_step reads `hazard_new` and
     `structure_new` (h′, c′); Def. 1 and CLAUDE.md invariant #2 write
     T_X(x, a, h, c). Joins the theory-doc ρ amendment as a §3 item.
  4. `j_pinned` vs "J_denied" naming in the phase-5 report: §7 item.
- Mechanism B GIF: agent 0 never sees fire, so it does not show Coupling B;
  the agent's option is to show all 12 agents' crops (no choice from a set).
- NEEDS LEDGER ROW list: `paper/figures/MANIFEST.md`; rows are added for the
  figures the owner keeps.

## Correction to the Fig 8 note above (builder, same day)

B̂'s "REJECT" **is** in a committed artifact: the post-unblind instrument's
table prints a decision for B̂ at z_α (`post_gamma4_t2000.md:16`, JSON
`reject: true`). What is true is narrower: no test was registered for B̂
(§7 PROPOSALS RULING: "Γ and Γ₄ are reported side by side … with B̂ and its
CI"; "no magnitude threshold on B̂"), and the decision log records no verdict
word for it. Showing the instrument's label is an owner's choice.

## Interactive set (`paper/figures/interactive/`)

- 10 HTML figures (18–175 KB) + static companions; no identifying strings;
  the only URL is the SVG namespace. Selection rules written before rendering
  (DESIGN §6), deterministic (the explorer's default agent: lowest-index
  alive agent at t = 128 with an unseen cell).
- Ladder: verdict chips only where recorded; B̂ shows estimate and CI; k = 60
  flagged UNDERPOWERED; cross-unit marks; the deviation footnote. Correct.
- Composer: correct values (DES-7, DES-8, DES-14). **Defect: its subtitle
  says "as certified: δ inert …"**; the checklist bars "certified".
- Γ(t): registered string first; no joining line. **Minor: the Šidák
  intervals at t ≠ 1000 are descriptive (no registered test there) and the
  figure does not say so.**
- Explorer static: observation vs state vs τ for one agent; clear.
- `branch_B.md` §1 and §8 "±0.7 points" lag: **fixed** (the agent and the
  owner's opening notes both flagged it).
