"""Tests for Civic Audit Engine, Dataset Correlator, Polyglot SDKs, Webhooks, and Vernacular AI."""

import pytest
from fastapi.testclient import TestClient
import pyarrow.parquet as pq

from datasetu.db import DatasetStore
from datasetu.router import build_app


@pytest.fixture(scope="module")
def client():
    store = DatasetStore()
    table = pq.read_table("demo/precompiled_master.parquet")
    store.load(table)
    app = build_app(store)
    return TestClient(app)


def test_civic_audit_anomalies(client):
    """Verify forensic audit detects anomalies and computes hygiene score."""
    resp = client.get("/v1/audit/anomalies")
    assert resp.status_code == 200
    data = resp.json()
    assert "hygiene_score" in data
    assert data["hygiene_score"] >= 50.0
    assert "grade" in data
    assert "summary" in data
    assert data["total_records_audited"] > 0
    assert isinstance(data["anomalies"], list)


def test_cross_ministerial_correlator(client):
    """Verify cross-dataset correlation and Pearson r computation."""
    resp = client.get("/v1/correlate?dataset_x=master&metric_x=expenditure&dataset_y=master&metric_y=allocation")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "success"
    assert "pearson_r" in data
    assert -1.0 <= data["pearson_r"] <= 1.0
    assert "policy_insight" in data
    assert len(data["data_points"]) > 0


def test_typescript_sdk_download(client):
    """Verify TypeScript SDK generation endpoint."""
    resp = client.get("/v1/sdk/typescript")
    assert resp.status_code == 200
    assert "export class DataSetuClient" in resp.text
    assert "getData" in resp.text


def test_go_sdk_download(client):
    """Verify Go SDK generation endpoint."""
    resp = client.get("/v1/sdk/go")
    assert resp.status_code == 200
    assert "package datasetu" in resp.text
    assert "NewClient" in resp.text


def test_webhook_simulation(client):
    """Verify webhook registration and HMAC signature test dispatch."""
    sub_resp = client.post(
        "/v1/webhooks/subscribe",
        json={"url": "https://example.com/webhook", "name": "Test Listener"}
    )
    assert sub_resp.status_code == 200
    assert "id" in sub_resp.json()

    sim_resp = client.post(
        "/v1/webhooks/simulate",
        json={"target_url": "https://httpbin.org/post", "event_type": "audit.anomaly_flagged"}
    )
    assert sim_resp.status_code == 200
    data = sim_resp.json()
    assert "signature_header" in data
    assert data["signature_header"].startswith("sha256=")


def test_vernacular_ai_query(client):
    """Verify vernacular Hindi and Punjabi AI queries."""
    resp_hi = client.post("/v1/ai/ask", json={"question": "पंजाब में सड़क परिवहन पर कितना खर्च हुआ?", "language": "hi"})
    assert resp_hi.status_code == 200
    data_hi = resp_hi.json()
    assert "Punjab" in data_hi["sql_query"]
    assert "शीर्ष जिला" in data_hi["summary"] or "वैधानिक" in data_hi["summary"]
