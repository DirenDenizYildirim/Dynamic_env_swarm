# g1_floors — the August 2026-08-10 G1.2 launch batch; archives REBUILT 2026-09-09

**What this directory is.** The G1.2 launch batch of 2026-08-10 (24 runs on
the first RTX PRO 6000; `../g1/g1_2_report.md`, `ladder.json`, `floors.json`,
`verdict.txt`). Every tracked file here is the original from that date,
restored from git HEAD on 2026-09-09.

**What happened to the archives.** On 2026-09-09 the new re-floor from the
grid card (`../g1_floors_2026-09-08/`) was pulled with rsync into this
directory by mistake: the box wrote its re-floor to the same relative path
(`che/bench/results/phase6/g1_floors`, per `gpu_launch_prompt.md` G1.2),
and the pull was pointed at the same local path without checking that it
already held a different artifact under identical filenames. Result:

- The 24 tracked small files (`eval_*.json/npz`, `*.jsonl`, `timings.txt`,
  `SHA256_CKPT.txt`, `floors.json`, `ladder.json`, `verdict.txt`) were
  overwritten and then **restored byte-for-byte from git** (`git checkout`).
- The 24 raw checkpoint directories `ckpt_<tag>/` (gitignored) were
  **never touched**: the pull excluded `ckpt_*/`. Each holds
  `config_hash.txt` and steps 900, 950, 1000, as on 2026-08-10.
- The 24 gitignored archives `ckpt_<tag>.tar.zst` from 2026-08-10 were
  **overwritten (20) or removed (4)** and no other copy exists on this
  machine. They were **rebuilt** from the intact raw directories with
  `tar --zstd -cf` on 2026-09-09.

**Consequence, stated precisely.** The checkpoint *content* of the August
batch is intact and is what the rebuilt archives contain. The archive
*bytes* are not the originals, so their hashes do **not** match
`SHA256_CKPT.txt` (which records the 2026-08-10 archives and is kept
unchanged as the original record). The rebuilt hashes are in
`SHA256_CKPT_rebuilt_2026-09-09.txt`. Anything that verifies this
directory's archives must use the rebuilt file; anything that cites the
original hashes is citing archives that no longer exist as bytes.

**No number in `g1_2_report.md`, `floors.json`, `ladder.json` or
`verdict.txt` is affected**: all were computed on 2026-08-10 from the eval
files, which are the originals.

**Rule this adds** (recorded in `che/scripts/pull_box_artifacts.sh`):
never pull into a local directory that already contains archives, and
never reuse a results path across rentals. Each card's re-floor gets a
dated local directory.
