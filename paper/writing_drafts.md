# Writing drafts (working record; never ships)

Kept under the *DRAFTS FILE* ruling (`docs/decision_log.md`, 2026-10-06).
The owner drafts in the chat; each draft is appended here **verbatim** in
the same turn, with the date, the step, and the builder's open check
findings beside it, labelled as the builder's. Entries are appended, never
edited. A section the owner calls done is copied from here into
`paper/finale.md`.

---

## 2026-10-10 · Title · draft 1

Owner's draft, verbatim:

```text
A Multi-Agent Environment with Causally Coupled Hazards and a Pre-Registered Test of Joint versus Isolated Training
```

**Builder's check findings (the builder's, not the owner's text; open):**

1. **Conflict, misreading risk: "Joint versus Isolated Training" has no
   object.** After "Multi-Agent", the default MARL reading is joint vs
   independent *learners*. The study holds that fixed: every arm is the same
   shared-parameter IPPO (ENV-11). What varies is which elements share a
   training episode (D2; DES-7). The second reading, from "Hazards", is
   joint vs isolated *hazards*, but the fire burns in every episode (D1); the
   composed elements are Coupling A, Coupling B and comms denial.
2. **Conflict with the record's terms, minor: "Causally Coupled Hazards".**
   Def. 2's "the hazard" is the fire (h) alone. Collapse is lethal
   (`deaths_collapse`, `che/env/env.py:183`) but is the structure state c.
   Coupling A links collapse to fire; Coupling B links the fire's smoke to
   perception, not to another hazard; comms denial is independent. The plural
   holds only if the paper defines "hazards" as fire and collapse, and then
   "coupled" names Coupling A only.
3. **Undersell (suggestion): Def. 2 is absent.** The record names the
   hazard-outside-reward-and-cost property as what separates the setting
   from CMDP/safe RL and JaxWildfire (`docs/theory_foundations.md`, Def. 2).
   Without it, "hazards" takes the field's default reading. Acceptable if
   `description` or the abstract carries it.
4. **"Pre-Registered": supported at this level.** The JOINT-vs-ISO test is
   the confirmatory Γ, registered 2026-08-13, pre-grid (DES-12). Binds
   elsewhere: the body states the registration's form (committed documents;
   no external registry found in the repository) and its deviations,
   k 40 → 46 → 72 (DES-1 to DES-3) and ISO-4 added mid-grid outside the
   family (DES-15).
5. **Passes.** Missing: none (no result claimed, so the inert-share
   qualifier and the Γ(t) suffix do not bind the title). Numbers: none.
   Mechanics: one line, no `"`, `$`, `{{` or `{%`; names no environment,
   so repository visibility does not bite the title. No "swarm", PBT or
   "adversary". Typos and grammar: none; title case consistent.

Open items: "swarm" is settled for the title if this wording stands;
"ambient" is still unratified (not used here; it bites at the abstract);
repository visibility still unanswered (it bites wherever the name appears).

## 2026-10-10 · Title · owner's answer (not a draft)

Repository visibility, asked under draft 1: "the repo will go private"
(decision log, REPO VISIBILITY). Draft 1's open item on visibility is
**resolved**; naming the environment stays the owner's choice wherever the
name could appear.
