"""Unique payload builders for independent, repeatable API tests."""

from typing import Any
from uuid import uuid4


def task_payload(**overrides: Any) -> dict[str, Any]:
    """Return a valid task payload with a collision-resistant title."""

    payload: dict[str, Any] = {
        "title": f"Automated task {uuid4().hex[:8]}",
        "description": "Created by the API automation framework",
        "status": "todo",
        "priority": "medium",
    }
    payload.update(overrides)
    return payload
