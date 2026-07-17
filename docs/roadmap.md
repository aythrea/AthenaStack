# AthenaStack CI/CD Roadmap

## Completed

### Phase 1: Repository Hygiene

* MegaLinter implementation;
* YAML linting;
* Markdown linting;
* GitHub Actions linting.

### Phase 2: Compose Validation

* Docker Compose model validation;
* explicit inventory of managed Compose files;
* proven failure path for unknown Compose properties.

## In Progress

### Phase 3: Platform Policy

* restart-policy validation;
* platform standards documentation;
* environment-configuration conventions;
* policy auditing.

### GitHub Governance

* PR Policy workflow implemented;
* failure behavior tested;
* issue-linked pull requests established;
* main-branch ruleset pending administrative configuration.

## Planned

### Phase 4: Release Engineering

Define how validated changes are packaged, reviewed, approved, and promoted.

### Phase 5: Deployment Readiness

Render deployment configuration and report operational impact before making
changes to the running platform.

### Phase 6: Continuous Deployment

Deploy approved changes to the OpenMediaVault Docker host through a documented
and reproducible process.

### Phase 7: AI-Assisted Operations

Explore AI-assisted change generation only after the underlying repository,
validation, governance, release, and deployment processes are understood.
