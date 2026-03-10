#wrapper (envoltura) para requests, para centralizar la configuración y el manejo de errores
import requests
import os
import time
from typing import Any, Dict, Optional

class ApiClient:
    def __init__(self, base_url: str, timeout_seconds: float = 10.0):
        self.base_url = base_url.rstrip("/")
        env_timeout = os.getenv("API_TIMEOUT")
        self.timeout_seconds = float(env_timeout) if env_timeout else timeout_seconds
        env_retries = os.getenv("API_RETRIES")
        self.max_retries = int(env_retries) if env_retries else 2
        env_retry_wait = os.getenv("API_RETRY_WAIT")
        self.retry_wait_seconds = float(env_retry_wait) if env_retry_wait else 0.1
        self.session = requests.Session()

    def post(self, path: str, json: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None):
        url = f"{self.base_url}{path}"
        return self.session.post(url, json=json, headers=headers, timeout=self.timeout_seconds)

    def get(self, path: str, headers: Optional[Dict[str, str]] = None):
        url = f"{self.base_url}{path}"
        attempts = self.max_retries + 1
        last_response = None

        for attempt in range(attempts):
            try:
                response = self.session.get(url, headers=headers, timeout=self.timeout_seconds)
            except requests.RequestException:
                if attempt == attempts - 1:
                    raise
                time.sleep(self.retry_wait_seconds)
                continue

            last_response = response
            if response.status_code < 500:
                return response

            if attempt < attempts - 1:
                time.sleep(self.retry_wait_seconds)

        return last_response
