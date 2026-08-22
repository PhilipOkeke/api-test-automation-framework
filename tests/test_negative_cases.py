"""Validation and missing-resource tests."""

from collections.abc import Callable
from typing import Any

import pytest

from taskflow_test_framework.assertions import assert_error_detail, assert_status
from taskflow_test_framework.client import TaskFlowClient
from taskflow_test_framework.factories import task_payload

pytestmark = pytest.mark.regression


@pytest.mark.parametrize(
    ("payload"),
    [
        task_payload(title="No"),
        task_payload(status="blocked"),
        task_payload(priority="urgent"),
    ],
    ids=["title-too-short", "unsupported-status", "unsupported-priority"],
)
def test_create_rejects_invalid_payload(
    api_client: TaskFlowClient,
    payload: dict[str, Any],
) -> None:
    response = api_client.create_task(payload)

    assert_status(response, 422)
    assert isinstance(response.json()["detail"], list)


def test_get_missing_task_returns_404(api_client: TaskFlowClient) -> None:
    response = api_client.get_task(999_999_999)

    assert_status(response, 404)
    assert_error_detail(response, "Task not found")


def test_list_rejects_invalid_limit(api_client: TaskFlowClient) -> None:
    response = api_client.list_tasks(limit=0)

    assert_status(response, 422)


def test_update_rejects_null_required_field(
    api_client: TaskFlowClient,
    create_task: Callable[..., dict[str, Any]],
) -> None:
    task = create_task()

    response = api_client.update_task(task["id"], {"title": None})

    assert_status(response, 422)
    assert_error_detail(response, "title cannot be null")
