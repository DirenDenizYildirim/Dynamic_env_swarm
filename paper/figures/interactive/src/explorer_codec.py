"""Compact per-frame encoding for the episode explorer, with a Python decoder
that mirrors the JS decoder line for line (round-trip asserted at build time;
the JS decoder itself is checked under node by test_explorer_decode.py).

Formats (all byte streams are base64 in the page):
- varint: unsigned LEB128.
- zrle(stream of uint8): repeated [zero-run varint][literal-run varint][literals].
- cell lists per frame: [count varint][cell index varint]... for frames 0..T-1.
- bits: numpy.packbits (big-endian bit order within each byte).
"""

from __future__ import annotations

import base64

import numpy as np
from common_web import load_template


def varint(n: int, out: bytearray):
    assert n >= 0
    while True:
        b = n & 0x7F
        n >>= 7
        if n:
            out.append(b | 0x80)
        else:
            out.append(b)
            return


def zrle(a: np.ndarray) -> bytes:
    a = np.ascontiguousarray(a, dtype=np.uint8).ravel()
    out = bytearray()
    n = a.size
    nz = (a != 0).astype(np.int8)
    # run boundaries: positions where nz changes
    edges = np.flatnonzero(np.diff(nz)) + 1
    starts = np.concatenate([[0], edges])
    ends = np.concatenate([edges, [n]])
    runs = list(zip(starts.tolist(), ends.tolist(), nz[starts].tolist(), strict=True))
    k = 0
    while k < len(runs):
        s, e, isnz = runs[k]
        if isnz:  # zero run of length 0, then this literal run
            varint(0, out)
            varint(e - s, out)
            out += a[s:e].tobytes()
            k += 1
            continue
        varint(e - s, out)
        if k + 1 < len(runs):
            s2, e2, _ = runs[k + 1]
            varint(e2 - s2, out)
            out += a[s2:e2].tobytes()
            k += 2
        else:
            varint(0, out)
            k += 1
    return bytes(out)


def cell_lists(masks: np.ndarray) -> bytes:
    """masks: [T, L, L] bool -> per-frame list of flat cell indices."""
    out = bytearray()
    flat = masks.reshape(masks.shape[0], -1)
    for f in range(flat.shape[0]):
        idx = np.flatnonzero(flat[f])
        varint(len(idx), out)
        for c in idx:
            varint(int(c), out)
    return bytes(out)


def hazard_diffs(hz: np.ndarray) -> bytes:
    """[T, L, L] uint8 -> per frame f >= 1: count, then (cell varint, value byte)."""
    out = bytearray()
    flat = hz.reshape(hz.shape[0], -1)
    for f in range(1, flat.shape[0]):
        idx = np.flatnonzero(flat[f] != flat[f - 1])
        varint(len(idx), out)
        for c in idx:
            varint(int(c), out)
            out.append(int(flat[f, c]))
    return bytes(out)


def b64(b: bytes) -> str:
    return base64.b64encode(b).decode("ascii")


# --- decoder (mirror of the JS) ---------------------------------------------
class Reader:
    def __init__(self, b: bytes):
        self.b, self.p = b, 0

    def v(self) -> int:
        n, s = 0, 0
        while True:
            x = self.b[self.p]
            self.p += 1
            n |= (x & 0x7F) << s
            s += 7
            if not x & 0x80:
                return n


def unzrle(b: bytes, n: int) -> np.ndarray:
    r, out, i = Reader(b), np.zeros(n, np.uint8), 0
    while i < n:
        z = r.v()
        i += z
        lit = r.v()
        out[i : i + lit] = np.frombuffer(b, np.uint8, lit, r.p)
        r.p += lit
        i += lit
    return out


def uncell_lists(b: bytes, T: int, L: int) -> np.ndarray:
    r, out = Reader(b), np.zeros((T, L * L), bool)
    for f in range(T):
        for _ in range(r.v()):
            out[f, r.v()] = True
    return out.reshape(T, L, L)


def unhazard(h0: np.ndarray, b: bytes, T: int) -> np.ndarray:
    r = Reader(b)
    out = np.zeros((T, h0.size), np.uint8)
    out[0] = h0.ravel()
    for f in range(1, T):
        out[f] = out[f - 1]
        for _ in range(r.v()):
            c = r.v()
            out[f, c] = b[r.p]
            r.p += 1
    return out.reshape(T, *h0.shape)


JS_DECODER = load_template("decoder.js")
