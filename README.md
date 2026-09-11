# pysnmp.github.io

The source of <https://pysnmp.github.io/> — the front page of the
[pysnmp organization](https://github.com/pysnmp). It says what the organization
maintains and points at each project's own documentation; it is not the
documentation for any one of them.

Those live in their own repositories and publish to their own paths under the
same domain:

| Site | Built from |
| --- | --- |
| <https://pysnmp.github.io/> | this repository |
| <https://pysnmp.github.io/pysnmp/> | [pysnmp/pysnmp](https://github.com/pysnmp/pysnmp) |
| <https://pysnmp.github.io/pysmi/> | [pysnmp/pysmi](https://github.com/pysnmp/pysmi) |
| <https://pysnmp.github.io/pyasn1/> | [pysnmp/pyasn1](https://github.com/pysnmp/pyasn1) |
| <https://pysnmp.github.io/mibs/> | [pysnmp/mibs](https://github.com/pysnmp/mibs) |

A project page is served from its own repository's GitHub Pages, so nothing
here can break one — and nothing here should duplicate one either. Link out
instead; a copy of an API reference is a copy that goes stale.

## Building it

Sphinx, with the same theme and the same flags the library repositories use for
their documentation:

```console
$ uv sync --locked
$ uv run --locked --group dev sphinx-build -n -W --keep-going -b html docs/source docs/build
$ python -m http.server -d docs/build
```

`-n` makes an unresolvable cross-reference a warning and `-W` makes every
warning an error, so a dead `:doc:` reference fails the build rather than
shipping. CI runs exactly that command, and so does the deployment.

Check the outbound links — most of this site is links — with:

```console
$ uv run --locked --group dev sphinx-build -b linkcheck docs/source docs/linkcheck
```

That runs weekly in CI rather than on every pull request; see
[`.github/workflows/linkcheck.yml`](.github/workflows/linkcheck.yml).

## Layout

```
docs/source/
├── conf.py        Sphinx configuration, theme, the :repo: and :docs: roles
├── index.rst      the landing page
├── projects.rst   what each repository is and when to reach for it
├── mibs.rst       the MIB distribution, resolving names and translating traps
├── community.rst  reporting, contributing, security
├── history.rst    the fork lineage, and which PyPI package is which
└── .static/       logo, favicon and a few lines of CSS over alabaster
```

`conf.py` defines two roles that keep URLs out of the prose: `` :repo:`pysmi` ``
links to the repository and `` :docs:`pysmi` `` to its documentation site.

## Deployment

A push to `main` runs [`.github/workflows/pages.yml`](.github/workflows/pages.yml),
which builds the site and deploys it as a Pages artifact.

**This requires the repository's Pages source to be set to "GitHub Actions"**
(Settings → Pages → Build and deployment → Source). While it is set to a
branch, GitHub runs Jekyll over `main` and ignores the workflow.

## Contributing

Same toolchain and the same commit conventions as every other repository here:
see [CONTRIBUTING.md](https://github.com/pysnmp/.github/blob/main/CONTRIBUTING.md).
Run `pre-commit install` once per checkout.
