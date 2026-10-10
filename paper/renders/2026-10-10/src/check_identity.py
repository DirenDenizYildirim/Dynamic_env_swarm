"""Checks behind paper/renders/2026-10-10/README.md. Run AFTER render_restyle.py.

Usage, from the repo root (thread-capped, CPU):

    OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 \
    XLA_FLAGS=--xla_cpu_multi_thread_eigen=false \
    taskset -c 0-3 nice -n 15 uv run python \
      paper/renders/2026-10-10/src/check_identity.py \
      --scratch <scratch dir> --rerun-dir <dir holding the README-command reruns>

1. Original renderer determinism: the committed 2026-09-27 GIFs vs GIFs made
   by re-running `che.scripts.render_episode` with the README's exact
   commands (done beforehand into --rerun-dir): file sha256 and decoded
   frame-by-frame pixel equality.
2. Per-frame state digests, in THIS process (a different process from the
   render): the original rollout untapped (A), the original rollout tapped
   (B), and the digests the restyle render recorded (R). Asserts A == B == R
   on the frame-dict arrays and B == R on the full drawn state (structure
   and weak included), for every frame.
3. Redraw: B's frames drawn with the ORIGINAL draw code and animation
   settings (render_episode.main, verbatim settings) must reproduce the
   committed GIFs pixel for pixel.
4. Informational, grades nothing: the first frame at which the hazard and
   structure fields of two episodes differ. All three share the episode key,
   and the fire CA's keys do not depend on actions (env.step splits them
   from the step key alone), so fire can differ between policies only
   through collapses, whose rate reads agent load (Def. 5), and the
   Coupling A ignitions they seed.
5. Metadata of every output file: GIF block inventory (only graphic-control
   and the NETSCAPE2.0 loop block allowed), PNG chunk inventory (no text,
   time or EXIF chunk), and a raw-byte search for identifying strings.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

import episodes as E
import numpy as np
from PIL import Image, ImageSequence

COMMITTED = E.REPO / "paper/renders/2026-09-27"
README_TAGS = {  # --tag values of the 2026-09-27 README commands
    "thetastar_random_seed0": "random policy, theta*",
    "thetastar_iso_s1_T1000_ep0": "ISO policy (seed 1, T=1000), theta*",
    "thetastar_joint_s1_T1000_ep0": "JOINT policy (seed 1, T=1000), theta*",
}
README_EVERY, README_FPS = 2, 12
# Generic strings; the identity strings proper (user, home, host, repo path,
# git user.name / user.email) are read at run time, so no name is written
# into this file or into the report (which records only how many were used).
GENERIC_FORBIDDEN = [
    b"home/",
    b"/tmp",
    b"claude",
    b"github",
    b"gitlab",
    b"dynamic_env",
    b"swarm",
    b"gmail",
    b"anthropic",
    b"matplotlib",
    b"pillow",
    b"software",
    b"author",
    b"comment",
    b"copyright",
]


def runtime_identity_strings() -> list[bytes]:
    import getpass
    import socket
    import subprocess

    vals = [getpass.getuser(), socket.gethostname(), str(Path.home()), str(E.REPO)]
    for key in ("user.name", "user.email"):
        r = subprocess.run(
            ["git", "config", key],
            capture_output=True,
            text=True,
            cwd=E.REPO,
            check=False,
        )
        vals.append(r.stdout.strip())
    toks = set()
    for v in vals:
        for t in v.replace("@", " ").replace("/", " ").replace(".", " ").split():
            if len(t) >= 4:
                toks.add(t.lower().encode())
        if v:
            toks.add(v.lower().encode())
    return sorted(toks)


FORBIDDEN = GENERIC_FORBIDDEN + runtime_identity_strings()


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def gif_frames(p: Path):
    im = Image.open(p)
    return [
        (np.asarray(f.convert("RGB")).copy(), f.info.get("duration"))
        for f in ImageSequence.Iterator(im)
    ]


def compare_gifs(a: Path, b: Path) -> dict:
    fa, fb = gif_frames(a), gif_frames(b)
    pairs = zip(fa, fb, strict=False)  # unequal lengths are reported, not raised
    differing = [
        i
        for i, ((x, _), (y, _)) in enumerate(pairs)
        if x.shape != y.shape or not np.array_equal(x, y)
    ]
    return {
        "frames": [len(fa), len(fb)],
        "size_px": [list(Image.open(a).size), list(Image.open(b).size)],
        "differing_frames": differing,
        "durations_equal": [d for _, d in fa] == [d for _, d in fb],
        "file_sha256_equal": sha(a) == sha(b),
        "pixel_identical": len(fa) == len(fb) and not differing,
    }


def redraw_original(frames, ecfg, tag: str, out: Path):
    """render_episode.main()'s drawing and saving, with its settings."""
    import matplotlib.pyplot as plt
    from matplotlib import animation

    RE = E.RE
    shown = frames[::README_EVERY]
    if shown[-1] is not frames[-1]:
        shown.append(frames[-1])
    fig, ax = plt.subplots(figsize=(5.4, 5.8), dpi=110)
    anim = animation.FuncAnimation(
        fig,
        lambda f: RE.draw_frame(ax, f, ecfg.n_agents, ecfg.grid_size, tag),
        frames=shown,
        interval=1000 // README_FPS,
    )
    anim.save(out, writer=animation.PillowWriter(fps=README_FPS))
    plt.close(fig)


def gif_blocks(p: Path) -> dict:
    b = p.read_bytes()
    if b[:6] not in (b"GIF87a", b"GIF89a"):
        raise ValueError("not a GIF")
    flags, i = b[10], 13
    if flags & 0x80:
        i += 3 * (2 ** ((flags & 7) + 1))
    blocks: Counter = Counter()

    def skip_subblocks(i):
        while True:
            n = b[i]
            i += 1
            if n == 0:
                return i
            i += n

    while True:
        c = b[i]
        i += 1
        if c == 0x3B:
            break
        if c == 0x21:
            label = b[i]
            i += 1
            if label == 0xFF:
                key = "application:" + b[i + 1 : i + 1 + b[i]].decode("latin1")
            else:
                key = {
                    0xF9: "graphic_control",
                    0xFE: "COMMENT",
                    0x01: "PLAIN_TEXT",
                }.get(label, f"ext_{label:#x}")
            blocks[key] += 1
            i = skip_subblocks(i)
        elif c == 0x2C:
            blocks["image"] += 1
            fl = b[i + 8]
            i += 9
            if fl & 0x80:
                i += 3 * (2 ** ((fl & 7) + 1))
            i = skip_subblocks(i + 1)
        else:
            raise ValueError(f"unexpected GIF byte {c:#x} at {i - 1}")
    return {
        "version": b[:6].decode(),
        "blocks": dict(blocks),
        "bytes_after_trailer": len(b) - i,
    }


def png_chunks(p: Path) -> list[str]:
    b = p.read_bytes()
    assert b[:8] == b"\x89PNG\r\n\x1a\n"
    i, out = 8, []
    while i < len(b):
        n = int.from_bytes(b[i : i + 4], "big")
        out.append(b[i + 4 : i + 8].decode("latin1"))
        i += 12 + n
    return out


def metadata_check(p: Path) -> dict:
    raw = p.read_bytes().lower()
    hits = [
        "generic:" + s.decode() if s in GENERIC_FORBIDDEN else "identity"
        for s in FORBIDDEN
        if s in raw
    ]
    rec = {
        "file": str(p.relative_to(E.OUT_ROOT)),
        "bytes": p.stat().st_size,
        "sha256": sha(p),
        "identifying_string_hits": hits,
    }
    if p.suffix == ".gif":
        g = gif_blocks(p)
        allowed = {"graphic_control", "application:NETSCAPE2.0", "image"}
        rec.update(g)
        rec["only_allowed_blocks"] = set(g["blocks"]) <= allowed
        rec["ok"] = (
            rec["only_allowed_blocks"] and not hits and not g["bytes_after_trailer"]
        )
    else:
        ch = png_chunks(p)
        rec["chunks"] = dict(Counter(ch))
        rec["ok"] = set(ch) <= {"IHDR", "PLTE", "IDAT", "IEND"} and not hits
    return rec


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--scratch", required=True, type=Path)
    p.add_argument("--rerun-dir", required=True, type=Path)
    args = p.parse_args(argv)
    report = {
        "episodes": {},
        "metadata": [],
        "metadata_search": {
            "generic_strings": [s.decode() for s in GENERIC_FORBIDDEN],
            "runtime_identity_strings_searched": len(FORBIDDEN)
            - len(GENERIC_FORBIDDEN),
        },
    }
    all_ok = True
    fields: dict[str, dict[str, list[np.ndarray]]] = {}
    for ep in E.EPISODES:
        stem = ep["stem"]
        rec: dict = {}
        # 1. committed vs README-command rerun
        rec["committed_vs_rerun"] = compare_gifs(
            COMMITTED / f"{stem}.gif", args.rerun_dir / f"{stem}.gif"
        )
        # 2. digests
        ecfg, policy, prov = E.build(ep, args.scratch)
        fa = E.untapped_rollout(ecfg, policy)
        fb, sb = E.tapped_rollout(ecfg, policy)
        fields[stem] = {k: [s[k] for s in sb] for k in ("hazard", "structure")}
        dA = [E.frame_digest(f) for f in fa]
        dB = [E.frame_digest(f) for f in fb]
        sB = [E.state_digest(s) for s in sb]
        R = json.loads((E.OUT_ROOT / "provenance" / f"{stem}.restyle.json").read_text())
        n = len(dA)
        rec["digests"] = {
            "n_frames": n,
            "frame_dict_untapped_eq_tapped": dA == dB,
            "frame_dict_original_eq_restyle": dA == R["frame_digests"],
            "full_state_original_tapped_eq_restyle": sB == R["state_digests"],
            "first_differing_frame": next(
                (
                    i
                    for i in range(n)
                    if not (
                        dA[i] == dB[i] == R["frame_digests"][i]
                        and sB[i] == R["state_digests"][i]
                    )
                ),
                None,
            ),
            "frame_digest_chain_original": E.chain(dA),
            "frame_digest_chain_restyle": R["frame_digest_chain"],
            "state_digest_chain_original_tapped": E.chain(sB),
            "state_digest_chain_restyle": R["state_digest_chain"],
        }
        # 3. redraw B with the original draw code
        out = args.scratch / "redraw" / f"{stem}.gif"
        out.parent.mkdir(parents=True, exist_ok=True)
        redraw_original(fb, ecfg, README_TAGS[stem], out)
        rec["tapped_frames_redrawn_with_original_code_vs_committed"] = compare_gifs(
            COMMITTED / f"{stem}.gif", out
        )
        ok = (
            rec["committed_vs_rerun"]["pixel_identical"]
            and rec["digests"]["frame_dict_untapped_eq_tapped"]
            and rec["digests"]["frame_dict_original_eq_restyle"]
            and rec["digests"]["full_state_original_tapped_eq_restyle"]
            and rec["tapped_frames_redrawn_with_original_code_vs_committed"][
                "pixel_identical"
            ]
        )
        rec["ok"] = ok
        all_ok &= ok
        report["episodes"][stem] = rec
        print(stem, "OK" if ok else "FAILED")
    # 4. cross-episode divergence (informational)
    stems = [ep["stem"] for ep in E.EPISODES]
    cross = {}
    for i, a in enumerate(stems):
        for b in stems[i + 1 :]:
            rec = {}
            for k in ("hazard", "structure"):
                pairs = zip(fields[a][k], fields[b][k], strict=True)
                diff = [t for t, (x, y) in enumerate(pairs) if not np.array_equal(x, y)]
                rec[f"{k}_first_differing_t"] = diff[0] if diff else None
                rec[f"{k}_frames_differing"] = len(diff)
            cross[f"{a} vs {b}"] = rec
    report["cross_episode_informational"] = cross
    print(json.dumps(cross, indent=1))
    # 5. metadata of every output image
    for f in sorted((E.OUT_ROOT / "gif").glob("*.gif")) + sorted(
        (E.OUT_ROOT / "img").glob("*.png")
    ):
        m = metadata_check(f)
        all_ok &= m["ok"]
        report["metadata"].append(m)
        print(m["file"], m["bytes"], "OK" if m["ok"] else "FAILED")
    report["all_ok"] = all_ok
    (E.OUT_ROOT / "provenance" / "identity_check.json").write_text(
        json.dumps(report, indent=1) + "\n"
    )
    if not all_ok:
        raise SystemExit("CHECK FAILED")


if __name__ == "__main__":
    main()
