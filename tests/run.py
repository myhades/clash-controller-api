#!/usr/bin/env python3
"""Run unit or real-core API compatibility tests."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

from core_compatibility.download_core import (
    MANIFEST_PATH,
    download_core,
    download_test_database,
)


def _pytest(*args: str, environment: dict[str, str] | None = None) -> int:
    return subprocess.run(
        (sys.executable, "-m", "pytest", "-q", *args),
        env=environment,
        check=False,
    ).returncode


def _run_core(core: str, cache_dir: Path) -> int:
    binary = download_core(core, cache_dir)
    database = download_test_database(cache_dir)
    environment = {
        **os.environ,
        "CLASH_CORE_BINARY": str(binary),
        "CLASH_CORE_NAME": core,
        "CLASH_TEST_DATABASE": str(database),
    }
    print(f"\n=== API contract: {core} ===", flush=True)
    return _pytest(
        "-m",
        "system",
        "tests/core_compatibility",
        environment=environment,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("layer", choices=("unit", "system"))
    parser.add_argument(
        "--core",
        action="append",
        dest="cores",
        help="restrict compatibility validation to selected cores",
    )
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=Path(".cache/core-compatibility"),
    )
    args = parser.parse_args()

    if args.layer == "unit":
        return _pytest("-m", "not system")

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    cores = args.cores or list(manifest)
    unknown = sorted(set(cores) - set(manifest))
    if unknown:
        parser.error(f"unknown core(s): {', '.join(unknown)}")

    failures: list[str] = []
    for core in cores:
        try:
            result = _run_core(core, args.cache_dir)
        except (OSError, RuntimeError, ValueError) as err:
            print(f"{core}: {err}", file=sys.stderr)
            result = 1
        if result:
            failures.append(core)

    if failures:
        print(f"Failed cores: {', '.join(failures)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
