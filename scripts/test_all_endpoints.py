import urllib.parse
import json
import httpx

base_url = "http://127.0.0.1:8000"
client = httpx.Client(base_url=base_url, timeout=10.0)

endpoints_to_test = [
    # 1. Base endpoints
    ("GET", "/health", None),
    ("GET", "/v1/data?page=1&limit=5", None),
    ("GET", "/v1/data/summary", None),
    ("GET", "/v1/data/summary?group_by=state&metric=expenditure", None),
    ("GET", "/v1/geojson?limit=10", None),
    ("GET", "/v1/hygiene", None),
    
    # 2. Audit & Correlator
    ("GET", "/v1/audit/anomalies", None),
    ("GET", "/v1/correlate?dataset_x=road_transport&dataset_y=rural_development&metric_x=allocation&metric_y=beneficiaries", None),
    
    # 3. AI Endpoint
    ("POST", "/v1/ai/ask", {"question": "Top districts by funds in UP", "max_rows": 5, "language": "en"}),
    
    # 4. SQL Studio
    ("POST", "/v1/sql", {"query": "SELECT * FROM dataset LIMIT 5"}),
    
    # 5. Catalog Search & Federation
    ("GET", "/v1/catalog/search?q=kisan", None),
    ("GET", "/v1/future-sync/status", None),
    
    # 6. Webhooks
    ("GET", "/v1/webhooks/subscriptions", None),
    ("POST", "/v1/webhooks/simulate", {"event_type": "cdc.mutation", "district": "Amritsar, Punjab"}),
    
    # 7. SDK generation
    ("GET", "/v1/sdk/python", None),
    ("GET", "/v1/sdk/typescript", None),
    ("GET", "/v1/sdk/go", None),
    
    # 8. LGD Crosswalk inspect
    ("GET", "/v1/crosswalk/inspect/Belgaum?state_hint=Karnataka", None),
]

passed = 0
failed = 0

for method, path, payload in endpoints_to_test:
    try:
        if method == "GET":
            r = client.get(path)
        else:
            r = client.post(path, json=payload)
        
        status = r.status_code
        if 200 <= status < 300:
            print(f"✅ {method} {path} -> HTTP {status} ({len(r.content)} bytes)")
            passed += 1
        else:
            print(f"❌ {method} {path} -> HTTP {status}: {r.text[:200]}")
            failed += 1
    except Exception as e:
        print(f"💥 {method} {path} -> Exception: {e}")
        failed += 1

print(f"\n--- TOTAL: {passed} PASSED, {failed} FAILED ---")
