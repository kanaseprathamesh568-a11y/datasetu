---
name: 🐛 Broken File Report
about: Report an open government dataset (CSV, XLSX, TSV) that failed to sniff or parse
title: "[BROKEN FILE]: <Ministry / Portal / Scheme Name>"
labels: ["broken-file", "bug", "needs-triage"]
assignees: []
---

## 1. Dataset Origin & Source
- **Publishing Portal**: [e.g. data.gov.in / State Portal / Departmental Dashboard]
- **Direct Source URL**: [Link to dataset download page if publicly accessible]
- **Ministry / Department**: [e.g. Ministry of Agriculture & Farmers Welfare]
- **Year / Period**: [e.g. 2023-2024]
- **File Format**: [e.g. CSV, XLSX, TSV]

## 2. What Happened?
- [ ] Sniffer failed to detect encoding or delimiter
- [ ] Preamble / metadata rows were not stripped cleanly
- [ ] Merged headers collapsed incorrectly
- [ ] Lakhs / Crores / Indic numerals failed to convert to float
- [ ] District / state names failed to resolve or mismatched
- [ ] Server crashed with unhandled traceback

## 3. Command Executed
```bash
datasetu inspect <filename>
# or
datasetu serve <filename>
```

## 4. Error Message / Traceback
```text
[Paste error output or terminal stack trace here]
```

## 5. Sample Data (First 10 Rows)
> **Privacy Notice**: Please ensure no non-public PII (Aadhaar numbers, personal phone numbers, bank accounts) is included.

```csv
[Paste the raw first 10 rows of the failing file here]
```

## 6. Expected Behavior
Describe how you expected DataSetu to normalize or interpret this file.
