"""Tests for Universal Open Data Federation & JIT Compiler (300,000+ Datasets)."""

import pytest
from fastapi.testclient import TestClient
import pyarrow.parquet as pq

from datasetu.db import DatasetStore
from datasetu.router import build_app, _preload_catalog_datasets
from datasetu.federation import OpenDataFederationEngine


@pytest.fixture(scope="module")
def client():
    store = DatasetStore()
    norm_tbl = pq.read_table("demo/precompiled_master.parquet")
    store.load(norm_tbl)
    _preload_catalog_datasets(store)
    app = build_app(store)
    return TestClient(app)


def test_federation_sources(client):
    response = client.get("/v1/federation/sources")
    assert response.status_code == 200
    data = response.json()
    assert "300,000+" in data["total_ecosystem_scale"]
    assert len(data["sources"]) >= 4


def test_federation_search(client):
    response = client.get("/v1/federation/search?q=gdp&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert data["total_matches"] > 0
    assert "300,000+" in data["total_ecosystem_datasets"]
    first = data["datasets"][0]
    assert "title" in first
    assert "compile_action" in first


@pytest.mark.asyncio
async def test_federation_engine_world_bank_search():
    store = DatasetStore()
    fed = OpenDataFederationEngine(store)
    res = fed.search_federated(query="inflation", source="world_bank")
    assert res["total_matches"] >= 1
    assert "CPI" in res["datasets"][0]["title"]


@pytest.mark.asyncio
async def test_federation_compile_catalog_jit():
    store = DatasetStore()
    fed = OpenDataFederationEngine(store)
    res = await fed.compile_remote_dataset_jit(url="pmfby_crop_insurance", title="PM Fasal Bima Yojana")
    assert res["status"] == "success"
    assert res["records_ingested"] == 782
    assert "tbl_pmfby_crop_insurance" in store.catalog["pmfby_crop_insurance"]["table_name"]

    # Verify queryable in DuckDB
    qr = store.execute_sql("SELECT COUNT(*) as c FROM tbl_pmfby_crop_insurance")
    assert qr.rows[0]["c"] == 782
