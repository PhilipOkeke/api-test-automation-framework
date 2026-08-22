"""Wait for the TaskFlow API to become ready during CI startup."""

import time

import requests

from taskflow_test_framework.config import Settings


def wait_for_api(attempts: int = 30, delay_seconds: float = 1.0) -> None:
    settings = Settings.from_env()
    health_url = f"{settings.base_url}/health"

    for attempt in range(1, attempts + 1):
        try:
            response = requests.get(health_url, timeout=2)
            if response.status_code == 200:
                print(f"TaskFlow API is ready after {attempt} attempt(s).")
                return
        except requests.RequestException:
            pass
        time.sleep(delay_seconds)

    raise RuntimeError(f"TaskFlow API did not become ready at {health_url}")


if __name__ == "__main__":
    wait_for_api()
