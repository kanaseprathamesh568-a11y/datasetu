"""Tests for Universal Catalog Index (2,500+ Datasets) & Continuous Future Harvester."""

import pytest
from fastapi.testclient import TestClient
import pyarrow.parquet as pq

from datasetu.db import DatasetStore
from datasetu.router import build_app, _preload_catalog_datasets
from datasetu.catalog_index import UniversalCatalogIndex
from datasetu.harvester import FutureSyncEngine


@pytest.fixture(scope="module")
def client():
    store = DatasetStore()
    norm_tbl = pq.read_table("demo/precompiled_master.parquet")
    store.load(norm_tbl)
    _preload_catalog_datasets(store)
    app = build_app(store)
    return TestClient(app)


def test_master_catalog_has_over_2500_datasets():
    idx = UniversalCatalogIndex()
    assert len(idx.catalog) >= 2500


def test_catalog_search_endpoint(client):
    response = client.get("/v1/catalog/search?q=water&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert data["total_datasets_indexed"] >= 2500
    assert data["total_matches"] > 0
    assert len(data["datasets"]) <= 10


def test_catalog_sectors_endpoint(client):
    response = client.get("/v1/catalog/sectors")
    assert response.status_code == 200
    data = response.json()
    assert len(data["sectors"]) >= 10
    assert len(data["ministries"]) >= 10


def test_future_sync_status(client):
    response = client.get("/v1/future-sync/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert data["active_subscriptions"] >= 4
    assert data["zero_downtime_swaps_enabled"] is True


def test_future_sync_trigger(client):
    response = client.post("/v1/future-sync/trigger")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["new_datasets_discovered"] >= 1


def test_future_sync_subscribe(client):
    payload = {
        "url": "https://data.gov.in/api/1/rest/dataset/rural-infrastructure-2027",
        "title": "Future Rural Roads Master 2027",
        "portal": "MoRD Open Portal",
        "cadence": "Monthly",
    }
    response = client.post("/v1/future-sync/subscribe", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "subscribed"
    assert data["title"] == "Future Rural Roads Master 2027"
