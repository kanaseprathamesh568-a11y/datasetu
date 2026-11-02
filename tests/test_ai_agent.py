"""Tests for DataSetu AI / LLM Semantic Query Agent."""

import pytest
from fastapi.testclient import TestClient
import pyarrow.parquet as pq

from datasetu.db import DatasetStore
from datasetu.router import build_app, _preload_catalog_datasets
from datasetu.ai import AIQueryEngine


@pytest.fixture(scope="module")
def client():
    store = DatasetStore()
    norm_tbl = pq.read_table("demo/precompiled_master.parquet")
    store.load(norm_tbl)
    _preload_catalog_datasets(store)
    app = build_app(store)
    return TestClient(app)


def test_ai_ask_pmkisan(client):
    response = client.post(
        "/v1/ai/ask",
        json={"question": "Which districts in Uttar Pradesh have the highest PM-KISAN funds?"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "PM-KISAN" in data["domain"]
    assert "tbl_pmkisan_national_dbt" in data["table_used"]
    assert "SELECT" in data["sql_query"]
    assert len(data["rows"]) > 0
    assert "Uttar Pradesh" in data["summary"]
    assert data["query_ms"] < 100.0
    assert "curl" in data["developer_snippets"]


def test_ai_ask_tap_water(client):
    response = client.post(
        "/v1/ai/ask",
        json={"question": "Show top 5 districts in Bihar by tap water connections under Jal Jeevan"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "Jal Jeevan" in data["domain"]
    assert len(data["rows"]) == 5
    assert data["metrics"]["top_district"] != "N/A"


def test_ai_ask_empty_prompt_validation(client):
    response = client.post(
        "/v1/ai/ask",
        json={"question": "   "},
    )
    assert response.status_code == 400
    assert "cannot be empty" in response.json()["detail"]


def test_ai_query_alias(client):
    response = client.post(
        "/v1/ai/query",
        json={"question": "What is the total MGNREGA employment wage disbursed in Maharashtra?"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "MGNREGA" in data["domain"]
    assert len(data["key_insights"]) >= 3
