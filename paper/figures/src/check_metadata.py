"""Double-blind check over every file in paper/figures/out/ (rule 7).

PNG: lists every chunk; FAILS on tEXt / zTXt / iTXt / eXIf / tIME.
GIF: walks every block; FAILS on a comment extension (0x21 0xFE) and on any
     application extension other than NETSCAPE2.0 (the loop count).
All files (text and binary): FAILS on identifying strings: the account and
     owner names, home paths, host name, repo hosting, e-mail, IP addresses,
     GPU UUID prefixes, and any commit hash of this repository (full or any
     7+-character prefix that occurs in the file).

The forbidden-string list is built at run time from the environment and the
repository's own history (read-only `git rev-list`), so it is never written
into any output.
"""

from __future__ import annotations

import getpass
import os
import re
import socket
import struct
import subprocess
import sys
from pathlib import Path

from common import OUT, ROOT


def png_chunks(b: bytes) -> list[str]:
    assert b[:8] == b"\x89PNG\r\n\x1a\n"
    i, out = 8, []
    while i < len(b):
        (n,) = struct.unpack(">I", b[i : i + 4])
        out.append(b[i + 4 : i + 8].decode("ascii"))
        i += 12 + n
    return out


def gif_blocks(b: bytes) -> list[str]:
    assert b[:6] in (b"GIF87a", b"GIF89a")
    flags = b[10]
    i = 13 + (3 * (2 ** ((flags & 7) + 1)) if flags & 0x80 else 0)
    out = []
    while i < len(b):
        t = b[i]
        if t == 0x3B:
            out.append("trailer")
            break
        if t == 0x21:
            lab = b[i + 1]
            j = i + 2
            name = {0xF9: "gce", 0xFE: "COMMENT", 0x01: "plaintext", 0xFF: "app"}.get(
                lab, hex(lab)
            )
            if lab == 0xFF:
                name = "app:" + b[j + 1 : j + 12].decode("latin1")
            while b[j] != 0:
                j += b[j] + 1
            out.append(name)
            i = j + 1
        elif t == 0x2C:
            fl = b[i + 9]
            j = i + 10 + (3 * (2 ** ((fl & 7) + 1)) if fl & 0x80 else 0)
            j += 1  # LZW min code size
            while b[j] != 0:
                j += b[j] + 1
            out.append("image")
            i = j + 1
        else:
            raise ValueError(f"bad GIF block 0x{t:02x} at {i}")
    return out


def forbidden() -> list[tuple[str, re.Pattern]]:
    words = {getpass.getuser(), socket.gethostname(), Path.home().name}
    try:
        name = subprocess.run(
            ["git", "config", "user.name"], cwd=ROOT, capture_output=True, text=True
        ).stdout.strip()
        email = subprocess.run(
            ["git", "config", "user.email"], cwd=ROOT, capture_output=True, text=True
        ).stdout.strip()
        words |= {name, email, email.split("@")[0]}
        words |= set(name.replace("-", " ").split())
    except OSError:
        pass
    words = {w for w in words if w and len(w) >= 4}
    pats = [
        (f"identity word #{i}", re.compile(re.escape(w).encode(), re.I))
        for i, w in enumerate(sorted(words))
    ]
    pats += [
        ("home path", re.compile(rb"/home/|/Users/|C:\\\\Users", re.I)),
        ("repo host", re.compile(rb"github|gitlab|bitbucket", re.I)),
        ("e-mail", re.compile(rb"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")),
        ("IPv4", re.compile(rb"\b(?:\d{1,3}\.){3}\d{1,3}\b")),
        ("GPU UUID", re.compile(rb"GPU-[0-9a-f]{6}", re.I)),
        ("rental host", re.compile(rb"vast\.ai|runpod|lambdalabs", re.I)),
        ("scratch path", re.compile(rb"/tmp/|scratchpad", re.I)),
    ]
    return pats


def commit_hashes() -> list[str]:
    r = subprocess.run(
        ["git", "rev-list", "--all"], cwd=ROOT, capture_output=True, text=True
    )
    return [h for h in r.stdout.split() if len(h) == 40]


HEX7 = re.compile(rb"(?<![0-9a-fA-F])[0-9a-f]{7,40}(?![0-9a-fA-F])")


def main() -> int:
    pats = forbidden()
    hashes = commit_hashes()
    files = sorted(p for p in OUT.rglob("*") if p.is_file())
    bad = 0
    for p in files:
        b = p.read_bytes()
        rel = p.relative_to(OUT)
        notes = []
        if p.suffix == ".png":
            ch = png_chunks(b)
            meta = [c for c in ch if c in ("tEXt", "zTXt", "iTXt", "eXIf", "tIME")]
            notes.append("chunks=" + ",".join(dict.fromkeys(ch)))
            if meta:
                notes.append(f"FAIL metadata chunks {meta}")
                bad += 1
        if p.suffix == ".gif":
            bl = gif_blocks(b)
            kinds = sorted(set(bl))
            notes.append("blocks=" + ",".join(kinds))
            if "COMMENT" in bl or any(
                k.startswith("app:") and k != "app:NETSCAPE2.0" for k in bl
            ):
                notes.append("FAIL comment/application block")
                bad += 1
        for lab, pat in pats:
            if pat.search(b):
                notes.append(f"FAIL {lab}")
                bad += 1
        for m in set(HEX7.findall(b)):
            s = m.decode()
            if any(h.startswith(s) for h in hashes):
                notes.append("FAIL commit hash prefix")
                bad += 1
                break
        print(
            f"{'FAIL' if any(n.startswith('FAIL') for n in notes) else 'ok  '} {rel}  "
            + "  ".join(notes)
        )
    print(
        f"\n{len(files)} files checked, {bad} failures; "
        f"{len(hashes)} commit hashes screened"
    )
    return 1 if bad else 0


if __name__ == "__main__":
    os.chdir(ROOT)
    sys.exit(main())
