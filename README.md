# DataSetu 🌉 (डेटासेतु)

> **Autonomous National Open Data to Open API Engine.**  
> Transform messy, non-standard Indian public tabular data into clean, validated, LGD-standardized OpenAPI 3.1 REST endpoints and sub-millisecond DuckDB columnar stores with **ONE command**.

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-brightgreen.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com)
[![DuckDB](https://img.shields.io/badge/DuckDB-Vectorized_Engine-FFF000.svg?logo=duckdb)](https://duckdb.org)
[![Apache Arrow](https://img.shields.io/badge/PyArrow-Zero--Copy_Columnar-E6522C.svg?logo=apachearrow)](https://arrow.apache.org)
[![Tests Passing](https://img.shields.io/badge/Tests-55%2F55_Passed-success.svg)](tests/)

---

## ⚡ Live Demos & Sandboxes

- **Live Public Sandbox**: [https://datasetu-five.vercel.app/](https://datasetu-five.vercel.app/)
- **Interactive Swagger OpenAPI 3.1 Specs**: [https://datasetu-five.vercel.app/docs](https://datasetu-five.vercel.app/docs)
- **Empirical Multi-Ministry Benchmark Report**: [`benchmark/BENCHMARK_REPORT.md`](benchmark/BENCHMARK_REPORT.md)
- **GitHub Repository**: [https://github.com/kanaseprathamesh568-a11y/datasetu](https://github.com/kanaseprathamesh568-a11y/datasetu)

> **Disclaimer**: DataSetu is an independent open-source civic tech initiative. It is not affiliated with, maintained by, or endorsed by the National Informatics Centre (NIC), Ministry of Electronics & IT (MeitY), or data.gov.in. Public datasets are processed under the Government Open Data License (GODL-India) and NDSAP.

---

## 1. The Challenge in Indian Open Data

India’s open data platforms ([data.gov.in](https://data.gov.in) and state repositories) host over **230,000 public datasets**, yet **less than 2% provide functional, queryable APIs**. Civic developers, researchers, and data journalists spend over 80% of project time writing fragile one-off cleaning scripts because real-world government spreadsheets contain:

1. **Non-Standard Encodings & Preambles**: Files encoded in Windows CP-1252 or UTF-8 with BOM, often prepended by 2–5 banner metadata lines before the actual table header.
2. **Merged & Multi-Row Headers**: Hierarchical ministry tables where column labels span multiple rows (e.g., parent ministry row above metric columns).
3. **Indic Monetary & Numeral Notations**: Mixed strings such as `"₹ 14.5 Lakhs"`, `"12 Crores"`, `"२,०००/-"` (Devanagari numerals), parentheses for negatives `(450.00)`, and commas with asterisks `"1,45.20*"`.
4. **Administrative Renamings & Orthographic Variants**: Colonial vs. gazetted district names (*Poona* vs *Pune*, *Belgaum* vs *Belagavi*, *Gurgaon* vs *Gurugram*, *Calcutta* vs *Kolkata*).
5. **Cross-State Name Collisions**: Over 15 district names recur identically across different States (e.g., *Bilaspur* in HP vs CG; *Hamirpur* in HP vs UP; *Pratapgarh* in UP vs RJ). Silent heuristic guessing causes dangerous data corruption in public policy applications.

---

## 2. Architecture & The Deterministic Compiler Pipeline

DataSetu solves this via a **100% deterministic 4-stage data compiler** with zero cloud lock-in and zero hallucination in the core execution path:

```
┌─────────────────┐     ┌──────────────────────┐     ┌────────────────────┐     ┌──────────────────┐
│ 1. SMART        │ ──▶ │ 2. BHARAT            │ ──▶ │ 3. DYNAMIC         │ ──▶ │ 4. SDK & CDC     │
│    SNIFFER      │     │    NORMALIZER        │     │    ROUTER (DUCKDB) │     │    WORKER        │
│ Encoding,       │     │ LGD Entity Resolver, │     │ In-memory columnar │     │ Typed Python SDK │
│ preambles,      │     │ Lakhs/Crores -> float│     │ FastAPI + OpenAPI  │     │ Atomic swap sync │
│ merged headers  │     │ Safe Ambiguity Guard │     │ sub-4ms queries    │     │ semver changelog │
└─────────────────┘     └──────────────────────┘     └────────────────────┘     └──────────────────┘
```

1. **Smart Sniffer**: Auto-detects encoding (UTF-8, UTF-8-BOM, CP-1252, Latin-1), strips non-tabular metadata banners, and collapses multi-row headers into clean snake_case identifiers.
2. **Bharat Normalizer**: Cleans Indic monetary amounts into pure floats, converts Devanagari numerals (`०-९`), and maps districts to statutory Local Government Directory (LGD) codes.
3. **Dynamic Router**: Loads standardized records into an in-memory vectorized **DuckDB** columnar table and synthesizes OpenAPI 3.1 RESTful endpoints on the fly.
4. **CDC & SDK Worker**: Watches source files for updates, executes atomic hot-swaps without server restarts, and auto-generates typed Python client SDKs.

---

## 3. Safe District Matching: The "Never Guess" Policy

Entity matching in government data must be safe. A wrong district assignment can misallocate crore-scale public welfare allocations.

DataSetu enforces a strict **Never Guess Policy**:
- **Confidence Tiers**: Every match receives a `confidence_tier` (`high`, `medium`, `low`, or `none`).
- **Needs Review Flag**: Any uncertain or ambiguous record is flagged with `lgd_needs_review = True` and a human-readable `lgd_review_reason`.
- **Ambiguous Districts Across States**: When an input contains a district name that exists in multiple states (such as *Bilaspur* in Himachal Pradesh and Chhattisgarh) without an explicit `state_hint`, DataSetu **refuses to guess**. It outputs:
  ```json
  {
    "lgd_state_code": null,
    "lgd_district_code": null,
    "lgd_match_method": "unmatched",
    "lgd_confidence_tier": "none",
    "lgd_needs_review": true,
    "lgd_review_reason": "Ambiguous: District 'Bilaspur' exists in multiple states (e.g. CG, HP). State hint required."
  }
  ```
- **Historical Renamings**: Handles historical and colonial names (*Poona* -> *Pune* (521), *Belgaum* -> *Belagavi* (555), *Gurgaon* -> *Gurugram* (70)) with `confidence_tier = "high"`.

---

## 4. Multi-Ministry Benchmark Suite (Empirical Results)

We evaluated DataSetu across **26 diverse public datasets** spanning 15+ central ministries and testing ugly real-world formatting edge cases (CP-1252, Lakhs/Crores, Devanagari numerals, empty files, and cross-state name collisions).

| Benchmark Metric | Measured Result | Methodology Notes |
| :--- | :--- | :--- |
| **Total Test Datasets** | **26 Datasets** | Ingested across 15+ Central Ministries |
| **Ingestion Success Rate** | **96.2%** (25/26) | 25 parsed perfectly; 1 corrupt empty file safely rejected upfront |
| **LGD District Match Rate** | **83.5%** | Exact & alias matches mapped to statutory MoPR codes |
| **Records Flagged for Review** | **21 Records** | Safely isolated by Ambiguity Guard ("Never Guess" policy) |
| **Average Pipeline Latency** | **6.12 ms** | End-to-end sniff, normalize, and DuckDB load |
| **DuckDB Query Latency** | **< 4.0 ms** | Filtered analytical queries on 2,500 records |

👉 *Full detailed report with dataset-by-dataset breakdown*: [`benchmark/BENCHMARK_REPORT.md`](benchmark/BENCHMARK_REPORT.md)

---

## 5. 5-Minute Quickstart

### Option A: Portable CLI (Local Python)

```bash
# 1. Clone repository
git clone https://github.com/kanaseprathamesh568-a11y/datasetu.git
cd datasetu

# 2. Set up virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install in editable mode
pip install -e .

# 4. Serve any messy CSV or Excel file
datasetu serve demo/bharat_governance_master_2026.csv
```

Open your browser:
- **Interactive UI & Disinfector Diff**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **OpenAPI 3.1 Swagger Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **REST Query Endpoint**: [http://127.0.0.1:8000/v1/data?state=KA&limit=10](http://127.0.0.1:8000/v1/data?state=KA&limit=10)

---

### Option B: Zero-Setup Docker Container

Run DataSetu without installing Python dependencies:

```bash
# Pull and run via Docker
docker build -t datasetu:latest .
docker run -p 8000:8000 datasetu:latest
```

Or using Docker Compose:
```bash
docker compose up
```

---

## 6. Worked Example: Messy CSV In -> Instant API Out

### Input: `raw_pmkisan_sample.csv` (CP-1252 Windows Encoded)
```csv
# Government of India Open Data Extract
# Source: Public Welfare Portal - Released: 2024-04-12
"State / UT","District","Subdistrict / Block","Disbursed Amount","Installment Date"
"Karnataka","Belgaum ","Chikkodi","२,०००/-","12/04/2024"
"Maharashtra","Poona","Haveli","₹ 4.5 Lakhs*","14/04/2024"
"All India","Bilaspur","Sadar","Rs. 12,00,000","15/04/2024"
```

### Run DataSetu:
```bash
datasetu inspect raw_pmkisan_sample.csv
```

### Output: Sanitized JSON REST API (`GET /v1/data`)
```json
{
  "meta": {
    "total": 3,
    "page": 1,
    "limit": 50,
    "latency_ms": 1.18,
    "version": "1.0.0"
  },
  "data": [
    {
      "state_ut": "Karnataka",
      "district": "Belgaum",
      "subdistrict_block": "Chikkodi",
      "disbursed_amount": 2000.0,
      "installment_date": "2024-04-12",
      "lgd_state_code": "KA",
      "lgd_district_code": 556,
      "lgd_district_name": "Belagavi",
      "lgd_match_method": "alias",
      "lgd_confidence_tier": "high",
      "lgd_needs_review": false,
      "lgd_review_reason": null
    },
    {
      "state_ut": "Maharashtra",
      "district": "Poona",
      "subdistrict_block": "Haveli",
      "disbursed_amount": 450000.0,
      "installment_date": "2024-04-14",
      "lgd_state_code": "MH",
      "lgd_district_code": 521,
      "lgd_district_name": "Pune",
      "lgd_match_method": "alias",
      "lgd_confidence_tier": "high",
      "lgd_needs_review": false,
      "lgd_review_reason": null
    },
    {
      "state_ut": "All India",
      "district": "Bilaspur",
      "subdistrict_block": "Sadar",
      "disbursed_amount": 1200000.0,
      "installment_date": "2024-04-15",
      "lgd_state_code": null,
      "lgd_district_code": null,
      "lgd_district_name": "Bilaspur",
      "lgd_match_method": "unmatched",
      "lgd_confidence_tier": "none",
      "lgd_needs_review": true,
      "lgd_review_reason": "Ambiguous: District 'Bilaspur' exists in multiple states (e.g. CG, HP). State hint required."
    }
  ]
}
```

Notice how:
1. Preamble lines (`# ...`) were stripped cleanly.
2. Devanagari `"२,०००/-"` became float `2000.0`.
3. `"₹ 4.5 Lakhs*"` became float `450000.0`.
4. Historical names *Belgaum* and *Poona* were resolved to canonical gazetteer codes *Belagavi (556)* and *Pune (521)*.
5. Ambiguous *Bilaspur* without a valid state was safely flagged for human review instead of silently corrupted.

---

## 7. CLI Command Reference

```text
Usage: datasetu [OPTIONS] COMMAND [ARGS]...

Commands:
  serve    Launch zero-config REST API with OpenAPI 3.1 docs and CDC.
  inspect  Run Sniffer and Bharat Normalizer; print terminal comparison diff.
  bench    Benchmark live in-memory DuckDB query throughput (p50/p95/p99).
  sdk      Synthesize a standalone, typed Python client SDK.
```

### Common Commands:
```bash
# Serve with live Change Data Capture (auto-reload on file edits)
datasetu serve demo/bharat_governance_master_2026.csv --cdc

# Inspect normalization diff and LGD match rates
datasetu inspect demo/bharat_governance_master_2026.csv

# Run latency benchmark across 500 random queries
datasetu bench demo/bharat_governance_master_2026.csv --n 500

# Generate standalone typed Python SDK
datasetu sdk demo/bharat_governance_master_2026.csv --out-dir ./sdk_out
```

---

## 8. API Specification

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/v1/data` | `GET` | Paginated query engine (`page`, `limit`, `sort`, `fields`, `q`, `<col>__gte`, `<col>__lte`, state/district filters). |
| `/v1/data/summary` | `GET` | Summary statistics (count, nulls, min, max, mean, sum, distinct counts) with optional `group_by`. |
| `/v1/schema` | `GET` | Inferred schema with DuckDB physical types and dynamic Pydantic v2 JSON Schema. |
| `/v1/report` | `GET` | Machine-readable Normalization Report (encoding, header rows, preamble count, LGD match rates). |
| `/v1/crosswalk/inspect/{name}` | `GET` | Inspect LGD gazetteer matches and aliases for a district name. |
| `/v1/hygiene` | `GET` | Return pipeline repair scorecard and sanitization audit metrics. |
| `/v1/changelog` | `GET` | Semantic version history with atomic hot-swap logs. |
| `/v1/upload` | `POST` | Upload and ingest a new CSV/XLSX file on the fly. |
| `/health` | `GET` | Production health check and engine readiness diagnostic. |
| `/docs` | `GET` | Interactive Swagger UI (OpenAPI 3.1). |

---

## 9. Known Limitations & Non-Goals

To maintain high engineering credibility and integrity, we explicitly document DataSetu’s boundaries:

1. **Non-Tabular Documents Rejected**: DataSetu does not parse freeform text, raw narrative PDFs, or scanned raster images. Files must contain tabular structures (CSV, TSV, XLSX).
2. **Ambiguous Districts Require Hints**: District names that exist in multiple States cannot and should not be resolved without a corresponding State column or `--state-hint` parameter.
3. **Complex Multi-Workbook Excel Formulas**: Excel files with cross-workbook external references or VBA macros are parsed using cell values only; macros are ignored.
4. **Sub-District Entities (Tehsils & Blocks)**: The current seed gazetteer covers all 738+ statutory districts of India. Sub-district (block/panchayat) resolution is scheduled for the v2.0 milestone.
5. **No Statutory Authority**: DataSetu is an open-source civic tech project. It does not issue official government notifications or statutory codes.

---

## 10. Reporting Broken Files & Contributing

Did an open government dataset break DataSetu's sniffer or normalizer? **We want to fix it!**

1. Check our [Broken File Report Template](.github/ISSUE_TEMPLATE/broken_file_report.md).
2. Open an issue on GitHub attaching the first 10 rows of the failing file.
3. See [`CONTRIBUTING.md`](CONTRIBUTING.md) for local developer guidelines, testing protocols, and pull request standards.

---

## 11. Licenses & Attribution

- **Code License**: [Apache License 2.0](LICENSE).
- **Third-Party Software**: Full notice in [`THIRD_PARTY.md`](THIRD_PARTY.md).
- **Data Source Terms**: See [`docs/DATA_SOURCES.md`](docs/DATA_SOURCES.md) for details on LGD (MoPR) and open data published under the Government Open Data License (GODL-India).
