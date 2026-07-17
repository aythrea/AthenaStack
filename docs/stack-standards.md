# AthenaStack Application Standards

## Purpose
AthenaStack defines containerized applications running on an OpenMediaVault
Docker host. Portainer is the current deployment and management interface.

The platform may move toward Compose-native deployment as the CI/CD process
matures. Such a migration will be treated as a separate operational change.

## Deployment Model
- Docker Compose defines independently deployable Portainer stacks.
- Application data persists beneath `/athenamedia/Appdata`.
- Shared storage is mounted from the `/athenamedia` hierarchy.
- CI validates repository content; deployment automation comes later.

## Restart Policies
CI validates restart policies that are explicitly declared. It does not yet
require every service to declare a restart policy.
Declared restart policies must be one of:
- `no`
- `always`
- `unless-stopped`
- `on-failure`
- `on-failure:<retry-count>`

## LinuxServer Containers
Normally define:
- PUID
- PGID
- TZ

## Persistent Configuration
Preferred convention:
`/athenamedia/Appdata/<application>:/config`

## Ports
Quote published ports for consistency.

## Networking
Bridge, host, and shared-network modes are acceptable when intentionally selected.

## AppArmor
`apparmor=unconfined` is a documented temporary operational exception pending a dedicated investigation.

## Secrets
Do not commit credentials.

## Policy Rollout
1. Document
2. Audit
3. Identify exceptions
4. Report
5. Correct drift
6. Enforce

## Platform Environment

Common, non-secret platform values should be defined once by the deployment
environment and referenced by Compose definitions where supported.

The current shared values are:

- `TZ`
- `PUID`
- `PGID`

### Timezone

AthenaStack uses `America/Chicago` as its platform timezone.

Services should reference the shared `TZ` value only when the image or
application supports configurable timezone behavior. `TZ` affects local-time
presentation; it does not synchronize the container clock.
