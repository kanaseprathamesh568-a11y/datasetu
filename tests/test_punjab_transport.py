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


def test_lgd_district_filter_and_export_limits(client):
    """Verify lgd_district comparator filter works without BinderException and export limits >= 11,742 succeed."""
    # 1. Test semantic alias filter lgd_district__gte
    resp = client.get("/v1/data?state=Assam&sector=Economy%20%26%20Finance&lgd_district__gte=1")
    assert resp.status_code == 200
    assert resp.json()["meta"]["total"] > 0

    # 2. Test exact column filter lgd_district_code__gte
    resp = client.get("/v1/data?state=Assam&sector=Economy%20%26%20Finance&lgd_district_code__gte=1")
    assert resp.status_code == 200
    assert resp.json()["meta"]["total"] > 0

    # 3. Test CSV export with full dataset limit
    csv_resp = client.get("/v1/data?format=csv&limit=11742")
    assert csv_resp.status_code == 200
    assert "text/csv" in csv_resp.headers["content-type"]
    assert "bharat_governance_master_2026.csv" in csv_resp.headers.get("content-disposition", "")

    # 4. Test GeoJSON export with full dataset limit
    geo_resp = client.get("/v1/geojson?limit=11742")
    assert geo_resp.status_code == 200
    assert "FeatureCollection" in geo_resp.text
    assert "bharat_governance_centroids.geojson" in geo_resp.headers.get("content-disposition", "")

