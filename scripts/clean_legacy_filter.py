import sys

for path in ['datasetu/static/index.html', 'api/datasetu/static/index.html']:
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    target = """function filterExplorerByHeroCategory(cat) {
  if (cat === 'ALL') resetFilters();
  else {
    document.getElementById('schemeFilter').value = cat;
    filterExplorerTable();
  }
}

function filterExplorerTable() {
  const state = document.getElementById('stateFilter').value;
  const scheme = document.getElementById('schemeFilter').value;
  const rows = document.querySelectorAll('#explorerTableBody tr');
  let visible = 0;

  rows.forEach(row => {
    const sMatch = (state === 'ALL' || row.getAttribute('data-state') === state);
    const scMatch = (scheme === 'ALL' || row.getAttribute('data-scheme') === scheme);
    if (sMatch && scMatch) {
      row.style.display = '';
      visible++;
    } else {
      row.style.display = 'none';
    }
  });
  document.getElementById('recordCountText').innerText = visible;
}

function resetFilters() {
  document.getElementById('stateFilter').value = 'ALL';
  document.getElementById('schemeFilter').value = 'ALL';
  document.getElementById('searchInput').value = '';
  const rows = document.querySelectorAll('#explorerTableBody tr');
  rows.forEach(r => r.style.display = '');
  document.getElementById('recordCountText').innerText = rows.length;
}

function toggleOnlyDisinfected() {
  onlyDisinfected = !onlyDisinfected;
  const btn = document.getElementById('btn-filter-disinfected');
  if (onlyDisinfected) {
    btn.className = 'bg-emerald-50 hover:bg-emerald-100 text-emerald-700 border border-emerald-200 text-[11px] font-semibold px-2 py-1 rounded flex items-center gap-1 transition';
    btn.innerHTML = '<span class="w-1.5 h-1.5 rounded-full bg-emerald-600"></span><span>84.5% Auto-Disinfected</span>';
  } else {
    btn.className = 'bg-slate-100 text-slate-600 border border-slate-300 text-[11px] font-semibold px-2 py-1 rounded flex items-center gap-1 transition';
    btn.innerHTML = '<span class="w-1.5 h-1.5 rounded-full bg-slate-400"></span><span>Show All (Raw + Disinfected)</span>';
  }
}"""

    replacement = """function filterExplorerByHeroCategory(cat) {
  if (cat === 'ALL') {
    resetExplorerFilters();
  } else {
    const el = document.getElementById('schemeFilter');
    if (el) el.value = cat;
    loadExplorerData(1);
  }
}"""

    assert target in html, f"Target block not found in {path}"
    html = html.replace(target, replacement)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Cleaned legacy filters in", path)

