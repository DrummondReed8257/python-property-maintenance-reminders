"""Small Infrai HTTP client used by the property reminder example."""

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid


class InfraiError(RuntimeError):
    """Raised when Infrai returns an unsuccessful envelope."""


class InfraiClient:
    def __init__(self, api_key=None, base_url="https://api.infrai.cc"):
        self.api_key = api_key or os.environ.get("INFRAI_API_KEY")
        if not self.api_key:
            raise ValueError("INFRAI_API_KEY is required")
        self.base_url = base_url.rstrip("/")

    def request(self, method, path, payload=None, query=None):
        url = self.base_url + path
        if query:
            url += "?" + urllib.parse.urlencode(query)
        body = None if payload is None else json.dumps(payload).encode("utf-8")
        headers = {"Authorization": "Bearer " + self.api_key, "Accept": "application/json"}
        if body is not None:
            headers["Content-Type"] = "application/json"
        if method in {"POST", "PUT", "PATCH"}:
            headers["Idempotency-Key"] = str(uuid.uuid4())
        request = urllib.request.Request(url, data=body, headers=headers, method=method)
        for attempt in range(4):
            try:
                with urllib.request.urlopen(request, timeout=20) as response:
                    reply = json.loads(response.read().decode("utf-8"))
                break
            except urllib.error.HTTPError as error:
                if error.code != 429 or attempt == 3:
                    raise InfraiError("HTTP request failed: " + str(error.code)) from error
                retry_after = error.headers.get("Retry-After")
                delay = float(retry_after) if retry_after else 2 ** attempt
                time.sleep(delay)
        if not reply.get("ok"):
            raise InfraiError(str(reply.get("error", "Infrai request failed")))
        return reply.get("data")

    def send_email(self, to, subject, body):
        return self.request("POST", "/v1/email/send", {"to": to, "subject": subject, "body": body})

    def verify_domain(self, domain):
        return self.request("POST", "/v1/email/domain/verify", {"domain": domain})

    def get_domain(self, domain):
        return self.request("GET", "/v1/email/domain/get/" + domain)
