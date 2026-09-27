# TMLR Beyond PDF author kit: builder's notes

Written 2026-09-27 in a Claude Code web session, following
`beyond_pdf_scaffold_prompt.md` (milestones S0–S5). **This file is
builder tooling. It never goes into the upload.** The upload is
`submission.md` + `assets/` only (§S1.8).

---

## S0: environment check (2026-09-27)

| check | result |
|---|---|
| `docker` client | present: Docker 29.3.1, buildx, compose |
| Docker daemon | **not running**: no `/var/run/docker.sock`. `dockerd` is installed, but this session's permission classifier **refused** starting it ("Containment Escape"). Not worked around. |
| kit source | reachable: `https://tmlr-beyond-pdf.org/assets/tmlr-beyond-pdf-author-kit.zip`, HTTP 200, `server: GitHub.com` (GitHub Pages) |
| hosts the kit's Docker build needs, probed from the host with `curl -I` | Docker Hub registry 401 (reachable, auth challenge), `deb.debian.org` 200, `rubygems.org` 200, `pypi.org` 200 |

The network policy did not deny any host the build needs. **The blocker is
the Docker daemon**, not the network. The kit's build also needs two hosts
beyond GitHub, PyPI and Docker Hub: the Debian apt mirrors and rubygems.org
(§S1.6). The session brief makes that a stop-and-ask, so it is an open
question for the owner, not a thing this session decides.
