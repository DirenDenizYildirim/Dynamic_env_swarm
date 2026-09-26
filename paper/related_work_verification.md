# Related-work and bibliography verification

**Date:** 2026-09-26
**Scope:** the `[VERIFY]` relays in `paper/00_common_spine.md` §1/§2/§10 and
`docs/theory_foundations.md` → References, the four LaTeX cite keys
(`keysers2020`, `bernstein2002`, `kesten1980`, `grassberger1983`), and the UED /
domain-randomization search that the spine said was never run.

**Method and what this document is not.** Every entry below was checked
against a record retrieved in this session: an arXiv abstract page or arXiv API
entry, the arXiv BibTeX export, a Crossref record by DOI, a NeurIPS / PMLR / RSS /
CVF proceedings BibTeX, or ML Anthology. **These checks are abstract-level.** No
full paper was read. Where a claim goes beyond the abstract (a reward function, an
agent count), it comes from an *automated summary of the paper's arXiv HTML* and
is marked **[HTML summary]**. It carries the same caveat the 2026-08-10 decision-log
entry already records: the owner must read the PDF before writing related work from it.

**Access limits hit (so the gaps are visible):** DBLP (Anubis block and HTTP 429),
OpenReview (browser check), MDPI full text (HTTP 403), Semantic Scholar (rate-limited,
one call succeeded). **IEEE Xplore was not queried.** That matters for item 4.

---

## Summary table

| # | Item | Status | One-line note |
|---|---|---|---|
| 1 | VULCAN | **CORRECTED** | Exists: arXiv:2604.12831, Liu & Yan, INFOCOM EIN Workshop 2026. It is **not RL and not CMDP/safe-RL**: a VLM global planner plus hazard-aware local planning. The "cost/constraint channel" framing is wrong. |
| 2 | Agrawal 2023 | **CORRECTED** (identity inferred) | Most likely A. Agrawal, Aralikatti, Sun, Huang, *Robustness to Multi-Modal Environment Uncertainty in MARL using Curriculum Learning*, NeurIPS 2023 MASEC **workshop**, arXiv:2310.08746. It is robust MARL under simultaneous uncertainty, not "compositional generalization". |
| 3 | Erdem & Üre 2025 | **CORRECTED** (identity inferred) | M. Erdem & N. K. Üre, *Learning to Balance Mixed Adversarial Attacks for Robust RL*, MAKE 7(4):108, doi:10.3390/make7040108. It is **adversarial**, mixed state+action attacks, not compositional generalization. |
| 4 | SMART (RA-L 2026) | **NOT FOUND** | No RA-L 2026 paper named SMART found. Three non-matching "SMART" papers are listed below. IEEE Xplore was not queried. |
| 5 | Keysers et al. 2020 | VERIFIED | ICLR 2020; arXiv:1912.09713; OpenReview SygcCnNKwr. |
| 6 | Bernstein et al. 2002 | VERIFIED | Math. Oper. Res. 27(4):819–840, doi:10.1287/moor.27.4.819.297. |
| 7 | Kesten 1980 | VERIFIED | Comm. Math. Phys. 74(1):41–59, doi:10.1007/BF01197577. |
| 8 | Grassberger 1983 | VERIFIED | Math. Biosci. 63(2):157–172 (Apr 1983), doi:10.1016/0025-5564(82)90036-0. |
| 9 | Jaderberg et al. 2017 | VERIFIED | arXiv:1711.09846. Preprint only; no venue on the record. |
| 10 | Haksar & Schwager 2018 | VERIFIED (bib) / claim unconfirmed | Full title "…with a Network of Aerial Robots", IROS 2018 pp. 1067–1074. The abstract says "local information", not "restricted communication". |
| 11 | Pynadath & Tambe 2002 | VERIFIED (bib) / claim is a paraphrase | JAIR 16:389–423. The abstract gives a complexity breakdown "along the dimensions of observability and communication cost". Locate the specific result before citing it for "observability gates communication value". |
| 12a | JaxMARL | VERIFIED | NeurIPS 2024 Datasets & Benchmarks, vol. 37, pp. 50925–50951. |
| 12b | Multi-Agent Craftax | VERIFIED | arXiv:2511.04904 (preprint), Al Omari, Matthews, Rutherford, Foerster. |
| 12c | Assistax | VERIFIED | arXiv:2507.21638; comment says "Accepted at RLC 2026". |
| 12d | POBAX | **CORRECTED** | Single-agent partial-observability benchmark (JAX), **not MARL**. arXiv:2508.00046, RLC 2025. |
| 12e | BenchMARL | **CORRECTED** | TorchRL/PyTorch, **not JAX**. JMLR 25 (MLOSS) 2024. |
| 13a | PureJaxRL → Lu et al. 2022 (DPO) | VERIFIED | The PureJaxRL README names DPO as its citation. NeurIPS 2022, vol. 35, pp. 16455–16468. |
| 13b | IPPO → de Witt et al. 2020 | VERIFIED | arXiv:2011.09533. Preprint only. |
| 14 | arXiv:2512.06102 (JaxWildfire) | VERIFIED (identity) / reward claim **not in abstract** | The abstract is silent on reward and agent count. [HTML summary]: single-agent, "penalty … proportional to the number of burning cells" + terminal +10. |
| 15 | arXiv:2604.26150 | **CORRECTED** | Single-agent PPO for power shutoffs. **No burning cells, no CA fire**: the reward is negative operating cost, and ignition probability depends on the operator's decisions. The spine's "burning cells" label looks copied over from JaxWildfire. |
| 16 | arXiv:2507.10142 | VERIFIED | A **survey** (Hu et al.). The abstract mentions no theorem, memorization gap or coverage bound. The spine's "hiding place" note is stale; the decision log already discharged it. |
| P2 | PAIRED, PLR, Robust PLR, ACCEL, Tobin DR, DR reviews, ZSG survey | VERIFIED | All with proceedings BibTeX. |
| P2 | Nearest joint-vs-isolated neighbours | VERIFIED | Gao et al. RSS 2024; Chen et al. ICLR 2022 (DR theory); Tramèr & Boneh 2019; Hsiung et al. 2023; CompoSuite. |
| P2 | Compound events / multiple stressors | VERIFIED | Zscheischler et al. 2018 and 2020; Crain et al. 2008; Côté et al. 2016. |
| **Scoop** | Joint vs isolated **with active-share / marginal matching** | **None found** | Closest: Gao et al. 2024 (matched *effort*, imitation learning) and Erdem & Üre 2025 (adversarial). See the scoop-risk section. |

---

## Part 1 — per-item sections

### 1. VULCAN — CORRECTED

- **Record:** *VULCAN: Vision-Language-Model Enhanced Multi-Agent Cooperative
  Navigation for Indoor Fire-Disaster Response*. Shengding Liu, Qiben Yan.
  arXiv:2604.12831 [cs.RO], v1 14 Apr 2026. Comments: "INFOCOM EIN Workshop 2026".
- **Sources retrieved:** https://arxiv.org/abs/2604.12831 ,
  https://arxiv.org/html/2604.12831 , https://arxiv.org/bibtex/2604.12831
- **Abstract-level content:** extends Habitat-Matterport3D with "smoke diffusion,
  thermal hazards, and sensor degradation". Evaluates multi-agent cooperative
  navigation baselines under normal and fire conditions. Calls for "robust
  perception and hazard-aware planning".
- **What is wrong in the repo:** `theory_foundations.md` Def. 2 and spine §2 place
  VULCAN in the **CMDP / safe-RL cost-or-constraint channel**. The abstract describes
  no RL, no CMDP and no cost channel. [HTML summary]: it is "a planning framework
  without reinforcement learning" (VLM global planner + Fast-Marching local planner).
  Agents must "remain within survivable hazard limits throughout the episode" — a
  **planning constraint**. No Beer–Lambert/transmittance model; smoke is "inferred
  from RGB degradation and depth consistency". No agent disabling; no structural
  collapse. The summary also says the fire is static, which is in tension with the
  abstract's "dynamically evolving"; that point is **unresolved**.
- **Suggested repositioning (for the owner to rule):** "nearest *domain*
  neighbour; hazard handled by a hazard-aware planner under a survivability
  constraint, not learned from a hazard-independent reward." Also cite it beside the
  Coupling B claim: it degrades perception with smoke, though not through a
  Beer–Lambert observation kernel [HTML summary].
- Note: `chaos_robotics_research_plan.md` already recorded the correct arXiv id and
  "hazard inside the planner" characterization. The theory doc's CMDP framing
  diverged from it.

```bibtex
@misc{liu2026vulcan,
  title         = {{VULCAN}: Vision-Language-Model Enhanced Multi-Agent Cooperative Navigation for Indoor Fire-Disaster Response},
  author        = {Shengding Liu and Qiben Yan},
  year          = {2026},
  eprint        = {2604.12831},
  archivePrefix = {arXiv},
  primaryClass  = {cs.RO},
  note          = {INFOCOM EIN Workshop 2026},
  url           = {https://arxiv.org/abs/2604.12831}
}
```

### 2. Agrawal 2023 — CORRECTED (identity inferred; confirm with the relay's source if possible)

- **Record:** *Robustness to Multi-Modal Environment Uncertainty in MARL using
  Curriculum Learning*. Aakriti Agrawal, Rohith Aralikatti, Yanchao Sun,
  Furong Huang. arXiv:2310.08746 [cs.LG], 12 Oct 2023. Venue per ML Anthology:
  **NeurIPS 2023 Workshops: MASEC** (a workshop, not the main track).
- **Sources retrieved:** https://arxiv.org/abs/2310.08746 ,
  https://arxiv.org/html/2310.08746 ,
  https://mlanthology.org/neuripsw/2023/agrawal2023neuripsw-robustness/ ;
  also seen in search: https://openreview.net/forum?id=D78HxVUg1Q ,
  https://neurips.cc/virtual/2023/75832
- **Why this is the likely referent:** it is the only 2023 first-author-Agrawal
  RL paper found whose question matches the spine's role. From the abstract:
  "in real-world situation uncertainty can occur in multiple environment variables
  simultaneously … This work is the first to formulate the generalised problem of
  robustness to multi-modal environment uncertainty in MARL." It pairs naturally
  with item 3. Queries that returned no better candidate: arXiv API
  `au:Agrawal AND abs:compositional AND abs:reinforcement`;
  `au:Agrawal AND abs:reinforcement` over Dec 2022–Feb 2024; web searches for
  "Agrawal 2023 compositional generalization reinforcement learning" and variants.
- **Correction:** the spine frames it as "compositional generalization in RL". It
  is **robust MARL under simultaneous uncertainty (reward/state/action), handled by
  a noise-magnitude curriculum**. [HTML summary]: the curriculum starts at zero
  noise and raises it on convergence. The paper "does not explicitly control for
  total perturbation exposure or per-factor marginal distributions".

```bibtex
@inproceedings{agrawal2023multimodal,
  title     = {Robustness to Multi-Modal Environment Uncertainty in {MARL} Using Curriculum Learning},
  author    = {Agrawal, Aakriti and Aralikatti, Rohith and Sun, Yanchao and Huang, Furong},
  booktitle = {NeurIPS 2023 Workshops: MASEC},
  year      = {2023},
  eprint    = {2310.08746},
  archivePrefix = {arXiv},
  url       = {https://mlanthology.org/neuripsw/2023/agrawal2023neuripsw-robustness/}
}
```

### 3. Erdem & Üre 2025 — CORRECTED (identity inferred; high confidence)

- **Record (Crossref):** *Learning to Balance Mixed Adversarial Attacks for Robust
  Reinforcement Learning*. Mustafa Erdem (ITU Mechatronics / Turkish-German Univ.),
  Nazım Kemal Üre (ITU AI & Data Eng.). *Machine Learning and Knowledge
  Extraction* **7**(4):108, published 24 Sep 2025. doi:10.3390/make7040108.
- **Sources retrieved:** https://api.crossref.org/works/10.3390/make7040108
  (full record + abstract). https://doi.org/10.3390/make7040108 resolves to
  https://www.mdpi.com/2504-4990/7/4/108 (HTTP 403, full text not read). The
  arXiv API has no Erdem+Üre paper (`au:Ure AND au:Erdem`, `au:Ure` listing).
- **Abstract-level content:** introduces ASA-MDP (a zero-sum game with an
  adversary attacking both states and actions) and ASA-PPO. States: "agents
  trained conventionally or against single-type attacks remain highly vulnerable
  to mixed perturbations". A naive mixed adversary fails to balance its budget
  across modalities.
- **Correction:** this is **adversarial robustness to co-occurring perturbation
  types**, not compositional generalization, and not an ambient stressor. It asks
  the joint-vs-isolated question. It is also the one found work whose headline
  says isolated (single-type) training fails on the combination — **the opposite
  direction** from CHE's matched-share result. That is worth one sentence.
  Whether its baselines match exposure could not be checked (full text blocked).

```bibtex
@article{erdem2025mixed,
  title   = {Learning to Balance Mixed Adversarial Attacks for Robust Reinforcement Learning},
  author  = {Erdem, Mustafa and {\"U}re, Naz{\i}m Kemal},
  journal = {Machine Learning and Knowledge Extraction},
  volume  = {7},
  number  = {4},
  pages   = {108},
  year    = {2025},
  doi     = {10.3390/make7040108}
}
```

### 4. SMART (RA-L 2026) — NOT FOUND

No IEEE RA-L 2026 paper titled or acronymed SMART was found. Candidates that
surfaced, **none of which matches** (wrong venue/year, or no hazard content):

| candidate | record | why it does not match |
|---|---|---|
| *SMART: Scalable Multi-Agent Reasoning and Trajectory Planning in Dense Environments* | Huang, Yang, Chen, Chen, Li, Chen; arXiv:2509.15737, Sep 2025 — https://arxiv.org/abs/2509.15737 | No RA-L journal-ref on the record; multi-vehicle trajectory planning, no hazard |
| *From Multi-agent to Multi-robot: A Scalable Training and Evaluation Platform for Multi-robot RL* ("SMART" platform) | Liang et al.; arXiv:2206.09590, Jun 2022 — https://arxiv.org/abs/2206.09590 | 2022, not RA-L, lane-change case study |
| *SMART-LLM: Smart Multi-Agent Robot Task Planning using LLMs* | arXiv:2309.10062 (seen in search only); IROS 2024 per search summary | IROS, 2024, LLM task planning |

Queries tried: "SMART IEEE Robotics and Automation Letters 2026 multi-robot hazard";
"'SMART' swarm robots 'Robotics and Automation Letters' 2026 failures reinforcement
learning"; "SMART multi-agent reinforcement learning hazardous environment benchmark
2026 arXiv"; "'SMART' ieeexplore 'IEEE Robotics and Automation Letters' 2026
multi-agent reinforcement learning"; "SMART swarm disaster fire robots RA-L 2026";
"'SMART:' multi-robot 'accepted' RA-L 2026"; "'SMART' resilient swarm robot failures
agent loss attrition RL 2026"; "'SMART' MARL communication degraded perception smoke";
ieeexplore.ieee.org-restricted search "SMART robotics automation letters 2026 swarm
multi-agent"; DBLP RA-L vol. 11 page (blocked).
**Recommendation:** do not cite, and remove limitation item 11, until the relay's
source is produced or an authenticated IEEE Xplore search finds the paper.
This is the same failure class as the relays the decision log already warns about.

### 5. Keysers et al. 2020 — VERIFIED (`keysers2020`)

Sources: arXiv API entry for 1912.09713 (comment "Accepted for publication at ICLR
2020"), https://arxiv.org/bibtex/1912.09713 , ICLR 2020 virtual poster page
https://iclr.cc/virtual_2020/poster_SygcCnNKwr.html . The OpenReview forum
https://openreview.net/forum?id=SygcCnNKwr was seen in search; the fetch was blocked.
The abstract's method (maximize compound divergence, keep atom divergence small)
matches the repo's use.

```bibtex
@inproceedings{keysers2020,
  title     = {Measuring Compositional Generalization: A Comprehensive Method on Realistic Data},
  author    = {Keysers, Daniel and Sch{\"a}rli, Nathanael and Scales, Nathan and Buisman, Hylke and Furrer, Daniel and Kashubin, Sergii and Momchev, Nikola and Sinopalnikov, Danila and Stafiniak, Lukasz and Tihon, Tibor and Tsarkov, Dmitry and Wang, Xiao and van Zee, Marc and Bousquet, Olivier},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year      = {2020},
  eprint    = {1912.09713},
  archivePrefix = {arXiv},
  url       = {https://openreview.net/forum?id=SygcCnNKwr}
}
```

### 6. Bernstein, Givan, Immerman, Zilberstein 2002 — VERIFIED (`bernstein2002`)

Source: Crossref, doi:10.1287/moor.27.4.819.297 (journal-article, Nov 2002).

```bibtex
@article{bernstein2002,
  title   = {The Complexity of Decentralized Control of {M}arkov Decision Processes},
  author  = {Bernstein, Daniel S. and Givan, Robert and Immerman, Neil and Zilberstein, Shlomo},
  journal = {Mathematics of Operations Research},
  volume  = {27},
  number  = {4},
  pages   = {819--840},
  year    = {2002},
  doi     = {10.1287/moor.27.4.819.297}
}
```

### 7. Kesten 1980 — VERIFIED (`kesten1980`)

Source: Crossref, doi:10.1007/BF01197577 (Feb 1980).

```bibtex
@article{kesten1980,
  title   = {The critical probability of bond percolation on the square lattice equals $\frac{1}{2}$},
  author  = {Kesten, Harry},
  journal = {Communications in Mathematical Physics},
  volume  = {74},
  number  = {1},
  pages   = {41--59},
  year    = {1980},
  doi     = {10.1007/BF01197577}
}
```

### 8. Grassberger 1983 — VERIFIED (`grassberger1983`)

Source: Crossref, doi:10.1016/0025-5564(82)90036-0. Issue dated April 1983; the
"(82)" in the DOI is the publisher's and is not an error. Crossref gives the
author as "P. Grassberger"; the initial is kept rather than expanded from memory.

```bibtex
@article{grassberger1983,
  title   = {On the critical behavior of the general epidemic process and dynamical percolation},
  author  = {Grassberger, P.},
  journal = {Mathematical Biosciences},
  volume  = {63},
  number  = {2},
  pages   = {157--172},
  year    = {1983},
  doi     = {10.1016/0025-5564(82)90036-0}
}
```

### 9. Jaderberg et al. 2017 — VERIFIED

Source: arXiv API + https://arxiv.org/bibtex/1711.09846 (v2, 28 Nov 2017). No
journal-ref or venue comment is on the record. Cite as arXiv.

```bibtex
@misc{jaderberg2017pbt,
  title         = {Population Based Training of Neural Networks},
  author        = {Max Jaderberg and Valentin Dalibard and Simon Osindero and Wojciech M. Czarnecki and Jeff Donahue and Ali Razavi and Oriol Vinyals and Tim Green and Iain Dunning and Karen Simonyan and Chrisantha Fernando and Koray Kavukcuoglu},
  year          = {2017},
  eprint        = {1711.09846},
  archivePrefix = {arXiv},
  primaryClass  = {cs.LG}
}
```

### 10. Haksar & Schwager 2018 — VERIFIED (bibliographic); characterization partly unconfirmed

- Sources: Crossref doi:10.1109/IROS.2018.8593539 (IROS 2018, pp. 1067–1074);
  Semantic Scholar API record with the abstract; lab page
  https://msl.stanford.edu/bibliography/haksar_distributed_2018 .
- Abstract: a distributed deep RL strategy for a UAV team to fight forest fires.
  The fire is a factored MDP; "each agent learns a policy requiring only local
  information". Robotarium demonstrations. Search snippets (not the abstract)
  mention MADQN.
- **Unconfirmed from the abstract:** "restrictive / restricted communication" and
  the exact reward. The spine's placement ("hazard in the reward") is plausible for
  a suppression task, but the owner should quote the reward from the PDF.
  The theory doc gives no title; use the full one below.

```bibtex
@inproceedings{haksar2018,
  title     = {Distributed Deep Reinforcement Learning for Fighting Forest Fires with a Network of Aerial Robots},
  author    = {Haksar, Ravi N. and Schwager, Mac},
  booktitle = {2018 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)},
  pages     = {1067--1074},
  year      = {2018},
  doi       = {10.1109/IROS.2018.8593539}
}
```

### 11. Pynadath & Tambe 2002 — VERIFIED (bibliographic); claim is a paraphrase

Source: Crossref doi:10.1613/jair.1024 with abstract. The abstract presents
COM-MTDP, "a breakdown of the computational complexity … along the dimensions of
observability and communication cost", and "a domain-independent criterion for
optimal communication". "Observability gates communication value" is a reasonable
reading, but it is **not a sentence of the abstract**. Cite the specific result
(section/table) from the paper.

```bibtex
@article{pynadath2002,
  title   = {The Communicative Multiagent Team Decision Problem: Analyzing Teamwork Theories and Models},
  author  = {Pynadath, David V. and Tambe, Milind},
  journal = {Journal of Artificial Intelligence Research},
  volume  = {16},
  pages   = {389--423},
  year    = {2002},
  doi     = {10.1613/jair.1024}
}
```

### 12. JAX / MARL benchmark neighbours

**Positioning correction for spine §2 row "JAX × MARL × hazards":** two of the
five named libraries do not belong to both halves of that row. **POBAX is
single-agent**: the abstract concerns partial observability for "general
reinforcement learning algorithms". **BenchMARL is built on TorchRL**, not JAX.
The row should say "JAX RL/MARL environments and MARL libraries", or drop those two.

**12a JaxMARL — VERIFIED.** NeurIPS 2024 D&B proceedings BibTeX
(https://proceedings.neurips.cc/paper_files/paper/2024/file/5aee125f052c90e326dcf6f380df94f6-Bibtex-Datasets_and_Benchmarks_Track.bib); arXiv:2311.10090.

```bibtex
@inproceedings{rutherford2024jaxmarl,
  author    = {Rutherford, Alexander and Ellis, Benjamin and Gallici, Matteo and Cook, Jonathan and Lupu, Andrei and Ingvarsson, Gar\dh ar and Willi, Timon and Hammond, Ravi and Khan, Akbir and de Witt, Christian Schroeder and Souly, Alexandra and Bandyopadhyay, Saptarashmi and Samvelyan, Mikayel and Jiang, Minqi and Lange, Robert and Whiteson, Shimon and Lacerda, Bruno and Hawes, Nick and Rockt\"{a}schel, Tim and Lu, Chris and Foerster, Jakob},
  booktitle = {Advances in Neural Information Processing Systems},
  editor    = {A. Globerson and L. Mackey and D. Belgrave and A. Fan and U. Paquet and J. Tomczak and C. Zhang},
  pages     = {50925--50951},
  publisher = {Curran Associates, Inc.},
  title     = {JaxMARL: Multi-Agent RL Environments and Algorithms in JAX},
  volume    = {37},
  year      = {2024},
  doi       = {10.52202/079017-1612}
}
```

**12b Multi-Agent Craftax — VERIFIED (preprint).** arXiv API + https://arxiv.org/bibtex/2511.04904 .

```bibtex
@misc{alomari2025macraftax,
  title         = {Multi-Agent Craftax: Benchmarking Open-Ended Multi-Agent Reinforcement Learning at the Hyperscale},
  author        = {Bassel Al Omari and Michael Matthews and Alexander Rutherford and Jakob Nicolaus Foerster},
  year          = {2025},
  eprint        = {2511.04904},
  archivePrefix = {arXiv},
  primaryClass  = {cs.LG}
}
```

**12c Assistax — VERIFIED.** arXiv API (v3 comment: "Accepted at the Reinforcement
Learning Conference 2026") + https://arxiv.org/bibtex/2507.21638 . Update to the
RLC/RLJ record when it is published.

```bibtex
@misc{hinckeldey2025assistax,
  title         = {Assistax: A Multi-Agent Hardware-Accelerated Reinforcement Learning Benchmark for Assistive Robotics},
  author        = {Leonard Hinckeldey and Elliot Fosong and Rimvydas Rubavicius and Elle Miller and Trevor McInroe and Fan Zhang and Patricia Wollstadt and Stefano V. Albrecht and Subramanian Ramamoorthy},
  year          = {2025},
  eprint        = {2507.21638},
  archivePrefix = {arXiv},
  primaryClass  = {cs.AI},
  note          = {Accepted at the Reinforcement Learning Conference 2026}
}
```

**12d POBAX — CORRECTED (single-agent).** arXiv API (comment "To appear at RLC
2025") + https://arxiv.org/bibtex/2508.00046 ; repo https://github.com/taodav/pobax
(seen in search).

```bibtex
@misc{tao2025pobax,
  title         = {Benchmarking Partial Observability in Reinforcement Learning with a Suite of Memory-Improvable Domains},
  author        = {Ruo Yu Tao and Kaicheng Guo and Cameron Allen and George Konidaris},
  year          = {2025},
  eprint        = {2508.00046},
  archivePrefix = {arXiv},
  primaryClass  = {cs.LG},
  note          = {RLC 2025}
}
```

**12e BenchMARL — CORRECTED (TorchRL, not JAX).** ML Anthology
https://mlanthology.org/mloss/2024/bettini2024jmlr-benchmarl/ ; arXiv:2312.01472;
JMLR PDF https://www.jmlr.org/papers/volume25/23-1612/23-1612.pdf (seen in search).

```bibtex
@article{bettini2024benchmarl,
  title   = {BenchMARL: Benchmarking Multi-Agent Reinforcement Learning},
  author  = {Bettini, Matteo and Prorok, Amanda and Moens, Vincent},
  journal = {Journal of Machine Learning Research},
  volume  = {25},
  pages   = {1--10},
  year    = {2024},
  note    = {Machine Learning Open Source Software track},
  url     = {https://www.jmlr.org/papers/volume25/23-1612/23-1612.pdf}
}
```

### 13. Training-method citations

**13a PureJaxRL → Lu et al. 2022 — VERIFIED.** The PureJaxRL README
(https://raw.githubusercontent.com/luchris429/purejaxrl/main/README.md) says:
"If you use PureJaxRL in your work, please cite the following paper:
Discovered policy optimisation". BibTeX below is from the NeurIPS proceedings file.

```bibtex
@inproceedings{lu2022dpo,
  author    = {Lu, Chris and Kuba, Jakub and Letcher, Alistair and Metz, Luke and Schroeder de Witt, Christian and Foerster, Jakob},
  booktitle = {Advances in Neural Information Processing Systems},
  editor    = {S. Koyejo and S. Mohamed and A. Agarwal and D. Belgrave and K. Cho and A. Oh},
  pages     = {16455--16468},
  publisher = {Curran Associates, Inc.},
  title     = {Discovered Policy Optimisation},
  volume    = {35},
  year      = {2022},
  doi       = {10.52202/068431-1197}
}
```

**13b IPPO → de Witt et al. 2020 — VERIFIED (preprint).** arXiv API +
https://arxiv.org/bibtex/2011.09533 . No venue on the record.

```bibtex
@misc{dewitt2020ippo,
  title         = {Is Independent Learning All You Need in the StarCraft Multi-Agent Challenge?},
  author        = {Christian Schroeder de Witt and Tarun Gupta and Denys Makoviichuk and Viktor Makoviychuk and Philip H. S. Torr and Mingfei Sun and Shimon Whiteson},
  year          = {2020},
  eprint        = {2011.09533},
  archivePrefix = {arXiv},
  primaryClass  = {cs.AI}
}
```

### 14. arXiv:2512.06102 — JaxWildfire — VERIFIED (identity); reward claim is not in the abstract

- **Title:** *JaxWildfire: A GPU-Accelerated Wildfire Simulator for Reinforcement
  Learning*. **Authors:** Ufuk Çakır, Victor-Alexandru Darvariu, Bruno Lacerda,
  Nick Hawes. **Date:** 5 Dec 2025 (v1). **Comment:** "To be presented at the
  NeurIPS 2025 Workshop on Machine Learning and the Physical Sciences (ML4PS)".
- **Sources:** https://arxiv.org/abs/2512.06102 , https://arxiv.org/html/2512.06102 ,
  https://arxiv.org/bibtex/2512.06102
- **Abstract-level summary:** a JAX wildfire simulator built on a probabilistic
  cellular-automaton fire-spread model, vectorized with `vmap`. Reports a 6–35×
  speedup over existing software and enables gradient-based fitting of simulator
  parameters. Used to train RL agents for wildfire suppression.
- **Does the abstract support "reward penalizes burning cells"?** **No — the abstract
  is silent** on reward and agent count. [HTML summary] supports both repo rows:
  reward is "a penalty at each timestep proportional to the number of burning
  cells and a terminal +10 reward if the fire is completely extinguished". The
  environment is single-agent; heterogeneous multi-agent teams are future work.
  Observations are "partial egocentric". Agent harm is not described. These still
  need the PDF read that the decision log records as owed.

```bibtex
@misc{cakir2025jaxwildfire,
  title         = {JaxWildfire: A GPU-Accelerated Wildfire Simulator for Reinforcement Learning},
  author        = {Ufuk {\c{C}}ak{\i}r and Victor-Alexandru Darvariu and Bruno Lacerda and Nick Hawes},
  year          = {2025},
  eprint        = {2512.06102},
  archivePrefix = {arXiv},
  primaryClass  = {cs.LG},
  note          = {NeurIPS 2025 Workshop on Machine Learning and the Physical Sciences}
}
```

### 15. arXiv:2604.26150 — CORRECTED

- **Title:** *Reinforcement Learning for Public Safety Power Shutoffs Under
  Decision-Dependent Uncertainty and Nonlinear Wildfire Ignition Models*.
  **Authors:** Prasanna Raut, Chaoyue Zhao, Alexandre Moreira. **Date:** 28 Apr 2026
  (v1). math.OC; no comments.
- **Sources:** https://arxiv.org/abs/2604.26150 , https://arxiv.org/html/2604.26150 ,
  https://arxiv.org/bibtex/2604.26150
- **Abstract-level summary:** utilities de-energize grid sections (PSPS) to reduce
  power-line wildfire ignitions, at a cost to communities. Mixed-integer methods
  need restrictive assumptions on line-failure probability models. The authors
  train PPO to reconfigure distribution-system topology against a simulator that
  accepts any failure-probability model. Tested on 54- and 138-bus systems, it
  lowers operational cost at marginally higher compute.
- **What is wrong in the spine (§2):** it records this paper as "single-agent,
  reward penalizes burning cells". Single-agent is supported [HTML summary]. **The
  reward is not** a burning-cell penalty: it is "the negative operating cost" —
  energy, switching and load-loss terms [HTML summary, §II-B5]. The model has
  **no cellular-automaton fire and no burning cells**. Wildfire enters only as a
  line-failure probability that depends on power flow — the operator's own
  decisions. The decision-log entry of 2026-08-10 (agent-mediated ignition
  endogeneity, a neighbour for Coupling A) is the correct reading. The spine line
  appears to have picked up JaxWildfire's reward and should be fixed.

```bibtex
@misc{raut2026psps,
  title         = {Reinforcement Learning for Public Safety Power Shutoffs Under Decision-Dependent Uncertainty and Nonlinear Wildfire Ignition Models},
  author        = {Prasanna Raut and Chaoyue Zhao and Alexandre Moreira},
  year          = {2026},
  eprint        = {2604.26150},
  archivePrefix = {arXiv},
  primaryClass  = {math.OC}
}
```

### 16. arXiv:2507.10142 — VERIFIED (a survey; no theorem in the abstract)

- **Current title (v2, 22 Jul 2026):** *Toward Adaptable Multi-Agent Reinforcement
  Learning: An Assumption-Aware Review*. **v1 title (14 Jul 2025):** *Adaptability
  in Multi-Agent Reinforcement Learning: A Framework and Unified Review*.
  **Authors:** Siyi Hu, Mohamad A Hady, Jianglin Qiao, Jimmy Cao, Mahardhika Pratama,
  Ryszard Kowalczyk. cs.AI.
- **Sources:** https://arxiv.org/abs/2507.10142 , https://arxiv.org/abs/2507.10142v1 ,
  https://arxiv.org/bibtex/2507.10142
- **Abstract-level summary:** MARL deployments violate design assumptions: agent
  populations change, objectives shift, centralized information disappears,
  execution goes asynchronous, partners are unfamiliar. The survey proposes
  "adaptability" as an assumption-aware taxonomy with three dimensions — learning,
  policy, and scenario-driven adaptability — and argues that current MARL
  evaluation is underspecified.
- **Memorization-gap theorem?** **Nothing in the abstract suggests one.** It
  mentions no theorem, value gap, memorization gap or coverage bound. This agrees
  with the decision log's 2026-08-10 "Check 3 — DISCHARGED". The spine §2 and the
  theory-doc references still carry the stale "hiding place" wording.
  **Better target for that check:** Chen et al. (ICLR 2022, Part 2 below) is an
  actual value-gap theorem about a training distribution (DR) that stresses
  history-dependent policies.

```bibtex
@misc{hu2025adaptablemarl,
  title         = {Toward Adaptable Multi-Agent Reinforcement Learning: An Assumption-Aware Review},
  author        = {Siyi Hu and Mohamad A Hady and Jianglin Qiao and Jimmy Cao and Mahardhika Pratama and Ryszard Kowalczyk},
  year          = {2025},
  eprint        = {2507.10142},
  archivePrefix = {arXiv},
  primaryClass  = {cs.AI},
  note          = {v1 (2025) titled ``Adaptability in Multi-Agent Reinforcement Learning: A Framework and Unified Review''; v2 (2026) retitled}
}
```

---

## Part 2 — UED / domain randomization / curriculum / multi-task

### Core works (all VERIFIED)

| work | record | source retrieved |
|---|---|---|
| **PAIRED** | Dennis, Jaques, Vinitsky, Bayen, Russell, Critch, Levine. *Emergent Complexity and Zero-shot Transfer via Unsupervised Environment Design*. NeurIPS 2020, vol. 33, pp. 13049–13061. arXiv:2012.02096 | NeurIPS BibTeX file; https://proceedings.neurips.cc/paper/2020/hash/985e9a46e10005356bbaf194249f6856-Abstract.html |
| **PLR** | Jiang, Grefenstette, Rocktäschel. *Prioritized Level Replay*. ICML 2021, PMLR 139:4940–4950. arXiv:2010.03934 | https://proceedings.mlr.press/v139/jiang21b.html |
| **Robust PLR / PLR⊥** | Jiang, Dennis, Parker-Holder, Foerster, Grefenstette, Rocktäschel. *Replay-Guided Adversarial Environment Design*. NeurIPS 2021, vol. 34, pp. 1884–1897. arXiv:2110.02439 | NeurIPS BibTeX file; https://proceedings.neurips.cc/paper/2021/hash/0e915db6326b6fb6a3c56546980a8c93-Abstract.html |
| **ACCEL** | Parker-Holder, Jiang, Dennis, Samvelyan, Foerster, Grefenstette, Rocktäschel. *Evolving Curricula with Regret-Based Environment Design*. ICML 2022, PMLR 162:17473–17498. arXiv:2203.01302 | https://proceedings.mlr.press/v162/parker-holder22a.html |
| **Domain randomization** | Tobin, Fong, Ray, Schneider, Zaremba, Abbeel. *Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World*. IROS 2017, pp. 23–30, doi:10.1109/IROS.2017.8202133. arXiv:1703.06907 | Crossref; arXiv API |
| **DR review** | Muratore, Ramos, Turk, Yu, Gienger, Peters. *Robot Learning From Randomized Simulations: A Review*. Front. Robot. AI 9 (2022), doi:10.3389/frobt.2022.799893. arXiv:2111.00956 | Crossref; arXiv API |
| **Sim-to-real survey** | Zhao, Peña Queralta, Westerlund. *Sim-to-Real Transfer in Deep Reinforcement Learning for Robotics: a Survey*. IEEE SSCI 2020, pp. 737–744, doi:10.1109/SSCI47803.2020.9308468. arXiv:2009.13303 | Crossref; arXiv API |
| **ZSG survey** | Kirk, Zhang, Grefenstette, Rocktäschel. *A Survey of Zero-shot Generalisation in Deep Reinforcement Learning*. JAIR 76:201–264 (2023), doi:10.1613/jair.1.14174. arXiv:2111.09794 | Crossref; arXiv API |
| **DR theory** | Chen, Hu, Jin, Li, Wang. *Understanding Domain Randomization for Sim-to-real Transfer*. ICLR 2022. arXiv:2110.03239 | https://arxiv.org/abs/2110.03239 ; ICLR 2022 poster page and OpenReview T8vZHIRTrY seen in search |

Which of the two DR reviews is standard is a judgment call. Muratore et al. is
DR-specific (its abstract calls it a review "focusing on a technique named 'domain
randomization'"). Zhao et al. is the broader sim-to-real survey. Cite Muratore as
the DR review, and Zhao only if sim-to-real framing is needed.

### Nearest joint-vs-isolated neighbours found (all VERIFIED)

- **Gao, Xie, Xiao, Finn, Sadigh. *Efficient Data Collection for Robotic
  Manipulation via Compositional Generalization*. RSS 2024,
  doi:10.15607/RSS.2024.XX.013; arXiv:2403.05110.** (RSS proceedings BibTeX
  retrieved from https://www.roboticsproceedings.org/rss20/p013.html.)
  - Abstract: asks whether policies "compose environmental factors from their
    data to succeed when encountering unseen factor combinations". Real-robot
    success on unseen combinations is 77.5% with a composition-aware strategy vs
    2.5% for data collected without accounting for variation (numbers as quoted in
    the abstract).
  - [HTML summary]: compares collection strategies including **L** ("varies only
    one factor at a time" from base values), **Stair**, **Diagonal**, **Random**
    and **Complete**. They are compared "with the total number of factor changes,
    which we use to quantify effort" — **matched effort, not matched active share
    or marginals**.
  - This is the single closest design to CHE's ISO/JOINT question, in imitation
    learning with benign factors.
- **Chen et al. ICLR 2022** (above). Sharp bounds on the sim-to-real gap of DR, and
  emphasizes "using memory (i.e., history-dependent policies)". It is the nearest
  value-gap *theorem* about a training distribution. By abstract it is not Thm. 1's
  form (Thm. 1 is a closed-form two-corridor toy). The owner should read it before
  writing that Thm. 1 is unsubsumed.
- **Tramèr & Boneh. *Adversarial Training and Robustness for Multiple
  Perturbations*. NeurIPS 2019, vol. 32; arXiv:1904.13000.** Supervised vision.
  Defenses tuned to one perturbation type give no guarantee on others; they train
  for several types simultaneously. Adjacent literature, not RL.
- **Hsiung, Tsai, Chen, Ho. *Towards Compositional Adversarial Robustness:
  Generalizing Adversarial Training to Composite Semantic Perturbations*. CVPR 2023,
  pp. 24658–24667; arXiv:2202.04235.** Supervised vision. Robustness to single
  attacks vs to their *compositions*. Adjacent, not RL.
- **Mendez, Hussing, Gummadi, Eaton. *CompoSuite: A Compositional Reinforcement
  Learning Benchmark*. CoLLAs 2022, PMLR 199:982–1003; arXiv:2207.04136.**
  Compositional multi-task RL over robot × object × objective × obstacle. Task
  composition, not stressor co-occurrence.
- Items 2 and 3 above (Agrawal et al. 2023; Erdem & Üre 2025) belong here too.
  They are the RL-side robust-learning neighbours.

### Compound events / multiple stressors (VERIFIED, for the one-sentence analogy)

- Zscheischler et al., *Future climate risk from compound events*, Nature Climate
  Change 8(6):469–477 (2018), doi:10.1038/s41558-018-0156-3. An author correction
  exists: doi:10.1038/s41558-018-0220-z.
- Zscheischler et al., *A typology of compound weather and climate events*, Nature
  Reviews Earth & Environment 1(7):333–347 (2020), doi:10.1038/s43017-020-0060-z.
- Crain, Kroeker, Halpern, *Interactive and cumulative effects of multiple human
  stressors in marine systems*, Ecology Letters 11(12):1304–1315 (2008),
  doi:10.1111/j.1461-0248.2008.01253.x.
- Côté, Darling, Brown, *Interactions among ecosystem stressors and their
  importance in conservation*, Proc. R. Soc. B 283(1824):20152592 (2016),
  doi:10.1098/rspb.2015.2592.

(All via Crossref bibliographic queries. Suggest one climate + one ecology:
Zscheischler 2018 + Côté 2016.)

### BibTeX — Part 2

```bibtex
@inproceedings{dennis2020paired,
  author    = {Dennis, Michael and Jaques, Natasha and Vinitsky, Eugene and Bayen, Alexandre and Russell, Stuart and Critch, Andrew and Levine, Sergey},
  booktitle = {Advances in Neural Information Processing Systems},
  editor    = {H. Larochelle and M. Ranzato and R. Hadsell and M.F. Balcan and H. Lin},
  pages     = {13049--13061},
  publisher = {Curran Associates, Inc.},
  title     = {Emergent Complexity and Zero-shot Transfer via Unsupervised Environment Design},
  volume    = {33},
  year      = {2020}
}

@inproceedings{jiang2021plr,
  title     = {Prioritized Level Replay},
  author    = {Jiang, Minqi and Grefenstette, Edward and Rockt{\"a}schel, Tim},
  booktitle = {Proceedings of the 38th International Conference on Machine Learning},
  pages     = {4940--4950},
  year      = {2021},
  editor    = {Meila, Marina and Zhang, Tong},
  volume    = {139},
  series    = {Proceedings of Machine Learning Research},
  publisher = {PMLR}
}

@inproceedings{jiang2021robustplr,
  author    = {Jiang, Minqi and Dennis, Michael and Parker-Holder, Jack and Foerster, Jakob and Grefenstette, Edward and Rockt\"{a}schel, Tim},
  booktitle = {Advances in Neural Information Processing Systems},
  editor    = {M. Ranzato and A. Beygelzimer and Y. Dauphin and P.S. Liang and J. Wortman Vaughan},
  pages     = {1884--1897},
  publisher = {Curran Associates, Inc.},
  title     = {Replay-Guided Adversarial Environment Design},
  volume    = {34},
  year      = {2021}
}

@inproceedings{parkerholder2022accel,
  title     = {Evolving Curricula with Regret-Based Environment Design},
  author    = {Parker-Holder, Jack and Jiang, Minqi and Dennis, Michael and Samvelyan, Mikayel and Foerster, Jakob and Grefenstette, Edward and Rockt{\"a}schel, Tim},
  booktitle = {Proceedings of the 39th International Conference on Machine Learning},
  pages     = {17473--17498},
  year      = {2022},
  editor    = {Chaudhuri, Kamalika and Jegelka, Stefanie and Song, Le and Szepesvari, Csaba and Niu, Gang and Sabato, Sivan},
  volume    = {162},
  series    = {Proceedings of Machine Learning Research},
  publisher = {PMLR}
}

@inproceedings{tobin2017dr,
  title     = {Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World},
  author    = {Tobin, Josh and Fong, Rachel and Ray, Alex and Schneider, Jonas and Zaremba, Wojciech and Abbeel, Pieter},
  booktitle = {2017 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)},
  pages     = {23--30},
  year      = {2017},
  doi       = {10.1109/IROS.2017.8202133}
}

@article{muratore2022drreview,
  title   = {Robot Learning From Randomized Simulations: A Review},
  author  = {Muratore, Fabio and Ramos, Fabio and Turk, Greg and Yu, Wenhao and Gienger, Michael and Peters, Jan},
  journal = {Frontiers in Robotics and AI},
  volume  = {9},
  year    = {2022},
  doi     = {10.3389/frobt.2022.799893}
}

@inproceedings{zhao2020simtoreal,
  title     = {Sim-to-Real Transfer in Deep Reinforcement Learning for Robotics: a Survey},
  author    = {Zhao, Wenshuai and Pe{\~n}a Queralta, Jorge and Westerlund, Tomi},
  booktitle = {2020 IEEE Symposium Series on Computational Intelligence (SSCI)},
  pages     = {737--744},
  year      = {2020},
  doi       = {10.1109/SSCI47803.2020.9308468}
}

@article{kirk2023zsg,
  title   = {A Survey of Zero-shot Generalisation in Deep Reinforcement Learning},
  author  = {Kirk, Robert and Zhang, Amy and Grefenstette, Edward and Rockt{\"a}schel, Tim},
  journal = {Journal of Artificial Intelligence Research},
  volume  = {76},
  pages   = {201--264},
  year    = {2023},
  doi     = {10.1613/jair.1.14174}
}

@inproceedings{chen2022understandingdr,
  title     = {Understanding Domain Randomization for Sim-to-real Transfer},
  author    = {Chen, Xiaoyu and Hu, Jiachen and Jin, Chi and Li, Lihong and Wang, Liwei},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year      = {2022},
  eprint    = {2110.03239},
  archivePrefix = {arXiv},
  url       = {https://openreview.net/forum?id=T8vZHIRTrY}
}

@inproceedings{gao2024composition,
  author    = {Gao, Jensen and Xie, Annie and Xiao, Ted and Finn, Chelsea and Sadigh, Dorsa},
  title     = {Efficient Data Collection for Robotic Manipulation via Compositional Generalization},
  booktitle = {Proceedings of Robotics: Science and Systems},
  address   = {Delft, Netherlands},
  year      = {2024},
  doi       = {10.15607/RSS.2024.XX.013}
}

@inproceedings{tramer2019multiple,
  author    = {Tramer, Florian and Boneh, Dan},
  booktitle = {Advances in Neural Information Processing Systems},
  editor    = {H. Wallach and H. Larochelle and A. Beygelzimer and F. d\textquotesingle Alch\'{e}-Buc and E. Fox and R. Garnett},
  publisher = {Curran Associates, Inc.},
  title     = {Adversarial Training and Robustness for Multiple Perturbations},
  volume    = {32},
  year      = {2019}
}

@inproceedings{hsiung2023compositional,
  author    = {Hsiung, Lei and Tsai, Yun-Yun and Chen, Pin-Yu and Ho, Tsung-Yi},
  title     = {Towards Compositional Adversarial Robustness: Generalizing Adversarial Training to Composite Semantic Perturbations},
  booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  month     = {June},
  year      = {2023},
  pages     = {24658--24667}
}

@inproceedings{mendez2022composuite,
  title     = {CompoSuite: A Compositional Reinforcement Learning Benchmark},
  author    = {Mendez, Jorge A. and Hussing, Marcel and Gummadi, Meghna and Eaton, Eric},
  booktitle = {Proceedings of The 1st Conference on Lifelong Learning Agents},
  pages     = {982--1003},
  year      = {2022},
  editor    = {Chandar, Sarath and Pascanu, Razvan and Precup, Doina},
  volume    = {199},
  series    = {Proceedings of Machine Learning Research},
  publisher = {PMLR}
}

@article{zscheischler2018compound,
  title   = {Future climate risk from compound events},
  author  = {Zscheischler, Jakob and Westra, Seth and van den Hurk, Bart J. J. M. and Seneviratne, Sonia I. and Ward, Philip J. and Pitman, Andy and AghaKouchak, Amir and Bresch, David N. and Leonard, Michael and Wahl, Thomas and Zhang, Xuebin},
  journal = {Nature Climate Change},
  volume  = {8},
  number  = {6},
  pages   = {469--477},
  year    = {2018},
  doi     = {10.1038/s41558-018-0156-3}
}

@article{zscheischler2020typology,
  title   = {A typology of compound weather and climate events},
  author  = {Zscheischler, Jakob and Martius, Olivia and Westra, Seth and Bevacqua, Emanuele and Raymond, Colin and Horton, Radley M. and van den Hurk, Bart and AghaKouchak, Amir and J{\'e}z{\'e}quel, Agla{\'e} and Mahecha, Miguel D. and Maraun, Douglas and Ramos, Alexandre M. and Ridder, Nina N. and Thiery, Wim and Vignotto, Edoardo},
  journal = {Nature Reviews Earth \& Environment},
  volume  = {1},
  number  = {7},
  pages   = {333--347},
  year    = {2020},
  doi     = {10.1038/s43017-020-0060-z}
}

@article{crain2008stressors,
  title   = {Interactive and cumulative effects of multiple human stressors in marine systems},
  author  = {Crain, Caitlin Mullan and Kroeker, Kristy and Halpern, Benjamin S.},
  journal = {Ecology Letters},
  volume  = {11},
  number  = {12},
  pages   = {1304--1315},
  year    = {2008},
  doi     = {10.1111/j.1461-0248.2008.01253.x}
}

@article{cote2016stressors,
  title   = {Interactions among ecosystem stressors and their importance in conservation},
  author  = {C{\^o}t{\'e}, Isabelle M. and Darling, Emily S. and Brown, Christopher J.},
  journal = {Proceedings of the Royal Society B: Biological Sciences},
  volume  = {283},
  number  = {1824},
  pages   = {20152592},
  year    = {2016},
  doi     = {10.1098/rspb.2015.2592}
}
```

### DRAFT — UED / DR related-work paragraph (not ratified; owner to edit)

> **DRAFT.** Choosing what an agent trains on is the central object of domain
> randomization and unsupervised environment design. Domain randomization trains
> on a fixed distribution over simulator parameters so that deployment looks like
> one more draw (Tobin et al., 2017; reviewed by Muratore et al., 2022). Chen et al.
> (2022) bound the resulting sim-to-real gap and show that history-dependent
> policies matter. UED instead adapts the distribution to the learner. PAIRED
> generates levels from a protagonist–antagonist regret (Dennis et al., 2020);
> Prioritized Level Replay resamples levels by estimated learning potential and was
> later recast as UED (Jiang et al., 2021a; 2021b); ACCEL evolves levels at the
> frontier of the agent's ability (Parker-Holder et al., 2022). Our question — can
> a policy trained on stressors in isolation handle them co-occurring? — is the
> combinatorial-interpolation case in Kirk et al.'s (2023) taxonomy. For
> imitation-learned manipulation, Gao et al. (2024) find that policies trained on
> data varying one factor at a time do compose at unseen combinations, under a
> matched budget of factor changes. Robust RL poses the same question for
> perturbations: agents trained against single-type attacks remain vulnerable to
> mixed state-and-action attacks (Erdem & Üre, 2025), and simultaneous uncertainty
> in several environment variables has been formulated as its own MARL robustness
> problem (Agrawal et al., 2023). We differ in what the comparison holds fixed.
> None of these works, to our search, matches the arms on how much of training
> carries any stressor at all. In CHE that one quantity accounts for the
> joint-training advantage, so a comparison that leaves it free can report an
> exposure effect as a composition effect. We compare two fixed training
> distributions and do not evaluate adaptive curricula (§10).

Notes for the owner on the draft. It contains no CHE numbers by design (sub-rule:
numbers enter documents derived). The Gao et al. 77.5% / 2.5% figures are left out
of the draft on purpose. The "to our search" hedge is load-bearing: this search was
web-level, not exhaustive, and IEEE Xplore was not queried.

---

## Scoop risk

**Bottom line: no scoop found.** No retrieved RL/MARL work compares training on
co-occurring stressors against training on the same stressors in isolation
**while matching active share (the fraction of training carrying any stressor) or
per-stressor marginals**. The paper's claimed separation stands **on this search**:
abstract-level, web search plus arXiv API, no IEEE Xplore, no full-text reads.

Ranked neighbours a reviewer could raise:

1. **Gao et al., RSS 2024 — moderate risk on the *question*, low on the *design*.**
   It is the closest design analogue: one-factor-at-a-time vs joint-coverage
   training data, compared at a matched budget. But the budget is *effort*
   (factor changes), not active share or marginals. It is imitation learning with
   benign visual/physical factors, not survival under a lethal stressor, and it
   finds composition *works*. **Must cite**, and say precisely which quantity each
   design matches.
2. **Erdem & Üre, MAKE 2025 — moderate on the question, low on the design.** Same
   joint-vs-isolated question in adversarial robust RL. Its headline ("single-type
   training … remain[s] highly vulnerable to mixed perturbations") runs *opposite*
   to CHE's matched-share null, which a reviewer may bring up. Differences: an
   adversarial perturbation budget vs an ambient, non-adversarial stressor. Its
   exposure design is **unverified** (MDPI full text blocked); read the paper before
   claiming it does not match exposure.
3. **Agrawal et al., NeurIPS 2023 workshop — low.** Multi-uncertainty robust MARL
   via a noise curriculum. [HTML summary]: no control of total exposure or
   per-factor marginals.
4. **Chen et al., ICLR 2022 — not a scoop of the empirical claim.** It is the
   nearest value-gap theorem for a training distribution (DR) and emphasizes memory.
   The decision log's "no theorem of E2C's form" conclusion predates this search.
   **Owner should read it before claiming Thm. 1 is unsubsumed.**
5. **VULCAN — low, but it touches a spine claim.** It is a hazard + smoke +
   sensor-degradation multi-agent fire environment. That is a neighbour for the
   Coupling B claim ("Beer–Lambert on a POMDP observation kernel: none found").
   Per [HTML summary] it uses no Beer–Lambert/transmittance model and no RL, so the
   claim survives. Cite VULCAN there rather than let a reviewer find it.
6. **Vision adversarial robustness (Tramèr & Boneh 2019; Hsiung et al. 2023) —
   low.** Single vs multiple/composite perturbation training, not RL, not exposure-matched.

**Items that are not scoops but are wrong in the repo and should be fixed before
submission:** VULCAN's CMDP framing (item 1); the "burning cells" label on
arXiv:2604.26150 (item 15); POBAX/BenchMARL in the JAX × MARL row (item 12); the
stale 2507.10142 "hiding place" note (item 16); and SMART, which could not be found
and should not be cited as it stands (item 4).
