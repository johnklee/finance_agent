---
name: publish-package
description: Use this skill when the user wants to publish the `financial-stock-agent` package.
---

# Publish Python Package

Use this skill when the user wants to publish the `financial-stock-agent` package.

## Usage

```
publish-package VERSION
```

Example:

```
publish-package 0.1.1
```

## What this skill does

1. Reads the current version from `finance_agent/__init__.py`.
2. Validates that the target version is greater than the current version.
3. Updates `finance_agent/__init__.py`.
4. Builds the package using `uv build`.
5. Publishes the package using `uv publish`.
6. Commits the release:

   ```shell
   git add finance_agent/__init__.py uv.lock pyproject.toml
   git commit -m "Publish vX.Y.Z"
   ```

7. Creates an annotated git tag:

   ```shell
   git tag -a vX.Y.Z -m "Release vX.Y.Z"
   ```

8. Displays a summary of all actions performed.

## Preconditions

* Must be executed from the repository root.
* User must already be authenticated for publishing:
  * `UV_PUBLISH_TOKEN`, or
  * Trusted Publishing.

* Working tree should be clean before publishing.

## Failure Conditions

The skill must stop immediately if:

* The target version is invalid.
* The target version is less than or equal to the current version.
* The git working tree is dirty.
* `uv build` fails.
* `uv publish` fails.
* `git commit` fails.
* `git tag` fails.
