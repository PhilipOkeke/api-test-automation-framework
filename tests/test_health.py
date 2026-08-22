"""Smoke tests for service availability."""

import pytest

from taskflow_test_framework.assertions import assert_status
from taskflow_test_framework.client import TaskFlowClient


@pytest.mark.smoke
def test_health_endpoint_reports_healthy(api_client: TaskFlowClient) -> None:
    response = api_client.health()

    assert_status(response, 200)
    assert response.json() == {"status": "healthy"}
