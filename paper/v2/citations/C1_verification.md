# C1 verification: Corollary 1 items (3) and (4)

Step-2 reviewer, Paper v2, 2026-10-11. This file covers the fix-list item
**C1** (`paper_v2_prompt.md:133-143`). It follows the method of
`paper/related_work_verification.md` Part 3: each source was read in full
text (PDF), quotes are given with their locations, and every BibTeX block was
retrieved from a record (Crossref by DOI, or the arXiv export), never written
from memory. Downloads stayed in the session scratchpad; nothing entered the
tree.

**This file edits nothing else.** `paper/related_work_verification.md` and
`submission.bib` are untouched. If v2 adopts a citation below, B2 transcribes
it in step 3 through `related_work_verification.md` first.

---

## 0. What the paper and the theory doc say

`docs/theory_foundations.md:210-232` (Corollary 1, tagged **[CITED]**):

> 3. **Critical scaling.** As $\beta \uparrow \beta_c$:
>    $\chi(\beta) \sim |\beta - \beta_c|^{-\gamma_p}$ with $\gamma_p = 43/18$,
>    and $\xi(\beta) \sim |\beta - \beta_c|^{-\nu_p}$ with $\nu_p = 4/3$
>    (2D percolation universality).
> 4. **Supercritical** ($\beta > \beta_c$): with positive probability the fire
>    spreads indefinitely; conditioned on survival, the burnt region grows
>    linearly in time with an asymptotic front speed $v(\beta) > 0$ and a
>    deterministic limiting shape (shape-theorem behavior for spatial epidemics).

The theory doc gives no source for (3) or (4). Its reference list
(`:735-772`) names, for percolation, Kesten (1980) and Grassberger (1983)
only (`:739-742`).

The demonstration repeats both items at `paper/demo_beyond/sections/04_severity.md:22-23`
with the same content ("the exponents of two-dimensional percolation"). Item (3)
also enters **Proposition 3**: "diverges as $\beta \uparrow \beta_c$ like
$\lvert \beta - \beta_c \rvert^{-43/18}$" (`05_coupling_a.md:68`;
`docs/theory_foundations.md:309-311`), and App. A's proof of Proposition 3
ends "The divergence rate is Corollary 1(3)" (`12_appendix.md:23`;
`docs/theory_foundations.md:318`). The severity lock record repeats the
exponent too ("asymptotic γ = 43/18 not reachable at L = 64",
`severity_lock.md:22-23`).

---

## 1. C1(3): the exponents 43/18 and 4/3

### Sources read

**S1. Smirnov & Werner (2001), "Critical exponents for two-dimensional
percolation".** arXiv:math/0109120v2 (PDF, 16 pp., read in full). Published
in Math. Res. Lett. 8(6):729–744, doi:10.4310/mrl.2001.v8.n6.a4 (Crossref
record; arXiv `journal_ref` "Math. Res. Lett. 8, 729-744 (2001)").

- Abstract (p. 1): "We show how to combine Kesten's scaling relations, the
  determination of critical exponents associated to the stochastic Loewner
  evolution process by Lawler, Schramm, and Werner, and Smirnov's proof of
  Cardy's formula, in order to determine the existence and value of critical
  exponents associated to percolation on the triangular lattice."
- §1 (p. 1): "The goal of the present note is to review and clarify the
  consequences of recent papers and preprints concerning the existence and
  values of critical exponents for site percolation on the triangular
  lattice."
- §2 (pp. 2–3): "$\chi(p) = E_p[N 1_{N<\infty}]$. This corresponds to the
  average cardinality of finite clusters", where "$P_p$, $E_p$ corresponds
  to site percolation on the triangular lattice with parameter p".
- **Theorem 1 (p. 3):** "(ii) When p → 1/2, χ(p) = (p − 1/2)^{−43/18+o(1)}.
  (iii) When p → 1/2, ξ(p) = (p − 1/2)^{−4/3+o(1)}."
- §5, open question 1 (p. 13): "Generalizing the results of Smirnov [30], to
  other lattices. The first two natural candidates are bond percolation on
  the square lattice and site percolation on a Voronoi tesselation […] It
  would be sufficient to prove Cardy's formula, but in both cases the method
  used in [30] does not apply directly."
- §5, open question 3 (p. 13): "Show that the power laws hold up to
  constants."

**S2. Grimmett & Manolescu (2013), "Universality for bond percolation in two
dimensions".** Ann. Probab. 41(5):3261–3283, doi:10.1214/11-AOP740
(Crossref); arXiv:1108.2784v2 (the IMS reprint, read: abstract and §1).
Received August 2011, revised December 2011.

- Abstract (p. 1): "All (in)homogeneous bond percolation models on the
  square, triangular, and hexagonal lattices belong to the same universality
  class, in the sense that they have identical critical exponents at the
  critical point (assuming the exponents exist). […] By earlier results of
  Kesten, this implies universality also for the near-critical exponents
  β, γ, ν, Δ (assuming these exist) for any of these models that satisfy a
  certain additional hypothesis, such as the homogeneous bond percolation
  models on these three lattices."
- §1.1 (p. 1): "Remarkable progress has been made toward a full
  understanding of site percolation on the triangular lattice, at and near
  its critical point. Other critical two-dimensional models have, however,
  resisted solution."
- §1.1 (p. 2): "No progress is made here on the problem of existence of
  exponents."

**S3. van den Berg & Nolin (2020), "On the four-arm exponent for 2D
percolation at criticality".** arXiv:2008.01606 (PDF read; no journal
reference on the arXiv record). Status context only; not proposed for the
bibliography.

- §1 (p. 2): "In the particular case of site percolation on the triangular
  lattice, this exponent is known to be equal to 5/4 [17], and this is
  widely believed to hold for all 'nice' two-dimensional lattices (for site
  percolation, as well as for bond percolation)." (The four-arm exponent is
  one of the two critical-point exponents that Kesten's scaling relations
  need, S1 p. 3, relation (2).)

**S4. Unrefereed claims, abstract level only (not read in full; not a basis
for the paper).** Tsai, Yam & Zhou, arXiv:1112.2017 (2011), and Zhou,
arXiv:2409.03235v6 (2024, "Minor revision. 115 pages"), each claim convergence
of the critical bond-percolation exploration path on the square lattice to
SLE₆. The arXiv metadata carries no journal reference for either. Neither
abstract states γ or ν. S2, published after the 2011 preprint, still treats
existence of the exponents for these bond models as open.

**Not read:** Kesten (1987), "Scaling relations for 2D-percolation",
Comm. Math. Phys. 109(1):109–156, doi:10.1007/BF01205674 (identity from
Crossref only). S1 and S2 cite it for the scaling relations.

### Verdict on (3)

The builder's understanding is **confirmed, with one sharpening**:

1. **Proved for site percolation on the triangular lattice**, by Smirnov &
   Werner (2001, Theorem 1), combining Kesten's scaling relations,
   Lawler–Schramm–Werner and Smirnov. **Even there the result is up to o(1)
   in the exponent**, χ(p) = |p − 1/2|^{−43/18+o(1)} and
   ξ(p) = |p − 1/2|^{−4/3+o(1)}; "power laws up to constants" were listed as
   open (S1 §5, question 3). So the paper's "χ(β) ∼ |β − β_c|^{−43/18}" is
   stronger than what is proved on any lattice.
2. **Not proved for bond percolation on ℤ²**, the model CHE's idealized
   kernel is equivalent to (Proposition 2). There the values are the physics
   predictions, conjectured by universality (S1 §1 and §5; S3). What is
   proved is conditional universality: if the exponents exist for one of the
   bond models on the square, triangular and hexagonal lattices, they agree
   across them (S2). S2 makes "no progress […] on the problem of existence".
3. The theory doc's label "(2D percolation universality)" is accurate as a
   label, but the item is tagged **[CITED]** with no citation, and "∼"
   overstates it. **Record item for the owner** (the theory doc is not
   edited here).

### Recommendation for (3): drop

- **Drop** item (3) from Corollary 1, and drop the rate
  "like |β − β_c|^{−43/18}" from Proposition 3's statement and proof
  (`05_coupling_a.md:68`, `:70`; `12_appendix.md:23`). §4.1 already says the
  paper does not measure the exponents and that the design relies on
  nothing that needs them (`04_severity.md:25`). Proposition 3 keeps its
  linear-in-λ_A content, which the handshake runs test.
- If the owner wants the sentence kept, the verified level is a **conjecture
  with a citation**: for bond percolation on ℤ², χ and ξ are conjectured to
  diverge with the exponents 43/18 and 4/3, which Smirnov & Werner (2001)
  proved, up to o(1) in the exponent, for site percolation on the triangular
  lattice. That needs `smirnov2001exponents` (BibTeX below) entered through
  `related_work_verification.md`, and optionally `grimmett2013universality`
  for the conditional universality.
- **Not verified this session:** a citable statement that χ(β) → ∞ as
  β ↑ 1/2 for bond percolation on ℤ² (without a rate). Kesten (1980) was not
  read past its record. If Proposition 3 keeps the word "diverges", B2 must
  find and record a source for it first, or the word goes too.
- If (3) goes, `03_environment.md:28`'s notation note ("Corollary 1 (§4)
  writes its critical exponents as numbers") goes with it.

---

## 2. C1(4): linear growth and a limiting shape

### What process CHE runs

From the theory doc and the code:

- **Def. 3** (`docs/theory_foundations.md:173-185`): states Fuel / Burning /
  Burnt; "independently for each ordered pair (Burning cell g, Fuel neighbor
  g′ ∈ N(g)): g′ ignites with probability β"; "A Burning cell becomes Burnt
  after exactly one step"; Burnt absorbing; ι = 0 in the propositions.
- **Implementation** (`che/env/hazard.py:39-64`): one synchronous step. A
  Fuel cell ignites if at least one Burning von Neumann neighbour's attempt
  succeeds (`caught = caught | (_shifted(burning, dr, dc) & (u_dir[d] < beta))`);
  Burning becomes Burnt; zero padding, so no wraparound (`:29-36`). The
  module docstring (`:8-16`) records why the per-direction uniforms realize
  Prop. 2's per-edge Bernoulli variables exactly.
- **Prop. 2** (`docs/theory_foundations.md:187-208`): with ι = 0 and one
  ignition, the eventually-Burnt set equals the open cluster of the origin in
  i.i.d. bond percolation with edge probability β.

**Derivation (reviewer, this session; arithmetic only, from Def. 3 and the
Prop.-2 coupling).** Let D(x) be the graph distance from the origin in the
subgraph of open edges (∞ off the cluster). By induction on t: if at step t
the Burning cells are {D = t} and the Burnt cells {D < t}, then a Fuel cell y
(D(y) > t) ignites at t + 1 iff some neighbour x with D(x) = t has its edge
{x, y} open, which holds iff D(y) = t + 1. So **the set burning at step t is
the set at chemical distance t, and the region burnt by step t is the
chemical ball of radius t** in the open cluster of the origin. "The fire
spreads indefinitely" is the event that this cluster is infinite. Item (4)
is therefore a statement about chemical-distance balls in supercritical
Bernoulli **bond** percolation on ℤ², conditioned on the origin lying in the
infinite cluster. (Cox & Durrett 1988 state the same identification, below.)

### Sources read

**S5. Cox & Durrett (1988), "Limit theorems for the spread of epidemics and
forest fires".** Stochastic Processes Appl. 30(2):171–191,
doi:10.1016/0304-4149(88)90083-X (Crossref; the version of record carries a
CC BY-NC-ND open-archive licence from 2003 per Crossref). Read in full from
the author's reprint page (`sites.math.duke.edu/~rtd/reprints/paper44.pdf`,
the journal's typeset pages 171–191); the two pages quoted below were read
as images, because the text layer is OCR-garbled.

- Abstract (p. 171): "We prove that the 'spatial epidemic with removal'
  grows linearly and has an asymptotic shape on the set of nonextinction."
- p. 174: "Consider the usual bond percolation model in which bonds are open
  (in both directions) with probability p, closed with probability 1 − p, and
  distinct bonds are independent. If we think of the open bonds as pieces of
  wood which take one unit of time to burn, and if we set the origin on fire
  at time 0, then at time n all sites in C₀ a distance less than n from 0
  will be burnt and those at distance n will be on fire."
- **(1.4), p. 174:** "If α > α°_c(F) then there is a convex set D such that
  for any ε > 0, P(C₀ ∩ n(1 − ε)D ⊂ ζ_n ⊂ n(1 + ε)D for all sufficiently
  large n) = 1 and P(ξ_n ⊂ n(1 + ε)D − n(1 − ε)D for all sufficiently large
  n) = 1", with ζ_n the sites burnt at time n and ξ_n the sites on fire.
  (The hypothesis is written in the epidemic model's notation, α and
  α°_c(F), on the same page.)
- p. 175: "the proof given in CD generalizes immediately to the case
  P(τ[x, y] = ∞) < ¼ […] By working harder […] one can show that the same
  bounds hold whenever the density of closed bonds is less than 1 − p_c, and
  the proofs of CD can be repeated to prove the result stated above. **We
  will not give the details of the proof of (1.4) for the burning percolation
  cluster.**"
- Theorem 1 (p. 175), the paper's proved shape theorem, concerns the
  continuous-time epidemic with Poisson germ emission and infection periods
  of distribution F, not CHE's synchronous, unit-burn-time kernel.
- p. 177, open problem (ii): the discrete-time model with the four diagonal
  neighbours added (Bailey's) "we cannot analyze". This matches Corollary
  1's caveat that other neighbourhoods break exactness.

**S6. Garet & Marchand (2004), "Asymptotic shape for the chemical distance
and first-passage percolation on the infinite Bernoulli cluster".** ESAIM:
Probability and Statistics 8:169–199, doi:10.1051/ps:2004009 (Crossref).
Published version read in full (Numdam, PS_2004__8__169_0); arXiv
math/0304144v1 (2003, different title) also read.

- Setup (p. 170): bonds between points of ℤ^d at Euclidean distance 1 (the
  von Neumann edges for d = 2); "p is assumed to satisfy to p ∈ (p_c, 1],
  where p_c = p_c(d) is the critical probability for bond percolation on
  ℤ^d"; "we introduce the conditional probability measure P̄_p on Ω_E by
  P̄_p(A) = P_p(A ∩ {0 ∈ C∞}) / P_p(0 ∈ C∞)".
- p. 171: "D(x, y) is thus, when it is finite, the minimal number of open
  edges needed to link x and y in the environment ω."
- Corollary 4.2 (p. 186): "The function µ associated to the chemical distance
  in Bernoulli percolation with parameter p > p_c(d) is a norm on ℝ^d."
- **Corollary 5.4 (p. 188), "asymptotic shape for chemical distance in
  supercritical Bernoulli percolation":** "Remember that on the event 'the
  origin is in the infinite cluster', we denote by B_n the random set of
  vertices in ℤ^d whose chemical distance from 0 is less or equal to n. For
  every d ≥ 2 and p > p_c(d), there exists a deterministic convex compact set
  A ⊂ ℝ^d with non-empty interior and invariant under permutations or
  reflections of the coordinates in ℝ^d such that: B_n / n → A for the
  Hausdorff topology P̄_p a.s."
- Introduction (p. 169): Cox & Durrett showed the classical first-passage
  shape theorem "under some moment conditions"; the paper extends it to the
  infinite cluster.

### Verdict on (4)

**Covered, by S6, for exactly CHE's idealized process on ℤ²;** with four
qualifications on how (4) is worded:

1. **The theorem.** For bond percolation on ℤ² with p = β > p_c(2) = ½, and
   conditioned on the origin being in the infinite cluster (= the fire
   spreading indefinitely), the region burnt by step n, rescaled by n,
   converges almost surely in Hausdorff distance to a deterministic convex
   compact set A with non-empty interior (Garet & Marchand 2004, Cor. 5.4,
   p. 188, via the derivation above). Cox & Durrett (1988) state the same
   result for this "burning percolation cluster", including that the burning
   front stays in a thin shell n(1 + ε)D − n(1 − ε)D, but give no full proof
   (p. 175).
2. **"An asymptotic front speed v(β) > 0" is one number for a
   direction-dependent object.** A is symmetric under coordinate
   permutations and reflections, not shown to be a disc; the speed in
   direction u is 1/µ(u) with µ a norm (Cor. 4.2). A single v(β) is right
   only per direction. (Def. 4's High "front speed", 0.83 cells/step, DX-6,
   is a measurement on the arena and is unaffected.)
3. **"A deterministic limiting shape" holds in the Hausdorff sense.** The
   burnt region is the chemical ball inside the cluster, so it has holes
   where the cluster does; the theorem does not say the region fills A.
4. **ℤ² only.** Nothing here concerns the finite 64 × 64 arena or the
   implemented kernel with Coupling A on, as §4.1 already says for the
   critical value.

The theory doc's own phrase, "shape-theorem behavior for spatial epidemics",
points at the right literature but cites none. **Record item for the owner.**

### Recommendation for (4): state it at the verified level, with a citation (or drop)

- **State**, with `garet2004chemical` (BibTeX below): "Supercritical,
  β > β_c. With positive probability the fire spreads indefinitely.
  Conditioned on that event, the burnt region grows linearly: rescaled by
  time, it converges in Hausdorff distance to a deterministic convex set
  (Garet & Marchand, 2004, Corollary 5.4); the speed depends on direction."
  Optionally add `cox1988epidemics` for the forest-fire reading (its (1.4) is
  this process, stated without full proof).
- **Or drop** (4): nothing in the design depends on it (§4.1), and Def. 4's
  "survival is a race" rests on the measured front speed, not on (4).
- Either way, the words "front speed v(β)" as a single scalar go.

---

## 3. BibTeX, retrieved from records (for B2, step 3; not entered anywhere)

Keys are proposals in the project's convention; the fields are the records'.
Per the M2 fix, any entry adopted should be entered with Unicode and an
en dash (–) in `pages`, as Crossref returns it; no TeX markup.

Smirnov & Werner 2001, Crossref by DOI (`https://doi.org/10.4310/mrl.2001.v8.n6.a4`,
Accept: application/x-bibtex), verbatim:

```bibtex
@article{Smirnov_2001, title={Critical exponents for two-dimensional percolation}, volume={8}, ISSN={1945-001X}, url={http://dx.doi.org/10.4310/mrl.2001.v8.n6.a4}, DOI={10.4310/mrl.2001.v8.n6.a4}, number={6}, journal={Mathematical Research Letters}, publisher={International Press of Boston}, author={Smirnov, Stanislav and Werner, Wendelin}, year={2001}, pages={729–744} }
```

arXiv export (`https://arxiv.org/bibtex/math/0109120`), verbatim:

```bibtex
@misc{smirnov2001criticalexponentstwodimensionalpercolation,
      title={Critical exponents for two-dimensional percolation}, 
      author={Stanislav Smirnov and Wendelin Werner},
      year={2001},
      eprint={math/0109120},
      archivePrefix={arXiv},
      primaryClass={math.PR},
      url={https://arxiv.org/abs/math/0109120}, 
}
```

Garet & Marchand 2004, Crossref by DOI (`https://doi.org/10.1051/ps:2004009`),
verbatim:

```bibtex
@article{Garet_2004, title={Asymptotic shape for the chemical distance and first-passage percolation on the infinite Bernoulli cluster}, volume={8}, ISSN={1262-3318}, url={http://dx.doi.org/10.1051/ps:2004009}, DOI={10.1051/ps:2004009}, journal={ESAIM: Probability and Statistics}, publisher={EDP Sciences}, author={Garet, Olivier and Marchand, Régine}, year={2004}, month=Sept, pages={169–199} }
```

Cox & Durrett 1988, Crossref by DOI (`https://doi.org/10.1016/0304-4149(88)90083-X`),
verbatim:

```bibtex
@article{Cox_1988, title={Limit theorems for the spread of epidemics and forest fires}, volume={30}, ISSN={0304-4149}, url={http://dx.doi.org/10.1016/0304-4149(88)90083-X}, DOI={10.1016/0304-4149(88)90083-x}, number={2}, journal={Stochastic Processes and their Applications}, publisher={Elsevier BV}, author={Cox, J.T. and Durrett, Richard}, year={1988}, month=Dec, pages={171–191} }
```

Grimmett & Manolescu 2013 (only if (3) is kept as a conjecture), Crossref by
DOI (`https://doi.org/10.1214/11-AOP740`), verbatim:

```bibtex
@article{Grimmett_2013, title={Universality for bond percolation in two dimensions}, volume={41}, ISSN={2168-894X}, url={http://dx.doi.org/10.1214/11-AOP740}, DOI={10.1214/11-aop740}, number={5}, journal={The Annals of Probability}, publisher={Institute of Mathematical Statistics}, author={Grimmett, Geoffrey R. and Manolescu, Ioan}, year={2013}, month=Sept, pages={3261–3283} }
```

Side observation for M2 (same session, Crossref API): Crossref's record for
`kesten1980` gives the title as "The critical probability of bond percolation
on the square lattice equals 1/2" and pages "41-59", and its BibTeX export
gives "…equals 1/2" and "41–59". The `$\frac{1}{2}$` and `41--59` in
`submission.bib` are therefore not what the record returns today.

---

## 4. What this file did not do

- It did not read Kesten (1980) or Kesten (1987) beyond their Crossref
  records, and did not verify any citable source for "χ diverges at β_c on
  bond ℤ²" without a rate (UNVERIFIED).
- It did not read the two SLE₆ preprints (S4) past their abstracts.
- It did not check item (2) of Corollary 1 (exponential tails of the
  subcritical cluster-size distribution, finite χ and ξ), which the paper
  states without a citation; out of C1's scope, noted in the main review.
- It made no edit outside `paper/v2/`.
