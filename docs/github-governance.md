# GitHub Governance

AthenaStack governance provides change traceability, protects the default
branch, and creates a professional CI/CD learning environment.

## Repository Policy

* Direct changes to `main` are prohibited.
* All changes must flow through pull requests.
* Every pull request must reference a GitHub Issue.
* Pull-request titles must begin with `#<issue-number>`.
* Pull-request bodies must include `Closes #<issue-number>`.

## Automated Enforcement

The PR Policy workflow validates:

* issue linkage;
* pull-request title format;
* matching issue numbers in the title and description;
* that the referenced item is an open GitHub Issue rather than another pull
  request.

## Required Checks

The intended required checks are:

* PR Policy;
* MegaLinter;
* Docker Compose Validation;
* AthenaStack Policy Validation.

## Branch Ruleset

The `main` branch ruleset must:

* require a pull request before merging;
* prohibit force pushes;
* prohibit branch deletion;
* leave the bypass list empty;
* require the approved CI status checks.

Until the ruleset is active, failed checks report violations but may not
prevent a merge.
