import re

for path in ['datasetu/static/index.html', 'api/datasetu/static/index.html']:
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. speakAiSummary: use aiSummaryText
    old_speak = "const summaryEl = document.getElementById('aiExecutiveSummary');"
    new_speak = "const summaryEl = document.getElementById('aiSummaryText') || document.getElementById('aiExecutiveSummary');"
    assert old_speak in html, f"Could not find old_speak in {path}"
    html = html.replace(old_speak, new_speak)

    # 2. Add id="kpi-latency-val" to Hero KPI card
    old_kpi_span = '<span class="text-amber-700 font-bold">782 Districts</span> • 0.45 ms Query Latency'
    new_kpi_span = '<span class="text-amber-700 font-bold">782 Districts</span> • <span id="kpi-latency-val">0.45</span> ms Query Latency'
    assert old_kpi_span in html, f"Could not find old_kpi_span in {path}"
    html = html.replace(old_kpi_span, new_kpi_span)

    # 3. openCompiledDatasetInSql: use sqlQueryInput and runSqlStudio
    old_compiled_sql = """function openCompiledDatasetInSql(tableName) {
  const editor = document.getElementById('sqlEditor');
  if (editor) {
    editor.value = `SELECT * FROM ${tableName} LIMIT 50;`;
  }
  switchGovTab('sql');
  runSqlQuery();
}"""
    new_compiled_sql = """function openCompiledDatasetInSql(tableName) {
  const editor = document.getElementById('sqlQueryInput') || document.getElementById('sqlEditor');
  if (editor) {
    editor.value = `SELECT * FROM ${tableName} LIMIT 50;`;
  }
  switchGovTab('sql');
  if (typeof runSqlStudio === 'function') {
    runSqlStudio();
  }
}"""
    assert old_compiled_sql in html, f"Could not find old_compiled_sql in {path}"
    html = html.replace(old_compiled_sql, new_compiled_sql)

    # 4. selectSuggestion: call loadExplorerData(1)
    old_select_sugg = """function selectSuggestion(name, state, scheme) {
  document.getElementById('searchInput').value = name;
  closeSearchSuggestions();
  if (state !== 'ALL') document.getElementById('stateFilter').value = state;
  if (scheme) document.getElementById('schemeFilter').value = scheme;
  filterExplorerTable();
  switchGovTab('explorer');
}"""
    new_select_sugg = """function selectSuggestion(name, state, scheme) {
  const sInput = document.getElementById('searchInput');
  if (sInput) sInput.value = name;
  closeSearchSuggestions();
  if (state && state !== 'ALL') {
    const stEl = document.getElementById('stateFilter');
    if (stEl) stEl.value = state;
  }
  if (scheme && scheme !== 'ALL') {
    const scEl = document.getElementById('schemeFilter');
    if (scEl) scEl.value = scheme;
  }
  switchGovTab('explorer');
  loadExplorerData(1);
}"""
    assert old_select_sugg in html, f"Could not find old_select_sugg in {path}"
    html = html.replace(old_select_sugg, new_select_sugg)

    # 5. quickFilterFromLgd: call loadExplorerData(1)
    old_qf_lgd = """function quickFilterFromLgd(st) {
  document.getElementById('stateFilter').value = st;
  switchGovTab('explorer');
  filterExplorerTable();
}"""
    new_qf_lgd = """function quickFilterFromLgd(st) {
  const stEl = document.getElementById('stateFilter');
  if (stEl) stEl.value = st;
  switchGovTab('explorer');
  loadExplorerData(1);
}"""
    assert old_qf_lgd in html, f"Could not find old_qf_lgd in {path}"
    html = html.replace(old_qf_lgd, new_qf_lgd)

    # 6. filterExplorerByHeroCategory: map categories to master sectors
    old_hero_filter = """function filterExplorerByHeroCategory(cat) {
  if (cat === 'ALL') {
    resetExplorerFilters();
  } else {
    const el = document.getElementById('schemeFilter');
    if (el) el.value = cat;
    loadExplorerData(1);
  }
}"""
    new_hero_filter = """function filterExplorerByHeroCategory(cat) {
  const catMap = {
    'ALL': 'ALL',
    'PMKISAN': 'Agriculture & Farmers Welfare',
    'MGNREGA': 'Rural Development',
    'HEALTH': 'Health & Family Welfare',
    'DBT': 'Housing & Urban Affairs',
    'LGD': 'ALL'
  };
  const targetSector = catMap[cat] || cat;
  const el = document.getElementById('schemeFilter');
  if (el) el.value = targetSector;
  if (cat === 'LGD') {
    onlyLgdVerified = true;
    const btn = document.getElementById('btn-filter-disinfected');
    const label = document.getElementById('btn-filter-disinfected-label');
    if (btn) btn.className = 'h-9 px-3.5 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white border border-emerald-700 text-xs font-semibold inline-flex items-center gap-2 transition-all duration-200 shadow-sm active:scale-95 cursor-pointer';
    if (label) label.innerText = 'Showing Verified LGD Only (11,742)';
  }
  switchGovTab('explorer');
  loadExplorerData(1);
}"""
    assert old_hero_filter in html, f"Could not find old_hero_filter in {path}"
    html = html.replace(old_hero_filter, new_hero_filter)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Patched {path} successfully!")
