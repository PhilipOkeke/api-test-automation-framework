"""HTTP client used by the TaskFlow API tests."""

from typing import Any

import requests
from requests import Response

from taskflow_test_framework.config import Settings


class TaskFlowClient:
    """Reusable authenticated client that keeps HTTP details out of tests."""

    def __init__(
        self,
        settings: Settings | None = None,
        session: requests.Session | None = None,
    ) -> None:
        self.settings = settings or Settings.from_env()
        self.session = session or requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def _request(self, method: str, path: str, **kwargs: Any) -> Response:
        return self.session.request(
            method,
            f"{self.settings.base_url}{path}",
            timeout=self.settings.request_timeout,
            **kwargs,
        )

    def health(self) -> Response:
        return self._request("GET", "/health")

    def register(self, email: str, password: str, full_name: str) -> Response:
        return self._request(
            "POST",
            "/api/v1/auth/register",
            json={"email": email, "password": password, "full_name": full_name},
        )

    def login(self, email: str, password: str) -> Response:
        response = self._request(
            "POST",
            "/api/v1/auth/token",
            data={"username": email, "password": password},
        )
        if response.ok:
            token = response.json()["access_token"]
            self.session.headers.update({"Authorization": f"Bearer {token}"})
        return response

    def create_task(self, payload: dict[str, Any]) -> Response:
        return self._request("POST", "/api/v1/tasks", json=payload)

    def list_tasks(self, **filters: Any) -> Response:
        params = {key: value for key, value in filters.items() if value is not None}
        return self._request("GET", "/api/v1/tasks", params=params)

    def get_task(self, task_id: int) -> Response:
        return self._request("GET", f"/api/v1/tasks/{task_id}")

    def update_task(self, task_id: int, payload: dict[str, Any]) -> Response:
        return self._request("PATCH", f"/api/v1/tasks/{task_id}", json=payload)

    def delete_task(self, task_id: int) -> Response:
        return self._request("DELETE", f"/api/v1/tasks/{task_id}")

    def close(self) -> None:
        self.session.close()

    def __enter__(self) -> "TaskFlowClient":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
"""HTTP client used by the TaskFlow API tests."""

from typing import Any

import requests
from requests import Response

from taskflow_test_framework.config import Settings


class TaskFlowClient:
    """Small reusable client that keeps HTTP details out of test cases."""

    def __init__(
        self,
        settings: Settings | None = None,
        session: requests.Session | None = None,
    ) -> None:
        self.settings = settings or Settings.from_env()
        self.session = session or requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def _request(self, method: str, path: str, **kwargs: Any) -> Response:
        return self.session.request(
            method,
            f"{self.settings.base_url}{path}",
            timeout=self.settings.request_timeout,
            **kwargs,
        )

    def health(self) -> Response:
        return self._request("GET", "/health")

    def create_task(self, payload: dict[str, Any]) -> Response:
        return self._request("POST", "/api/v1/tasks", json=payload)

    def list_tasks(self, **filters: Any) -> Response:
        params = {key: value for key, value in filters.items() if value is not None}
        return self._request("GET", "/api/v1/tasks", params=params)

    def get_task(self, task_id: int) -> Response:
        return self._request("GET", f"/api/v1/tasks/{task_id}")

    def update_task(self, task_id: int, payload: dict[str, Any]) -> Response:
        return self._request("PATCH", f"/api/v1/tasks/{task_id}", json=payload)

    def delete_task(self, task_id: int) -> Response:
        return self._request("DELETE", f"/api/v1/tasks/{task_id}")

    def close(self) -> None:
        self.session.close()

    def __enter__(self) -> "TaskFlowClient":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
