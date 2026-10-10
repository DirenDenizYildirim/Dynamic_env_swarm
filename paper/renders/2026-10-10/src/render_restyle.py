"""Restyled renders of the three 2026-09-27 episodes: presentation only.

Usage, from the repo root (thread-capped, CPU):

    OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 \
    XLA_FLAGS=--xla_cpu_multi_thread_eigen=false \
    taskset -c 0-3 nice -n 15 uv run python \
      paper/renders/2026-10-10/src/render_restyle.py --scratch <scratch dir>

The trajectory is the original renderer's (`episodes.tapped_rollout`, which
calls `che.scripts.render_episode.rollout_frames` unmodified). This file only
draws it. What is drawn, per cell, is the state as it is:

- hazard h (Def. 3): flat fill. fuel = light, burning = orange, burnt = dark.
- smoke rho (Def. 6), the ENVIRONMENT's density field (not any agent's
  view): diagonal light hatching whose opacity is proportional to rho on
  [0, 1], shown in 16 equal steps. The run asserts rho <= 1 on every frame
  (burning lasts one step, so rho' = 1 on a burning cell and decays by
  e^-eta afterwards); the ramp therefore needs no clipping.
- weak floor (state.weak, Def. 5 substrate): a centre dot on weak cells that
  are still intact.
- collapsed floor (state.structure == COLLAPSED): a boxed X (the drafting
  symbol for a floor void), dark on light cells and white on burnt ones; the
  triangles between the strokes keep the cell's hazard fill, because a
  collapsed cell still has a fire state.
- food (state.food, the task variable): aqua square with a dark ring.
- agents (state.agent_pos, state.agent_alive): blue disc with white and dark
  rings if alive; a hollow dark ring with white either side if dead.

Labels are factual only: the policy and "t = k / 256". No counter, score or
tally is drawn. The three episodes are styled identically and written as
separate files.

Collapse-seeded ignitions (Coupling A) are NOT marked: the step's `info`
exposes only their per-step count (`seeded_ignitions`), and the per-cell
mask is internal to `che.env.env.step`. They are drawn as ordinary burning
cells.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import episodes as E
import matplotlib  # only to locate the bundled DejaVu font files
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from che.env.types import BURNING, BURNT, COLLAPSED, FUEL, INTACT

# --- geometry ---------------------------------------------------------------
S = 8  # pixels per grid cell (integer, nearest-neighbour by construction)
PAD = 8  # surface around the arena, so markers on the walls are not clipped
MX = 16  # outer margin
HEADER = 44
LEGEND_GAP = 14

# --- colour -----------------------------------------------------------------
# Marks use the first three slots of the dataviz reference palette (blue,
# orange, aqua), which pass its all-pairs CVD and normal-vision checks. The
# hazard states are told apart by LIGHTNESS first (fuel light, burning mid,
# burnt dark), so the map reads in greyscale; smoke, weak floor and collapse
# are patterns, not hues.


def _hex(h: str) -> np.ndarray:
    h = h.lstrip("#")
    return np.array([int(h[i : i + 2], 16) for i in (0, 2, 4)], dtype=np.float64)


SURFACE = _hex("#fcfcfb")
INK = _hex("#0b0b0b")
INK2 = _hex("#52514e")
MUTED = _hex("#898781")
WHITE = _hex("#ffffff")
FUEL_C = _hex("#e9ebe0")
BURNING_C = _hex("#eb6834")
BURNT_C = _hex("#3d3a36")
SMOKE_C = _hex("#f4f1eb")
GRID_C = _hex("#8c8a83")
AGENT_C = _hex("#2a78d6")
FOOD_C = _hex("#1baf7a")

HAZ_C = np.zeros((3, 3))
HAZ_C[FUEL], HAZ_C[BURNING], HAZ_C[BURNT] = FUEL_C, BURNING_C, BURNT_C
GRID_MIX = 0.16
SMOKE_LEVELS = 16  # rho shown in 16 equal steps on [0, 1]
SMOKE_ALPHA = 0.9  # hatch opacity at rho = 1
DOT_MIX = 0.5
# weak-floor dot: darker than a light cell, lighter than a dark one
DOT_C = np.zeros((3, 3))
DOT_C[FUEL] = FUEL_C * (1 - DOT_MIX) + INK * DOT_MIX
DOT_C[BURNING] = BURNING_C * (1 - DOT_MIX) + INK * DOT_MIX
DOT_C[BURNT] = BURNT_C * (1 - DOT_MIX) + WHITE * DOT_MIX

VOID_C = np.zeros((3, 3))
VOID_C[FUEL], VOID_C[BURNING], VOID_C[BURNT] = INK, INK, WHITE

FONT_DIR = Path(matplotlib.get_data_path()) / "fonts" / "ttf"
F_LABEL = ImageFont.truetype(str(FONT_DIR / "DejaVuSans-Bold.ttf"), 17)
F_TIME = ImageFont.truetype(str(FONT_DIR / "DejaVuSans.ttf"), 15)
F_LEG = ImageFont.truetype(str(FONT_DIR / "DejaVuSans.ttf"), 13)
F_TICK = ImageFont.truetype(str(FONT_DIR / "DejaVuSans.ttf"), 11)
TEXT_LEVELS = 12  # anti-aliasing levels kept, so the GIF palette stays exact


# --- the map raster -----------------------------------------------------------


def _up(a: np.ndarray) -> np.ndarray:
    return np.repeat(np.repeat(a, S, axis=0), S, axis=1)


def _sprites():
    d = np.arange(-7, 8)
    dy, dx = np.meshgrid(d, d, indexing="ij")
    r2 = dy**2 + dx**2
    alive = np.full(dy.shape, -1, dtype=np.int8)  # -1 = transparent
    alive[r2 <= 6.6**2] = 0  # dark outer ring
    alive[r2 <= 5.6**2] = 1  # white ring
    alive[r2 <= 4.5**2] = 2  # fill
    # dead: a hollow ring (dark, with white either side); the centre stays
    # transparent so the cell underneath remains visible
    dead = np.full(dy.shape, -1, dtype=np.int8)
    dead[r2 <= 6.6**2] = 1
    dead[r2 <= 5.6**2] = 0
    dead[r2 <= 3.6**2] = 1
    dead[r2 <= 2.6**2] = -1
    return alive, dead


SPRITE_ALIVE, SPRITE_DEAD = _sprites()
SPRITE_C = {0: INK, 1: WHITE, 2: AGENT_C}


def compose_map(hazard, smoke, weak, structure, food, pos, alive) -> np.ndarray:
    """RGB uint8 raster of one state, (rows*S + 2*PAD) x (cols*S + 2*PAD)."""
    nh, nw = hazard.shape[0] * S, hazard.shape[1] * S
    img = _up(HAZ_C[hazard])
    yy, xx = np.indices((nh, nw))
    py, px = yy % S, xx % S
    grid = (py == S - 1) | (px == S - 1)
    img[grid] = img[grid] * (1 - GRID_MIX) + GRID_C * GRID_MIX
    # smoke rho: hatch opacity proportional to rho, 16 steps on [0, 1]
    level = np.rint(np.asarray(smoke, np.float64) * (SMOKE_LEVELS - 1))
    alpha = _up(level / (SMOKE_LEVELS - 1) * SMOKE_ALPHA)
    hatch = ((xx + yy) % 4 == 0) & ~grid & (alpha > 0)
    a = alpha[hatch][:, None]
    img[hatch] = img[hatch] * (1 - a) + SMOKE_C * a
    # weak floor, still intact: centre dot
    dot = (py >= 3) & (py <= 4) & (px >= 3) & (px <= 4)
    m = dot & _up(np.asarray(weak, bool) & (structure == INTACT))
    img[m] = _up(DOT_C[hazard])[m]
    # collapsed floor: the drafting symbol for a floor void (a boxed X),
    # inked dark on light cells and white on the dark burnt cell; the four
    # triangles keep the cell's hazard fill, since a collapsed cell still has
    # a fire state
    inner = (py <= S - 2) & (px <= S - 2)
    void = inner & (
        (py == 0)
        | (py == S - 2)
        | (px == 0)
        | (px == S - 2)
        | (py == px)
        | (py + px == S - 2)
    )
    m = void & _up(structure == COLLAPSED)
    img[m] = _up(VOID_C[hazard])[m]
    # food: aqua 5 x 5 with a dark ring, filling the cell interior
    fd = _up(np.asarray(food).astype(bool))
    f_in = (py >= 1) & (py <= S - 3) & (px >= 1) & (px <= S - 3)
    f_ring = inner & ~f_in
    img[fd & f_ring] = INK
    img[fd & f_in] = FOOD_C
    # pad, then agents (dead first, alive on top)
    out = np.empty((nh + 2 * PAD, nw + 2 * PAD, 3))
    out[:] = SURFACE
    out[PAD : PAD + nh, PAD : PAD + nw] = img
    # arena border: one muted line just outside the cells
    out[PAD - 1, PAD - 1 : PAD + nw + 1] = MUTED
    out[PAD + nh, PAD - 1 : PAD + nw + 1] = MUTED
    out[PAD - 1 : PAD + nh + 1, PAD - 1] = MUTED
    out[PAD - 1 : PAD + nh + 1, PAD + nw] = MUTED
    pos = np.asarray(pos)
    alive = np.asarray(alive, bool)
    for sprite, which in ((SPRITE_DEAD, ~alive), (SPRITE_ALIVE, alive)):
        for r, c in pos[which]:
            cy, cx = PAD + int(r) * S + 3, PAD + int(c) * S + 3
            win = out[cy - 7 : cy + 8, cx - 7 : cx + 8]
            for v, colr in SPRITE_C.items():
                win[sprite == v] = colr
    return np.rint(out).astype(np.uint8)


# --- text and legend ------------------------------------------------------------


def draw_text(img: np.ndarray, xy, text, font, ink, anchor="la"):
    """Composite text with anti-aliasing quantized to TEXT_LEVELS levels."""
    h, w = img.shape[:2]
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).text(xy, text, font=font, fill=255, anchor=anchor)
    m = np.asarray(mask, np.float64)
    step = 255 / (TEXT_LEVELS - 1)
    a = (np.rint(m / step) * step / 255.0)[..., None]
    region = a[..., 0] > 0
    img[region] = np.rint(img[region] * (1 - a[region]) + ink * a[region]).astype(
        np.uint8
    )


def text_width(text, font) -> int:
    x0, _, x1, _ = font.getbbox(text)
    return x1 - x0


def _swatch(kind: str) -> np.ndarray:
    """3 x 3 cells drawn by compose_map itself, so the key is exact."""
    hz = np.full((3, 3), FUEL, np.uint8)
    sm = np.zeros((3, 3), np.float32)
    wk = np.zeros((3, 3), bool)
    stc = np.full((3, 3), INTACT, np.uint8)
    fd = np.zeros((3, 3), np.uint8)
    pos = np.zeros((0, 2), np.int32)
    al = np.zeros((0,), bool)
    if kind == "burning":
        hz[:] = BURNING
        sm[:] = 1.0  # a burning cell always carries rho = 1 (Def. 6, 1-step burn)
    elif kind == "burnt":
        hz[:] = BURNT
    elif kind == "weak":
        wk[:] = True
    elif kind == "collapsed":
        wk[:] = True
        stc[1, 1] = COLLAPSED
    elif kind == "food":
        fd[1, 1] = 1
    elif kind in ("agent", "dead"):
        pos = np.array([[1, 1]], np.int32)
        al = np.array([kind == "agent"])
    full = compose_map(hz, sm, wk, stc, fd, pos, al)
    # drop the pad and the last gridline
    return full[PAD : PAD + 3 * S - 1, PAD : PAD + 3 * S - 1]


def _smoke_ramp() -> np.ndarray:
    lv = np.arange(SMOKE_LEVELS, dtype=np.float32) / (SMOKE_LEVELS - 1)
    sm = np.tile(lv, (2, 1))
    hz = np.full(sm.shape, BURNT, np.uint8)
    full = compose_map(
        hz,
        sm,
        np.zeros(sm.shape, bool),
        np.full(sm.shape, INTACT, np.uint8),
        np.zeros(sm.shape, np.uint8),
        np.zeros((0, 2), np.int32),
        np.zeros((0,), bool),
    )
    return full[PAD : PAD + 2 * S - 1, PAD : PAD + SMOKE_LEVELS * S - 1]


def _frame(img, y, x, h, w):
    """Hairline (muted) just outside a legend swatch."""
    c = MUTED.astype(np.uint8)
    img[y - 1, x - 1 : x + w + 1] = c
    img[y + h, x - 1 : x + w + 1] = c
    img[y - 1 : y + h + 1, x - 1] = c
    img[y - 1 : y + h + 1, x + w] = c


LEGEND_ITEMS = (
    ("fuel", "fuel"),
    ("burning", "burning"),
    ("burnt", "burnt"),
    ("weak", "weak floor"),
    ("collapsed", "collapsed floor"),
    ("food", "food item"),
    ("agent", "agent"),
    ("dead", "agent, dead"),
)
ROW_H = 30
SMOKE_TEXT = "smoke density ρ (environment field)"


def legend_height(cols: int) -> int:
    rows = -(-len(LEGEND_ITEMS) // cols)
    return rows * ROW_H + 36


def draw_legend(img: np.ndarray, x0: int, y0: int, width: int, cols: int):
    colw = width // cols
    for i, (kind, label) in enumerate(LEGEND_ITEMS):
        r, c = divmod(i, cols)
        x, y = x0 + c * colw, y0 + r * ROW_H
        sw = _swatch(kind)
        img[y : y + sw.shape[0], x : x + sw.shape[1]] = sw
        _frame(img, y, x, sw.shape[0], sw.shape[1])
        draw_text(
            img,
            (x + sw.shape[1] + 8, y + sw.shape[0] // 2),
            label,
            F_LEG,
            INK2,
            anchor="lm",
        )
    rows = -(-len(LEGEND_ITEMS) // cols)
    y = y0 + rows * ROW_H + 2
    draw_text(img, (x0, y + 7), SMOKE_TEXT, F_LEG, INK2, anchor="lm")
    ramp = _smoke_ramp()
    rx = x0 + text_width(SMOKE_TEXT, F_LEG) + 14
    img[y : y + ramp.shape[0], rx : rx + ramp.shape[1]] = ramp
    _frame(img, y, rx, ramp.shape[0], ramp.shape[1])
    for frac, lab in ((0.0, "0"), (0.5, "0.5"), (1.0, "1")):
        cx = rx + int(round(frac * (ramp.shape[1] - 1)))
        draw_text(img, (cx, y + ramp.shape[0] + 2), lab, F_TICK, MUTED, anchor="ma")


# --- frames -----------------------------------------------------------------------


def time_label(t: int, horizon: int) -> str:
    return f"t = {t} / {horizon}"


def gif_background(label: str, map_px: int) -> tuple[np.ndarray, int]:
    w = map_px + 2 * MX
    leg_y = HEADER + map_px + LEGEND_GAP
    h = leg_y + legend_height(3) + 6
    bg = np.empty((h, w, 3), np.uint8)
    bg[:] = SURFACE.astype(np.uint8)
    draw_text(bg, (MX + PAD, HEADER // 2 + 1), label, F_LABEL, INK, anchor="lm")
    draw_legend(bg, MX + PAD, leg_y, map_px - 2 * PAD, cols=3)
    return bg, HEADER


def gif_frame(bg, y_map, mp, t, horizon) -> np.ndarray:
    f = bg.copy()
    f[y_map : y_map + mp.shape[0], MX : MX + mp.shape[1]] = mp
    draw_text(
        f,
        (MX + mp.shape[1] - PAD, HEADER // 2 + 1),
        time_label(t, horizon),
        F_TIME,
        INK2,
        anchor="rm",
    )
    return f


def static_strip(label: str, maps: list[np.ndarray], ts: list[int], horizon: int):
    gap = 16
    mpx = maps[0].shape[1]
    w = 2 * MX + 3 * mpx + 2 * gap
    top = HEADER + 24
    leg_y = top + mpx + LEGEND_GAP
    h = leg_y + legend_height(4) + 6
    img = np.empty((h, w, 3), np.uint8)
    img[:] = SURFACE.astype(np.uint8)
    draw_text(img, (MX + PAD, HEADER // 2 + 1), label, F_LABEL, INK, anchor="lm")
    for i, (mp, t) in enumerate(zip(maps, ts, strict=True)):
        x = MX + i * (mpx + gap)
        img[top : top + mp.shape[0], x : x + mpx] = mp
        draw_text(
            img, (x + PAD, top - 6), time_label(t, horizon), F_TIME, INK2, anchor="ls"
        )
    draw_legend(img, MX + PAD, leg_y, 2 * mpx, cols=4)
    return img


# --- exact palette, GIF and PNG writers -----------------------------------------


class ExactPalette:
    """Maps RGB frames to indices with no approximation; fails past 256."""

    def __init__(self):
        self.index: dict[int, int] = {}

    def encode(self, rgb: np.ndarray) -> np.ndarray:
        key = (
            (rgb[..., 0].astype(np.uint32) << 16)
            | (rgb[..., 1].astype(np.uint32) << 8)
            | rgb[..., 2]
        )
        uniq, inv = np.unique(key, return_inverse=True)
        for u in uniq.tolist():
            if u not in self.index:
                self.index[u] = len(self.index)
        if len(self.index) > 256:
            raise SystemExit(f"{len(self.index)} colours: GIF palette would be lossy")
        lut = np.array([self.index[u] for u in uniq.tolist()], np.uint8)
        return lut[inv].reshape(key.shape)

    def flat(self) -> list[int]:
        pal = [0] * 768
        for u, i in self.index.items():
            pal[3 * i : 3 * i + 3] = [(u >> 16) & 255, (u >> 8) & 255, u & 255]
        return pal


def to_p(idx: np.ndarray, pal: ExactPalette) -> Image.Image:
    im = Image.fromarray(idx, mode="P")
    im.putpalette(pal.flat())
    return im


def write_gif(path: Path, idx_frames, pal, durations_ms):
    ims = [to_p(f, pal) for f in idx_frames]
    ims[0].info.clear()
    ims[0].save(
        path,
        save_all=True,
        append_images=ims[1:],
        duration=durations_ms,
        loop=0,
        optimize=False,
        disposal=1,
    )


def write_png(path: Path, rgb: np.ndarray):
    pal = ExactPalette()
    idx = pal.encode(rgb)
    im = to_p(idx, pal)
    im.info.clear()
    im.save(path, format="PNG", optimize=True)


# --- main ------------------------------------------------------------------------

FPS = 20  # every step shown (257 frames, t = 0..256)
HOLD_FIRST_MS = 800
HOLD_LAST_MS = 2500


def render_episode(ep: dict, scratch: Path, out_root: Path) -> dict:
    ecfg, policy, prov = E.build(ep, scratch)
    frames, states = E.tapped_rollout(ecfg, policy)
    horizon = int(ecfg.horizon)
    rho_max_seen = float(max(s["smoke"].max() for s in states))
    if rho_max_seen > 1.0:
        raise SystemExit(f"rho reached {rho_max_seen} > 1: the smoke ramp would clip")
    maps = [
        compose_map(
            s["hazard"],
            s["smoke"],
            s["weak"],
            s["structure"],
            s["food"],
            s["agent_pos"],
            s["agent_alive"],
        )
        for s in states
    ]
    bg, y_map = gif_background(ep["label"], maps[0].shape[1])
    pal = ExactPalette()
    idx_frames = [
        pal.encode(gif_frame(bg, y_map, mp, s["t"], horizon))
        for mp, s in zip(maps, states, strict=True)
    ]
    dur = [1000 // FPS] * len(idx_frames)
    dur[0], dur[-1] = HOLD_FIRST_MS, HOLD_LAST_MS
    gif_path = out_root / "gif" / f"{ep['stem']}.gif"
    write_gif(gif_path, idx_frames, pal, dur)
    mid = len(states) // 2
    pick = [0, mid, len(states) - 1]
    strip = static_strip(
        ep["label"], [maps[i] for i in pick], [states[i]["t"] for i in pick], horizon
    )
    png_path = out_root / "img" / f"{ep['stem']}_static.png"
    write_png(png_path, strip)
    infos = [s["info"] for s in states[1:]]
    return {
        "stem": ep["stem"],
        "label": ep["label"],
        **prov,
        "n_frames": len(states),
        "t_first": states[0]["t"],
        "t_last": states[-1]["t"],
        "static_frames_t": [states[i]["t"] for i in pick],
        "gif_palette_colours": len(pal.index),
        "rho_max_seen": rho_max_seen,
        "episode_info_totals": {
            "collapse_events": int(sum(i["collapse_events"] for i in infos)),
            "seeded_ignitions": int(sum(i["seeded_ignitions"] for i in infos)),
        },
        "frame_digests": [E.frame_digest(f) for f in frames],
        "state_digests": [E.state_digest(s) for s in states],
    }


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--scratch",
        required=True,
        type=Path,
        help="where verified checkpoint archives are extracted",
    )
    p.add_argument("--only", default=None, help="render one stem (debugging)")
    args = p.parse_args(argv)
    out_root = E.OUT_ROOT
    (out_root / "gif").mkdir(parents=True, exist_ok=True)
    (out_root / "img").mkdir(parents=True, exist_ok=True)
    (out_root / "provenance").mkdir(parents=True, exist_ok=True)
    for ep in E.EPISODES:
        if args.only and ep["stem"] != args.only:
            continue
        rec = render_episode(ep, args.scratch, out_root)
        rec["frame_digest_chain"] = E.chain(rec["frame_digests"])
        rec["state_digest_chain"] = E.chain(rec["state_digests"])
        out = out_root / "provenance" / f"{ep['stem']}.restyle.json"
        out.write_text(json.dumps(rec, indent=1) + "\n")
        print(
            ep["stem"],
            rec["n_frames"],
            "frames, palette",
            rec["gif_palette_colours"],
            "state chain",
            rec["state_digest_chain"],
        )


if __name__ == "__main__":
    main()
