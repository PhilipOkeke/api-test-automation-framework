# Contributing to the API Test Automation Framework

Contributions should keep the framework readable, repeatable, and independent of a single test environment.

## Development setup

1. Start the TaskFlow API locally.
2. Create and activate a virtual environment.
3. Install development dependencies:

```bash
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

4. Run the suite:

```bash
pytest
```

Use `BASE_URL` to target another authorized test environment.

## Quality checks

Run these commands before submitting a change:

```bash
ruff check .
ruff format --check .
pytest
```

For reports:

```bash
pytest --html=reports/api-test-report.html --self-contained-html --junitxml=reports/junit.xml
```

## Framework conventions

- Keep business-readable scenarios in `tests/`.
- Put reusable HTTP operations in the client layer.
- Add shared assertions instead of duplicating response checks.
- Generate unique test data and clean up created resources.
- Extend JSON Schemas when response contracts change.
- Mark critical checks with `smoke` and broader coverage with `regression`.
- Never run destructive tests against an environment without authorization.

## Commit messages

Use focused, action-oriented messages:

- `Add contract checks for paginated responses`
- `Fix cleanup after failed task creation`
- `Document staging environment configuration`

## Pull-request checklist

- Tests are deterministic and can run repeatedly
- New behaviour includes positive and negative coverage
- Secrets and environment-specific values are excluded
- Linting, formatting, and the complete suite pass
- Documentation is updated when usage changes
