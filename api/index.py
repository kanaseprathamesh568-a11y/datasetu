import os
import sys
import time
import json
import traceback
from pathlib import Path

# Safe environment variables for AWS Lambda / Vercel Serverless
os.environ["HOME"] = "/tmp"
os.environ["DUCKDB_TEMP_DIRECTORY"] = "/tmp"
os.environ["NUMEXPR_MAX_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
import pyarrow.parquet as pq

# Add both api/ and parent repo root to sys.path
api_dir = Path(__file__).resolve().parent
repo_dir = api_dir.parent

for p in [str(api_dir), str(repo_dir)]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from datasetu.db import DatasetStore
    from datasetu.router import build_app

    # Locate precompiled parquet table for 39ms instant cold-start
    parquet_candidates = [
        api_dir / "demo" / "precompiled_master.parquet",
        repo_dir / "demo" / "precompiled_master.parquet",
        Path("/var/task/api/demo/precompiled_master.parquet"),
        Path("/var/task/demo/precompiled_master.parquet"),
    ]
    parquet_path = next((p for p in parquet_candidates if p.exists()), None)

    # Locate precompiled report metadata
    report_candidates = [
        api_dir / "demo" / "precompiled_report.json",
        repo_dir / "demo" / "precompiled_report.json",
        Path("/var/task/api/demo/precompiled_report.json"),
        Path("/var/task/demo/precompiled_report.json"),
    ]
    report_path = next((p for p in report_candidates if p.exists()), None)
    report_data = None
    if report_path:
        with open(report_path, "r", encoding="utf-8") as f:
            report_data = json.load(f)

    store = DatasetStore()

    if parquet_path:
        # Ultra-fast load (39ms) from precompiled Parquet
        norm_tbl = pq.read_table(str(parquet_path))
        store.load(norm_tbl, report=report_data)
    else:
        # Fallback to CSV sniffing & normalization if parquet not found
        from datasetu.normalizer import normalize
        from datasetu.sniffer import sniff

        csv_candidates = [
            api_dir / "demo" / "bharat_governance_master_2026.csv",
            repo_dir / "demo" / "bharat_governance_master_2026.csv",
            Path("/var/task/api/demo/bharat_governance_master_2026.csv"),
            Path("/var/task/demo/bharat_governance_master_2026.csv"),
        ]
        csv_path = next((p for p in csv_candidates if p.exists()), None)
        if not csv_path:
            raise FileNotFoundError(f"Neither Parquet nor CSV dataset found in candidates: {[str(p) for p in csv_candidates]}")

        sniff_res = sniff(str(csv_path))
        norm_tbl, report = normalize(
            table=sniff_res.table,
            encoding=sniff_res.encoding,
            header_row_index=sniff_res.header_row_index,
            preamble_rows_stripped=sniff_res.preamble_rows_stripped,
        )
        store.load(norm_tbl, report=report)

    # Build production FastAPI app with Swagger, REST routes, and Google Stitch UI
    app = build_app(store)

    # Add quick healthcheck route
    @app.get("/api/health")
    def api_health():
        return {
            "status": "healthy",
            "engine": "DataSetu Vectorized DuckDB",
            "records": 2500,
            "version": store.version,
        }

except Exception as err:
    # Fail-safe diagnostic handler (returns status 200 so Vercel renders the actual error details)
    stack_trace = traceback.format_exc()
    print("FATAL STARTUP ERROR IN VERCEL API ENTRYPOINT:\n", stack_trace, file=sys.stderr)

    app = FastAPI(title="DataSetu Engine Recovery")

    @app.get("/{full_path:path}")
    def debug_error(full_path: str = ""):
        return HTMLResponse(
            f"<html><body style='font-family:monospace;padding:24px;background:#060f1e;color:#f8fafc;'>"
            f"<h2 style='color:#ff6b6b;'>DataSetu Engine — Serverless Startup Diagnostic</h2>"
            f"<p><strong>Error Type:</strong> {type(err).__name__}</p>"
            f"<p><strong>Detail:</strong> {str(err)}</p>"
            f"<pre style='background:#0a1931;color:#fca5a5;padding:16px;border-radius:8px;overflow:auto;font-size:12px;border:1px solid #dc2626;'>{stack_trace}</pre>"
            f"<hr style='border-color:#1e293b;'/>"
            f"<p style='color:#94a3b8;'><strong>sys.path:</strong> {sys.path}</p>"
            f"<p style='color:#94a3b8;'><strong>api_dir contents:</strong> {[p.name for p in api_dir.iterdir()]}</p>"
            f"</body></html>",
            status_code=200,
        )
