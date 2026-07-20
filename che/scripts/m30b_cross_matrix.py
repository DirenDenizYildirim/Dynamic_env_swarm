"""M3.0b Audit 2: cross-severity 3x3 evaluation matrix (H1 vs H2).

Evaluates all 9 M3.0 checkpoints (3 training severities x 3 seeds,
dp = 0.5) in all 3 severity environments, 512 episodes per cell, and
writes per-cell npz/json plus `cross_matrix.md` (pooled-over-seeds 3x3
tables for completion, survival, and completion | zero-deaths).

Split-setup note (M3.0b): this driver lives in the MAIN tree but always
executes the pinned M3.0 code — it prepends --worktree (the 8de4976
worktree) to sys.path before importing `che`, so behavioral results come
from exactly the code the checkpoints were trained under, even after
M3.1 merges. The hash guard is satisfied per-checkpoint by loading with
the checkpoint's own TRAINING config; the EVAL config (which differs
only in theta.beta across severities) is then used for the rollouts —
that is the whole point of the cross matrix, and the network is
architecture-identical across severities (same obs_window / planes).

Usage (from the main repo root, after extracting the m30 checkpoints):
  uv run python che/scripts/m30b_cross_matrix.py \
      --worktree ../che-m30 \
      --ckpt-root ../che-m30/che/bench/results/phase3/m30 \
      --out-dir che/bench/results/phase3/m30b
"""

import argparse
import dataclasses
import json
import sys
from pathlib import Path

import numpy as np

SEVERITIES = ("low", "medium", "high")
SEEDS = (0, 1, 2)
DP = 0.5


def cell_tag(train_sev: str, seed: int, eval_sev: str) -> str:
    return f"train_{train_sev}_s{seed}_eval_{eval_sev}"


def run_matrix(worktree: Path, ckpt_root: Path, out: Path, n_episodes: int):
    sys.path.insert(0, str(worktree.resolve()))
    from che.env.config import load_config  # noqa: PLC0415 — pinned worktree code
    from che.eval.harness import evaluate, load_params, summarize  # noqa: PLC0415

    def cfg_for(sev: str):
        cfg = load_config(worktree / f"che/configs/severity_{sev}.yaml")
        return dataclasses.replace(
            cfg,
            env=dataclasses.replace(
                cfg.env,
                theta=dataclasses.replace(cfg.env.theta, death_penalty=DP),
            ),
        )

    cfgs = {sev: cfg_for(sev) for sev in SEVERITIES}
    out.mkdir(parents=True, exist_ok=True)
    for train_sev in SEVERITIES:
        for seed in SEEDS:
            ckpt_dir = ckpt_root / f"ckpt_{train_sev}_dp{DP}_s{seed}"
            params, step = load_params(ckpt_dir, cfgs[train_sev])
            for eval_sev in SEVERITIES:
                tag = cell_tag(train_sev, seed, eval_sev)
                per_ep = evaluate(
                    cfgs[eval_sev], params, n_episodes=n_episodes, seed=0
                )
                np.savez(out / f"{tag}.npz", **per_ep)
                (out / f"{tag}.json").write_text(
                    json.dumps(
                        {
                            "train_severity": train_sev,
                            "train_seed": seed,
                            "eval_severity": eval_sev,
                            "ckpt_dir": str(ckpt_dir),
                            "ckpt_step": step,
                            "n_episodes": n_episodes,
                            "eval_seed": 0,
                            "death_penalty": DP,
                            "metrics": summarize(per_ep),
                        },
                        indent=1,
                    )
                    + "\n"
                )
                print(f"{tag}: done")


def load_pooled(out: Path, train_sev: str, eval_sev: str):
    """Concatenate the 3 seeds' per-episode arrays for one (train, eval) cell."""
    parts = [
        np.load(out / f"{cell_tag(train_sev, s, eval_sev)}.npz") for s in SEEDS
    ]
    return {
        k: np.concatenate([p[k] for p in parts]) for k in parts[0].files
    }


def fmt_table(out: Path, value_fn, caption: str) -> str:
    lines = [
        f"**{caption}** (rows = training severity, cols = eval severity; "
        f"pooled over seeds {list(SEEDS)}, per-episode mean ± std)",
        "",
        "| train \\ eval | " + " | ".join(s.capitalize() for s in SEVERITIES) + " |",
        "|---|" + "---|" * len(SEVERITIES),
    ]
    for train_sev in SEVERITIES:
        row = [f"| **{train_sev.capitalize()}**"]
        for eval_sev in SEVERITIES:
            row.append(value_fn(load_pooled(out, train_sev, eval_sev)))
        lines.append(" | ".join(row) + " |")
    return "\n".join(lines)


def write_report(out: Path, n_episodes: int):
    def mean_std(vals):
        return f"{vals.mean():.3f} ± {vals.std(ddof=1):.3f}"

    completion = fmt_table(
        out, lambda d: mean_std(d["completion"]), "Completion"
    )
    survival = fmt_table(
        out, lambda d: mean_std(d["survival_rate"]), "Survival rate"
    )

    def compl_zero_deaths(d):
        mask = (d["deaths_fire"] + d["deaths_collapse"]) == 0
        n = int(mask.sum())
        if n == 0:
            return "n/a (0 eps)"
        return f"{mean_std(d['completion'][mask])} (N={n})"

    zero = fmt_table(
        out,
        compl_zero_deaths,
        "Completion | zero-deaths (episodes with no fire or collapse deaths)",
    )
    md = "\n\n".join(
        [
            "# M3.0b Audit 2 — cross-severity 3x3 matrix",
            f"9 checkpoints (3 train severities x 3 seeds, dp={DP}) x 3 eval "
            f"envs, {n_episodes} episodes/cell/seed, eval seed 0, stochastic "
            "policy as-trained. Code: pinned 8de4976 worktree.",
            completion,
            survival,
            zero,
            "## Reading (filled in after the numbers exist)",
            "- Fixed policy, varying environment (across a row): TODO",
            "- Fixed environment, varying training (down the Low column): TODO",
        ]
    )
    (out / "cross_matrix.md").write_text(md + "\n")
    print(f"wrote {out / 'cross_matrix.md'}")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--worktree", default="../che-m30")
    p.add_argument("--ckpt-root",
                   help="dir containing the 9 ckpt_{sev}_dp0.5_s{seed} dirs "
                        "(required unless --report-only)")
    p.add_argument("--out-dir", default="che/bench/results/phase3/m30b/cross")
    p.add_argument("--n-episodes", type=int, default=512)
    p.add_argument("--report-only", action="store_true",
                   help="skip evaluation; rebuild cross_matrix.md from npz")
    args = p.parse_args(argv)
    out = Path(args.out_dir)
    if not args.report_only:
        if not args.ckpt_root:
            p.error("--ckpt-root is required unless --report-only")
        run_matrix(Path(args.worktree), Path(args.ckpt_root), out,
                   args.n_episodes)
    write_report(out, args.n_episodes)


if __name__ == "__main__":
    main()
