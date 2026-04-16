# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this package is

`Products.MeetingPROVHainaut` is a Plone 4.3 / Python 2.7 add-on that customizes `Products.PloneMeeting` for the Province of Hainaut (Belgium). It sits at the top of a three-level inheritance chain:

```
Products.PloneMeeting  →  Products.MeetingCommunes  →  Products.MeetingPROVHainaut
```

The package's main concern is a **three-variant finance advice workflow** where meeting items must be reviewed by finance directors before they can proceed to a meeting.

## Commands

The project uses `zc.buildout`. All commands below assume you are in the buildout root (the directory containing `bin/`), not inside this package.

**Bootstrap the buildout** (first time or after `buildout.cfg` changes):
```bash
python bootstrap.py
bin/buildout
```

**Run all package tests:**
```bash
bin/testhainaut
```

**Run tests for the MeetingCommunes dependency:**
```bash
bin/testmc
```

**Run a single test module:**
```bash
bin/testhainaut -t testAdvices
```

**Run a single test method:**
```bash
bin/testhainaut -t testAdvices.testAdviceWorkflow
```

**Run with coverage:**
```bash
coverage run bin/testhainaut
coverage report
```

**Code analysis (flake8 etc.):**
```bash
bin/code-analysis
```

## Architecture

### Customization via Zope adapters

All business-logic overrides live in `adapters.py`. The classes there inherit from their MeetingCommunes equivalents and override specific methods:

- `MeetingItemPROVHainautWorkflowActions` — what happens when a workflow transition fires (e.g. whether to ask completeness re-evaluation)
- `MeetingItemPROVHainautWorkflowConditions` — guards on transitions (e.g. only `financialmanagers` can send an item back to `validated`)
- `MeetingAdvicePROVHainautWorkflowConditions` — guards on finance advice transitions
- `CustomMeetingConfig` — routes finance advice types to the correct conditions interface
- `CustomMeetingItem` — higher-level item behaviour (completeness gating, advice addability, delay start logic)

Adapters are registered in `configure.zcml` / `overrides.zcml` against the interfaces declared in `interfaces.py`.

### Finance group system

Three finance organizations are defined in `config.py` and used throughout:

| Constant | Group ID | Role |
|---|---|---|
| `FINANCE_GROUP_ID` | `dirfin` | Main finance director |
| `FINANCE_GROUP_CEC_ID` | `dirfincec` | Finance director with CEC |
| `FINANCE_GROUP_NO_CEC_ID` | `dirfinnocec` | Finance director without CEC |

Helper functions in `utils.py` (`finance_group_uid()`, `finance_group_cec_uid()`, `finance_group_no_cec_uid()`, `finance_group_uids()`) return the Plone UIDs of those organizations. Always use these helpers rather than hard-coding UIDs.

`config.py` also **mutates** `Products.PloneMeeting.config.MEETING_GROUP_SUFFIXES` and `EXTRA_GROUP_SUFFIXES` at import time to add the five financial role suffixes (`financialprecontrollers`, `financialcontrollers`, `financialeditors`, `financialreviewers`, `financialmanagers`).

### Completeness gating

Finance advice can only be added or edited when the item is considered "complete". Completeness is evaluated exclusively by members of the `financialprecontrollers` sub-group of `dirfin` or `dirfincec`. The logic lives in `CustomMeetingItem.mayEvaluateCompleteness()` and `_adviceIsAddableByCurrentUser()` / `_adviceIsEditableByCurrentUser()`.

### Profiles

Three GenericSetup profiles under `profiles/`:

- `default` — installs the three finance advice portal types and base CSS/skins. Depended on by the two profiles below.
- `testing` — minimal fixture used by the `MPH_TESTING_PROFILE` test layer.
- `zprovhainaut` — full production data: organizations, categories, POD templates, meeting configurations. Used by the `MPH_FIN_TESTING_PROFILE` test layer and in production.

The current profile version is `4204` (see `profiles/default/metadata.xml`). Migration steps live in `migrations/migrate_to_42XX.py`.

### Test layers

Two test layers are defined in `testing.py`:

- `MPH_TESTING_PROFILE` — applies the `testing` GS profile; used by most tests.
- `MPH_FIN_TESTING_PROFILE` — applies the full `zprovhainaut` profile; used for tests that require real finance organizations (e.g. `testAdvices.py` finance-specific cases).

The base test case is `MeetingPROVHainautTestCase` in `tests/MeetingPROVHainautTestCase.py`, which inherits from `MeetingCommunesTestCase`.

### Events

`events.py` contains a single subscriber (`onAdviceAfterTransition`) that automatically re-triggers completeness evaluation when a finance advice reverts from `advice_given` back to `advicecreated`.

### Document generation

`browser/overrides.py` provides `MPHFolderDocumentGenerationHelperView`, which extends the MeetingCommunes equivalent and adds `get_finance_advices_stats()` for producing finance statistics in POD (OpenDocument) templates.
