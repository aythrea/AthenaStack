# AthenaStack Application Standards

## Purpose
AthenaStack defines containerized applications deployed with Docker and Portainer. This document defines platform standards independently of CI implementation.

## Deployment Model
- Docker Compose defines independently deployable Portainer stacks.
- Application data persists beneath `/athenamedia/Appdata`.
- Shared storage is mounted from the `/athenamedia` hierarchy.
- CI validates repository content; deployment automation comes later.

## Restart Policies
Declared restart policies must be one of:
- no
- always
- unless-stopped
- on-failure
- on-failure:<retry-count>

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
