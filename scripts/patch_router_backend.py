#!/usr/bin/env python3
"""Patch router.py in both datasetu/ and api/datasetu/ with enhanced endpoints and download-safe middleware."""

import sys
from pathlib import Path

ROUTER_FILES = [
    Path("/Users/_needtochill_/.gemini/antigravity/scratch/datasetu/datasetu/router.py"),
    Path("/Users/_needtochill_/.gemini/antigravity/scratch/datasetu/api/datasetu/router.py"),
]

for rf in ROUTER_FILES:
    content = rf.read_text(encoding="utf-8")

    # 1. Update GZipMiddleware imports and add DownloadSafeGZipMiddleware
    if "class DownloadSafeGZipMiddleware" not in content:
        content = content.replace(
            "from starlette.middleware.gzip import GZipMiddleware",
            "from starlette.middleware.gzip import GZipMiddleware, IdentityResponder\nfrom starlette.types import Scope, Receive, Send"
        )
        
        ds_middleware_code = """
class DownloadSafeGZipMiddleware(GZipMiddleware):
    \"\"\"GZipMiddleware that bypasses compression for binary and file download attachments to prevent browser interruptions.\"\"\"

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        qs = scope.get("query_string", b"").decode("latin1").lower()
        path = scope.get("path", "").lower()
        if (
            "format=csv" in qs
            or "format=parquet" in qs
            or "format=geojson" in qs
            or "/geojson" in path
            or "/sdk/" in path
            or path.endswith(".csv")
            or path.endswith(".parquet")
        ):
            responder = IdentityResponder(self.app, self.minimum_size)
            await responder(scope, receive, send)
            return
        await super().__call__(scope, receive, send)
"""
        content = content.replace(
            "app.add_middleware(GZipMiddleware, minimum_size=1000)",
            "app.add_middleware(DownloadSafeGZipMiddleware, minimum_size=1000)"
        )
        # Insert DownloadSafeGZipMiddleware class before def build_app
        content = content.replace("def build_app(", ds_middleware_code + "\ndef build_app(")

    # 2. Add Content-Length and Cache-Control to /v1/data CSV export
    old_csv_resp = """                return Response(
                    content=csv_bytes,
                    media_type="text/csv",
                    headers={
                        "Content-Disposition": f'attachment; filename="{fname}"',
                        "X-Query-Latency-MS": str(query_ms),
                    },
                )"""
    new_csv_resp = """                return Response(
                    content=csv_bytes,
                    media_type="text/csv; charset=utf-8",
                    headers={
                        "Content-Disposition": f'attachment; filename="{fname}"',
                        "Content-Length": str(len(csv_bytes)),
                        "Cache-Control": "no-transform, public, max-age=0",
                        "X-Query-Latency-MS": str(query_ms),
                    },
                )"""
    content = content.replace(old_csv_resp, new_csv_resp)

    # 3. Add Content-Length and Cache-Control to /v1/data Parquet export
    old_parquet_resp = """                return Response(
                    content=parquet_bytes,
                    media_type="application/octet-stream",
                    headers={
                        "Content-Disposition": f'attachment; filename="{fname}"',
                        "X-Query-Latency-MS": str(query_ms),
                    },
                )"""
    new_parquet_resp = """                return Response(
                    content=parquet_bytes,
                    media_type="application/octet-stream",
                    headers={
                        "Content-Disposition": f'attachment; filename="{fname}"',
                        "Content-Length": str(len(parquet_bytes)),
                        "Cache-Control": "no-transform, public, max-age=0",
                        "X-Query-Latency-MS": str(query_ms),
                    },
                )"""
    content = content.replace(old_parquet_resp, new_parquet_resp)

    # 4. Enhance /v1/crosswalk/districts and add /v1/lgd/districts
    old_crosswalk = """    # 9. LGD Administrative Gazette Crosswalk API
    @app.get(
        "/v1/crosswalk/districts",
        tags=["Metadata"],
        summary="Official Local Government Directory (LGD) district gazetteer with administrative aliases",
    )
    def get_lgd_crosswalk():
        import json
        lgd_path = Path(__file__).parent / "data" / "lgd_districts.json"
        if lgd_path.exists():
            return json.loads(lgd_path.read_text(encoding="utf-8"))
        return {"error": "LGD gazetteer not found"}"""

    new_crosswalk = """    # 9. LGD Administrative Gazette Crosswalk API
    @app.get(
        "/v1/crosswalk/districts",
        tags=["Metadata"],
        summary="Official Local Government Directory (LGD) district gazetteer with administrative aliases",
    )
    @app.get(
        "/v1/lgd/districts",
        tags=["Metadata"],
        summary="Official Local Government Directory (LGD) district gazetteer with administrative aliases",
    )
    def get_lgd_crosswalk(
        state: Optional[str] = Query(None, description="2-letter ISO state code (e.g. KA, UP, MH, PB) or State name"),
        limit: int = Query(782, ge=1, le=1000, description="Max districts to return"),
        offset: int = Query(0, ge=0, description="Pagination offset"),
        q: Optional[str] = Query(None, description="Filter district name or alias"),
        format: Optional[str] = Query("json", description="Output format: json, csv, parquet"),
    ):
        import json
        import io
        import csv as _csv

        lgd_path = Path(__file__).parent / "data" / "lgd_districts.json"
        if not lgd_path.exists():
            lgd_path = Path("/var/task/datasetu/data/lgd_districts.json")
        if not lgd_path.exists():
            lgd_path = Path("/var/task/api/datasetu/data/lgd_districts.json")

        if not lgd_path.exists():
            return {"error": "LGD gazetteer not found"}

        raw_data = json.loads(lgd_path.read_text(encoding="utf-8"))
        states = raw_data.get("states", {})
        all_districts = raw_data.get("districts", [])

        filtered = all_districts
        if state and state.strip():
            st_clean = state.strip().upper()
            matched_codes = set()
            for code, info in states.items():
                if (
                    info.get("iso", "").upper() == st_clean
                    or info.get("name", "").upper() == st_clean
                    or any(a.upper() == st_clean for a in info.get("aliases", []))
                ):
                    try:
                        matched_codes.add(int(code))
                    except ValueError:
                        pass
            if matched_codes:
                filtered = [d for d in filtered if d.get("state_code") in matched_codes]
            else:
                filtered = [
                    d for d in filtered
                    if d.get("state_name", "").upper() == st_clean or st_clean in d.get("state_name", "").upper()
                ]

        if q and q.strip():
            q_clean = q.strip().lower()
            filtered = [
                d for d in filtered
                if q_clean in d.get("canonical_name", "").lower()
                or any(q_clean in a.lower() for a in d.get("aliases", []))
            ]

        fmt = (format or "json").lower().strip()
        if fmt == "csv":
            out = io.StringIO()
            writer = _csv.writer(out)
            writer.writerow(["lgd_state_code", "state_name", "lgd_district_code", "canonical_name", "latitude", "longitude", "aliases"])
            for d in filtered[offset : offset + limit]:
                aliases_str = "; ".join(d.get("aliases", []))
                writer.writerow([
                    d.get("state_code", ""),
                    d.get("state_name", ""),
                    d.get("district_code", ""),
                    d.get("canonical_name", ""),
                    d.get("latitude", ""),
                    d.get("longitude", ""),
                    aliases_str,
                ])
            csv_bytes = out.getvalue().encode("utf-8")
            return Response(
                content=csv_bytes,
                media_type="text/csv; charset=utf-8",
                headers={
                    "Content-Disposition": 'attachment; filename="mopr_lgd_master_directory_2026.csv"',
                    "Content-Length": str(len(csv_bytes)),
                    "Cache-Control": "no-transform, public, max-age=0",
                },
            )

        return {
            "meta": {
                "source": "Official Local Government Directory (LGD) of India",
                "authority": "Ministry of Panchayati Raj (MoPR), Government of India",
                "total": len(filtered),
                "limit": limit,
                "offset": offset,
                "state_filter": state,
                "version": raw_data.get("_meta", {}).get("version", "2026.4-comprehensive"),
            },
            "districts": filtered[offset : offset + limit],
        }"""
    content = content.replace(old_crosswalk, new_crosswalk)

    # 5. Enhance /v1/datasets/{dataset_id}/data with filtering and formats
    old_catalog_data = """    @app.get(
        "/v1/datasets/{dataset_id}/data",
        tags=["Catalog"],
        summary="Query paginated records from a specific catalog dataset",
    )
    def query_catalog_dataset(
        dataset_id: str,
        page: int = Query(1, ge=1, description="Page number"),
        limit: int = Query(50, ge=1, le=1000, description="Records per page"),
    ):
        clean_id = dataset_id.lower().replace("-", "_").replace(" ", "_")
        target_tbl = f"tbl_{clean_id}"
        if clean_id not in store.catalog and target_tbl != store.table_name:
            raise HTTPException(status_code=404, detail=f"Dataset '{dataset_id}' not found in catalog.")

        tbl_name = store.catalog[clean_id]["table_name"] if clean_id in store.catalog else store.table_name
        offset = (page - 1) * limit
        total = store.conn.execute(f"SELECT COUNT(*) FROM {tbl_name}").fetchone()[0]
        cursor = store.conn.execute(f"SELECT * FROM {tbl_name} LIMIT {limit} OFFSET {offset}")
        cols = [d[0] for d in cursor.description]
        rows = [dict(zip(cols, r)) for r in cursor.fetchall()]
        return {
            "meta": {
                "dataset_id": dataset_id,
                "table": tbl_name,
                "total": total,
                "page": page,
                "limit": limit,
                "pages": (total + limit - 1) // limit,
            },
            "data": rows,
        }"""

    new_catalog_data = """    @app.get(
        "/v1/datasets/{dataset_id}/data",
        tags=["Catalog"],
        summary="Query paginated records from a specific catalog dataset",
    )
    def query_catalog_dataset(
        dataset_id: str,
        request: Request,
        page: int = Query(1, ge=1, description="Page number"),
        limit: int = Query(50, ge=1, le=50000, description="Records per page"),
        sort: Optional[str] = Query(None, description="Sort column (prefix with '-' for descending)"),
        fields: Optional[str] = Query(None, description="Comma-separated column names"),
        q: Optional[str] = Query(None, description="Full-text search query across all string columns"),
        format: Optional[str] = Query("json", description="Output format: json, csv, parquet, ndjson"),
    ):
        import io
        clean_id = dataset_id.lower().replace("-", "_").replace(" ", "_")
        target_tbl = f"tbl_{clean_id}"
        if clean_id not in store.catalog and target_tbl != store.table_name and clean_id != "master":
            raise HTTPException(status_code=404, detail=f"Dataset '{dataset_id}' not found in catalog.")

        tbl_name = store.catalog[clean_id]["table_name"] if clean_id in store.catalog else store.table_name

        cols_info = store.conn.execute(f"DESCRIBE {tbl_name}").fetchall()
        col_names = [r[0] for r in cols_info]
        col_types = {r[0]: str(r[1]).lower() for r in cols_info}

        reserved_params = {"page", "limit", "sort", "fields", "q", "format"}
        where_clauses = []
        params = []

        for p_key, p_val in request.query_params.items():
            if p_key in reserved_params or p_val == "":
                continue
            op = "="
            col_search = p_key
            if p_key.endswith("__gte"):
                op = ">="
                col_search = p_key[:-5]
            elif p_key.endswith("__lte"):
                op = "<="
                col_search = p_key[:-5]

            matched_col = None
            for c in col_names:
                c_low = c.lower()
                s_low = col_search.lower()
                if c_low == s_low:
                    matched_col = c
                    break
                if s_low in ("state", "state_name") and "state" in c_low and "status" not in c_low:
                    matched_col = c
                    break
                if s_low in ("district", "district_name") and "district" in c_low:
                    matched_col = c
                    break
                if s_low in ("sector", "scheme") and any(k in c_low for k in ["sector", "scheme", "mission"]):
                    matched_col = c
                    break
                if s_low in c_low:
                    matched_col = c
                    break

            if not matched_col:
                continue

            safe_c = _safe_sql_ident(matched_col)
            c_type = col_types.get(matched_col, "varchar")
            is_num = any(t in c_type for t in ["int", "double", "float", "decimal", "numeric", "real"])

            if op == "=" and isinstance(p_val, str) and not is_num:
                where_clauses.append(f"LOWER(CAST({safe_c} AS VARCHAR)) = LOWER(?)")
                params.append(p_val)
            elif is_num:
                try:
                    num_val = float(p_val) if "." in str(p_val) else int(p_val)
                    where_clauses.append(f"{safe_c} {op} ?")
                    params.append(num_val)
                except ValueError:
                    where_clauses.append(f"{safe_c} {op} ?")
                    params.append(p_val)
            else:
                where_clauses.append(f"{safe_c} {op} ?")
                params.append(p_val)

        if q and q.strip():
            q_clean = q.strip()[:256]
            token = f"%{q_clean.lower()}%"
            q_parts = []
            for c in col_names:
                q_parts.append(f"LOWER(CAST({_safe_sql_ident(c)} AS VARCHAR)) LIKE ?")
                params.append(token)
            if q_parts:
                where_clauses.append(f"({' OR '.join(q_parts)})")

        where_sql = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""

        sort_sql = ""
        if sort and sort.strip():
            desc = sort.strip().startswith("-")
            s_col = sort.strip()[1:] if desc else sort.strip()
            for c in col_names:
                if c.lower() == s_col.lower():
                    sort_sql = f"ORDER BY {_safe_sql_ident(c)} {'DESC' if desc else 'ASC'}"
                    break

        offset = (page - 1) * limit
        total = store.conn.execute(f"SELECT COUNT(*) FROM {tbl_name} {where_sql}", params).fetchone()[0]

        select_clause = "*"
        if fields:
            req_fields = [f.strip() for f in fields.split(",") if f.strip()]
            valid_fields = [_safe_sql_ident(c) for c in col_names if c in req_fields or any(c.lower() == rf.lower() for rf in req_fields)]
            if valid_fields:
                select_clause = ", ".join(valid_fields)

        data_sql = f"SELECT {select_clause} FROM {tbl_name} {where_sql} {sort_sql} LIMIT {limit} OFFSET {offset}"
        t0 = time.perf_counter()
        cursor = store.conn.execute(data_sql, params)
        cols = [d[0] for d in cursor.description]
        fetched_rows = cursor.fetchall()
        query_ms = round((time.perf_counter() - t0) * 1000.0, 2)

        fmt = (format or "json").lower().strip()
        if fmt == "csv":
            import csv as _csv
            out = io.StringIO()
            writer = _csv.writer(out)
            writer.writerow(cols)
            for r in fetched_rows:
                writer.writerow(r)
            csv_bytes = out.getvalue().encode("utf-8")
            fname = f"{clean_id}_2026.csv" if limit >= 5000 else f"{clean_id}_p{page}.csv"
            return Response(
                content=csv_bytes,
                media_type="text/csv; charset=utf-8",
                headers={
                    "Content-Disposition": f'attachment; filename="{fname}"',
                    "Content-Length": str(len(csv_bytes)),
                    "Cache-Control": "no-transform, public, max-age=0",
                    "X-Query-Latency-MS": str(query_ms),
                },
            )

        if fmt == "parquet":
            import pyarrow as pa
            import pyarrow.parquet as pq
            pydict = {col: [r[i] for r in fetched_rows] for i, col in enumerate(cols)}
            pa_table = pa.Table.from_pydict(pydict)
            buf = io.BytesIO()
            pq.write_table(pa_table, buf, compression="snappy")
            parquet_bytes = buf.getvalue()
            fname = f"{clean_id}_2026.parquet" if limit >= 5000 else f"{clean_id}_p{page}.parquet"
            return Response(
                content=parquet_bytes,
                media_type="application/octet-stream",
                headers={
                    "Content-Disposition": f'attachment; filename="{fname}"',
                    "Content-Length": str(len(parquet_bytes)),
                    "Cache-Control": "no-transform, public, max-age=0",
                    "X-Query-Latency-MS": str(query_ms),
                },
            )

        rows = [dict(zip(cols, r)) for r in fetched_rows]
        return {
            "meta": {
                "dataset_id": dataset_id,
                "table": tbl_name,
                "total": total,
                "page": page,
                "limit": limit,
                "pages": max(1, (total + limit - 1) // limit),
                "query_ms": query_ms,
            },
            "data": rows,
        }"""
    content = content.replace(old_catalog_data, new_catalog_data)

    rf.write_text(content, encoding="utf-8")
    print(f"Successfully patched {rf}")

