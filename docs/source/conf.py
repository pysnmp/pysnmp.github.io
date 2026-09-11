"""Sphinx configuration for the pysnmp organization site.

This builds https://pysnmp.github.io/ -- the front page of the organization,
not the documentation for any one package. Each project publishes its own
versioned documentation to https://pysnmp.github.io/<project>/ from its own
repository; everything here links out to those rather than restating them,
because a copy of an API reference is a copy that goes stale.
"""

# -- Project information -----------------------------------------------------

project = "pysnmp"
author = "The pysnmp maintainers"
copyright = "2005-2019, Ilya Etingof; 2022-2026, the pysnmp maintainers"

# The site is not versioned -- it describes whatever is current -- so there is
# nothing sensible to put in |version| or |release|, and the theme is
# configured below not to show them.
version = ""
release = ""

# -- General configuration ---------------------------------------------------

extensions = [
    # Pages are reStructuredText, but CONTRIBUTING.md and the rest of the
    # organization's health files are Markdown. myst_parser is here so a page
    # can include one rather than paraphrase it.
    "myst_parser",
    "sphinx.ext.extlinks",
]

source_suffix = {".rst": "restructuredtext", ".md": "markdown"}
master_doc = "index"
language = "en"
templates_path = [".templates"]
exclude_patterns = []
pygments_style = "sphinx"

# The three places this site refers to constantly. `:rfc:` is built into
# Sphinx; these are the ones that are not.
extlinks = {
    "repo": ("https://github.com/pysnmp/%s", "pysnmp/%s"),
    "docs": ("https://pysnmp.github.io/%s/", "%s documentation"),
}
extlinks_detect_hardcoded_links = True

# -- Options for HTML output -------------------------------------------------

html_theme = "furo"

# The same theme the three project documentation sites use, so moving between
# them is moving within one site. furo supplies its own sidebar and needs no
# html_sidebars; the logo is a theme option rather than the standard setting.
html_theme_options = {
    "light_logo": "logo.svg",
    "dark_logo": "logo.svg",
    "source_repository": "https://github.com/pysnmp/pysnmp.github.io/",
    "source_branch": "main",
    "source_directory": "docs/source/",
}

html_title = "pysnmp"
html_short_title = "pysnmp"
html_favicon = ".static/favicon.ico"
html_static_path = [".static"]
html_css_files = ["site.css"]
html_show_sourcelink = False
html_copy_source = False

# -- Options for the link checker --------------------------------------------

# This site is mostly links, so `sphinx-build -b linkcheck` is the test suite.
# CI runs it on a schedule rather than on every pull request: a link rots on
# someone else's timetable, not on ours, and a third-party outage should not
# fail an unrelated change.
linkcheck_anchors = False
linkcheck_timeout = 30
linkcheck_retries = 2
linkcheck_ignore = [
    # Every module under these two is generated and neither tree carries an
    # HTML index, so a HEAD against the directory is a 404 by design. The
    # distribution's own documentation sits at the site root and is checked
    # like any other link.
    r"https://pysnmp\.github\.io/mibs/asn1/.*",
    r"https://pysnmp\.github\.io/mibs/json/.*",
    # Reporting forms: GitHub answers these with a login redirect for anyone
    # not signed in, which the checker reads as a failure.
    r"https://github\.com/pysnmp/[^/]+/security/advisories/new",
]
