# ChangeLog

All notable changes to `gitlike-commands` are documented here, newest first.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [v0.4.0](#v040)
    - [Features](#features)
    - [Build tooling](#build-tooling)
    - [Documentation](#documentation)
    - [Tests](#tests)
- [v0.3.1 — 2026-03-31](#v031-2026-03-31)
    - [Build tooling](#build-tooling-1)
    - [CI](#ci)
- [v0.3.0 — 2024-01-26](#v030-2024-01-26)
    - [Features](#features-1)
    - [Build tooling](#build-tooling-2)
    - [CI](#ci-1)
- [v0.2.1 — 2022-06-13](#v021-2022-06-13)
    - [Packaging](#packaging)
    - [Documentation](#documentation-1)
- [v0.1.0 — 2022-03-09](#v010-2022-03-09)
    - [Features](#features-2)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## v0.4.0

### Features

- `subcommand_driver` now passes `stdin`, `stdout`, and `stderr` explicitly to
  the subcommand it runs with `subprocess.check_call`, via a new
  `_stream_target` helper. Streams with a real file descriptor (the normal CLI
  case) pass through unchanged; streams without one (a `StringIO`, a
  test-capture wrapper) fall back to inheriting the parent descriptor instead
  of raising. For a normal invocation this matches the previous inherit-by-
  default behavior; the helper hardens the fd-less case.

### Build tooling

- Finished the poetry-to-uv migration. `pyproject.toml` is now PEP 621:
  `[project]` metadata with `requires-python = ">=3.9"`, dev dependencies
  consolidated into a single `[dependency-groups]` dev group (`pytest`,
  `pytest-cov`), and the build backend switched from `poetry-core` to
  `hatchling`.
- Added `pytest-cov` as a dev dependency.

### Documentation

- README `Usage` section documents the inherited `stdin`/`stdout`/`stderr`
  behavior.
- README scripts-entry example now shows the PEP 621 `[project.scripts]` form
  alongside the poetry form.

### Tests

- Added unit tests covering `is_program`, `find_subcommand`, `_stream_target`,
  and `subcommand_driver` (100% line coverage).
- Removed the `test_version` placeholder test, which asserted a hardcoded
  version string and had to be edited on every release.

## v0.3.1 — 2026-03-31

### Build tooling

- Converted the project from poetry to uv.
- Cut a release to pull in accumulated dependency updates.
- Bumped the pytest requirement from `^7.4` to `^8.0`.

### CI

- Updated mega-linter and applied its fixer suggestions.

## v0.3.0 — 2024-01-26

### Features

- Load the package version from installed metadata rather than hardcoding it.

### Build tooling

- Replaced `distutils` with `shutil` (removes the deprecated dependency).
- Updated the pytest requirement from `^5.2` to `^7.4`.

### CI

- Updated megalinter to v7 and demoted KICS findings to warnings.

## v0.2.1 — 2022-06-13

### Packaging

- Added classifier entries, license, and issue-tracker URL to `pyproject.toml`.

### Documentation

- Clarified the requirements for subcommands in the README.
- Added a PyPI badge and cleaned up the license blurb.

## v0.1.0 — 2022-03-09

### Features

- Initial release. Code refactored out of
  [thelogrus](https://github.com/unixorn/thelogrus/) so consumers depend only on
  the Python standard library.
- `subcommand_driver`, `find_subcommand`, and `is_program` for building
  git-style subcommand dispatch.
