# AthenaStack Application Standards

## Purpose

AthenaStack defines containerized applications running on an OpenMediaVault
Docker host. Portainer is the current deployment and management interface.

The platform may move toward Compose-native deployment as the CI/CD process
matures. Such a migration will be treated as a separate operational change.

## Deployment Model

* Docker Compose defines independently deployable application stacks.
* Application data persists beneath `/athenamedia/Appdata`.
* Shared storage is mounted from the `/athenamedia` hierarchy.
* CI validates repository content.
* Deployment automation will be introduced separately.

## Restart Policies

Every managed service must explicitly declare a restart policy.

AthenaStack does not require one universal policy because restart behavior
depends on the operational role and failure characteristics of the service.

Allowed values are:

- `no`
- `always`
- `unless-stopped`
- `on-failure`
- `on-failure:<retry-count>`

Using `no` is acceptable when automatic restart could mask a persistent fault
or create an undesirable restart loop.
## Platform Environment

Common, non-secret platform values should be defined once by the deployment
environment and referenced by Compose definitions where supported.

The current shared values are:

* `TZ`;
* `PUID`;
* `PGID`.

### Timezone

AthenaStack uses `America/Chicago` as its platform timezone.

Services should reference the shared `TZ` value only when the image or
application supports configurable timezone behavior. `TZ` affects local-time
presentation; it does not synchronize the container clock.

### LinuxServer Containers

LinuxServer containers should normally reference the shared:

* `PUID`;
* `PGID`;
* `TZ`, when supported by the image.

Exceptions should be intentional and documented.

## Persistent Configuration

The preferred persistent configuration convention is:

```text
/athenamedia/Appdata/<application>:/config
```

Existing storage paths must not be renamed solely for consistency without a
migration plan.

## Ports

Published port mappings should use quoted string syntax for consistency.

Example:

```yaml
ports:
  - "8080:8080"
```

Quoting is an AthenaStack formatting convention rather than a Docker
requirement.

## Networking

Bridge, host, and shared-network namespace modes are acceptable when
intentionally selected for the application.

Networking policy is documented but is not yet automatically enforced.

## AppArmor

`apparmor=unconfined` is a documented temporary operational exception where
AppArmor previously disrupted the environment.

AppArmor remediation will be handled as a separate investigation and must not
be mixed into unrelated CI/CD work.

## Secrets

Credentials, passwords, API keys, and tokens must not be committed to the
repository.

Secrets must eventually be supplied by the deployment mechanism or another
approved secret-management process.

## Policy Rollout

New AthenaStack policies follow this sequence:

1. Document the intended standard.
2. Audit the existing platform.
3. Identify valid exceptions.
4. Introduce reporting where practical.
5. Correct unintended drift.
6. Enforce the rule through CI.
