import pytest
from starlette.testclient import TestClient

from datasetu.db import DatasetStore
from datasetu.router import build_app
import pyarrow as pa

@pytest.fixture
def upgraded_client():
    store = DatasetStore()
    schema = pa.schema([
        ("Administrative Units - State Name", pa.string()),
        ("Administrative Units - District Name", pa.string()),
        ("Financial Provisions (INR) - Central Sanctioned Allocation", pa.float64()),
        ("Impact Metrics - Beneficiaries Reached", pa.int64()),
        ("lgd_district_code", pa.int64()),
        ("lgd_state_code", pa.int64()),
    ])
    table = pa.Table.from_pydict({
        "Administrative Units - State Name": ["Karnataka", "Maharashtra", "Uttar Pradesh"],
        "Administrative Units - District Name": ["Bengaluru Urban", "Pune", "Varanasi"],
        "Financial Provisions (INR) - Central Sanctioned Allocation": [2500000.0, 1800000.0, 3200000.0],
        "Impact Metrics - Beneficiaries Reached": [14500, 9800, 21000],
        "lgd_district_code": [556, 521, 142],
        "lgd_state_code": [29, 27, 9],
    }, schema=schema)
    store.load(table)

    # Register an additional domain dataset in catalog
    cat_schema = pa.schema([
        ("state", pa.string()),
        ("district", pa.string()),
        ("disbursed_inr", pa.float64()),
    ])
    cat_table = pa.Table.from_pydict({
        "state": ["Karnataka", "Bihar"],
        "district": ["Belagavi", "Patna"],
        "disbursed_inr": [4500000.0, 6200000.0]
    }, schema=cat_schema)
    store.register_dataset("pmkisan_dbt", cat_table, {"title": "PM-Kisan Farmer Direct Transfers"})

    app = build_app(store)
    return TestClient(app)

def test_list_catalog_datasets(upgraded_client: TestClient):
    resp = upgraded_client.get("/v1/datasets")
    assert resp.status_code == 200
    data = resp.json()
    assert "datasets" in data
    assert data["total_datasets"] >= 2
    ids = [d["id"] for d in data["datasets"]]
    assert "master" in ids
    assert "pmkisan_dbt" in ids

def test_query_catalog_dataset(upgraded_client: TestClient):
    resp = upgraded_client.get("/v1/datasets/pmkisan_dbt/data?limit=10")
    assert resp.status_code == 200
    body = resp.json()
    assert body["meta"]["dataset_id"] == "pmkisan_dbt"
    assert len(body["data"]) == 2
    assert body["data"][0]["district"] == "Belagavi"

def test_sql_execution_get_and_post(upgraded_client: TestClient):
    # Test POST /v1/sql
    post_resp = upgraded_client.post("/v1/sql", json={
        "query": "SELECT state, SUM(allocation) as total_alloc FROM dataset GROUP BY state ORDER BY total_alloc DESC"
    })
    assert post_resp.status_code == 200
    post_body = post_resp.json()
    assert len(post_body["rows"]) == 3
    assert post_body["rows"][0]["state"] == "Uttar Pradesh"
    assert post_body["rows"][0]["total_alloc"] == 3200000.0

    # Test GET /v1/sql
    get_resp = upgraded_client.get("/v1/sql?query=SELECT COUNT(*) as cnt FROM dataset")
    assert get_resp.status_code == 200
    get_body = get_resp.json()
    assert get_body["rows"][0]["cnt"] == 3

def test_sql_security_guard(upgraded_client: TestClient):
    # Attempt prohibited operations
    bad_resp = upgraded_client.post("/v1/sql", json={"query": "DROP TABLE dataset"})
    assert bad_resp.status_code == 403

    bad_resp2 = upgraded_client.post("/v1/sql", json={"query": "INSERT INTO dataset VALUES (1, 2)"})
    assert bad_resp2.status_code == 403

def test_geojson_export(upgraded_client: TestClient):
    # Test /v1/geojson
    resp = upgraded_client.get("/v1/geojson?limit=10")
    assert resp.status_code == 200
    geo = resp.json()
    assert geo["type"] == "FeatureCollection"
    assert len(geo["features"]) >= 1
    feature = geo["features"][0]
    assert feature["type"] == "Feature"
    assert "coordinates" in feature["geometry"]
    assert len(feature["geometry"]["coordinates"]) == 2

    # Test /v1/data?format=geojson
    resp2 = upgraded_client.get("/v1/data?format=geojson&limit=10")
    assert resp2.status_code == 200
    assert resp2.json()["type"] == "FeatureCollection"

def test_import_url_validation(upgraded_client: TestClient):
    # Reject non-http
    bad_resp = upgraded_client.post("/v1/import-url", json={"url": "ftp://example.com/data.csv"})
    assert bad_resp.status_code == 400
    assert "Invalid URL" in bad_resp.json()["detail"]

    # Reject empty
    empty_resp = upgraded_client.post("/v1/import-url", json={"url": ""})
    assert empty_resp.status_code == 400
    resp_fmt = upgraded_client.get("/v1/data?format=geojson&limit=5")
    assert resp_fmt.status_code == 200
    assert "application/geo+json" in resp_fmt.headers["content-type"]
