#!/usr/bin/env python3
"""Apply comprehensive fixes across index.html files."""

import sys

for path in ["datasetu/static/index.html", "api/datasetu/static/index.html"]:
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Update export buttons in explorer
    html = html.replace('href="/v1/data?format=csv&limit=10170"', 'href="/v1/data?format=csv&limit=11742"')
    html = html.replace('href="/v1/data?format=parquet&limit=10170"', 'href="/v1/data?format=parquet&limit=11742"')
    html = html.replace('href="/v1/geojson?limit=10170"', 'href="/v1/geojson?limit=11742"')
    html = html.replace('href="/v1/data?limit=10170"', 'href="/v1/data?limit=50"')

    # 2. Update default pagination info
    html = html.replace('Showing Page 1 of 407 (10,170 Total Records in In-Memory DuckDB)', 'Showing Page 1 of 470 (11,742 Total Records in In-Memory DuckDB)')
    html = html.replace('10,170 master governance records', '11,742 master governance records')
    html = html.replace('let totalExplorerRecords = 10170;', 'let totalExplorerRecords = 11742;')

    # 3. Update updateExportLinks
    old_update = """  if (isMaster) {
    if (csvBtn) csvBtn.href = '/v1/data?format=csv&limit=10170';
    if (parquetBtn) parquetBtn.href = '/v1/data?format=parquet&limit=10170';
    if (geojsonBtn) {
      geojsonBtn.href = '/v1/geojson?limit=10170';
      geojsonBtn.classList.remove('opacity-50', 'pointer-events-none');
    }
    if (jsonBtn) jsonBtn.href = '/v1/data?limit=10170';
  } else {"""

    new_update = """  if (isMaster) {
    if (csvBtn) csvBtn.href = '/v1/data?format=csv&limit=11742';
    if (parquetBtn) parquetBtn.href = '/v1/data?format=parquet&limit=11742';
    if (geojsonBtn) {
      geojsonBtn.href = '/v1/geojson?limit=11742';
      geojsonBtn.classList.remove('opacity-50', 'pointer-events-none');
    }
    if (jsonBtn) jsonBtn.href = '/v1/data?limit=50';
  } else {"""

    assert old_update in html, f"Could not find old_update in {path}"
    html = html.replace(old_update, new_update)

    # 4. Update loadExplorerData onlyLgdVerified param
    html = html.replace("if (onlyLgdVerified) url += `&lgd_district__gte=1`;", "if (onlyLgdVerified) url += `&lgd_district_code__gte=1`;")

    # 5. Update openTestApiForRecord to use window.location.origin
    old_modal_api = "document.getElementById('modalApiEndpointInput').value = `http://localhost:8000/v1/data?district=${encodeURIComponent(dist)}`;"
    new_modal_api = "document.getElementById('modalApiEndpointInput').value = `${window.location.origin}/v1/data?district=${encodeURIComponent(dist)}`;"
    if old_modal_api in html:
        html = html.replace(old_modal_api, new_modal_api)

    # 6. Update executePlaygroundQuery to make real live queries
    old_pg = """function executePlaygroundQuery() {
  const out = document.getElementById('apiResponseOutput');
  const badge = document.getElementById('responseStatusBadge');
  badge.innerHTML = '<span class="text-amber-600">Executing...</span>';
  setTimeout(() => {
    badge.className = 'bg-emerald-100 text-emerald-800 text-[10px] font-bold px-2 py-0.5 rounded';
    badge.innerText = '200 OK • 1.18 ms';
    out.innerText = JSON.stringify({
      meta: { gateway: "NIC-Bharat-API-Gateway/2.4", timestamp: new Date().toISOString(), records_count: 5, latency_ms: 1.18, lgd_directory_version: "2026.1" },
      data: [
        { lgd_district_code: 556, district_name_en: "Belagavi", state_code: "KA", status: "DISINFECTED" },
        { lgd_district_code: 557, district_name_en: "Ballari", state_code: "KA", status: "DISINFECTED" }
      ]
    }, null, 2);
  }, 250);
}"""

    new_pg = """async function executePlaygroundQuery() {
  const inputEl = document.getElementById('apiEndpointPath');
  const out = document.getElementById('apiResponseOutput');
  const badge = document.getElementById('responseStatusBadge');
  if (!inputEl || !out) return;

  const path = inputEl.value.trim();
  if (badge) badge.innerHTML = '<span class="text-amber-600">Executing live request...</span>';

  try {
    const t0 = performance.now();
    const cleanPath = path.startsWith('/') ? path : `/v1/${path}`;
    const resp = await fetch(cleanPath);
    const latency = (performance.now() - t0).toFixed(2);
    const text = await resp.text();
    let formatted = text;
    try {
      formatted = JSON.stringify(JSON.parse(text), null, 2);
    } catch(e) {}
    if (badge) {
      badge.className = resp.ok ? 'bg-emerald-100 text-emerald-800 text-[10px] font-bold px-2 py-0.5 rounded' : 'bg-rose-100 text-rose-800 text-[10px] font-bold px-2 py-0.5 rounded';
      badge.innerText = `${resp.status} ${resp.statusText || 'OK'} • ${latency} ms`;
    }
    out.innerText = formatted;
  } catch (err) {
    if (badge) {
      badge.className = 'bg-rose-100 text-rose-800 text-[10px] font-bold px-2 py-0.5 rounded';
      badge.innerText = 'Network Error';
    }
    out.innerText = `// Live Query Error: ${err.message}`;
  }
}"""

    assert old_pg in html, f"Could not find old_pg in {path}"
    html = html.replace(old_pg, new_pg)

    # 7. Update drawCorrelatorScatter to handle x, x_value, y, y_value
    old_scatter_pts = """  const xs = points.map(p => p.x);
  const ys = points.map(p => p.y);"""

    new_scatter_pts = """  const xs = points.map(p => (p.x !== undefined ? p.x : p.x_value));
  const ys = points.map(p => (p.y !== undefined ? p.y : p.y_value));"""

    if old_scatter_pts in html:
        html = html.replace(old_scatter_pts, new_scatter_pts)

    # 8. Webhook subscription URL fallback
    html = html.replace("max-w-xs\">${escapeHtml(s.target_url)}</div>", "max-w-xs\">${escapeHtml(s.target_url || s.url)}</div>")

    # 9. Load audit anomalies counters safe check
    old_audit_counters = """    // Counters
    const lc = document.getElementById('auditLeakageCount');
    const lt = document.getElementById('auditLeakageTotal');
    const dc = document.getElementById('auditDormantCount');
    const dt = document.getElementById('auditDormantTotal');
    const bc = document.getElementById('auditLowBeneCount');

    if (lc) lc.innerText = `${data.fiscal_leakages.count} Anomalies`;
    if (lt) lt.innerText = `Total: ₹ ${(data.fiscal_leakages.total_amount_inr / 10000000).toFixed(2)} Cr`;
    if (dc) dc.innerText = `${data.dormant_funds.count} Dormant`;
    if (dt) dt.innerText = `Idle: ₹ ${(data.dormant_funds.total_unutilized_inr / 10000000).toFixed(2)} Cr`;
    if (bc) bc.innerText = `${data.low_beneficiary_outliers.count} Outliers`;"""

    new_audit_counters = """    // Counters
    const lc = document.getElementById('auditLeakageCount');
    const lt = document.getElementById('auditLeakageTotal');
    const dc = document.getElementById('auditDormantCount');
    const dt = document.getElementById('auditDormantTotal');
    const bc = document.getElementById('auditLowBeneCount');

    const leakCount = (data.fiscal_leakages && data.fiscal_leakages.count !== undefined)
      ? data.fiscal_leakages.count
      : (data.summary ? data.summary.fiscal_leakage_count : 0);
    const leakTotal = (data.fiscal_leakages && data.fiscal_leakages.total_amount_inr !== undefined)
      ? data.fiscal_leakages.total_amount_inr
      : (data.summary ? data.summary.total_leakage_inr : 0);

    const dormCount = (data.dormant_funds && data.dormant_funds.count !== undefined)
      ? data.dormant_funds.count
      : (data.summary ? data.summary.dormant_funds_count : 0);
    const dormTotal = (data.dormant_funds && data.dormant_funds.total_unutilized_inr !== undefined)
      ? data.dormant_funds.total_unutilized_inr
      : (data.summary ? data.summary.total_dormant_inr : 0);

    const lowBeneCount = (data.low_beneficiary_outliers && data.low_beneficiary_outliers.count !== undefined)
      ? data.low_beneficiary_outliers.count
      : 0;

    if (lc) lc.innerText = `${leakCount} Anomalies`;
    if (lt) lt.innerText = `Total: ₹ ${(leakTotal / 10000000).toFixed(2)} Cr`;
    if (dc) dc.innerText = `${dormCount} Dormant`;
    if (dt) dt.innerText = `Idle: ₹ ${(dormTotal / 10000000).toFixed(2)} Cr`;
    if (bc) bc.innerText = `${lowBeneCount} Outliers`;"""

    if old_audit_counters in html:
        html = html.replace(old_audit_counters, new_audit_counters)

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Successfully patched", path)
