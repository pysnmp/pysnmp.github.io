// The commit convention the other pysnmp repositories use, kept here so a
// contributor writes messages the same way whichever repository they are in.
// Nothing is released from this repository, so a malformed message costs no
// release note -- it costs the shared habit, which is the point of checking it.
//
// One file, two places. The commit-msg hook in .pre-commit-config.yaml checks a
// message as it is written; .github/workflows/commit-conventions.yml checks
// every commit in a pull request. Both read this config, so a message that
// passes locally passes in CI.
export default {
  extends: ["@commitlint/config-conventional"],
  rules: {
    // The same set the sibling repositories allow, restated here so it stays
    // put if the shared preset ever widens it.
    "type-enum": [
      2,
      "always",
      [
        "build",
        "chore",
        "ci",
        "docs",
        "feat",
        "fix",
        "perf",
        "refactor",
        "revert",
        "style",
        "test",
      ],
    ],

    // Bodies are written by tools as often as by hand -- a dependabot body
    // carries compare links, which do not wrap to a column and are not worth
    // failing over.
    "body-max-line-length": [0],
    "footer-max-line-length": [0],

    // The subject is prose and starts with whatever word it starts with --
    // "fix: Windows path handling" is not a style error. The type stays lower
    // case (type-case, from the shared preset).
    "subject-case": [0],
  },
};
