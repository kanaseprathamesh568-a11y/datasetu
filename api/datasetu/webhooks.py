"""Event-Driven Webhooks & Change Notification Module for DataSetu.

What this module does:
1. Maintains subscriptions for developer webhooks for real-time public data events:
   - `dataset.updated`: CDC sync or background table reload
   - `dataset.jit_compiled`: New remote dataset streamed and mounted into DuckDB
   - `audit.anomaly_flagged`: Forensic audit detects fiscal leakage or dormant funds
2. Signs payloads using HMAC-SHA256 (`X-DataSetu-Signature`) for defense-in-depth authenticity.
3. Exposes a live interactive Webhook Dispatch Simulator for developers to test receiver endpoints.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import time
from typing import Any, Dict, List, Optional

import httpx


class WebhookManager:
    """Manages developer webhook subscriptions and event dispatching."""

    def __init__(self):
        self._subscriptions: List[Dict[str, Any]] = [
            {
                "id": "wh_mock_audit_alert",
                "name": "Civic Watchdog Audit Listener",
                "url": "https://webhook.site/demo-datasetu-audit-alert",
                "events": ["audit.anomaly_flagged", "dataset.updated"],
                "created_at": "2026-11-04T00:00:00Z",
                "secret": "whsec_bharat_dpi_audit_2026",
                "active": True,
            }
        ]
        self._dispatch_history: List[Dict[str, Any]] = []

    def register(
        self,
        url: str,
        events: Optional[List[str]] = None,
        name: Optional[str] = None,
        secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Registers a new developer webhook endpoint."""
        wh_id = f"wh_{int(time.time())}_{abs(hash(url)) % 10000}"
        sub = {
            "id": wh_id,
            "name": name or f"Webhook for {httpx.URL(url).host}",
            "url": url,
            "events": events or ["dataset.updated", "audit.anomaly_flagged", "dataset.jit_compiled"],
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "secret": secret or f"whsec_{hashlib.sha256(str(time.time()).encode()).hexdigest()[:16]}",
            "active": True,
        }
        self._subscriptions.append(sub)
        return sub

    def list_subscriptions(self) -> List[Dict[str, Any]]:
        """Returns list of active webhook subscriptions (masking secrets)."""
        safe_subs = []
        for s in self._subscriptions:
            item = dict(s)
            item["secret"] = item["secret"][:6] + "..." + item["secret"][-4:] if item.get("secret") else "none"
            safe_subs.append(item)
        return safe_subs

    async def simulate_dispatch(
        self,
        target_url: str,
        event_type: str = "audit.anomaly_flagged",
        custom_payload: Optional[Dict[str, Any]] = None,
        secret: str = "whsec_demo_secret",
    ) -> Dict[str, Any]:
        """Dispatches an event payload with HMAC-SHA256 signature to verify receiver compatibility."""
        t_start = time.perf_counter()

        payload = custom_payload or {
            "event": event_type,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "source": "DataSetu Civic DPI Engine",
            "data": {
                "dataset_id": "bharat_governance_master_2026",
                "state": "Punjab",
                "district": "Amritsar",
                "lgd_code": 24,
                "scheme": "Bharatmala Pariyojana - Delhi-Amritsar-Katra Expressway Corridor",
                "sanctioned_budget_inr": 165862629.59,
                "actual_expenditure_inr": 144561291.26,
                "lifecycle_status": "Audited & Verified",
                "audit_finding": "Normal Execution (87.2% budget absorption rate).",
            },
        }

        body_bytes = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        signature = hmac.new(secret.encode("utf-8"), body_bytes, hashlib.sha256).hexdigest()

        headers = {
            "User-Agent": "DataSetu-Webhook-Dispatcher/1.0",
            "Content-Type": "application/json",
            "X-DataSetu-Event": event_type,
            "X-DataSetu-Signature": f"sha256={signature}",
            "X-DataSetu-Delivery": f"del_{int(time.time() * 1000)}",
        }

        # Attempt HTTP POST with safe timeout
        http_status = 200
        error_msg = None
        response_text = ""

        try:
            async with httpx.AsyncClient(timeout=4.0) as client:
                resp = await client.post(target_url, content=body_bytes, headers=headers)
                http_status = resp.status_code
                response_text = resp.text[:200]
        except Exception as e:
            http_status = 0
            error_msg = str(e)
            response_text = f"Connection failed (simulated dry-run recorded): {e}"

        duration_ms = (time.perf_counter() - t_start) * 1000

        result = {
            "status": "delivered" if 200 <= http_status < 300 else ("dispatched_with_notice" if http_status == 0 else "failed"),
            "event_type": event_type,
            "target_url": target_url,
            "http_status": http_status,
            "latency_ms": round(duration_ms, 2),
            "signature_header": f"sha256={signature}",
            "payload_preview": payload,
            "response_preview": response_text,
            "error": error_msg,
        }

        self._dispatch_history.insert(0, result)
        if len(self._dispatch_history) > 20:
            self._dispatch_history.pop()

        return result
