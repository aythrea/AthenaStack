#!/usr/bin/env python3
"""Generate a non-enforcing audit of AthenaStack Compose conventions."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

COMPOSE_FILES = (
    "athenastack-compose.yml",
    "glances-stack.yml",
    "jackett.yml",
    "plex-stack.yml",
    "transfer.yml",
)


def render_compose_file(filename: str) -> dict[str, Any]:
    """Ask Docker Compose to produce its normalized JSON model."""
    result = subprocess.run(
        [
            "docker",
            "compose",
            "--project-name",
            "policy-audit",
            "--file",
            filename,
            "config",
            "--format",
            "json",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    return json.loads(result.stdout)


def environment_names(service: dict[str, Any]) -> set[str]:
    """Return the environment-variable names declared by a service."""
    environment = service.get("environment", {})

    if isinstance(environment, dict):
        return set(environment)

    if isinstance(environment, list):
        names: set[str] = set()

        for entry in environment:
            if isinstance(entry, str):
                names.add(entry.split("=", 1)[0])

        return names

    return set()


def volume_targets(service: dict[str, Any]) -> set[str]:
    """Return normalized container-side volume targets."""
    targets: set[str] = set()

    for volume in service.get("volumes", []):
        if not isinstance(volume, dict):
            continue

        target = volume.get("target")

        if isinstance(target, str):
            targets.add(target)

    return targets


def apparmor_mode(service: dict[str, Any]) -> str:
    """Return the AppArmor mode explicitly declared by a service."""
    security_options = service.get("security_opt", [])

    if not isinstance(security_options, list):
        return "default"

    for option in security_options:
        if option == "apparmor=unconfined":
            return "unconfined"

    return "default"


def yes_or_no(condition: bool) -> str:
    """Return a human-readable Boolean value."""
    return "yes" if condition else "no"


def audit_rows() -> list[str]:
    """Return one Markdown table row per managed service."""
    rows: list[str] = []

    for filename in COMPOSE_FILES:
        if not Path(filename).is_file():
            raise FileNotFoundError(
                f"{filename}: expected Compose file is missing"
            )

        document = render_compose_file(filename)
        services = document.get("services", {})

        if not isinstance(services, dict):
            raise TypeError(
                f"{filename}: rendered services value is not an object"
            )

        for service_name, service in services.items():
            if not isinstance(service, dict):
                continue

            environment = environment_names(service)
            targets = volume_targets(service)
            restart_policy = service.get("restart", "not declared")

            rows.append(
                "| "
                f"`{filename}` | "
                f"`{service_name}` | "
                f"`{restart_policy}` | "
                f"{yes_or_no('PUID' in environment)} | "
                f"{yes_or_no('PGID' in environment)} | "
                f"{yes_or_no('TZ' in environment)} | "
                f"{yes_or_no('/config' in targets)} | "
                f"{apparmor_mode(service)} |"
            )

    return rows


def main() -> int:
    """Write the AthenaStack policy audit as Markdown."""
    try:
        rows = audit_rows()
    except (
        FileNotFoundError,
        TypeError,
        subprocess.CalledProcessError,
        json.JSONDecodeError,
    ) as exc:
        if isinstance(exc, subprocess.CalledProcessError) and exc.stderr:
            print(exc.stderr, file=sys.stderr)

        print(f"Policy audit failed: {exc}", file=sys.stderr)
        return 1

    print("# AthenaStack Policy Audit")
    print()
    print(
        "This report describes current Compose conventions. "
        "It does not enforce them."
    )
    print()
    print(
        "| Stack | Service | Restart | PUID | PGID | TZ | "
        "Persistent `/config` | AppArmor |"
    )
    print("|---|---|---|---:|---:|---:|---:|---|")

    for row in rows:
        print(row)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
