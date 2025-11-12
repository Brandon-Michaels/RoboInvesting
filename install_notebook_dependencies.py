#!/usr/bin/env python3
"""
install_notebook_dependencies.py
--------------------------------

Scan every Jupyter notebook (*.ipynb) in the repository, infer the third-party
Python packages they rely on, and install those dependencies in the current
environment via pip.

Usage:
    python install_notebook_dependencies.py
        Installs every inferred dependency.

    python install_notebook_dependencies.py --dry-run
        Only prints the packages that would be installed.

    python install_notebook_dependencies.py --requirements notebook-requirements.txt
        Writes the inferred package list to the given requirements file (in
        addition to installing, unless --dry-run is also supplied).
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Iterable, Set
import re

# Modules that belong to the Python standard library (or common built-ins) and
# therefore do not require installation from PyPI.
STD_LIB_MODULES: Set[str] = {
    "argparse",
    "array",
    "asyncio",
    "collections",
    "contextlib",
    "csv",
    "dataclasses",
    "datetime",
    "functools",
    "glob",
    "io",
    "itertools",
    "json",
    "logging",
    "math",
    "numbers",
    "operator",
    "os",
    "pathlib",
    "pickle",
    "random",
    "re",
    "statistics",
    "string",
    "subprocess",
    "sys",
    "tempfile",
    "textwrap",
    "time",
    "typing",
    "urllib",
    "warnings",
}

# Map import/module names to the corresponding package name on PyPI when they
# differ.
PACKAGE_ALIASES = {
    "bs4": "beautifulsoup4",
    "cv2": "opencv-python",
    "google": "google-colab",
    "google.colab": "google-colab",
    "PIL": "Pillow",
    "sklearn": "scikit-learn",
    "yaml": "PyYAML",
}

IMPORT_RE = re.compile(r"^\s*import\s+(.+)")
FROM_IMPORT_RE = re.compile(r"^\s*from\s+([A-Za-z0-9_\.]+)\s+import\s+(.+)")
PIP_INSTALL_RE = re.compile(r"^!\s*pip\s+install\s+(.+)$")


def normalize_module(module: str) -> str:
    """Return the canonical module key without trailing comments or spaces."""
    module = module.strip()
    if not module:
        return ""
    # Drop alias (e.g., "numpy as np").
    module = module.split()[0]
    # Remove trailing commas.
    return module.rstrip(",")


def extract_modules_from_source(source: str) -> Set[str]:
    """
    Extract imported module names from a block of notebook source code.

    Returns the set of modules referenced by `import` or `from ... import`
    statements, alongside any packages requested via `!pip install`.
    """
    modules: Set[str] = set()
    for line in source.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        pip_match = PIP_INSTALL_RE.match(stripped)
        if pip_match:
            packages = [
                token
                for token in pip_match.group(1).split()
                if token and not token.startswith("-")
            ]
            modules.update(packages)
            continue

        import_match = IMPORT_RE.match(stripped)
        if import_match:
            targets = import_match.group(1).split(",")
            for target in targets:
                module = normalize_module(target)
                if module:
                    modules.add(module)
                    root = module.split(".")[0]
                    modules.add(root)
            continue

        from_match = FROM_IMPORT_RE.match(stripped)
        if from_match:
            module = normalize_module(from_match.group(1))
            if module:
                modules.add(module)
                root = module.split(".")[0]
                modules.add(root)
    return modules


def scan_notebook(path: Path) -> Set[str]:
    """Return the set of modules/import targets referenced by a notebook."""
    modules: Set[str] = set()
    try:
        with path.open("r", encoding="utf-8") as f:
            notebook = json.load(f)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Failed to parse notebook {path}: {exc}") from exc

    for cell in notebook.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        source = cell.get("source", "")
        if isinstance(source, list):
            source = "".join(source)
        modules.update(extract_modules_from_source(source))
    return modules


def discover_packages(notebooks: Iterable[Path]) -> Set[str]:
    """Aggregate the set of PyPI packages required across notebooks."""
    packages: Set[str] = set()
    for nb_path in notebooks:
        modules = scan_notebook(nb_path)
        for module in modules:
            if not module:
                continue
            normalized = module.strip()
            lower = normalized.lower()
            if lower in STD_LIB_MODULES:
                continue
            package_name = PACKAGE_ALIASES.get(
                normalized,
                PACKAGE_ALIASES.get(lower, normalized),
            )
            packages.add(package_name)
    return packages


def install_packages(packages: Iterable[str], dry_run: bool) -> None:
    """Install each package via pip, unless --dry-run is specified."""
    for package in sorted(set(packages)):
        if dry_run:
            print(f"[dry-run] {package}")
            continue
        print(f"Installing {package} ...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def write_requirements(packages: Iterable[str], path: Path) -> None:
    """Write the packages to a requirements-style text file."""
    lines = [f"{pkg}\n" for pkg in sorted(set(packages))]
    path.write_text("".join(lines), encoding="utf-8")
    print(f"Wrote {len(lines)} packages to {path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Install dependencies referenced by all notebooks."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only list packages without installing them.",
    )
    parser.add_argument(
        "--requirements",
        type=Path,
        help="Optional path to a requirements file to write.",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("."),
        help="Repository root to scan (defaults to current directory).",
    )
    args = parser.parse_args()

    notebooks = list(args.root.rglob("*.ipynb"))
    if not notebooks:
        print("No notebooks found. Nothing to do.")
        return

    print(f"Discovered {len(notebooks)} notebooks. Scanning for dependencies...")
    packages = discover_packages(notebooks)
    if not packages:
        print("No third-party packages detected.")
        return

    if args.requirements:
        write_requirements(packages, args.requirements)

    install_packages(packages, dry_run=args.dry_run)


if __name__ == "__main__":
    main()

