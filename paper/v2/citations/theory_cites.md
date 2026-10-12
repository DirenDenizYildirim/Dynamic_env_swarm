# Support quotes for the three theory citations (review N15)

Builder B2, Paper v2 phase 1, step 3, 2026-10-11. `paper/related_work_verification.md`
verifies `bernstein2002`, `kesten1980` and `grassberger1983` for **identity
only** (its items 6–8). The demonstration uses them for specific claims
(`paper/v2/review_of_demo.md` N15). This file records, for each claim, a
quote from a record retrieved this session, with its location, and says
what the quote supports and what it does not.

**Method.** Each record was downloaded with `curl` into its own new
directory in this session's scratchpad (never the tree) and read there:
the PDFs as text (`pdftotext -layout`), and one page also as an image where
the text layer was garbled. Web search was used only to find where the
files are hosted; no quote below comes from a search snippet or a
summarizer. **These are assistant reads, not the owner's.** The three
`.bib` entries are unchanged by this file. The separate M2 Unicode pass
touched only their `pages`, Bernstein's `{M}arkov` and Kesten's
`$\frac{1}{2}$` (see the dated note at the top of
`related_work_verification.md`).

| key | claim the demo makes (location) | record read | verdict |
|---|---|---|---|
| `bernstein2002` | "finite-horizon Dec-POMDPs are NEXP-complete" (`demo_beyond/sections/03_environment.md:36`, Remark 1) | Crossref abstract; the authors' full text (25 pp.) | **SUPPORTED, with a qualifier**: NEXP-complete as the paper defines the decision problem (horizon T < number of states); NEXP-hard for the finite horizon in general. A worst-case result for the class (C2) |
| `kesten1980` | β_c = 1/2 exactly for bond percolation on ℤ² (`04_severity.md:20`, Cor. 1(1)) | Springer abstract page; Crossref record | **SUPPORTED** at abstract level (the abstract is one sentence pointing to the title); full text not read |
| `grassberger1983` | the burnt region is a bond-percolation cluster because an epidemic with a **constant infectious period** maps to bond percolation (`01_introduction.md:9`, `03_environment.md:115`, `12_appendix.md:19`) | full text (journal scan, 16 pp.) | **SUPPORTED**: §2, p. 159 states exactly this mapping |

---

## 1. `bernstein2002`: NEXP-completeness of the general class

**Records.**

- Crossref, doi:10.1287/moor.27.4.819.297 (`api.crossref.org/works/…`,
  retrieved 2026-10-11), abstract field, verbatim:
  > "We consider decentralized control of Markov decision processes and give
  > complexity bounds on the worst-case running time for algorithms that find
  > optimal solutions. Generalizations of both the fully observable case and
  > the partially observable case that allow for decentralized control are
  > described. For even two agents, the finite-horizon problems corresponding
  > to both of these models are hard for nondeterministic exponential time.
  > These complexity results illustrate a fundamental difference between
  > centralized and decentralized control of Markov decision processes. In
  > contrast to the problems involving centralized control, the problems we
  > consider provably do not admit polynomial-time algorithms. Furthermore,
  > assuming EXP ≠ NEXP, the problems require superexponential time to solve
  > in the worst case."
- Full text: the authors' PDF linked from co-author N. Immerman's
  publications page at the University of Massachusetts (`bgiz.pdf`, 25
  pages, US Letter, a Ghostscript manuscript, not the journal's typeset
  pages 819–840; that page's abstract entry names Mathematics of Operations
  Research 27(4) (2002), 819–840). Its abstract matches Crossref's in
  substance (hyphenation only). Locations below are this PDF's page numbers.
  - p. 2 (Introduction): "We strengthen this result by showing that both the
    DEC-POMDP and DEC-MDP problems are NEXP-hard, even when the horizon is
    limited to be less than the number of states (and they are NEXP-complete
    in the latter case)."
  - pp. 4–5 (the model definitions): "T is a positive integer representing
    the horizon (and T < |S|)."
  - p. 6: "The decision problem is stated as follows: Given a DEC-POMDP D =
    ⟨S, A1, A2, P, R, Ω1, Ω2, O, T, K⟩, is there a joint policy for which
    V_δ^T(s0) equals or exceeds K?" and "Theorem 1 For all m ≥ 2,
    DEC-POMDP_m ∈ NEXP."
  - p. 19: "Theorem 2 DEC-MDP_2 is NEXP-hard." "Corollary 1 For all m ≥ 2,
    both DEC-POMDP_m and DEC-MDP_m are NEXP-complete." §6: "we proved that
    the finite-horizon m-agent DEC-POMDP problem is NEXP-hard for m ≥ 2 and
    the finite-horizon m-agent DEC-MDP problem is also NEXP-hard for m ≥ 2.
    When the horizon is limited to be less than the number of states, the
    problems are NEXP-complete."

**What it supports.** "Finite-horizon Dec-POMDPs are NEXP-complete" is the
paper's Corollary 1, for two or more agents, for the decision problem as
the paper defines it (horizon T < |S|). Without that bound the paper states
NEXP-hardness. The abstract itself says only "hard for nondeterministic
exponential time".

**What it does not support (fix-list C2).** Every statement is about the
worst case over the class ("complexity bounds on the worst-case running
time"). It says nothing about a particular instance such as CHE. So it
licenses "no general exact planner for this class is expected to scale",
not "this hardness applies" to CHE. Writers should also not drop the
"two or more agents, finite horizon" scope.

## 2. `kesten1980`: β_c = 1/2 for bond percolation on ℤ²

**Records.**

- Springer article page (`link.springer.com/article/10.1007/BF01197577`,
  retrieved 2026-10-11): `citation_title` "The critical probability of bond
  percolation on the square lattice equals 1/2"; the Abstract section reads,
  in full: "We prove the statement in the title of the paper."
  `citation_firstpage` 41, `citation_lastpage` 59, date 1980/02.
- Crossref, doi:10.1007/BF01197577: same title, no abstract.
- Corroboration (secondary, not a substitute): Grassberger (1983), p. 165
  (§5): "bond percolation, where the critical percolation probability is
  rigorously known [10] to be pc = 0.5", where [10] is "H. Kesten, Comm.
  Math. Phys. 74:41 (1980)" (p. 172).

**What it supports.** The critical probability of bond percolation on the
square lattice, that is ℤ² with nearest-neighbour (von Neumann) bonds, is
1/2. That is Corollary 1(1)'s "β_c = 1/2 exactly" for the idealized kernel
of Proposition 2.

**Not read.** The paper's full text (Springer paywall). Which of the
equivalent definitions of the critical probability it proves the value for
is therefore not recorded here. Corollary 1(1) needs no more than the
title states. Nothing here concerns the finite 64 × 64 arena, whose
measured threshold is a separate, measured quantity (ledger CAL-1, CAL-4).

## 3. `grassberger1983`: the constant-infectious-period mapping

**Record.** The journal pages (a scan, 16 pages, journal pp. 157–172), as
hosted on a University of Vermont course-reading page
(`pdodds.w3.uvm.edu/files/papers/others/1983/grassberger1983a.pdf`),
retrieved 2026-10-11 and read in full. Page 159 was also read as an image,
because its text layer garbles the formula. Locations are journal pages.
Side note: the first page's running footer prints "63: 151-172", while the
page itself is numbered 157 and the publisher's code reads "02157+16"; the
`.bib` entry's 157–172 follows Crossref and the page numbers.

- Abstract (p. 157): "Scaling laws are formulated for the behavior of a
  space-dependent fluctuating general epidemic process near the critical
  point. Restricted to stationary properties, these laws describe also the
  critical behavior of random percolation. Monte Carlo calculations are used
  to estimate the critical exponents and the universal shape of the
  propagating wave, in the case of 2-dimensional space."
- §2, "The basic model and percolation" (pp. 158–159), the model: sites of
  a d-dimensional cubic lattice, susceptible X, infected Y, immune Z;
  infection of nearest neighbours with rate σ, recovery with rate ρ
  (Eqs. 2.1–2.2), credited to reference [1] (D. Mollison, 1977).
- p. 159: "In discussing percolation, one usually assumes that it is
  decided from the very beginning whether a certain site (or link) can be
  passed or not, it being a property of the lattice. In the GEP, one
  assumes in contrast that the link between two sites is established (or
  not) only at the moment when the infection is to pass across it. Since
  infection can however pass only once through any link, this difference
  does not matter mathematically."
- **p. 159, the mapping:** "The GEP defined by Equations (2.1) and (2.2)
  corresponds to neither site nor bond percolation. Notice that Equation
  (2.2) implies that the times of illness are exponentially distributed
  with mean value T = 1/ρ. Let us now replace this by the assumption—which
  for many diseases is more realistic anyhow—that these times are all equal
  to a fixed time T. Then the chances that an infection can pass from site
  n to a neighbouring site m (provided the latter is still susceptible) are
  all independent and equal to p = 1 − e^{−σT}. (2.3) It is easy to see
  that this is precisely the problem of bond percolation, with probability
  p for the bonds to be unbroken."

**What it supports.** An epidemic on a lattice in which every infected site
stays infectious for the same fixed time is bond percolation: each link
passes the infection independently, with one probability p, and at most
once. That is the correspondence the demo names at `03_environment.md:115`
and `12_appendix.md:19`, and the "link decided at the moment of passage"
remark is the same argument the demo's Appendix A makes for per-edge
Bernoulli variables.

**Caveats for the writers.**

- Grassberger's process runs in continuous time with infection rate σ, so
  its p is 1 − e^{−σT}. CHE's kernel (Def. 3) is synchronous discrete time
  with a burn time of one step and an ignition probability β per attempt,
  so p = β directly. The structure (independent per-link passage, at most
  once per link) is the same, and Proposition 2's own proof is
  self-contained (App. A). So "the correspondence … described by
  Grassberger (1983)" is supported; "Grassberger proves Proposition 2" would
  not be.
- The paper is non-rigorous by its own account (p. 158: "in the
  nonrigorous treatment of the present paper we shall as usually rely on
  intuition"). The mapping sentence is an elementary observation, not a
  theorem.
- Grassberger credits the model to Mollison (1977). Cox & Durrett (1988,
  p. 172) credit the epidemic-to-percolation relation to Mollison (1977)
  and Kuulasmaa (1982) (`paper/v2/review_of_demo.md` N15). Citing
  Grassberger for the constant-period mapping is accurate; it is not a
  claim of priority.

## UNVERIFIED

- Kesten (1980) beyond its title, abstract and record (above).
- The typeset journal version of Bernstein et al. (2002). The quotes are
  from the authors' manuscript PDF, whose abstract matches the journal's;
  page numbers are the PDF's.
