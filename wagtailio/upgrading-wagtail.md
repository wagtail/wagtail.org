---
name: upgrade-wagtail
description: Plan and optionally execute an upgrade to a new Wagtail release, including all needed dependency updates.
license: MIT
---

# Upgrade Wagtail

Usage:

- For planning: `/upgrade-wagtail with a plan from v5.2 to latest`.
- For sites: `/upgrade-wagtail to v7.3`.
- For packages: `/upgrade-wagtail with support for v7.3 and clean up now-unsupported versions`.

## Overview

Comprehensive project and dependencies review to identify needed changes to upgrade to a new Wagtail version, and potential opt-in improvements based on any changes in the release.

## Methodology

### Goals

- Upgrade the project to the target Wagtail release, including any needed dependencies upgrades.
- For packages: clean up code or tooling related to compatibility with now-unsupported Wagtail versions.
- Baseline QA that the upgrade works correctly - migrations run, linting passes, test suite passes, check framework passes, all with no deprecation warnings if possible.
- A thorough upgrade report for the user (upgrade methodology, what changed, what further tests to do, links to relevant information), ideally with guidance on opt-in changes to consider.

### Guardrails

- Prefer minimal, reviewable changes. Avoid introducing technical debt.
- Make dependency updates explicit and reproducible (lockfile updates included).
- No fixes unrelated to the upgrade (like linting/formatting), unless required for the QA checks to pass.
- If a change is ambiguous, choose the option with the least technical debt. Ask for further input if needed.
- When there are issues that seem like bugs in the dependencies, encourage the user to report back with feedback for maintainers based on the project’s [contributing guidance](https://docs.wagtail.org/en/latest/contributing/index.html.md).

### Input

To detect from the context or request from the user if unclear:

- Agent mode: whether we want to provide an audit of the needed work for an upgrade, or actually directly do the upgrade. Default: assume "direct update on current code".
- Current versions of Python, Django, Wagtail. Default: read from `pyproject.toml` or `requirements.txt` files, or lockfiles
- Target version for Wagtail. Default: assume "latest", fetch the [release schedule](https://github.com/wagtail/wagtail/wiki/Release-schedule) and check which version is latest based on the current date.
- Current dependencies management tool: `pip` / `poetry` / `uv`. Default: detect from README / contributor docs
- Upgrade strategy for packages vs. apps/sites: check whether we want to switch to only the new version, or add it in an existing version range. Default: upgrade to version if the current project is a site/app, extend range if it’s a package.
- Optional: high-level understanding of the project’s customizations likely to be impacted. Default: determine later based on your own review.

### Reference data sources

Always fetch latest information from the official Wagtail docs if possible.

- [Official release schedule with support dates](https://github.com/wagtail/wagtail/wiki/Release-schedule)
- [llms.txt index of developer docs pages](https://docs.wagtail.org/en/latest/llms.txt)
- Example: [7.3 release notes](https://docs.wagtail.org/en/latest/releases/7.3.html.md)
- Example: [7.3 CMS user release notes](https://guide.wagtail.org/en-latest/releases/new-in-wagtail-7-3/markdown/)

Combine it with project-specific information:

- Guidance for contributors.
- Upgrade considerations / test plans / documentation on customizations.
- Implementation details in the code, in particular Python files.

### Reporting

Upgrades are sensitive tasks, it’s critical you provide clear information to the user throughout the upgrade tasks, with clear requests for any extra input. And as a comprehensive report at the end.

- Use text formatting if supported (tables, lists, Markdown links)
- Link directly to release notes and other documentation pages where relevant.
- When sharing docs references in reporting, make sure to link to the HTML pages (.html, not .html.md for developer docs; and remove /markdown/ from user guide URLs).
- Report on both your methodology, and the outcome.
- Use artifacts in addition to messages if supported.

### Commit and pull request strategy

If the current task mode is to work directly on the project code, commit regularly on a new branch unless otherwise noted by project instructions.

Commit for:

- Version upgrades of dependencies
- Fixes in the code
- Fixes / additions in test suites
- Documentation updates

Push if allowed from current permissions or after user confirmation, when:

- We want to see results from Continuous Integration tools.
- We want human review.
- We think the work is done.

### Quality Assurance

Options to check that the upgrade works correctly, to use as needed through upgrade steps:

- Project linting passes
- Project test suite passes
- No unapplied migrations
- Django check framework passes
- Any other automated or manual checks documented for the project (test plans? upgrade considerations?)
- If supported by your AI harness: running the server and manually navigating the site/app to do manual checks.

Look for any deprecation warnings coming from Wagtail in particular.

### Definition of done

To adapt from the specifics of the project:

- Dependency files + lockfiles updated and consistent
- Test suite / QA tools / CI all passing
- No new deprecation warnings introduced (or explicitly documented)
- Any relevant project doc is updated
- Upgrade report created

## Steps

### Confirm upgrade path

- [ ] Confirm all input sources from the upgrade methodology.
- [ ] Retrieve the current Python / Django / Wagtail versions from context or user input
- [ ] Determine the target Wagtail version ("latest" or a specific version number)
- [ ] Fetch [Upgrading Wagtail](https://docs.wagtail.org/en/latest/releases/upgrading.html.md) and use its table to confirm which releases are along the upgrade path, from current to target.
- [ ] From the table, ensure Django/Python versions meet the target Wagtail version’s compatibility requirements.
- [ ] Report the upgrade path to the user
- [ ] If there are Python / Django compatibility mismatches, get confirmation on how to proceed from the user.

At this stage, if there are multiple Wagtail versions on the upgrade path, make sure that all subsequent work is done in sequence for every one of those versions. For example, upgrading from Wagtail 7.0 to 7.2 should involve running through all the steps in this file with 7.1 as the target; then asking the user to confirm the successful 7.1 upgrade; then restarting this all from 7.1 to 7.2.

### Baseline setup and QA

- [ ] Check for project-specific information about quality assurance tools and methodologies, dependencies management, and upgrades considerations.
- [ ] Create a branch for the upgrade (check any conventions for branch names, or `upgrade-wagtail-vx.y`)
- [ ] Run the project’s QA tools / test suite to capture a baseline. At least tests, linting, Django checks.

### Dependencies audit and upgrades

You may need to do this in a different order depending on whether dependency compatibility issues are reported when upgrading to the new Wagtail version.

- [ ] Bump Wagtail version constraints in `pyproject.toml` or `requirements.txt` files.
- [ ] Install the new version with the relevant tool for the project’s package manager (`pip` / `poetry` / `uv`).
- [ ] Identify the project’s dependencies related to Wagtail / Django that would potentially be impacted.
- [ ] Fetch those dependencies’ Wagtail / Django version compatibilities to confirm needed updates.
- [ ] Report the needed dependencies upgrades to the user
- [ ] If there are needed dependencies upgrades, get confirmation on how to proceed from the user.
- [ ] Upgrade the relevant dependencies after confirmation.
- [ ] Update the project’s documentation about dependencies to reflect any of those changes.
- [ ] Use the project’s QA tools / test suite as needed when doing the upgrades.

Note any warnings or errors from package managers or from the project’s QA tools. Those might indicate further actions needed for the upgrades to be successful. You may need to move to the subsequent steps to resolve them.

### Apply official upgrade guidance

- [ ] Fetch the Wagtail release notes from the next version on the upgrade path, from the official docs.
- [ ] Review the required actions from "Upgrade considerations" and think about which ones are likely to affect this project.
- [ ] Review the project’s implementation of Wagtail APIs, to identify possible code that needs changes. Do this for changes noted in the release notes as:
  - [ ] "affecting all projects"
  - [ ] "deprecation of old functionality"
  - [ ] "undocumented internals"
  - [ ] Any other changes that feel like they might be relevant.
- [ ] Report your findings to the user. Consider providing a "Status" for every entry in the release notes, even if just to report the current project is "Not affected"

### Update code and fix any QA failures

- [ ] Make all necessary updates based on the upgrade guidance.
- [ ] When tests or QA fails, classify the needed change: import/API changes, settings, templates, DB / migration. Or is it flaky tests? Confirm.
- [ ] Fix smaller API changes first, bigger ones after.
- [ ] Add / adjust tests if behavior truly changed and the project should follow new defaults in Wagtail.
- [ ] Update corresponding documentation for any behavior changes.
- [ ] If the current project is a package - consider whether some of those changes should be wrapped in a conditional version check, to preserve compatibility with older versions.
- [ ] Report what code changes you did / are doing to the user.

### Update documentation

- [ ] Review whether there is any further project documentation to update, and make necessary changes if so.
- [ ] If the project documents "upgrade considerations" for future updates, add information if necessary.
- [ ] If the project has a changelog, add needed details about the steps you took, following the existing style.

### Produce the upgrade report

- [ ] Check specific instructions from the user / coding harness on how to report information.
- [ ] Report on any assumptions you took while interpreting the methodology for upgrades.
- [ ] Add your reporting for every step in the upgrade process.
- [ ] Report on any opt-in changes from the Wagtail release notes that haven’t been applied.
- [ ] Suggest follow-up tasks based on the project’s context: other upgrades (Python, Django, other packages), other aspects of tech debt, etc.
- [ ] If it seems helpful, produce a manual test plan for the user.
- [ ] If it seems helpful, produce a recap of relevant changes that can be shared with CMS users.