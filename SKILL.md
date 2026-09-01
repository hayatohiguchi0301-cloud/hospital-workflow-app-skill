---
name: build-clinical-workflow-app
description: Build, improve, or repair simple Japanese workflow applications for hospitals, clinics, pathology departments, and clinical laboratories using Python, Streamlit, SQLite, requirements.txt, and README.md. Use when Codex is asked to create a medical workplace operations tool, inspection log, document tracker, task or incident inventory, specimen workflow aid, equipment ledger, or another non-diagnostic internal app that non-engineers must operate and move to another PC.
---

# Build Clinical Workflow App

Create small, dependable internal workflow apps for non-engineers. Optimize for clarity, safe local operation, portability, and maintainability—not feature count.

## Required workflow

1. Inspect the target directory with `rg --files` and read relevant existing files before editing.
2. Preserve user changes. Never replace, delete, migrate, or rename an existing file or database without explicit authorization. If an existing implementation overlaps, patch it minimally.
3. Translate the request into one primary workflow, user roles, fields, statuses, and acceptance criteria. Make conservative assumptions when they are reversible; ask only when a choice changes clinical risk, data handling, or the core workflow.
4. Read [references/quality-and-safety.md](references/quality-and-safety.md) for every app. Read [references/patterns.md](references/patterns.md) when selecting screens or database fields. Read [references/windows-portability.md](references/windows-portability.md) for every new app and whenever another PC, LAN sharing, deployment, backup, or migration is in scope.
5. For a new project, copy `assets/streamlit-starter/` into the requested folder, then adapt it. Do not overwrite files already present.
6. Keep the default stack unless the user requests otherwise: Python 3.11+, Streamlit, SQLite through the standard library, `requirements.txt` with compatible version ranges, and a Japanese `README.md` with Windows-first setup steps.
   For a Windows-delivered app, adapt `assets/windows-launcher/起動.bat`; do not copy an existing `.venv` as a usable runtime.
7. Implement the smallest complete version. Prefer one main list, one input form, search/filter, explicit edit/delete confirmation, and CSV export. Add dashboards, authentication, or notifications only when required.
8. Validate inputs in the UI and immediately before database writes. Use parameterized SQL and transactions. Store timestamps in ISO 8601 format. Keep schema creation idempotent.
9. Use Japanese labels, plain terms, visible required markers, actionable errors, sensible defaults, and a clear empty state. Never depend on color alone to convey status.
10. Never include real patient data, staff secrets, credentials, or realistic identifiers in fixtures, screenshots, tests, or source control. Do not automate diagnosis, treatment recommendations, or clinical decisions.
11. Run tests before completion: `python -m compileall .`; `python -m unittest discover -s tests -v` when tests exist; `python scripts/validate_project.py <project>` using this skill's validator; and start Streamlit headlessly and confirm its health endpoint when dependencies are available.
12. Report what was created, exact test results, how to start it, where data is stored, and any limitation. Do not claim visual or runtime validation that was not performed.

## Output contract

Every new app must contain:

```text
project/
├── app.py
├── db.py
├── 起動.bat
├── requirements.txt
├── README.md
└── tests/
    └── test_db.py
```

Add `.gitignore` for the virtual environment, caches, local SQLite files, exports, and secrets. Keep business rules separate from presentation when they grow beyond a few lines.

## Completion gate

- App opens without a Python exception.
- A record can be created, listed, searched, updated, and deliberately deleted.
- Empty and invalid inputs produce understandable Japanese guidance.
- Database initialization can run repeatedly without destroying data.
- README steps work on a clean PC and identify the Python version.
- Windows delivery uses a project-relative launcher, recreates a copied or broken virtual environment, and documents whether the app is local-only or shared on the hospital LAN.
- Shared use runs one host process against the SQLite database; client PCs connect with a browser and do not start competing app instances on the same database.
- Existing files unrelated to the request remain unchanged.
- No sample personal or patient information is present.

If a check cannot run because a dependency or browser is unavailable, keep the app usable, state the unverified check, and provide the exact command for the user.
