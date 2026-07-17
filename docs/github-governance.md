# GitHub Governance

## Rules
- No direct commits to `main`.
- All work flows through Pull Requests.
- Every PR references a GitHub Issue.
- PR titles begin with `#<issue-number>`.
- PR body includes `Closes #<issue-number>`.

## Required Checks
- PR Policy
- MegaLinter
- Docker Compose Validation
- AthenaStack Policy Validation

This governance exists to practice professional workflows.
## Repository Policy

- Direct changes to `main` are prohibited.
- All changes must flow through pull requests.
- Every pull request must reference a GitHub Issue.
- Pull-request titles must begin with `#<issue-number>`.
- Pull-request bodies must include `Closes #<issue-number>`.

## Automated Enforcement

The PR Policy workflow validates issue linkage and title format.

## Branch Ruleset

The `main` ruleset must:

- require a pull request;
- prohibit force pushes and deletion;
- leave the bypass list empty;
- require the approved CI status checks.

Until the ruleset is active, failed checks report violations but may not
prevent a merge.
