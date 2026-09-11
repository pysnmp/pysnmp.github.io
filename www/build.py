#!/usr/bin/env python3
"""Render the pysnmp organisation landing page.

Reads ``site.toml`` beside this file, renders ``templates/`` against it with
Jinja2 and writes the result, plus everything under ``static/``, into the
output directory. The output is self-contained and uses relative links only,
so the same tree serves correctly from a project page under ``/<repo>/`` and
from an organisation root.

Usage: build.py [output directory]   (default: ``_site`` at the repository root)
"""

from __future__ import annotations

import argparse
import pathlib
import shutil
import sys
import tomllib
from typing import Any

from jinja2 import Environment, FileSystemLoader, StrictUndefined

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent

# Rendered one-to-one: each becomes the same name without the .jinja suffix.
# base.html.jinja is extended rather than rendered, so it is not listed.
#
# Every page links to its assets relatively, which is what lets the built tree
# serve unchanged from a project page under /<repo>/ and from an organisation
# root. A page at a deeper path would break that, so pages stay at the root.
PAGES = ("index.html.jinja",)

REQUIRED_PROJECT_KEYS = (
    "id",
    "name",
    "layer",
    "role",
    "tagline",
    "description",
    "repo",
    "docs",
    "install",
    "highlights",
)


class ContentError(Exception):
    """The content file is missing something the templates require."""


def load_content(path: pathlib.Path) -> dict[str, Any]:
    """Read and validate ``site.toml``.

    Validation is here rather than in the templates because StrictUndefined
    reports a missing key as a failure at the point of use, naming the
    template; this names the field and the project instead.
    """
    with path.open("rb") as handle:
        content: dict[str, Any] = tomllib.load(handle)

    for section in ("site", "projects", "endpoints", "start"):
        if section not in content:
            raise ContentError(f"{path.name}: no [{section}] section")

    for project in content["projects"]:
        missing = [key for key in REQUIRED_PROJECT_KEYS if key not in project]
        if missing:
            name = project.get("name", "<unnamed>")
            raise ContentError(f"{path.name}: {name} is missing {', '.join(missing)}")

    content["projects"].sort(key=lambda project: project["layer"])

    return content


def check_assets(static: pathlib.Path) -> None:
    """Fail the build when a file the templates reference is not there.

    A missing stylesheet or favicon costs nothing at build time and shows up
    only as a page that renders wrong once published, which is too late.
    """
    for name in ("style.css", "logo.svg", "favicon.ico"):
        if not (static / name).is_file():
            raise ContentError(f"static/{name} is missing")


def render(content: dict[str, Any], out: pathlib.Path) -> list[pathlib.Path]:
    """Render every page in ``PAGES`` into ``out`` and return what was written."""
    env = Environment(
        loader=FileSystemLoader(HERE / "templates"),
        undefined=StrictUndefined,
        autoescape=True,
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )

    written = []

    for page in PAGES:
        target = out / page.removesuffix(".jinja")
        target.write_text(env.get_template(page).render(**content), encoding="utf-8")
        written.append(target)

    return written


def build(out: pathlib.Path) -> int:
    """Build the site into ``out``, replacing whatever was there."""
    content = load_content(HERE / "site.toml")
    check_assets(HERE / "static")

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    shutil.copytree(HERE / "static", out / "static")

    written = render(content, out)

    # GitHub Pages runs Jekyll over a branch it serves unless told otherwise,
    # and Jekyll drops paths beginning with an underscore.
    (out / ".nojekyll").touch()

    print(
        f"{len(written)} page(s) and {len(list((out / 'static').iterdir()))} assets -> {out}"
    )

    return 0


def main(argv: list[str] | None = None) -> int:
    """Parse the command line and build the site."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "output",
        nargs="?",
        default=ROOT / "_site",
        type=pathlib.Path,
        help="directory to write the site into (default: _site)",
    )
    args = parser.parse_args(argv)

    try:
        return build(args.output)
    except ContentError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
