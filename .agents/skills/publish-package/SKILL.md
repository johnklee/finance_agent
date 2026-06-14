---
name: publish-package
description: Use this skill when the user wants to publish the `financial-stock-agent` package.
---

# Publish Python Package

Use this skill when the user wants to publish the `financial-stock-agent` package.

## Usage

```shell
publish-package VERSION
```

Example:

```shell
publish-package 0.1.1
```

## What this skill does

1. Reads the current version from:

   * `pyproject.toml`
   * `finance_agent/__init__.py`

2. Validates that:

   * both versions are identical;
   * the target version is a valid semantic version;
   * the target version is greater than the current version.

3. Ensures the git working tree is clean.

4. Updates the version in both files:

   * `pyproject.toml`
   * `finance_agent/__init__.py`

5. Verifies that the environment variable `UV_PUBLISH_TOKEN` exists.

   * If `UV_PUBLISH_TOKEN` exists, continue.
   * Otherwise, stop immediately and ask the user to provide a PyPI API token.

6. Builds the package:

   ```shell
   uv build
   ```

7. Publishes the package to PyPI:

   ```shell
   uv publish
   ```

   The command relies on:

   ```shell
   UV_PUBLISH_TOKEN
   ```

   being available in the environment.

8. Commits the release:

   ```shell
   git add pyproject.toml finance_agent/__init__.py
   git commit -m "Publish vX.Y.Z"
   ```

9. Creates an annotated git tag:

   ```shell
   git tag -a vX.Y.Z -m "Release vX.Y.Z"
   ```

10. Displays a release summary to the user.

## Preconditions

* Must be executed from the repository root.
* The git working tree must be clean.
* `pyproject.toml` and `finance_agent/__init__.py` must contain the same version.
* The user must have permission to publish the package to PyPI.
* The environment variable below must be configured:

  ```shell
  UV_PUBLISH_TOKEN
  ```

## Failure Conditions

The skill must stop immediately if:

* The target version is invalid.
* The target version is less than or equal to the current version.
* The versions in `pyproject.toml` and `finance_agent/__init__.py` do not match.
* The git working tree is dirty.
* `UV_PUBLISH_TOKEN` is not defined.
* `uv build` fails.
* `uv publish` fails.
* `git commit` fails.
* `git tag` fails.

## Release Workflow

```text
Verify git status
↓
Verify version consistency
↓
Validate target version
↓
Update pyproject.toml
↓
Update finance_agent/__init__.py
↓
Verify UV_PUBLISH_TOKEN
↓
uv build
↓
uv publish
↓
git commit
↓
git tag
↓
Display summary
```

## Summary Output

After a successful release, display a summary similar to:

```text
Release completed successfully.

Previous version : 0.1.0
Published version: 0.1.1

Updated files:
- pyproject.toml
- finance_agent/__init__.py

Package published to PyPI using UV_PUBLISH_TOKEN.

Git commit:
Publish v0.1.1

Git tag:
v0.1.1
```

## Example Environment Setup

Before invoking this skill:

```shell
export UV_PUBLISH_TOKEN="pypi-xxxxxxxxxxxxxxxxxxxxxxxx"
```

Verify that it is configured:

```shell
echo "${UV_PUBLISH_TOKEN:+configured}"
```

Expected output:

```text
configured
```
