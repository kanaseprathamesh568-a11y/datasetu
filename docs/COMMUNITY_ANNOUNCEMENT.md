# DataSetu (डेटासेतु) Community Launch Announcements

Ready-to-post announcements for open data, civic tech, and developer communities.

---

## 1. Post for DataMeet Google Group & Civic Tech India

**Subject**: [Project] DataSetu — Turning messy Indian open datasets into clean OpenAPI 3.1 REST APIs & DuckDB columnar tables

**Body**:
```text
Namaste DataMeet Community,

Anyone who has worked with datasets on data.gov.in or state portals knows the drill: CP-1252 encodings, 3 rows of preamble banners before the table starts, merged headers, "₹ 14.5 Lakhs", Devanagari numerals, and district names spelled 5 different ways ("Poona" vs "Pune", "Belgaum" vs "Belagavi").

We just open-sourced DataSetu (डेटासेतु) under the Apache 2.0 license to help automate this entire hygiene and publishing pipeline with a single command:

👉 GitHub: https://github.com/kanaseprathamesh568-a11y/datasetu
👉 Live Sandbox & Docs: https://datasetu-five.vercel.app/

What it does:
1. Smart Sniffer: Automatically detects encoding (CP-1252, Latin-1, UTF-8), strips banner rows, and collapses merged multi-row headers.
2. Bharat Normalizer: Parses Lakhs/Crores, Indic currency notations, and Devanagari numerals into clean floats.
3. Safe District Crosswalk: Maps district strings against the official Local Government Directory (LGD) gazetteer (738+ districts).
   - "Never Guess" policy: District names that exist in multiple states (e.g. Bilaspur in HP vs CG, Hamirpur in HP vs UP) without a state hint are strictly flagged as `needs_review: true` with a clear explanation, rather than falsely guessing.
4. Instant REST API & Vectorized DuckDB: Spawns OpenAPI 3.1 endpoints on the fly with sub-4ms query times and an in-memory analytical columnar engine.
5. Live CDC & Python SDK synthesis: Watches for file updates and generates typed Python SDKs.

We ran an empirical benchmark on 26 real datasets across 15+ central ministries (MoRD, MoHFW, Jal Shakti, MoA, etc.):
- 96.2% ingestion reliability (25/26 parsed cleanly; 1 corrupt empty file safely caught)
- 83.5% LGD match rate
- 21 records safely flagged for human review
- Average pipeline latency: 6.12 ms

We'd love your feedback! If you have messy government CSVs or Excel spreadsheets that break our sniffer, please open an issue with the sample rows so we can make the parser bulletproof:
https://github.com/kanaseprathamesh568-a11y/datasetu/issues/new/choose

Looking forward to your thoughts and contributions!
```

---

## 2. Post for Reddit (`r/developersIndia` & `r/opendata`)

**Title**: [Show & Tell] I built DataSetu: An open-source tool that turns messy Indian government spreadsheets into clean REST APIs & DuckDB queries with 1 command

**Post**:
```text
Hey r/developersIndia,

If you've ever tried building a project using data from data.gov.in, you've probably faced these headaches:
- Files encoded in Windows CP-1252 that crash Python's `open()`
- 3-5 rows of disclaimer text before the actual header
- Numbers written as "₹ 12.5 Lakhs", "14,500*", or with Devanagari digits (२,०००/-)
- Districts spelled inconsistently ("Poona", "Bangalore (U)", "Belgaum")
- Over 230,000 datasets published, but less than 2% have working APIs

We built and open-sourced **DataSetu (डेटासेतु)** (Apache 2.0):
🔗 Repo: https://github.com/kanaseprathamesh568-a11y/datasetu
🌐 Live Sandbox: https://datasetu-five.vercel.app/

### How to use it:
```bash
pip install datasetu
datasetu serve messy_ministry_data.csv
```
This gives you:
1. Instant Swagger docs (`/docs`) with OpenAPI 3.1
2. Sub-4ms query engine powered by embedded DuckDB (`/v1/data?state=KA&limit=10`)
3. Automatic LGD district code mapping (Local Government Directory)
4. A strict "Never Guess" policy: If a district name exists in multiple states (like *Bilaspur* in HP & CG) and the state is missing, it refuses to guess and flags it as `needs_review: true`.
5. Automatic Change Data Capture (CDC): Edit the CSV and the API updates atomically without rebooting.

We tested it on 26 multi-ministry files and documented all successes and edge-case failures in `benchmark/BENCHMARK_REPORT.md`.

Docker container:
```bash
docker run -p 8000:8000 datasetu:latest
```

It's completely free and open source. Please try it on any ugly public spreadsheets you have, and let us know what breaks!
```

---

## 3. Short Post for LinkedIn / X (Twitter)

```text
Excited to share DataSetu (डेटासेतु) — an open-source civic tech initiative to turn India's messy public tabular data into clean, validated OpenAPI 3.1 REST endpoints and sub-millisecond DuckDB columnar stores with ONE command! 🌉🇮🇳

Key Highlights:
✨ Auto-sniffs CP-1252, preambles & merged headers
✨ Normalizes Lakhs, Crores & Devanagari numerals into clean ISO floats
✨ Maps 738+ districts to official Local Government Directory (LGD) codes with a strict "Never Guess" ambiguity guard
✨ Sub-4ms in-memory queries via DuckDB
✨ Live Change Data Capture (CDC) + typed Python SDK generator
✨ Tested across 26 central ministry datasets (96.2% reliability, 83.5% LGD match)

🔗 GitHub (Apache 2.0): https://github.com/kanaseprathamesh568-a11y/datasetu
🌐 Try the live sandbox: https://datasetu-five.vercel.app/

Let's make India's open data truly open, queryable, and developer-ready! #OpenData #DigitalPublicInfrastructure #Python #DuckDB #DataGov #CivicTech #OpenSource
```
