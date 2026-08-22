"""Domain-specific assertions that keep test cases concise."""

import json
from importlib.resources import files
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from requests import Response


def assert_status(response: Response, expected_status: int) -> None:
    """Assert an HTTP status and include the response body on failure."""

    assert response.status_code == expected_status, (
        f"Expected HTTP {expected_status}, received {response.status_code}. "
        f"Response body: {response.text}"
    )


def assert_schema(payload: dict[str, Any], schema_name: str) -> None:
    """Validate a JSON response against a bundled Draft 2020-12 schema."""

    schema_file = files("taskflow_test_framework.schemas").joinpath(schema_name)
    schema = json.loads(schema_file.read_text(encoding="utf-8"))
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(payload)


def assert_error_detail(response: Response, expected_detail: str) -> None:
    """Assert the API's standard error message."""

    assert response.json()["detail"] == expected_detail
