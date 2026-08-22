"""End-to-end task lifecycle tests."""

from collections.abc import Callable
from typing import Any

import pytest

from taskflow_test_framework.assertions import assert_error_detail, assert_schema, assert_status
from taskflow_test_framework.client import TaskFlowClient
from taskflow_test_framework.factories import task_payload

pytestmark = pytest.mark.regression


@pytest.mark.smoke
def test_create_and_read_task(
    api_client: TaskFlowClient,
    created_task_ids: list[int],
) -> None:
    payload = task_payload(priority="high")

    create_response = api_client.create_task(payload)
    assert_status(create_response, 201)
    created_task = create_response.json()
    created_task_ids.append(created_task["id"])
    assert_schema(created_task, "task.json")
    assert created_task["title"] == payload["title"]
    assert created_task["priority"] == "high"

    read_response = api_client.get_task(created_task["id"])
    assert_status(read_response, 200)
    assert read_response.json() == created_task


def test_update_task(
    api_client: TaskFlowClient,
    create_task: Callable[..., dict[str, Any]],
) -> None:
    task = create_task()

    response = api_client.update_task(
        task["id"],
        {"status": "done", "priority": "high", "description": "Verified by automation"},
    )

    assert_status(response, 200)
    updated_task = response.json()
    assert_schema(updated_task, "task.json")
    assert updated_task["status"] == "done"
    assert updated_task["priority"] == "high"
    assert updated_task["description"] == "Verified by automation"


def test_delete_task(
    api_client: TaskFlowClient,
    create_task: Callable[..., dict[str, Any]],
) -> None:
    task = create_task()

    delete_response = api_client.delete_task(task["id"])
    assert_status(delete_response, 204)
    assert delete_response.content == b""

    read_response = api_client.get_task(task["id"])
    assert_status(read_response, 404)
    assert_error_detail(read_response, "Task not found")
