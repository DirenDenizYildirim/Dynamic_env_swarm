"""Compile-only memory probe for the population training step (M5.1g).

Why this exists. The gate configuration failed to compile twice: first at
float32 obs (11.39 GiB trajectory), then again after uint8 storage fixed
that, this time wanting 49.08 GiB. Arithmetic says the dominant term is no
longer storage but *backprop activations across the population vmap* —
98,304 agent-rows per minibatch x ~18.7 KiB of retained convolution
activations x 12 members, doubled by the backward pass, which lands within
3 % of XLA's own 49.08 GiB. Arithmetic is not measurement, and choosing a
remedy from arithmetic is how the ÷81 projection happened.

So: lower and compile each candidate ahead of time and ask XLA what it
would need. Compilation with autotuning disabled does not allocate the
working set, so candidates that cannot run can still be *priced* — and when
XLA refuses outright, the requirement it names is itself the measurement,
so that is parsed out rather than discarded.

Nothing here changes a config. It prints what each option would cost, which
is the input to a human scope decision, not a substitute for one.

  uv run python -m che.bench.memprobe --config che/configs/gate_pop12.yaml
"""

import argparse
import dataclasses
import json
import re

GIB = 2**30


def _candidates(cfg):
    """(label, config, what-it-changes) — engineering-neutral options first,
    then the ones that alter the experiment."""
    t = cfg.train

    def with_train(**kw):
        return dataclasses.replace(cfg, train=dataclasses.replace(t, **kw))

    return [
        ("baseline", cfg, "as committed"),
        ("remat", with_train(remat=True),
         "recompute activations; same hyperparameters, same updates"),
        ("remat+nmb8", with_train(remat=True, n_minibatches=8),
         "remat + smaller minibatch (CHANGES optimization)"),
        ("nmb8", with_train(n_minibatches=8),
         "smaller minibatch (CHANGES optimization)"),
        ("nmb16", with_train(n_minibatches=16),
         "smaller minibatch (CHANGES optimization)"),
        ("pop6", with_train(pop_size=6), "half the population (CHANGES the design)"),
        # The gate config took rung 2 (256 -> 128) on 2026-07-29, so the
        # next rung-2 application is the one worth pricing. Rungs 1/3/4
        # are unavailable (they move calibrated quantities) — see
        # decision_log.md "Phase-5 delegated rulings".
        (f"envs{t.n_envs // 2}", with_train(n_envs=t.n_envs // 2),
         "half the envs per member again (fallback-ladder rung 2)"),
    ]


def probe(cfg) -> dict:
    """Compile the population chunk AOT; return its predicted memory."""
    import jax

    from che.train.pbt import make_pbt_fns

    fns = make_pbt_fns(cfg)
    # eval_shape gives the Runner's structure without allocating a byte of it.
    shape = jax.eval_shape(fns.init, jax.random.PRNGKey(0))
    try:
        analysis = fns.chunk.lower(shape).compile().memory_analysis()
    except Exception as exc:  # noqa: BLE001 — the failure text carries the number
        text = str(exc)
        wanted = re.findall(r"([\d.]+)\s*GiB", text)
        return {
            "ok": False,
            "wanted_gib": max(float(w) for w in wanted) if wanted else None,
            "error": text.strip().splitlines()[0][:200],
        }
    if analysis is None:  # some backends decline to report
        return {"ok": True, "temp_gib": None, "total_gib": None}
    temp = getattr(analysis, "temp_size_in_bytes", 0) or 0
    args = getattr(analysis, "argument_size_in_bytes", 0) or 0
    out = getattr(analysis, "output_size_in_bytes", 0) or 0
    alias = getattr(analysis, "alias_size_in_bytes", 0) or 0
    return {
        "ok": True,
        "temp_gib": temp / GIB,
        "argument_gib": args / GIB,
        "output_gib": out / GIB,
        # Peak is what has to fit: transient workspace plus the live
        # arguments and outputs that are not aliased onto each other.
        "total_gib": (temp + args + out - alias) / GIB,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--config", default="che/configs/gate_pop12.yaml")
    p.add_argument("--out-json")
    p.add_argument("--only", help="comma-separated subset of candidate labels")
    args = p.parse_args()

    from che.env.config import load_config

    base = load_config(args.config)
    wanted = set(args.only.split(",")) if args.only else None
    rows = []
    for label, cfg, note in _candidates(base):
        if wanted and label not in wanted:
            continue
        print(f"[memprobe] compiling {label} ...", flush=True)
        r = probe(cfg)
        r.update(label=label, note=note, n_minibatches=cfg.train.n_minibatches,
                 pop_size=cfg.train.pop_size, n_envs=cfg.train.n_envs,
                 uint8_obs=cfg.train.uint8_obs, remat=cfg.train.remat)
        rows.append(r)
        if r["ok"]:
            print(f"           total {r['total_gib']:.2f} GiB "
                  f"(temp {r['temp_gib']:.2f})", flush=True)
        else:
            w = r["wanted_gib"]
            print(f"           DID NOT COMPILE — wanted "
                  f"{w:.2f} GiB" if w else "           DID NOT COMPILE", flush=True)

    # M5.1j: the toolchain goes in the artifact. The m51g -> m51i comparison
    # (24.69 -> 27.53 GiB for a byte-identical config) could not be resolved
    # into "code changed" vs "toolchain changed" because neither run recorded
    # a jax/jaxlib version — the env-only-throughput mistake in a different
    # unit. See decision_log.md, "Phase-5 delegated rulings, round 2".
    from che.bench.rowb_probe import toolchain

    tc = toolchain()
    print(f"\n[memprobe] jax {tc['jax']} / jaxlib {tc['jaxlib']} on "
          f"{tc['backend']} ({tc['device_kind']})")

    print("\n" + "=" * 72)
    print(f"{'candidate':12s} {'peak GiB':>10s}  changes")
    print("-" * 72)
    for r in rows:
        peak = (f"{r['total_gib']:.2f}" if r["ok"] and r["total_gib"] is not None
                else (f">{r['wanted_gib']:.2f}" if r.get("wanted_gib") else "?"))
        print(f"{r['label']:12s} {peak:>10s}  {r['note']}")
    print("=" * 72)
    print("A candidate that fits is not automatically the right choice: remat")
    print("preserves the experiment exactly (same hyperparameters, same")
    print("updates, loss verified identical), while n_minibatches / pop_size /")
    print("n_envs change what is being run. That trade is a human call.")
    if args.out_json:
        # The toolchain rides in the artifact as its own labelled row, after
        # the candidates so the table loop above never sees it.
        json.dump(rows + [{"label": "_toolchain", **tc}],
                  open(args.out_json, "w"), indent=1)


if __name__ == "__main__":
    main()
