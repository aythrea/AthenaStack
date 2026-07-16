#!/usr/bin/env python3
"""Report current AthenaStack Compose conventions without enforcing them."""

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


def render_compose(filename: str) -> dict[str, Any]:
    result = subprocess.run(
        [
            "docker",
            "compose",
            "--project-name",
            "athenastack-audit",
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
    environment = service.get("environment", {})

    if isinstance(environment, dict):
        return set(environment)

    # Defensive support for list-form environment entries.
    names: set[str] = set()

    if isinstance(environment, list):
        for entry in environment:
            if isinstance(entry, str):
                names.add(entry.split("=", 1)[0])

    return names


def volume_targets(service: dict[str, Any]) -> set[str]:
    targets: set[str] = set()

    for volume in service.get("volumes", []):
        if isinstance(volume, dict):
            target = volume.get("target")
            if isinstance(target, str):
                targets.add(target)

    return targets


def main() -> int:
    print("# AthenaStack policy audit")
    print()
    print(
        "| Stack | Service | Restart | PUID | PGID | TZ | "
        "Persistent /config | AppArmor |"
    )
    print(
        "|---|---|---|---:|---:|---:|---:|---|"
    )

    for filename in COMPOSE_FILES:
        path = Path(filename)

        if not path.is_file():
            print(f"Missing expected Compose file: {filename}", file=sys.stderr)
            return 1

        model = render_compose(filename)

        for service_name, service in model.get("services", {}).items():
            environment = environment_names(service)
            targets = volume_targets(service)
            security_options = service.get("security_opt", [])

            apparmor = "default"

            if any(
                isinstance(option, str)
                and option == "apparmor=unconfined"
                for option in security_options
            ):
                apparmor = "unconfined"

            print(
                f"| {filename} "
                f"| {service_name} "
                f"| {service.get('restart', 'not declared')} "
                f"| {'yes' if 'PUID' in environment else 'no'} "
                f"| {'yes' if 'PGID' in environment else 'no'} "
                f"| {'yes' if 'TZ' in environment else 'no'} "
                f"| {'yes' if '/config' in targets else 'no'} "
                f"| {apparmor} |"
            )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())