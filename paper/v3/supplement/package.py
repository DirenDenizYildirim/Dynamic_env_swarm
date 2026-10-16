"""Assemble the anonymized code supplement (Paper v3, V3-V1).

    .venv/bin/python paper/v3/supplement/package.py            # default build
    .venv/bin/python paper/v3/supplement/package.py --help     # switches

What it does, in order:

  1. SELECT files from the working tree by rule (`rules.INCLUDE`), starting
     from what git would track (tracked + untracked-not-ignored). Re-runnable:
     files added later in the phase are picked up by the same rules.
  2. STAGE a copy into a temporary directory. Text files are SCRUBBED in the
     copy (`rules.SCRUBS` plus commit-hash redaction); every rewrite is logged.
     The source tree is never written.
  3. RECONSTRUCT `.manifest/<tag>.done` entries (default on, `--no-manifests`)
     for result directories that ship eval JSONs. The grid wrote one entry per
     run and DERIVED `SHA256_CKPT.txt` by concatenating them
     (`che/scripts/lib_run_manifest.sh`, `manifest_write_aggregate`). The
     entries themselves are excluded by `.gitignore` (`*.manifest`), so the
     registered instruments refuse to run on a fresh checkout. Splitting the
     committed aggregate back into per-tag entries is the exact inverse.
  4. Write the neutral README.md and SHA256SUMS (every file's sha256).
  5. ZIP deterministically to `paper/v3/out/che_supplement.zip`.

Logs (NOT shipped; they quote the original strings) go to `paper/v3/out/`:
`selection_log.tsv`, `excluded_summary.txt`, `scrub_log.tsv`, `build_summary.json`.
"""

from __future__ import annotations

import argparse
import bisect
import collections
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE))
import rules as R  # noqa: E402

TOP = "che_supplement"
ZIP_DATE = (1980, 1, 1, 0, 0, 0)


# ------------------------------------------------------------------ select


def git_files() -> list[str]:
    out = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=REPO,
        capture_output=True,
        check=True,
    ).stdout
    seen, files = set(), []
    for raw in out.split(b"\0"):
        if not raw:
            continue
        p = raw.decode()
        if p in seen:
            continue
        seen.add(p)
        files.append(p)
    return sorted(files)


def known_commits() -> list[str]:
    out = subprocess.run(
        ["git", "rev-list", "--all", "--reflog"],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.split()
    return sorted(set(out))


def select(files: list[str], opts: argparse.Namespace):
    chosen: list[tuple[str, str]] = []
    excluded: list[tuple[str, str]] = []
    rules = [r for r in R.INCLUDE if r.option is None or getattr(opts, r.option)]
    pats = [(r, re.compile(r.pattern)) for r in rules]
    notes = [(re.compile(p), why) for p, why in R.EXCLUDE_NOTES]
    for f in files:
        src = REPO / f
        if src.is_symlink():
            excluded.append((f, "symlink (not shipped)"))
            continue
        if not src.is_file():
            excluded.append((f, "absent from the working tree"))
            continue
        deny = next((w for p, w in R.DENY if re.fullmatch(p, f)), None)
        if deny is not None:
            excluded.append((f, deny))
            continue
        hit = next((r for r, rx in pats if rx.fullmatch(f)), None)
        if hit is None:
            why = next(w for rx, w in notes if rx.fullmatch(f))
            excluded.append((f, why))
            continue
        if src.stat().st_size > R.MAX_FILE_BYTES:
            excluded.append(
                (f, f"larger than {R.MAX_FILE_BYTES} bytes (rule {hit.rid})")
            )
            continue
        chosen.append((f, hit.rid))
    return chosen, excluded


# ------------------------------------------------------------------ scrub


class Scrubber:
    def __init__(self, commits: list[str]):
        self.commits = commits
        self.map: dict[str, str] = {}  # full commit -> placeholder
        self.log: list[tuple[str, int, str, str, str]] = []

    def _commit_for(self, tok: str) -> str | None:
        i = bisect.bisect_left(self.commits, tok)
        if i < len(self.commits) and self.commits[i].startswith(tok):
            return self.commits[i]
        return None

    def _placeholder(self, full: str) -> str:
        if full not in self.map:
            self.map[full] = f"COMMIT_REDACTED_{len(self.map) + 1:02d}"
        return self.map[full]

    def scrub_path(self, rel: str) -> str:
        """Commit hashes inside a FILE NAME (e.g. requirement_<commit>.txt).

        The same placeholder replaces the hash in the name and in every text
        that refers to it, so references stay consistent."""

        def sub(m: re.Match) -> str:
            full = self._commit_for(m.group(1))
            if full is None:
                return m.group(0)
            ph = self._placeholder(full)
            self.log.append((rel, 0, "PATH-COMMIT", m.group(1), ph))
            return ph

        return R.HEX_TOKEN.sub(sub, rel)

    def scrub(self, rel: str, text: str) -> str:
        def lineno(s: str, pos: int) -> int:
            return s.count("\n", 0, pos) + 1

        for sc in R.SCRUBS:
            if sc.skip and re.fullmatch(sc.skip, rel):
                continue
            if not sc.regex.search(text):
                continue
            pieces, last = [], 0
            for m in sc.regex.finditer(text):
                self.log.append(
                    (rel, lineno(text, m.start()), sc.rid, m.group(0), sc.repl)
                )
                pieces += [text[last : m.start()], sc.repl]
                last = m.end()
            pieces.append(text[last:])
            text = "".join(pieces)

        # Commit hashes: a 7-40 hex token that prefixes a commit in this
        # repository's history; and any 40-hex in a git context (it may be a
        # commit of a ref this checkout does not have).
        pieces, last = [], 0
        for m in R.HEX_TOKEN.finditer(text):
            tok = m.group(1)
            full = self._commit_for(tok)
            rid = "COMMIT"
            if full is None and len(tok) == 40:
                ctx = text[max(0, m.start() - 40) : m.end()]
                if R.GIT_CONTEXT_40.search(ctx):
                    full, rid = tok, "COMMIT-CTX"
            if full is None:
                continue
            ph = self._placeholder(full)
            self.log.append((rel, lineno(text, m.start()), rid, tok, ph))
            pieces += [text[last : m.start()], ph]
            last = m.end()
        if pieces:
            pieces.append(text[last:])
            text = "".join(pieces)
        return text


def is_text(rel: str, data: bytes) -> bool:
    suf = Path(rel).suffix.lower()
    if suf not in R.TEXT_SUFFIXES:
        return False
    if b"\0" in data[:8192]:
        return False
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return True


# ------------------------------------------------------------------ extras


def reconstruct_manifests(stage: Path, log: list[str]) -> int:
    """Inverse of lib_run_manifest.sh::manifest_write_aggregate, per directory."""
    n = 0
    for agg in sorted((stage / "che/bench/results").rglob("SHA256_CKPT.txt")):
        d = agg.parent
        if not any(d.glob("eval_*.json")):
            continue
        entries: dict[str, str] = {}
        for ln in agg.read_text().splitlines():
            if not ln.strip():
                continue
            parts = ln.split()
            if len(parts) != 2:
                raise SystemExit(f"unexpected line in {agg}: {ln!r}")
            tag = Path(parts[1]).name
            if not (tag.startswith("ckpt_") and tag.endswith(".tar.zst")):
                raise SystemExit(f"unexpected archive name in {agg}: {ln!r}")
            tag = tag[len("ckpt_") : -len(".tar.zst")]
            if tag in entries:
                raise SystemExit(f"duplicate tag {tag} in {agg}")
            entries[tag] = ln + "\n"
        md = d / ".manifest"
        md.mkdir(exist_ok=True)
        for tag, ln in entries.items():
            (md / f"{tag}.done").write_text(ln)
            n += 1
        (md / "RECONSTRUCTED.txt").write_text(
            "These per-run completion entries were RECONSTRUCTED when the\n"
            "supplement was packaged. The originals are excluded from version\n"
            "control by a .gitignore pattern. Each entry is the line for its\n"
            "run in ../SHA256_CKPT.txt, which the grid derived by concatenating\n"
            "the entries (che/scripts/lib_run_manifest.sh,\n"
            "manifest_write_aggregate). They let the registered analysis\n"
            "scripts, which require an entry per evaluated run, run on the\n"
            "committed artifacts. The checkpoint archives they name are not\n"
            "included.\n"
        )
        log.append(f"{d.relative_to(stage)}: {len(entries)} entries")
    return n


def decision_log_excerpts(patterns: list[str]) -> str | None:
    if not patterns:
        return None
    text = (REPO / "docs/decision_log.md").read_text()
    secs = re.split(r"(?m)^(?=## )", text)
    keep = [
        s
        for s in secs
        if s.startswith("## ")
        and any(re.search(p, s.splitlines()[0]) for p in patterns)
    ]
    if not keep:
        raise SystemExit(f"--decision-log-section matched no heading: {patterns}")
    head = (
        "# Decision-log excerpts\n\nVerbatim sections of the project's decision "
        "log, selected for this supplement. Other sections are omitted.\n\n"
    )
    return head + "\n".join(keep)


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def write_zip(stage: Path, zpath: Path) -> None:
    tmp = zpath.with_suffix(".zip.tmp")
    files = sorted(p for p in stage.rglob("*") if p.is_file())
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in files:
            rel = p.relative_to(stage).as_posix()
            zi = zipfile.ZipInfo(f"{TOP}/{rel}", date_time=ZIP_DATE)
            mode = 0o755 if (p.stat().st_mode & stat.S_IXUSR) else 0o644
            zi.external_attr = (stat.S_IFREG | mode) << 16
            zi.compress_type = zipfile.ZIP_DEFLATED
            with open(p, "rb") as f:
                z.writestr(zi, f.read(), compresslevel=9)
    os.replace(tmp, zpath)


# ------------------------------------------------------------------ main


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--out", type=Path, default=REPO / "paper/v3/out")
    ap.add_argument("--zip-name", default="che_supplement.zip")
    ap.add_argument(
        "--stage",
        type=Path,
        default=None,
        help="keep the staged tree here (must not exist); default: a "
        "temporary directory that is deleted",
    )
    ap.add_argument(
        "--no-theory",
        dest="theory",
        action="store_false",
        help="leave out docs/theory_foundations.md (rule D3)",
    )
    ap.add_argument(
        "--no-lock-records",
        dest="lock_records",
        action="store_false",
        help="leave out the *_lock.md records (rule D4)",
    )
    ap.add_argument(
        "--conf-logs",
        dest="conf_logs",
        action="store_true",
        help="add the confirmatory arms' training logs (rule R6, ~23 MB compressed)",
    )
    ap.add_argument(
        "--no-manifests",
        dest="manifests",
        action="store_false",
        help="do not reconstruct .manifest entries (the registered "
        "instruments will then refuse to run)",
    )
    ap.add_argument(
        "--decision-log-section",
        action="append",
        default=[],
        metavar="REGEX",
        help="OWNER DECISION, off by default: ship the decision-log "
        "sections whose '## ' heading matches REGEX (repeatable), "
        "as docs/decision_log_excerpts.md",
    )
    opts = ap.parse_args(argv)

    opts.out.mkdir(parents=True, exist_ok=True)
    files = git_files()
    chosen, excluded = select(files, opts)
    scrubber = Scrubber(known_commits())

    tmpdir = None
    if opts.stage is None:
        tmpdir = tempfile.mkdtemp(prefix="che_supp_")
        stage = Path(tmpdir) / TOP
    else:
        stage = opts.stage
        if stage.exists():
            raise SystemExit(f"--stage {stage} exists; refusing to overwrite")
    stage.mkdir(parents=True)

    try:
        n_text = n_bin = 0
        for rel, _rid in chosen:
            src = REPO / rel
            dst = stage / scrubber.scrub_path(rel)
            dst.parent.mkdir(parents=True, exist_ok=True)
            data = src.read_bytes()
            if is_text(rel, data):
                dst.write_text(
                    scrubber.scrub(rel, data.decode("utf-8")), encoding="utf-8"
                )
                n_text += 1
            else:
                dst.write_bytes(data)
                n_bin += 1
            if src.stat().st_mode & stat.S_IXUSR:
                dst.chmod(0o755)

        extras: list[str] = []
        man_log: list[str] = []
        if opts.manifests:
            n_man = reconstruct_manifests(stage, man_log)
            extras.append(f"reconstructed {n_man} .manifest entries")
        dl = decision_log_excerpts(opts.decision_log_section)
        if dl is not None:
            p = stage / "docs/decision_log_excerpts.md"
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(scrubber.scrub("docs/decision_log_excerpts.md", dl))
            extras.append("docs/decision_log_excerpts.md (owner-selected)")
        shutil.copyfile(HERE / "SHIPPED_README.md", stage / "README.md")

        sums = []
        for p in sorted(q for q in stage.rglob("*") if q.is_file()):
            rel = p.relative_to(stage).as_posix()
            sums.append(f"{sha256(p)}  {rel}\n")
        (stage / "SHA256SUMS").write_text("".join(sums))

        zpath = opts.out / opts.zip_name
        write_zip(stage, zpath)

        # ---- logs (not shipped)
        with open(opts.out / "selection_log.tsv", "w") as f:
            f.write("path\trule\tbytes\n")
            for rel, rid in chosen:
                f.write(f"{rel}\t{rid}\t{(REPO / rel).stat().st_size}\n")
        ex = collections.defaultdict(lambda: [0, 0])
        for rel, why in excluded:
            p = REPO / rel
            sz = p.stat().st_size if p.is_file() and not p.is_symlink() else 0
            ex[why][0] += 1
            ex[why][1] += sz
        with open(opts.out / "excluded_summary.txt", "w") as f:
            f.write("# files left out, by reason: count  bytes(uncompressed)  reason\n")
            for why, (n, sz) in sorted(ex.items(), key=lambda kv: -kv[1][1]):
                f.write(f"{n:6d}  {sz:13d}  {why}\n")
        with open(opts.out / "scrub_log.tsv", "w") as f:
            f.write("path\tline\trule\tbefore\tafter\n")
            for rel, ln, rid, before, after in scrubber.log:
                f.write(f"{rel}\t{ln}\t{rid}\t{before}\t{after}\n")
        by_rule = collections.Counter(r for _, r in chosen)
        bytes_by_rule = collections.Counter()
        for rel, rid in chosen:
            bytes_by_rule[rid] += (REPO / rel).stat().st_size
        summary = {
            "zip": str(zpath.relative_to(REPO)),
            "zip_bytes": zpath.stat().st_size,
            "zip_sha256": sha256(zpath),
            "files_shipped": len(sums) + 1,
            "files_selected": len(chosen),
            "text_scrubbed": n_text,
            "binary_copied": n_bin,
            "by_rule": {
                k: {"files": by_rule[k], "bytes": bytes_by_rule[k]}
                for k in sorted(by_rule)
            },
            "options": {
                "theory": opts.theory,
                "lock_records": opts.lock_records,
                "conf_logs": opts.conf_logs,
                "manifests": opts.manifests,
                "decision_log_section": opts.decision_log_section,
            },
            "extras": extras,
            "manifest_dirs": man_log,
            "scrub_rewrites": len(scrubber.log),
            "scrub_rewrites_by_rule": dict(
                collections.Counter(x[2] for x in scrubber.log)
            ),
            "commits_redacted": len(scrubber.map),
        }
        (opts.out / "build_summary.json").write_text(
            json.dumps(summary, indent=1) + "\n"
        )
        print(json.dumps(summary, indent=1))
    finally:
        if tmpdir is not None:
            shutil.rmtree(tmpdir, ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
