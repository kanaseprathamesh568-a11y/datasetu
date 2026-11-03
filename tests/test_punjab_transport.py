"""Test specific sector and state filtering scenarios, including Punjab + Road Transport & Highways."""

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


def test_punjab_road_transport_records_exist(client):
    """Verify that filtering for Punjab and Road Transport & Highways returns verified records."""
    resp = client.get("/v1/data?state=Punjab&sector=Road%20Transport%20%26%20Highways&limit=50")
    assert resp.status_code == 200
    data = resp.json()
    assert data["meta"]["total"] > 0
    assert len(data["data"]) > 0

    first = data["data"][0]
    assert first["Administrative Units - State Name"] == "Punjab"
    assert first["Governance Portfolio - Sector Category"] == "Road Transport & Highways"
    assert "Bharatmala" in first["Governance Portfolio - National Flagship Scheme"] or "Central Road" in first["Governance Portfolio - National Flagship Scheme"]
    assert first["Financial Provisions (INR) - Central Sanctioned Allocation"] > 0
    assert first["lgd_district_code"] is not None
