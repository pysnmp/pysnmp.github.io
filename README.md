# .github

Two things live here: the organisation's GitHub configuration, and the source
of the landing page at
**<https://pysnmp.github.io/.github/>**.

## The site

`www/` is the source; `_site/` is what a build produces and is not committed.
The page is generated from one content file, so adding a project or moving a
documentation URL is an edit to TOML rather than to markup.

```
www/
├── build.py      the generator: renders templates against site.toml
├── site.toml     every claim the page makes -- projects, endpoints, example
├── templates/    Jinja2, extending base.html.jinja
└── static/       stylesheet, logo and favicon (shared with the Sphinx docs)
```

Build it:

```bash
uv sync
uv run python www/build.py          # writes ./_site
python -m http.server -d _site      # http://localhost:8000
```

`build.py` fails the build when `site.toml` is missing a field the templates
need or when a referenced asset is absent, so CI catches a broken page before
it is published rather than after.

Every link on the page is relative, so the built tree serves correctly from
this repository's project page and would serve unchanged from an organisation
root (a `pysnmp.github.io` repository) if the site is ever moved there.

## CI

| Workflow | What it does |
|---|---|
| `ci.yml` | pre-commit, Ruff, mypy, and a build of the site uploaded as an artifact so a pull request can be reviewed as the rendered page |
| `site-publish.yml` | builds and pushes to `gh-pages` on a push to `main` that touches `www/`, and on dispatch |
| `commit-conventions.yml` | commitlint over a pull request's commits, the same check the other repositories run |

`gh-pages` holds exactly what the build produced: the publish job clears the
branch before copying, so a file the site no longer emits leaves the branch
with it and a re-run repairs whatever is there.

## Toolchain

The same one the rest of the organisation uses: [uv](https://docs.astral.sh/uv/)
for environments and locking, [Ruff](https://docs.astral.sh/ruff/) for lint and
formatting, mypy in strict mode, and pre-commit over all of it. Python 3.14.

```bash
uv sync
pre-commit install
```

## The projects this page points at

| | |
|---|---|
| [pysnmp](https://github.com/pysnmp/pysnmp) | the SNMP v1/v2c/v3 engine |
| [pysmi](https://github.com/pysnmp/pysmi) | the SMI MIB parser and compiler |
| [pyasn1](https://github.com/pysnmp/pyasn1) | ASN.1 types and BER/CER/DER codecs |
| [mibs](https://github.com/pysnmp/mibs) | the MIB corpus, served over HTTP |
