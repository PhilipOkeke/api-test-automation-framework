"""Tests for filtering, search, and pagination behavior."""

from collections.abc import Callable
from typing import Any
from uuid import uuid4

import pytest

from taskflow_test_framework.assertions import assert_schema, assert_status
from taskflow_test_framework.client import TaskFlowClient

pytestmark = pytest.mark.regression


def test_filter_by_status_and_priority(
    api_client: TaskFlowClient,
    create_task: Callable[..., dict[str, Any]],
) -> None:
    keyword = f"filter-{uuid4().hex[:8]}"
    expected = create_task(title=f"{keyword} completed", status="done", priority="high")
    create_task(title=f"{keyword} pending", status="todo", priority="low")

    response = api_client.list_tasks(status="done", priority="high", search=keyword)

    assert_status(response, 200)
    body = response.json()
    assert_schema(body, "task_list.json")
    assert body["total"] == 1
    assert [task["id"] for task in body["items"]] == [expected["id"]]


def test_search_and_paginate_results(
    api_client: TaskFlowClient,
    create_task: Callable[..., dict[str, Any]],
) -> None:
    keyword = f"page-{uuid4().hex[:8]}"
    for index in range(3):
        create_task(title=f"{keyword} task {index}")

    first_page = api_client.list_tasks(search=keyword, limit=2, offset=0)
    second_page = api_client.list_tasks(search=keyword, limit=2, offset=2)

    assert_status(first_page, 200)
    assert_status(second_page, 200)
    assert_schema(first_page.json(), "task_list.json")
    assert first_page.json()["total"] == 3
    assert len(first_page.json()["items"]) == 2
    assert second_page.json()["total"] == 3
    assert len(second_page.json()["items"]) == 1
