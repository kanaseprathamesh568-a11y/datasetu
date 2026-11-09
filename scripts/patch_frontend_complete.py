#!/usr/bin/env python3
"""Comprehensive patch for index.html in datasetu/static and api/datasetu/static."""

import re
from pathlib import Path

HTML_FILES = [
    Path("/Users/_needtochill_/.gemini/antigravity/scratch/datasetu/datasetu/static/index.html"),
    Path("/Users/_needtochill_/.gemini/antigravity/scratch/datasetu/api/datasetu/static/index.html"),
]

ALL_STATES_HTML = """        <select id="stateFilter" class="h-9 text-xs border border-slate-300 rounded-lg focus:ring-2 focus:ring-govNavy-800 text-slate-700 px-3 py-0 bg-white font-medium shadow-xs transition-all cursor-pointer" onchange="loadExplorerData(1)">
          <option value="ALL">All States / UTs (All India)</option>
          <option value="Andaman and Nicobar Islands">Andaman and Nicobar Islands</option>
          <option value="Andhra Pradesh">Andhra Pradesh</option>
          <option value="Arunachal Pradesh">Arunachal Pradesh</option>
          <option value="Assam">Assam</option>
          <option value="Bihar">Bihar</option>
          <option value="Chandigarh">Chandigarh</option>
          <option value="Chhattisgarh">Chhattisgarh</option>
          <option value="Dadra and Nagar Haveli and Daman and Diu">Dadra and Nagar Haveli and Daman and Diu</option>
          <option value="Delhi">Delhi (NCT)</option>
          <option value="Goa">Goa</option>
          <option value="Gujarat">Gujarat</option>
          <option value="Haryana">Haryana</option>
          <option value="Himachal Pradesh">Himachal Pradesh</option>
          <option value="Jammu and Kashmir">Jammu and Kashmir</option>
          <option value="Jharkhand">Jharkhand</option>
          <option value="Karnataka">Karnataka</option>
          <option value="Kerala">Kerala</option>
          <option value="Ladakh">Ladakh</option>
          <option value="Lakshadweep">Lakshadweep</option>
          <option value="Madhya Pradesh">Madhya Pradesh</option>
          <option value="Maharashtra">Maharashtra</option>
          <option value="Manipur">Manipur</option>
          <option value="Meghalaya">Meghalaya</option>
          <option value="Mizoram">Mizoram</option>
          <option value="Nagaland">Nagaland</option>
          <option value="Odisha">Odisha</option>
          <option value="Puducherry">Puducherry</option>
          <option value="Punjab">Punjab</option>
          <option value="Rajasthan">Rajasthan</option>
          <option value="Sikkim">Sikkim</option>
          <option value="Tamil Nadu">Tamil Nadu</option>
          <option value="Telangana">Telangana</option>
          <option value="Tripura">Tripura</option>
          <option value="Uttar Pradesh">Uttar Pradesh</option>
          <option value="Uttarakhand">Uttarakhand</option>
          <option value="West Bengal">West Bengal</option>
        </select>"""

for hf in HTML_FILES:
    content = hf.read_text(encoding="utf-8")

    # 1. Replace stateFilter select options with all 36 States/UTs
    pattern = r'<select id="stateFilter"[^>]*>[\s\S]*?</select>'
    content = re.sub(pattern, ALL_STATES_HTML, content)

    # 2. Add triggerDownload helper and download button handlers
    if "async function triggerDownload" not in content:
        download_helper = """
async function triggerDownload(url, filename) {
  try {
    showToast('Download Starting', `Preparing ${filename}...`, 'info');
    const resp = await fetch(url);
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    const blob = await resp.blob();
    const blobUrl = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = blobUrl;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(blobUrl);
    showToast('Download Complete', `${filename} downloaded successfully!`, 'success');
  } catch (err) {
    showToast('Download Failed', `Opening direct link: ${err.message}`, 'warning');
    window.open(url, '_blank');
  }
}
"""
        content = content.replace("function showToast(", download_helper + "\nfunction showToast(")

    # 3. Enhance Instant Export buttons to use triggerDownload with fallback
    content = content.replace(
        'download="bharat_governance_master_2026.csv">',
        'download="bharat_governance_master_2026.csv" onclick="event.preventDefault(); triggerDownload(this.href, this.download || \'bharat_governance_master_2026.csv\')">'
    )
    content = content.replace(
        'download="bharat_governance_master_2026.parquet">',
        'download="bharat_governance_master_2026.parquet" onclick="event.preventDefault(); triggerDownload(this.href, this.download || \'bharat_governance_master_2026.parquet\')">'
    )
    content = content.replace(
        'download="bharat_governance_centroids.geojson">',
        'download="bharat_governance_centroids.geojson" onclick="event.preventDefault(); triggerDownload(this.href, this.download || \'bharat_governance_centroids.geojson\')">'
    )

    # 4. Wire LGD Export CSV button
    content = content.replace(
        'onclick="showToast(\'Export Started\', \'Downloading verified LGD directory crosswalk CSV...\', \'info\')">Export CSV</button>',
        'onclick="triggerDownload(\'/v1/crosswalk/districts?format=csv\', \'mopr_lgd_master_directory_2026.csv\')">Export CSV</button>'
    )

    # 5. Fix quickFilterFromLgd with state code mapping
    old_qf = """function quickFilterFromLgd(st) {
  const stEl = document.getElementById('stateFilter');
  if (stEl) stEl.value = st;
  switchGovTab('explorer');
  loadExplorerData(1);
}"""
    new_qf = """const STATE_CODE_MAP = {
  'KA': 'Karnataka', 'UP': 'Uttar Pradesh', 'MH': 'Maharashtra', 'TN': 'Tamil Nadu',
  'PB': 'Punjab', 'DL': 'Delhi', 'GJ': 'Gujarat', 'RJ': 'Rajasthan', 'MP': 'Madhya Pradesh',
  'WB': 'West Bengal', 'BR': 'Bihar', 'AP': 'Andhra Pradesh', 'TS': 'Telangana', 'KL': 'Kerala',
  'OR': 'Odisha', 'OD': 'Odisha', 'AS': 'Assam', 'JH': 'Jharkhand', 'CT': 'Chhattisgarh',
  'CG': 'Chhattisgarh', 'HR': 'Haryana', 'JK': 'Jammu and Kashmir', 'UT': 'Uttarakhand',
  'UK': 'Uttarakhand', 'HP': 'Himachal Pradesh', 'GA': 'Goa', 'SK': 'Sikkim', 'TR': 'Tripura',
  'MN': 'Manipur', 'ML': 'Meghalaya', 'MZ': 'Mizoram', 'NL': 'Nagaland', 'AR': 'Arunachal Pradesh',
  'PY': 'Puducherry', 'CH': 'Chandigarh', 'LA': 'Ladakh', 'AN': 'Andaman and Nicobar Islands',
  'DN': 'Dadra and Nagar Haveli and Daman and Diu', 'LD': 'Lakshadweep'
};

function quickFilterFromLgd(st) {
  const fullState = STATE_CODE_MAP[String(st).trim().toUpperCase()] || st;
  const stEl = document.getElementById('stateFilter');
  if (stEl) stEl.value = fullState;
  switchGovTab('explorer');
  loadExplorerData(1);
}"""
    content = content.replace(old_qf, new_qf)

    # 6. Fix triggerHeroSearch and applyTrendingFilter
    old_ths = """function triggerHeroSearch() {
  const q = document.getElementById('searchInput').value.toLowerCase();
  closeSearchSuggestions();
  switchGovTab('explorer');
  const rows = document.querySelectorAll('#explorerTableBody tr');
  let count = 0;
  rows.forEach(r => {
    if (r.innerText.toLowerCase().includes(q)) {
      r.style.display = '';
      count++;
    } else {
      r.style.display = 'none';
    }
  });
  document.getElementById('recordCountText').innerText = count;
}

function applyTrendingFilter(query) {
  document.getElementById('searchInput').value = query;
  triggerHeroSearch();
}"""
    new_ths = """function triggerHeroSearch() {
  closeSearchSuggestions();
  switchGovTab('explorer');
  loadExplorerData(1);
}

function applyTrendingFilter(query) {
  const sInput = document.getElementById('searchInput');
  if (sInput) sInput.value = query;
  triggerHeroSearch();
}"""
    content = content.replace(old_ths, new_ths)

    # 7. Enhance toggleHeroCurlLiveConsole to make real API request
    old_curl_con = """function toggleHeroCurlLiveConsole() {
  const box = document.getElementById('heroCurlConsoleBox');
  const label = document.getElementById('heroCurlRunLabel');
  if (box.classList.contains('hidden')) {
    box.classList.remove('hidden');
    label.innerText = 'Hide Response';
  } else {
    box.classList.add('hidden');
    label.innerText = 'Run Live Query';
  }
}"""
    new_curl_con = """async function toggleHeroCurlLiveConsole() {
  const box = document.getElementById('heroCurlConsoleBox');
  const label = document.getElementById('heroCurlRunLabel');
  const pre = box ? box.querySelector('pre') : null;
  if (!box) return;
  if (box.classList.contains('hidden')) {
    box.classList.remove('hidden');
    if (label) label.innerText = 'Hide Response';
    if (pre) {
      pre.innerText = '// Executing GET /v1/data?state=Karnataka&limit=2 against DuckDB in-memory columnar engine...';
      const t0 = performance.now();
      try {
        const resp = await fetch('/v1/data?state=Karnataka&limit=2');
        const ms = (performance.now() - t0).toFixed(2);
        const json = await resp.json();
        pre.innerText = JSON.stringify(json, null, 2);
        const latSpan = document.getElementById('heroCurlLatencyBadge');
        if (latSpan) latSpan.innerText = `Vectorized DuckDB Engine • In-Memory Columnar Latency: ${ms} ms`;
      } catch (err) {
        pre.innerText = `// Error: ${err.message}`;
      }
    }
  } else {
    box.classList.add('hidden');
    if (label) label.innerText = 'Run Live Query';
  }
}"""
    content = content.replace(old_curl_con, new_curl_con)
    # Add id="heroCurlLatencyBadge" to the latency span in heroCurlConsoleBox
    content = content.replace(
        '<span class="text-slate-400 text-[11px]">Vectorized DuckDB Engine • In-Memory Columnar Latency: 1.18 ms</span>',
        '<span id="heroCurlLatencyBadge" class="text-slate-400 text-[11px]">Vectorized DuckDB Engine • In-Memory Columnar Latency: 1.18 ms</span>'
    )

    # 8. Add tab lifecycle dispatch to switchGovTab
    old_switch_tab = """  const main = document.getElementById('main-content');
  if (main && window.scrollY < main.offsetTop - 150) {
    main.scrollIntoView({ behavior: 'smooth' });
  }
}"""
    new_switch_tab = """  const main = document.getElementById('main-content');
  if (main && window.scrollY < main.offsetTop - 150) {
    main.scrollIntoView({ behavior: 'smooth' });
  }

  // Automatic Tab Lifecycle Dispatch
  if (tabKey === 'catalog') {
    if (typeof loadMasterCatalogUi === 'function') loadMasterCatalogUi(1);
  } else if (tabKey === 'futuresync') {
    if (typeof loadFutureSyncStatusUi === 'function') loadFutureSyncStatusUi();
  } else if (tabKey === 'map') {
    if (typeof loadMapChoropleth === 'function') loadMapChoropleth();
  } else if (tabKey === 'audit') {
    if (typeof loadAuditAnomalies === 'function') loadAuditAnomalies();
  } else if (tabKey === 'correlator') {
    if (typeof runCorrelator === 'function') runCorrelator();
  } else if (tabKey === 'webhooks') {
    if (typeof loadWebhooksView === 'function') loadWebhooksView();
  } else if (tabKey === 'sql') {
    if (typeof loadPresetSql === 'function' && (!lastSqlResult || !lastSqlResult.rows)) loadPresetSql(0);
  } else if (tabKey === 'lgd' || tabKey === 'directory') {
    if (typeof loadLgdDirectory === 'function') loadLgdDirectory();
  }
}"""
    content = content.replace(old_switch_tab, new_switch_tab)

    # 9. Multi-dataset filtering and export link updates
    old_update_exports = """function updateExportLinks() {
  const isMaster = currentCatalogDataset === 'master';
  const csvBtn = document.getElementById('btnExportCsv');
  const parquetBtn = document.getElementById('btnExportParquet');
  const geojsonBtn = document.getElementById('btnExportGeoJson');
  const jsonBtn = document.getElementById('btnExportJson');

  const stateVal = document.getElementById('stateFilter') ? document.getElementById('stateFilter').value : 'ALL';
  const schemeVal = document.getElementById('schemeFilter') ? document.getElementById('schemeFilter').value : 'ALL';
  const qVal = document.getElementById('searchInput') ? document.getElementById('searchInput').value.trim() : '';

  let filterQuery = '';
  if (isMaster) {
    if (qVal) filterQuery += `&q=${encodeURIComponent(qVal)}`;
    if (stateVal && stateVal !== 'ALL') filterQuery += `&state=${encodeURIComponent(stateVal)}`;
    if (schemeVal && schemeVal !== 'ALL') filterQuery += `&sector=${encodeURIComponent(schemeVal)}`;
    if (onlyLgdVerified) filterQuery += `&lgd_district_code__gte=1`;
  }

  if (isMaster) {
    if (csvBtn) csvBtn.href = `/v1/data?format=csv&limit=11742${filterQuery}`;
    if (parquetBtn) parquetBtn.href = `/v1/data?format=parquet&limit=11742${filterQuery}`;
    if (geojsonBtn) {
      geojsonBtn.href = `/v1/geojson?limit=11742${filterQuery}`;
      geojsonBtn.classList.remove('opacity-50', 'pointer-events-none');
    }
    if (jsonBtn) jsonBtn.href = `/v1/data?limit=50${filterQuery}`;
  } else {
    if (csvBtn) csvBtn.href = `/v1/datasets/${currentCatalogDataset}/data?limit=5000`;
    if (parquetBtn) parquetBtn.href = `/v1/datasets/${currentCatalogDataset}/data?limit=5000`;
    if (geojsonBtn) {
      geojsonBtn.href = '#';
      geojsonBtn.classList.add('opacity-50', 'pointer-events-none');
    }
    if (jsonBtn) jsonBtn.href = `/v1/datasets/${currentCatalogDataset}/data?limit=5000`;
  }
}"""
    new_update_exports = """function updateExportLinks() {
  const isMaster = currentCatalogDataset === 'master';
  const csvBtn = document.getElementById('btnExportCsv');
  const parquetBtn = document.getElementById('btnExportParquet');
  const geojsonBtn = document.getElementById('btnExportGeoJson');
  const jsonBtn = document.getElementById('btnExportJson');

  const stateVal = document.getElementById('stateFilter') ? document.getElementById('stateFilter').value : 'ALL';
  const schemeVal = document.getElementById('schemeFilter') ? document.getElementById('schemeFilter').value : 'ALL';
  const qVal = document.getElementById('searchInput') ? document.getElementById('searchInput').value.trim() : '';

  let filterQuery = '';
  if (qVal) filterQuery += `&q=${encodeURIComponent(qVal)}`;
  if (stateVal && stateVal !== 'ALL') filterQuery += `&state=${encodeURIComponent(stateVal)}`;
  if (isMaster) {
    if (schemeVal && schemeVal !== 'ALL') filterQuery += `&sector=${encodeURIComponent(schemeVal)}`;
    if (onlyLgdVerified) filterQuery += `&lgd_district_code__gte=1`;
  }

  if (isMaster) {
    if (csvBtn) {
      csvBtn.href = `/v1/data?format=csv&limit=11742${filterQuery}`;
      csvBtn.download = 'bharat_governance_master_2026.csv';
    }
    if (parquetBtn) {
      parquetBtn.href = `/v1/data?format=parquet&limit=11742${filterQuery}`;
      parquetBtn.download = 'bharat_governance_master_2026.parquet';
    }
    if (geojsonBtn) {
      geojsonBtn.href = `/v1/geojson?limit=11742${filterQuery}`;
      geojsonBtn.download = 'bharat_governance_centroids.geojson';
      geojsonBtn.classList.remove('opacity-50', 'pointer-events-none');
    }
    if (jsonBtn) jsonBtn.href = `/v1/data?limit=50${filterQuery}`;
  } else {
    if (csvBtn) {
      csvBtn.href = `/v1/datasets/${currentCatalogDataset}/data?format=csv&limit=5000${filterQuery}`;
      csvBtn.download = `${currentCatalogDataset}_2026.csv`;
    }
    if (parquetBtn) {
      parquetBtn.href = `/v1/datasets/${currentCatalogDataset}/data?format=parquet&limit=5000${filterQuery}`;
      parquetBtn.download = `${currentCatalogDataset}_2026.parquet`;
    }
    if (geojsonBtn) {
      geojsonBtn.href = '#';
      geojsonBtn.classList.add('opacity-50', 'pointer-events-none');
    }
    if (jsonBtn) jsonBtn.href = `/v1/datasets/${currentCatalogDataset}/data?limit=50${filterQuery}`;
  }
}"""
    content = content.replace(old_update_exports, new_update_exports)

    # 10. Update loadExplorerData to apply filters across all catalog datasets
    old_explorer_filters = """  let baseUrl = currentCatalogDataset === 'master' 
    ? '/v1/data' 
    : `/v1/datasets/${currentCatalogDataset}/data`;
  let url = `${baseUrl}?page=${page}&limit=${currentExplorerLimit}`;
  if (currentCatalogDataset === 'master') {
    if (qVal) url += `&q=${encodeURIComponent(qVal)}`;
    if (stateVal && stateVal !== 'ALL') url += `&state=${encodeURIComponent(stateVal)}`;
    if (schemeVal && schemeVal !== 'ALL') url += `&sector=${encodeURIComponent(schemeVal)}`;
    if (onlyLgdVerified) url += `&lgd_district_code__gte=1`;
  }"""
    new_explorer_filters = """  let baseUrl = currentCatalogDataset === 'master' 
    ? '/v1/data' 
    : `/v1/datasets/${currentCatalogDataset}/data`;
  let url = `${baseUrl}?page=${page}&limit=${currentExplorerLimit}`;
  if (qVal) url += `&q=${encodeURIComponent(qVal)}`;
  if (stateVal && stateVal !== 'ALL') url += `&state=${encodeURIComponent(stateVal)}`;
  if (currentCatalogDataset === 'master') {
    if (schemeVal && schemeVal !== 'ALL') url += `&sector=${encodeURIComponent(schemeVal)}`;
    if (onlyLgdVerified) url += `&lgd_district_code__gte=1`;
  }"""
    content = content.replace(old_explorer_filters, new_explorer_filters)

    # 11. Add loadLgdDirectory and renderLgdTable
    if "async function loadLgdDirectory" not in content:
        lgd_loader = """
let allLgdDistricts = [];
async function loadLgdDirectory() {
  const tbody = document.getElementById('lgdTableBody');
  if (!tbody || allLgdDistricts.length > 0) return;
  tbody.innerHTML = '<tr><td colspan="6" class="py-6 text-center text-slate-400">Loading statutory LGD gazetteer from Ministry of Panchayati Raj...</td></tr>';
  try {
    const resp = await fetch('/v1/lgd/districts?limit=100');
    const data = await resp.json();
    allLgdDistricts = data.districts || [];
    renderLgdTable(allLgdDistricts);
  } catch (e) {
    console.error('Failed to load LGD:', e);
  }
}

function renderLgdTable(list) {
  const tbody = document.getElementById('lgdTableBody');
  if (!tbody) return;
  if (!list.length) {
    tbody.innerHTML = '<tr><td colspan="6" class="py-6 text-center text-slate-400">No matching districts found.</td></tr>';
    return;
  }
  tbody.innerHTML = list.map(d => `
    <tr class="hover:bg-slate-50 transition">
      <td class="py-3 px-3 font-bold font-mono text-govNavy-900">${d.district_code || d.lgd_district_code || '—'}</td>
      <td class="py-3 px-3 font-medium text-slate-900">${escapeHtml(d.canonical_name || d.name)}</td>
      <td class="py-3 px-3 text-slate-700">${escapeHtml(d.state_name || d.state)}</td>
      <td class="py-3 px-3 text-slate-600 font-devanagari">${escapeHtml(d.indic_name || d.canonical_name)}</td>
      <td class="py-3 px-3 text-slate-500 text-[11px]">${escapeHtml((d.aliases || []).join(', ') || '—')}</td>
      <td class="py-3 px-3 text-right">
        <button class="text-[11px] text-govNavy-800 hover:text-govNavy-950 font-semibold underline" onclick="quickFilterFromLgd('${escapeHtml(d.state_name || d.state)}')">Filter state</button>
      </td>
    </tr>
  `).join('');
}
"""
        content = content.replace("function filterLgdTable() {", lgd_loader + "\nfunction filterLgdTable() {")

    hf.write_text(content, encoding="utf-8")
    print(f"Successfully patched {hf}")

