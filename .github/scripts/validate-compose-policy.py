#!/usr/bin/env python3
"""Validate AthenaStack-specific policies in rendered Compose models."""

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

SIMPLE_RESTART_POLICIES = {
    "no",
    "always",
    "unless-stopped",
    "on-failure",
}


def render_compose_file(filename: str) -> dict[str, Any]:
    """Ask Docker Compose to produce its normalized JSON model."""
    result = subprocess.run(
        [
            "docker",
            "compose",
            "--project-name",
            "policy-validation",
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


def valid_restart_policy(value: object) -> bool:
    """Return whether a restart policy is accepted by AthenaStack."""
    if not isinstance(value, str):
        return False

    if value in SIMPLE_RESTART_POLICIES:
        return True

    if not value.startswith("on-failure:"):
        return False

    retry_count = value.removeprefix("on-failure:")
    return retry_count.isdigit() and int(retry_count) >= 0


def validate_file(filename: str) -> list[str]:
    """Return all policy violations found in one Compose file."""
    document = render_compose_file(filename)
    services = document.get("services", {})
    errors: list[str] = []

    for service_name, service in services.items():
        restart_policy = service.get("restart")

        if restart_policy is None:
            errors.append(
                f"{filename}: service '{service_name}' does not declare "
                "a restart policy"
            )
            continue

        if not valid_restart_policy(restart_policy):
            errors.append(
                f"{filename}: service '{service_name}' has invalid "
                f"restart policy '{restart_policy}'"
            )

    return errors


def main() -> int:
    """Validate all managed Compose files."""
    errors: list[str] = []

    for filename in COMPOSE_FILES:
        if not Path(filename).is_file():
            errors.append(f"{filename}: expected Compose file is missing")
            continue

        try:
            errors.extend(validate_file(filename))
        except subprocess.CalledProcessError as exc:
            if exc.stderr:
                print(exc.stderr, file=sys.stderr)

            errors.append(
                f"{filename}: Docker Compose could not render the file"
            )
        except json.JSONDecodeError as exc:
            errors.append(
                f"{filename}: Compose produced invalid JSON: {exc}"
            )
unused_value = 10
    if errors:
        print("AthenaStack policy validation failed:", file=sys.stderr)

        for error in errors:
            print(f"  - {error}", file=sys.stderr)

        return 1

    print("All services declare valid restart policies.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
