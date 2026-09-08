# paper/ — outcome-conditional scaffolds for the TMLR submission

Written 2026-09-07, **pre-grid and pre-unblind**. No Phase-6 outcome mean
exists and none appears in these files. Every number quoted here is a
committed pre-grid measurement with its source; every grid quantity is a
`⟨placeholder⟩`.

## How to use this directory

1. **Write `00_common_spine.md` now**, before or during the grid. It is
   roughly 80 % of the paper and none of it depends on Γ.
2. **After unblinding**, read the confirmatory report, find the row of the
   registered branch table you landed in, and open the matching file:

   | completion | survival | file |
   |---|---|---|
   | reject | reject | `branch_A.md` |
   | fail to reject | reject, AND falsifier passes | `branch_B.md` |
   | fail to reject | fail to reject | `branch_C.md` |
   | fail to reject | reject, falsifier FAILS | `branch_C.md` (with the asymmetry note) |
   | Γ < 0 on either | | `branch_D.md` |

   Then apply the **budget-robustness suffix** from the Γ(t) reading: every
   branch file has a "sign stable" and a "sign unstable" variant, and the
   suffix is not optional (`phase6_framing_branches.md` §4).
3. Splice the branch file's abstract, §8 results, and discussion into the
   spine. Delete the other three branch files from the submission tree; keep
   them in the repo as the pre-registered framing record.
4. Work `99_pre_submission_checklist.md` to zero.

## Rules these files obey, and you should keep

- **Nothing here is a registration.** The registered branches, falsifiers
  and analysis plan live in `phase6_framing_branches.md`,
  `phase6_design_v2.md` and `docs/decision_log.md`. If a sentence here
  conflicts with those, those win.
- **No new threshold, constant or family.** Branch D has no magnitude
  threshold and none may be introduced post-unblind.
- **Every citation marked `[VERIFY]` is a name relayed in chat, never
  confirmed against a real record.** Relays in this project have twice named
  documents that do not exist. Verify each one by hand before it enters
  the `.bib`.
- **TMLR is double-blind.** No repo links, no OSF links, no commit hashes
  that resolve to a named account. Pre-registration is described in-text as
  a dated, hashed artifact "released upon publication".
- **"At matched budget", never "at convergence".** T\* ruling.

## Files

| file | what it is |
|---|---|
| `00_common_spine.md` | the Γ-independent paper: intro, related work, environment, calibration, couplings, comms, methodology, confirmatory design, shared limitations, appendix manifest, figure list |
| `branch_A.md` | both co-primaries positive |
| `branch_B.md` | completion null, survival positive, falsifier passes |
| `branch_C.md` | both null (and the failed-falsifier case) |
| `branch_D.md` | Γ negative on either co-primary |
| `99_pre_submission_checklist.md` | defects found in the 2026-09-07 review plus the standing owed items, as a checklist |
