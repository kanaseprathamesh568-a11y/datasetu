# DataSetu Data Sources & Attribution Policy

DataSetu (डेटासेतु) operates strictly as an autonomous ingestion, harmonization, and translation bridge. It transforms public open government tabular data into queryable, standardized OpenAPI 3.1 REST endpoints and columnar DuckDB stores.

This document details the regulatory framework, source attribution, and terms of use for all gazetteer and public datasets bundled or queried by DataSetu.

---

## 1. Regulatory & Open Data Licensing Frameworks

### 1.1 Government Open Data License - India (GODL)
Public datasets ingested through DataSetu are published under the **Government Open Data License (GODL) - India**, notified via the Gazette of India ([Gazette Notification No. 12(28)/2012-IPHW](https://data.gov.in/sites/default/files/Gazette_Notification_OGDL.pdf)).

Under GODL:
- **Permission**: Users are granted a worldwide, royalty-free, non-exclusive license to use, adapt, publish, translate, and exploit the data in any medium or format for lawful commercial and non-commercial purposes.
- **Attribution**: The user must explicitly attribute the data source by citing the provider, source portal ([data.gov.in](https://data.gov.in)), and release year.
- **Integrity**: Any adaptation or derivation must not state or imply endorsement by the Government of India or the publishing Ministry.

### 1.2 National Data Sharing and Accessibility Policy (NDSAP)
DataSetu complies with the principles of the **National Data Sharing and Accessibility Policy (NDSAP-2012)**:
- Promoting standard, machine-readable, open formats (CSV, JSON, Apache Parquet).
- Removing proprietary barriers to civic data utilization.
- Providing unambiguous metadata and schema descriptions.

---

## 2. Local Government Directory (LGD) Crosswalk

### 2.1 LGD Source & Authority
The canonical district directory (`datasetu/resources/lgd_districts.json`) is derived from the **Local Government Directory (LGD)** maintained by the **Ministry of Panchayati Raj (MoPR)** ([lgd.gov.in](https://lgd.gov.in)):
- **Total active administrative districts recorded**: 738+ across 28 States and 8 Union Territories.
- **Key attributes**:
  - `state_code`: Two-letter ISO 3166-2:IN state code (e.g., `KA`, `UP`, `MH`, `DL`).
  - `lgd_code`: Unique statutory integer identifier assigned by MoPR (e.g., `556` for Belagavi, `521` for Pune).
  - `canonical_name`: Standardized English spelling as gazetted.
  - `aliases`: Recognized historical, colonial, and phonetic variants (e.g., *Poona* -> *Pune*, *Belgaum* -> *Belagavi*, *Gurgaon* -> *Gurugram*, *Calcutta* -> *Kolkata*).

### 2.2 Matching Safety & "Never Guess" Ambiguity Guard
In Indian administrative geography, more than 15 district names recur identically across different States:
- *Bilaspur*: Present in Himachal Pradesh (`HP`, LGD `23`) and Chhattisgarh (`CG`, LGD `375`).
- *Hamirpur*: Present in Himachal Pradesh (`HP`, LGD `24`) and Uttar Pradesh (`UP`, LGD `154`).
- *Pratapgarh*: Present in Uttar Pradesh (`UP`, LGD `173`) and Rajasthan (`RJ`, LGD `119`).
- *Balrampur*: Present in Uttar Pradesh (`UP`, LGD `164`) and Chhattisgarh (`CG`, LGD `644`).
- *Aurangabad*: Present in Bihar (`BR`, LGD `228`) and Maharashtra (`MH`, LGD `476`, now Chhatrapati Sambhaji Nagar).

**Safety Protocol**:
1. When input records lack an explicit `state_hint`, DataSetu **strictly refuses to guess**.
2. It assigns:
   - `method = "unmatched"`
   - `confidence_tier = "none"`
   - `needs_review = True`
   - `review_reason = "Ambiguous: District 'X' exists in multiple states (e.g., State A, State B). State hint required."`
3. Only when a matching state hint is verified is the record mapped with `confidence_tier = "high"`.

---

## 3. Benchmark & Demonstration Datasets

The repository includes curated representative sample datasets from public portals:
1. `demo/bharat_governance_master_2026.csv`: 2,500 harmonized governance records across 15 flagship welfare schemes (PM-Kisan, MGNREGA, PMAY-G, NHM, JJM, PMGSY, SBM, PM-SVANidhi, PMUY, Poshan Abhiyaan, Ayushman Bharat, BBBP, Samagra Shiksha, PM-KUSUM, PMMSY).
2. `benchmark/datasets/`: 26 multi-ministry evaluation datasets generated from published historical patterns (CP-1252 encodings, non-standard preambles, Devanagari numerals, Lakhs/Crores monetary notation).

All benchmark datasets are intended exclusively for testing sanitization reliability and schema inference accuracy.

---

## 4. Legal Disclaimer
DataSetu is an **independent open-source civic tech project**. It is not owned, operated, or endorsed by the National Informatics Centre (NIC), the Ministry of Electronics & IT (MeitY), the Ministry of Panchayati Raj (MoPR), or data.gov.in. All government logos, trademarks, and statutory directory names belong to their respective authorities.
