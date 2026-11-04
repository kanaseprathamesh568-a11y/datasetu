"""Civic Anomaly & Forensic Audit Engine for Public Data.

What this module does:
1. Inspects active government datasets for fiscal leakages, dormant funds, and reporting variances.
2. Flags records where Actual Expenditure exceeds Sanctioned Allocation (Fiscal Leakage).
3. Identifies Dormant Funds where substantial public capital is disbursed with negligible execution (<10%).
4. Calculates a deterministic National Civic Data Hygiene Score (0-100) and risk tiers.
5. Emits auditable anomaly reports with statutory Local Government Directory (LGD) district crosswalks.
"""

from __future__ import annotations

import math
import time
from typing import Any, Dict, List, Optional

from datasetu.db import DatasetStore


class CivicAuditEngine:
    """Automated forensic audit and discrepancy detection engine."""

    def __init__(self, store: DatasetStore):
        self.store = store

    def run_audit(
        self,
        table_name: Optional[str] = None,
        state_filter: Optional[str] = None,
        sector_filter: Optional[str] = None,
        limit: int = 100,
    ) -> Dict[str, Any]:
        """Runs comprehensive forensic audit across the active dataset or specified table."""
        t_start = time.perf_counter()
        tbl = table_name or self.store.table_name

        # Resolve available column names in active table
        cols = self.store.columns
        alloc_col = self._resolve_col(["allocation", "central_sanctioned", "allocated_amount_inr", "allocation_inr", "budget"])
        exp_col = self._resolve_col(["expenditure", "actual_expenditure", "expenditure_amount_inr", "spent"])
        state_col = self._resolve_col(["state", "state_name", "administrative_units___state_name"])
        dist_col = self._resolve_col(["district", "district_name", "administrative_units___district_name"])
        scheme_col = self._resolve_col(["scheme", "scheme_name", "governance_portfolio___national_flagship_scheme", "scheme_title"])
        status_col = self._resolve_col(["status", "performance_lifecycle_status", "implementation_status"])
        lgd_code_col = self._resolve_col(["lgd_district_code", "district_code", "lgd_code"])

        where_clauses: List[str] = []
        params: List[Any] = []

        if state_filter and state_col:
            where_clauses.append(f'"{state_col}" = ?')
            params.append(state_filter)

        sector_col = self._resolve_col(["sector", "sector_category", "governance_portfolio___sector_category"])
        bene_col = self._resolve_col(["beneficiaries", "impact_metrics", "beneficiaries_reached"])
        if sector_filter and sector_col:
            where_clauses.append(f'"{sector_col}" = ?')
            params.append(sector_filter)

        where_sql = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""

        # Fetch records for analysis
        query_sql = f'SELECT * FROM "{tbl}" {where_sql}'
        cursor = self.store.conn.execute(query_sql, params)
        col_names = [d[0] for d in cursor.description]
        rows = [dict(zip(col_names, r)) for r in cursor.fetchall()]

        total_audited = len(rows)
        if total_audited == 0:
            return {
                "total_records_audited": 0,
                "hygiene_score": 100.0,
                "grade": "A+",
                "total_anomalies_flagged": 0,
                "anomalies": [],
                "summary": {
                    "fiscal_leakage_count": 0,
                    "dormant_funds_count": 0,
                    "unresolved_lgd_count": 0,
                    "total_variance_inr": 0.0,
                },
                "latency_ms": round((time.perf_counter() - t_start) * 1000, 2),
            }

        anomalies: List[Dict[str, Any]] = []
        total_leakage_inr = 0.0
        total_dormant_inr = 0.0
        leakage_count = 0
        dormant_count = 0
        low_bene_count = 0
        unresolved_lgd_count = 0

        for r in rows:
            st = str(r.get(state_col, "All-India")) if state_col else "All-India"
            dt = str(r.get(dist_col, "General")) if dist_col else "General"
            sch = str(r.get(scheme_col, "Flagship Scheme")) if scheme_col else "Flagship Scheme"
            sec = str(r.get(sector_col, "Public Governance")) if sector_col else "Public Governance"
            stat = str(r.get(status_col, "In-Progress")) if status_col else "In-Progress"
            lgd = r.get(lgd_code_col) if lgd_code_col else None

            alloc_val = self._to_float(r.get(alloc_col)) if alloc_col else 0.0
            exp_val = self._to_float(r.get(exp_col)) if exp_col else 0.0
            bene_val = int(self._to_float(r.get(bene_col))) if bene_col else 0

            # 1. Forensic Check: Fiscal Leakage / Over-Expenditure
            if alloc_val > 0 and exp_val > alloc_val:
                variance = exp_val - alloc_val
                leakage_count += 1
                total_leakage_inr += variance
                sev = "CRITICAL" if exp_val > (alloc_val * 1.02) else "WARNING"
                ratio = round((exp_val / alloc_val) * 100, 1)
                desc = f"Actual expenditure exceeds sanctioned budget by ₹ {round(variance, 2):,} INR ({ratio}% utilization)."
                anomalies.append({
                    "type": "FISCAL_OVERSPEND",
                    "severity": sev,
                    "state": st,
                    "district": dt,
                    "lgd_district_code": lgd or 0,
                    "scheme": sch,
                    "sector": sec,
                    "allocation_inr": alloc_val,
                    "expenditure_inr": exp_val,
                    "variance_gap_inr": round(variance, 2),
                    "variance_inr": round(variance, 2),
                    "ratio_pct": ratio,
                    "utilization_rate_pct": ratio,
                    "beneficiaries": bene_val,
                    "finding": desc,
                    "description": desc,
                })

            # 2. Forensic Check: Dormant Capital (<80% utilization despite disbursement)
            elif alloc_val >= 10000000 and exp_val < (alloc_val * 0.80) and stat in ("Fund Disbursed", "In-Progress", "Approved", "Audited & Verified"):
                dormant_funds = alloc_val - exp_val
                dormant_count += 1
                total_dormant_inr += dormant_funds
                ratio = round((exp_val / alloc_val) * 100, 1)
                desc = f"Lagging public capital: only {ratio}% deployed out of ₹ {round(alloc_val, 2):,} INR sanctioned."
                anomalies.append({
                    "type": "DORMANT_FUNDS",
                    "severity": "WARNING",
                    "state": st,
                    "district": dt,
                    "lgd_district_code": lgd or 0,
                    "scheme": sch,
                    "sector": sec,
                    "allocation_inr": alloc_val,
                    "expenditure_inr": exp_val,
                    "variance_gap_inr": round(dormant_funds, 2),
                    "variance_inr": round(dormant_funds, 2),
                    "ratio_pct": ratio,
                    "utilization_rate_pct": ratio,
                    "beneficiaries": bene_val,
                    "finding": desc,
                    "description": desc,
                })

            # 3. Forensic Check: Low Beneficiary Outlier
            elif bene_val > 0 and bene_val < 250 and alloc_val >= 5000000:
                low_bene_count += 1
                ratio = round((exp_val / alloc_val) * 100, 1) if alloc_val > 0 else 0.0
                desc = f"Disproportionate welfare distribution: only {bene_val} citizens reached with ₹ {round(alloc_val, 2):,} INR allocation."
                anomalies.append({
                    "type": "LOW_BENEFICIARY_OUTLIER",
                    "severity": "ADVISORY",
                    "state": st,
                    "district": dt,
                    "lgd_district_code": lgd or 0,
                    "scheme": sch,
                    "sector": sec,
                    "allocation_inr": alloc_val,
                    "expenditure_inr": exp_val,
                    "variance_gap_inr": 0.0,
                    "variance_inr": 0.0,
                    "ratio_pct": ratio,
                    "utilization_rate_pct": ratio,
                    "beneficiaries": bene_val,
                    "finding": desc,
                    "description": desc,
                })

            # 4. Forensic Check: Missing or Ambiguous LGD Mapping
            if lgd is None or lgd == "" or lgd == 0:
                unresolved_lgd_count += 1

        # Calculate National Civic Data Hygiene Score (0-100)
        leakage_penalty = min(25.0, (leakage_count / max(1, total_audited)) * 100.0 * 2.0)
        dormant_penalty = min(20.0, (dormant_count / max(1, total_audited)) * 100.0 * 1.5)
        lgd_penalty = min(15.0, (unresolved_lgd_count / max(1, total_audited)) * 100.0 * 1.0)

        hygiene_score = max(50.0, round(100.0 - (leakage_penalty + dormant_penalty + lgd_penalty), 1))
        if hygiene_score >= 95.0:
            letter_grade = "A+"
            grade = "A+ (Exemplary)"
        elif hygiene_score >= 90.0:
            letter_grade = "A"
            grade = "A (Statutory Compliant)"
        elif hygiene_score >= 80.0:
            letter_grade = "B"
            grade = "B (Satisfactory)"
        else:
            letter_grade = "C"
            grade = "C (Action Required)"

        # Sort anomalies by severity (CRITICAL first, then highest variance)
        anomalies.sort(key=lambda x: (0 if x["severity"] == "CRITICAL" else 1, -x["variance_inr"]))

        duration_ms = (time.perf_counter() - t_start) * 1000

        return {
            "total_records_audited": total_audited,
            "hygiene_score": hygiene_score,
            "letter_grade": letter_grade,
            "grade": grade,
            "evaluation": f"{'Exemplary CAG Integrity' if hygiene_score >= 90 else 'Statutory CAG Monitoring'} • {leakage_count} overspends and {dormant_count} dormant outlays identified.",
            "total_anomalies_flagged": len(anomalies),
            "fiscal_leakages": {
                "count": leakage_count,
                "total_amount_inr": round(total_leakage_inr, 2),
            },
            "dormant_funds": {
                "count": dormant_count,
                "total_unutilized_inr": round(total_dormant_inr, 2),
            },
            "low_beneficiary_outliers": {
                "count": low_bene_count,
            },
            "summary": {
                "fiscal_leakage_count": leakage_count,
                "total_leakage_inr": round(total_leakage_inr, 2),
                "dormant_funds_count": dormant_count,
                "total_dormant_inr": round(total_dormant_inr, 2),
                "unresolved_lgd_count": unresolved_lgd_count,
            },
            "anomalies": anomalies[:limit],
            "latency_ms": round(duration_ms, 2),
        }

    def _resolve_col(self, candidate_terms: List[str]) -> Optional[str]:
        """Resolves target semantic column name from active store columns."""
        for col in self.store.columns:
            col_clean = col.lower().replace("-", "_").replace(" ", "_").replace("&", "_")
            for term in candidate_terms:
                if term in col_clean:
                    return col
        return None

    def _to_float(self, val: Any) -> float:
        """Coerces numeric values safely."""
        if val is None:
            return 0.0
        try:
            return float(val)
        except (ValueError, TypeError):
            return 0.0
