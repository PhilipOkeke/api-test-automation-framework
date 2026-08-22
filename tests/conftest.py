"""Shared PyTest fixtures for TaskFlow API tests."""

from collections.abc import Callable, Generator
from typing import Any

import pytest
import requests

from taskflow_test_framework.assertions import assert_status
from taskflow_test_framework.client import TaskFlowClient
from taskflow_test_framework.config import Settings
from taskflow_test_framework.factories import task_payload


@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings.from_env()


@pytest.fixture(scope="session")
def api_client(settings: Settings) -> Generator[TaskFlowClient, None, None]:
    with TaskFlowClient(settings) as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
def require_running_api(api_client: TaskFlowClient) -> None:
    try:
        response = api_client.health()
    except requests.RequestException as error:
        pytest.fail(
            "TaskFlow API is not reachable. Start it before running these tests. "
            f"Connection error: {error}",
            pytrace=False,
        )
    assert_status(response, 200)


@pytest.fixture(scope="session")
def created_task_ids() -> Generator[list[int], None, None]:
    task_ids: list[int] = []
    yield task_ids


@pytest.fixture
def create_task(
    api_client: TaskFlowClient,
    created_task_ids: list[int],
) -> Generator[Callable[..., dict[str, Any]], None, None]:
    def _create(**overrides: Any) -> dict[str, Any]:
        response = api_client.create_task(task_payload(**overrides))
        assert_status(response, 201)
        task = response.json()
        created_task_ids.append(task["id"])
        return task

    yield _create

    for task_id in created_task_ids[:]:
        response = api_client.delete_task(task_id)
        if response.status_code in {204, 404}:
            created_task_ids.remove(task_id)
