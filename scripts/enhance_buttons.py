#!/usr/bin/env python3
"""Make all buttons smooth, cohesive, responsive, and pixel-aligned across index.html files."""

import sys
import re

CSS_ADDITIONS = """
/* ============================================================
   BUTTERY SMOOTH & PIXEL-PERFECT BUTTON FOUNDATIONS
   ============================================================ */
button, a[role="button"], .btn-action, .subview-btn, .tab-trigger {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  vertical-align: middle;
  line-height: 1.25;
  cursor: pointer;
  user-select: none;
  font-family: inherit;
  transition: all 0.18s cubic-bezier(0.16, 1, 0.3, 1);
  outline: none;
}

button:active, a[role="button"]:active, .btn-action:active {
  transform: scale(0.97) translateY(1px);
}

button:focus-visible, a:focus-visible, select:focus-visible, input:focus-visible {
  outline: 2px solid #FF9933 !important;
  outline-offset: 2px !important;
}

/* Subtle elevation for primary interactive buttons */
.btn-elevated {
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
}
.btn-elevated:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px -1px rgba(0, 0, 0, 0.12), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}
.btn-elevated:active {
  transform: translateY(0) scale(0.97);
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
}

/* Smooth Tab Bar transitions */
.tab-trigger {
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}
.tab-trigger:hover:not(.tab-active) {
  transform: translateY(-1px);
}
.tab-active {
  background-color: #ffffff !important;
  color: #0A1931 !important;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06) !important;
  font-weight: 700 !important;
}
"""

for path in ["datasetu/static/index.html", "api/datasetu/static/index.html"]:
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Inject CSS additions into <style>
    if "BUTTERY SMOOTH & PIXEL-PERFECT BUTTON FOUNDATIONS" not in html:
        html = html.replace("</style>", f"{CSS_ADDITIONS}\n</style>")

    # 2. Header action buttons alignment (LGD Quick Lookup & Upload Dataset)
    old_header_actions = """      <div class="flex items-center space-x-2.5">
        <button class="bg-govNavy-800 hover:bg-govNavy-700 text-slate-200 border border-slate-700 px-3 py-2 rounded text-xs font-semibold flex items-center space-x-1.5 transition" onclick="openLgdLookupModal()">
          <svg class="w-3.5 h-3.5 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
          <span class="hidden sm:inline">LGD Quick Lookup</span>
        </button>
        <button class="bg-govRed hover:bg-govRed-hover text-white px-4 py-2.5 rounded text-xs font-semibold uppercase tracking-wider flex items-center space-x-2 shadow-sm transition active:scale-95" onclick="openCdcUploadModal()">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M12 4v16m8-8H4" stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5"></path></svg>
          <span id="btn-upload-label" class="">Upload Dataset / योगदान दें</span>
        </button>
      </div>"""

    new_header_actions = """      <div class="flex items-center space-x-2.5">
        <button class="h-9 bg-govNavy-800 hover:bg-govNavy-700 text-slate-200 border border-slate-700/80 px-3.5 rounded-lg text-xs font-semibold inline-flex items-center gap-1.5 transition-all duration-200 hover:-translate-y-0.5 active:scale-95 shadow-xs hover:shadow" onclick="openLgdLookupModal()">
          <svg class="w-3.5 h-3.5 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
          <span class="hidden sm:inline">LGD Quick Lookup</span>
        </button>
        <button class="h-9 bg-govRed hover:bg-govRed-hover text-white px-4 rounded-lg text-xs font-bold uppercase tracking-wider inline-flex items-center gap-2 shadow-sm hover:shadow transition-all duration-200 hover:-translate-y-0.5 active:scale-95" onclick="openCdcUploadModal()">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M12 4v16m8-8H4" stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5"></path></svg>
          <span id="btn-upload-label" class="">Upload Dataset / योगदान दें</span>
        </button>
      </div>"""

    if old_header_actions in html:
        html = html.replace(old_header_actions, new_header_actions)

    # 3. Hero cURL buttons alignment
    old_hero_curl_btns = """      <div class="flex items-center space-x-2 shrink-0 self-end sm:self-auto">
        <button class="bg-govRed hover:bg-govRed-hover text-white px-2.5 py-1 rounded text-[11px] font-sans font-medium transition flex items-center gap-1 shadow" onclick="toggleHeroCurlLiveConsole()">
          <span class="w-2 h-2 rounded-full bg-emerald-400 live-pulse"></span>
          <span id="heroCurlRunLabel" class="">Run Live Query</span>
        </button>
        <button id="copyHeroCurlBtn" class="bg-slate-800 hover:bg-slate-700 text-slate-200 px-2.5 py-1 rounded text-[11px] font-sans transition flex items-center gap-1" onclick="copyHeroCurlCommand()">
          <svg class="w-3 h-3 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
          <span id="copyHeroCurlLabel" class="">Copy cURL</span>
        </button>
      </div>"""

    new_hero_curl_btns = """      <div class="flex items-center space-x-2 shrink-0 self-end sm:self-auto">
        <button class="h-8 bg-govRed hover:bg-govRed-hover text-white px-3 rounded-lg text-xs font-semibold transition-all duration-150 inline-flex items-center gap-1.5 shadow-xs hover:shadow active:scale-95" onclick="toggleHeroCurlLiveConsole()">
          <span class="w-2 h-2 rounded-full bg-emerald-400 live-pulse"></span>
          <span id="heroCurlRunLabel" class="">Run Live Query</span>
        </button>
        <button id="copyHeroCurlBtn" class="h-8 bg-slate-800 hover:bg-slate-700 text-slate-200 px-3 rounded-lg text-xs font-semibold transition-all duration-150 inline-flex items-center gap-1.5 border border-slate-700 active:scale-95 shadow-xs hover:shadow" onclick="copyHeroCurlCommand()">
          <svg class="w-3.5 h-3.5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
          <span id="copyHeroCurlLabel" class="">Copy cURL</span>
        </button>
      </div>"""

    if old_hero_curl_btns in html:
        html = html.replace(old_hero_curl_btns, new_hero_curl_btns)

    # 4. Workspace Tabs Bar buttons
    old_tabs_bar = """    <div class="flex bg-slate-200/80 p-1 rounded-lg border border-slate-300 self-start md:self-auto overflow-x-auto max-w-full">
      <button id="tab-btn-explorer" class="tab-trigger px-3.5 py-1.5 rounded-md text-xs font-semibold text-govNavy-900 bg-white shadow-sm whitespace-nowrap" onclick="switchGovTab('explorer')">National Data Explorer</button>
      <button id="tab-btn-map" class="tab-trigger px-3.5 py-1.5 rounded-md text-xs font-semibold text-sky-700 hover:text-sky-900 hover:bg-sky-50 whitespace-nowrap flex items-center gap-1 font-bold" onclick="switchGovTab('map'); loadMapChoropleth();">🗺️ Bharat Geospatial Map</button>
      <button id="tab-btn-audit" class="tab-trigger px-3.5 py-1.5 rounded-md text-xs font-semibold text-rose-700 hover:text-rose-900 hover:bg-rose-50 whitespace-nowrap flex items-center gap-1 font-bold" onclick="switchGovTab('audit'); loadAuditAnomalies();">🛡️ Civic Audit Engine</button>
      <button id="tab-btn-correlator" class="tab-trigger px-3.5 py-1.5 rounded-md text-xs font-semibold text-indigo-700 hover:text-indigo-900 hover:bg-indigo-50 whitespace-nowrap flex items-center gap-1 font-bold" onclick="switchGovTab('correlator'); runCorrelator();">🔗 Cross-Ministry Correlator</button>
      <button id="tab-btn-webhooks" class="tab-trigger px-3.5 py-1.5 rounded-md text-xs font-semibold text-amber-800 hover:text-amber-950 hover:bg-amber-50 whitespace-nowrap flex items-center gap-1 font-bold" onclick="switchGovTab('webhooks'); loadWebhooksView();">⚡ Webhooks &amp; Events</button>
      <button id="tab-btn-ai" class="tab-trigger px-3.5 py-1.5 rounded-md text-xs font-semibold text-purple-700 hover:text-purple-900 hover:bg-purple-50 whitespace-nowrap flex items-center gap-1 font-bold" onclick="switchGovTab('ai')">🤖 DataSetu AI Agent</button>
      <button id="tab-btn-catalog" class="tab-trigger px-3.5 py-1.5 rounded-md text-xs font-semibold text-amber-700 hover:text-amber-900 hover:bg-amber-50 whitespace-nowrap flex items-center gap-1 font-bold" onclick="switchGovTab('catalog')">🌐 Universal Gateway (300k+ Datasets)</button>
      <button id="tab-btn-futuresync" class="tab-trigger px-3.5 py-1.5 rounded-md text-xs font-semibold text-emerald-700 hover:text-emerald-900 hover:bg-emerald-50 whitespace-nowrap flex items-center gap-1 font-bold" onclick="switchGovTab('futuresync')">🔄 Future Auto-Sync</button>
      <button id="tab-btn-sql" class="tab-trigger px-3.5 py-1.5 rounded-md text-xs font-semibold text-slate-600 hover:text-govNavy-900 whitespace-nowrap" onclick="switchGovTab('sql')">⚡ SQL Studio</button>
      <button id="tab-btn-playground" class="tab-trigger px-3.5 py-1.5 rounded-md text-xs font-semibold text-slate-600 hover:text-govNavy-900 whitespace-nowrap" onclick="switchGovTab('playground')">Bharat API Playground &amp; SDKs</button>
      <button id="tab-btn-directory" class="tab-trigger px-3.5 py-1.5 rounded-md text-xs font-semibold text-slate-600 hover:text-govNavy-900 whitespace-nowrap" onclick="switchGovTab('directory')">🏛️ Govt Sites Directory</button>
      <button id="tab-btn-disinfector" class="tab-trigger px-3.5 py-1.5 rounded-md text-xs font-semibold text-slate-600 hover:text-govNavy-900 whitespace-nowrap" onclick="switchGovTab('disinfector')">Data Disinfector</button>
      <button id="tab-btn-lgd" class="tab-trigger px-3.5 py-1.5 rounded-md text-xs font-semibold text-slate-600 hover:text-govNavy-900 whitespace-nowrap" onclick="switchGovTab('lgd')">LGD Directory</button>
    </div>"""

    new_tabs_bar = """    <div class="flex items-center gap-1 bg-slate-200/90 p-1.5 rounded-xl border border-slate-300 self-start md:self-auto overflow-x-auto max-w-full custom-scrollbar shadow-inner">
      <button id="tab-btn-explorer" class="tab-trigger h-9 px-3.5 rounded-lg text-xs font-semibold text-govNavy-900 bg-white shadow-sm whitespace-nowrap inline-flex items-center gap-1.5 shrink-0" onclick="switchGovTab('explorer')">National Data Explorer</button>
      <button id="tab-btn-map" class="tab-trigger h-9 px-3.5 rounded-lg text-xs font-semibold text-sky-700 hover:text-sky-900 hover:bg-sky-50 whitespace-nowrap inline-flex items-center gap-1.5 shrink-0 font-bold" onclick="switchGovTab('map'); loadMapChoropleth();">🗺️ Bharat Geospatial Map</button>
      <button id="tab-btn-audit" class="tab-trigger h-9 px-3.5 rounded-lg text-xs font-semibold text-rose-700 hover:text-rose-900 hover:bg-rose-50 whitespace-nowrap inline-flex items-center gap-1.5 shrink-0 font-bold" onclick="switchGovTab('audit'); loadAuditAnomalies();">🛡️ Civic Audit Engine</button>
      <button id="tab-btn-correlator" class="tab-trigger h-9 px-3.5 rounded-lg text-xs font-semibold text-indigo-700 hover:text-indigo-900 hover:bg-indigo-50 whitespace-nowrap inline-flex items-center gap-1.5 shrink-0 font-bold" onclick="switchGovTab('correlator'); runCorrelator();">🔗 Cross-Ministry Correlator</button>
      <button id="tab-btn-webhooks" class="tab-trigger h-9 px-3.5 rounded-lg text-xs font-semibold text-amber-800 hover:text-amber-950 hover:bg-amber-50 whitespace-nowrap inline-flex items-center gap-1.5 shrink-0 font-bold" onclick="switchGovTab('webhooks'); loadWebhooksView();">⚡ Webhooks &amp; Events</button>
      <button id="tab-btn-ai" class="tab-trigger h-9 px-3.5 rounded-lg text-xs font-semibold text-purple-700 hover:text-purple-900 hover:bg-purple-50 whitespace-nowrap inline-flex items-center gap-1.5 shrink-0 font-bold" onclick="switchGovTab('ai')">🤖 DataSetu AI Agent</button>
      <button id="tab-btn-catalog" class="tab-trigger h-9 px-3.5 rounded-lg text-xs font-semibold text-amber-700 hover:text-amber-900 hover:bg-amber-50 whitespace-nowrap inline-flex items-center gap-1.5 shrink-0 font-bold" onclick="switchGovTab('catalog')">🌐 Universal Gateway (300k+ Datasets)</button>
      <button id="tab-btn-futuresync" class="tab-trigger h-9 px-3.5 rounded-lg text-xs font-semibold text-emerald-700 hover:text-emerald-900 hover:bg-emerald-50 whitespace-nowrap inline-flex items-center gap-1.5 shrink-0 font-bold" onclick="switchGovTab('futuresync')">🔄 Future Auto-Sync</button>
      <button id="tab-btn-sql" class="tab-trigger h-9 px-3.5 rounded-lg text-xs font-semibold text-slate-600 hover:text-govNavy-900 hover:bg-white/60 whitespace-nowrap inline-flex items-center gap-1.5 shrink-0" onclick="switchGovTab('sql')">⚡ SQL Studio</button>
      <button id="tab-btn-playground" class="tab-trigger h-9 px-3.5 rounded-lg text-xs font-semibold text-slate-600 hover:text-govNavy-900 hover:bg-white/60 whitespace-nowrap inline-flex items-center gap-1.5 shrink-0" onclick="switchGovTab('playground')">Bharat API Playground &amp; SDKs</button>
      <button id="tab-btn-directory" class="tab-trigger h-9 px-3.5 rounded-lg text-xs font-semibold text-slate-600 hover:text-govNavy-900 hover:bg-white/60 whitespace-nowrap inline-flex items-center gap-1.5 shrink-0" onclick="switchGovTab('directory')">🏛️ Govt Sites Directory</button>
      <button id="tab-btn-disinfector" class="tab-trigger h-9 px-3.5 rounded-lg text-xs font-semibold text-slate-600 hover:text-govNavy-900 hover:bg-white/60 whitespace-nowrap inline-flex items-center gap-1.5 shrink-0" onclick="switchGovTab('disinfector')">Data Disinfector</button>
      <button id="tab-btn-lgd" class="tab-trigger h-9 px-3.5 rounded-lg text-xs font-semibold text-slate-600 hover:text-govNavy-900 hover:bg-white/60 whitespace-nowrap inline-flex items-center gap-1.5 shrink-0" onclick="switchGovTab('lgd')">LGD Directory</button>
    </div>"""

    if old_tabs_bar in html:
        html = html.replace(old_tabs_bar, new_tabs_bar)

    # 5. Explorer Toolbar: Subview, Dataset Dropdown, and Export Buttons
    old_explorer_toolbar = """    <div class="flex items-center justify-between flex-wrap gap-2 text-xs">
      <div class="flex items-center space-x-2 flex-wrap">
        <div class="flex items-center space-x-1 bg-white border border-slate-200 rounded p-1 shadow-xs">
          <button id="btn-view-table" class="subview-btn px-2.5 py-1 rounded bg-govNavy-900 text-white font-semibold" onclick="switchSubView('table')">Table View</button>
          <button id="btn-view-cards" class="subview-btn px-2.5 py-1 rounded text-slate-600 hover:text-slate-900" onclick="switchSubView('cards')">Schema Cards</button>
          <button id="btn-view-validator" class="subview-btn px-2.5 py-1 rounded text-slate-600 hover:text-slate-900" onclick="switchSubView('validator')">Pipeline Telemetry</button>
        </div>
        <!-- Dataset Catalog Switcher -->
        <div class="flex items-center space-x-1.5 bg-amber-50 border border-amber-200 rounded px-2.5 py-1 shadow-xs">
          <span class="text-[11px] font-bold text-amber-900 flex items-center gap-1">📚 Dataset:</span>
          <select id="catalogDatasetSelect" class="text-xs font-semibold border-amber-300 rounded text-govNavy-900 py-0.5 px-1 bg-white focus:ring-govNavy-900 max-w-xs md:max-w-md" onchange="onCatalogDatasetChange(this.value)">"""

    new_explorer_toolbar = """    <div class="flex items-center justify-between flex-wrap gap-3 text-xs">
      <div class="flex items-center gap-2.5 flex-wrap">
        <div class="inline-flex items-center bg-slate-100 p-1 rounded-lg border border-slate-200 shadow-xs gap-1">
          <button id="btn-view-table" class="subview-btn h-8 px-3 rounded-md bg-govNavy-900 text-white font-semibold inline-flex items-center justify-center transition-all duration-150 shadow-xs active:scale-95" onclick="switchSubView('table')">Table View</button>
          <button id="btn-view-cards" class="subview-btn h-8 px-3 rounded-md text-slate-600 hover:text-slate-900 font-medium inline-flex items-center justify-center transition-all duration-150 active:scale-95" onclick="switchSubView('cards')">Schema Cards</button>
          <button id="btn-view-validator" class="subview-btn h-8 px-3 rounded-md text-slate-600 hover:text-slate-900 font-medium inline-flex items-center justify-center transition-all duration-150 active:scale-95" onclick="switchSubView('validator')">Pipeline Telemetry</button>
        </div>
        <!-- Dataset Catalog Switcher -->
        <div class="inline-flex items-center h-10 bg-amber-50/90 border border-amber-200 rounded-lg px-3 shadow-xs gap-2">
          <span class="text-xs font-bold text-amber-900 flex items-center gap-1 shrink-0">📚 Dataset:</span>
          <select id="catalogDatasetSelect" class="h-7 text-xs font-semibold border-amber-300 rounded-md text-govNavy-900 py-0 px-2 bg-white focus:ring-2 focus:ring-govNavy-900 max-w-xs md:max-w-md shadow-2xs" onchange="onCatalogDatasetChange(this.value)">"""

    if old_explorer_toolbar in html:
        html = html.replace(old_explorer_toolbar, new_explorer_toolbar)

    # 6. Export Buttons in Explorer
    old_export_btns = """      <div class="flex items-center space-x-1.5 flex-wrap">
        <span class="text-slate-500 font-medium text-[11px]">Instant Export:</span>
        <a id="btnExportCsv" href="/v1/data?format=csv&limit=11742" class="bg-slate-100 hover:bg-slate-200 text-slate-700 px-2 py-1 rounded border border-slate-300 font-medium text-xs transition flex items-center gap-1" download="bharat_governance_master_2026.csv">
          <span>⬇️ CSV</span>
        </a>
        <a id="btnExportParquet" href="/v1/data?format=parquet&limit=11742" class="bg-slate-100 hover:bg-slate-200 text-slate-700 px-2 py-1 rounded border border-slate-300 font-medium text-xs transition flex items-center gap-1" download="bharat_governance_master_2026.parquet">
          <span>⬇️ Parquet</span>
        </a>
        <a id="btnExportGeoJson" href="/v1/geojson?limit=11742" class="bg-slate-100 hover:bg-slate-200 text-slate-700 px-2 py-1 rounded border border-slate-300 font-medium text-xs transition flex items-center gap-1" download="bharat_governance_centroids.geojson">
          <span>🗺️ GeoJSON</span>
        </a>
        <a id="btnExportJson" href="/v1/data?limit=50" target="_blank" class="bg-slate-100 hover:bg-slate-200 text-slate-700 px-2 py-1 rounded border border-slate-300 font-medium text-xs transition flex items-center gap-1">
          <span>⬇️ REST API</span>
        </a>
        <button onclick="switchGovTab('sql')" class="bg-amber-100 hover:bg-amber-200 text-amber-900 border border-amber-300 px-2 py-1 rounded font-semibold text-xs transition flex items-center gap-1">
          <span>⚡ SQL Studio</span>
        </button>
      </div>"""

    new_export_btns = """      <div class="flex items-center gap-2 flex-wrap">
        <span class="text-slate-500 font-semibold text-xs">Instant Export:</span>
        <a id="btnExportCsv" href="/v1/data?format=csv&limit=11742" class="h-9 px-3 rounded-lg border border-slate-300 bg-white hover:bg-slate-50 text-slate-700 font-semibold text-xs transition-all duration-150 shadow-xs hover:shadow-sm hover:-translate-y-0.5 active:scale-95 inline-flex items-center gap-1.5" download="bharat_governance_master_2026.csv">
          <span>⬇️ CSV</span>
        </a>
        <a id="btnExportParquet" href="/v1/data?format=parquet&limit=11742" class="h-9 px-3 rounded-lg border border-slate-300 bg-white hover:bg-slate-50 text-slate-700 font-semibold text-xs transition-all duration-150 shadow-xs hover:shadow-sm hover:-translate-y-0.5 active:scale-95 inline-flex items-center gap-1.5" download="bharat_governance_master_2026.parquet">
          <span>⬇️ Parquet</span>
        </a>
        <a id="btnExportGeoJson" href="/v1/geojson?limit=11742" class="h-9 px-3 rounded-lg border border-slate-300 bg-white hover:bg-slate-50 text-slate-700 font-semibold text-xs transition-all duration-150 shadow-xs hover:shadow-sm hover:-translate-y-0.5 active:scale-95 inline-flex items-center gap-1.5" download="bharat_governance_centroids.geojson">
          <span>🗺️ GeoJSON</span>
        </a>
        <a id="btnExportJson" href="/v1/data?limit=50" target="_blank" class="h-9 px-3 rounded-lg border border-slate-300 bg-white hover:bg-slate-50 text-slate-700 font-semibold text-xs transition-all duration-150 shadow-xs hover:shadow-sm hover:-translate-y-0.5 active:scale-95 inline-flex items-center gap-1.5">
          <span>⚡ REST API</span>
        </a>
        <button onclick="switchGovTab('sql')" class="h-9 px-3 rounded-lg border border-amber-300 bg-amber-100 hover:bg-amber-200 text-amber-900 font-semibold text-xs transition-all duration-150 shadow-xs hover:shadow-sm hover:-translate-y-0.5 active:scale-95 inline-flex items-center gap-1.5">
          <span>⚡ SQL Studio</span>
        </button>
      </div>"""

    if old_export_btns in html:
        html = html.replace(old_export_btns, new_export_btns)

    # 7. Filters Bar (Matching h-9 heights across select dropdowns, LGD filter button, and Reset All button)
    old_filters_bar = """    <!-- Filters -->
    <div class="bg-white p-4 rounded-lg border border-slate-200 shadow-sm flex flex-col lg:flex-row gap-4 justify-between items-stretch lg:items-center">
      <div class="flex flex-wrap items-center gap-3">
        <span class="text-xs font-bold text-slate-700 uppercase">Filters:</span>
        <select id="stateFilter" class="text-xs border-slate-300 rounded focus:ring-govNavy-800 text-slate-700 py-1.5" onchange="loadExplorerData(1)">"""

    new_filters_bar = """    <!-- Filters -->
    <div class="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm flex flex-col lg:flex-row gap-3.5 justify-between items-stretch lg:items-center">
      <div class="flex flex-wrap items-center gap-2.5">
        <span class="text-xs font-bold text-slate-700 uppercase tracking-wide flex items-center mr-1">Filters:</span>
        <select id="stateFilter" class="h-9 text-xs border border-slate-300 rounded-lg focus:ring-2 focus:ring-govNavy-800 text-slate-700 px-3 py-0 bg-white font-medium shadow-xs transition-all cursor-pointer" onchange="loadExplorerData(1)">"""

    if old_filters_bar in html:
        html = html.replace(old_filters_bar, new_filters_bar)

    html = html.replace(
        '<select id="schemeFilter" class="text-xs border-slate-300 rounded focus:ring-govNavy-800 text-slate-700 py-1.5" onchange="loadExplorerData(1)">',
        '<select id="schemeFilter" class="h-9 text-xs border border-slate-300 rounded-lg focus:ring-2 focus:ring-govNavy-800 text-slate-700 px-3 py-0 bg-white font-medium shadow-xs transition-all cursor-pointer" onchange="loadExplorerData(1)">'
    )

    old_lgd_filter_btn = """        <button id="btn-filter-disinfected" class="bg-emerald-50 hover:bg-emerald-100 text-emerald-700 border border-emerald-200 text-[11px] font-semibold px-2 py-1 rounded flex items-center gap-1 transition" onclick="toggleOnlyDisinfected()">
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-600"></span>
          <span id="btn-filter-disinfected-label">100% LGD Match (782 Districts)</span>
        </button>
      </div>
      <div class="text-xs text-slate-500 flex items-center justify-between lg:justify-end gap-2">
        <span class="">Showing <strong id="recordCountText" class="text-slate-800">1 – 25 of 11,742</strong> verified records</span>
        <button class="text-xs text-govRed hover:underline font-medium" onclick="resetExplorerFilters()">Reset All</button>
      </div>"""

    new_lgd_filter_btn = """        <button id="btn-filter-disinfected" class="h-9 px-3.5 rounded-lg bg-emerald-50 hover:bg-emerald-100/90 text-emerald-800 border border-emerald-300/80 text-xs font-semibold inline-flex items-center gap-2 transition-all duration-200 shadow-xs hover:shadow-sm active:scale-95 hover:-translate-y-0.5 active:translate-y-0 cursor-pointer" onclick="toggleOnlyDisinfected()">
          <span class="w-2 h-2 rounded-full bg-emerald-600 live-pulse"></span>
          <span id="btn-filter-disinfected-label">100% LGD Match (782 Districts)</span>
        </button>
      </div>
      <div class="text-xs text-slate-500 flex items-center justify-between lg:justify-end gap-3">
        <span class="font-medium text-slate-600">Showing <strong id="recordCountText" class="text-govNavy-900 font-bold">1 – 25 of 11,742</strong> verified records</span>
        <button class="h-9 px-3.5 rounded-lg border border-slate-200 bg-slate-50 hover:bg-rose-50 hover:border-rose-200 text-slate-600 hover:text-govRed text-xs font-semibold inline-flex items-center gap-1.5 transition-all duration-200 shadow-xs hover:shadow-sm active:scale-95 hover:-translate-y-0.5 active:translate-y-0 cursor-pointer" onclick="resetExplorerFilters()">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
          <span>Reset All</span>
        </button>
      </div>"""

    if old_lgd_filter_btn in html:
        html = html.replace(old_lgd_filter_btn, new_lgd_filter_btn)

    # 8. Table Action Buttons inside renderExplorerTable
    old_row_actions = """        <td class="py-3.5 px-4 text-right space-x-2">
          <button class="bg-govNavy-900 hover:bg-govNavy-800 text-white px-2.5 py-1.5 rounded text-[11px] font-semibold transition" onclick="openTestApiForRecord(${idx})">Test API</button>
          <button class="text-slate-600 hover:text-slate-900 px-2 py-1 text-[11px] border border-slate-300 rounded" onclick="openDiffForRecord(${idx})">View Diff</button>
        </td>"""

    new_row_actions = """        <td class="py-3 px-4 text-right">
          <div class="inline-flex items-center justify-end gap-1.5">
            <button class="h-7 px-3 rounded-md text-[11px] font-semibold bg-govNavy-900 hover:bg-govNavy-800 text-white shadow-xs hover:shadow inline-flex items-center justify-center gap-1 transition-all duration-150 hover:-translate-y-0.5 active:scale-95 active:translate-y-0" onclick="openTestApiForRecord(${idx})">
              <span>Test API</span>
            </button>
            <button class="h-7 px-3 rounded-md text-[11px] font-semibold bg-white hover:bg-slate-50 text-slate-700 border border-slate-300 hover:border-slate-400 shadow-xs hover:shadow inline-flex items-center justify-center gap-1 transition-all duration-150 hover:-translate-y-0.5 active:scale-95 active:translate-y-0" onclick="openDiffForRecord(${idx})">
              <span>View Diff</span>
            </button>
          </div>
        </td>"""

    if old_row_actions in html:
        html = html.replace(old_row_actions, new_row_actions)

    # 9. Pagination Controls & changeExplorerPage
    old_render_pag = """function renderPagination(meta) {
  const info = document.getElementById('explorerPaginationInfo');
  const controls = document.getElementById('explorerPaginationControls');
  if (!info || !controls) return;

  const start = (meta.page - 1) * meta.limit + 1;
  const end = Math.min(meta.page * meta.limit, meta.total);
  info.innerHTML = `Showing Page <strong>${meta.page}</strong> of <strong>${meta.pages || 1}</strong> (${meta.total.toLocaleString('en-IN')} Total Records in In-Memory DuckDB)`;

  let html = '';
  html += `<button onclick="changeExplorerPage(${meta.page - 1})" class="px-2.5 py-1 bg-white border border-slate-300 rounded hover:bg-slate-100 disabled:opacity-30 disabled:pointer-events-none text-xs" ${meta.page <= 1 ? 'disabled' : ''}>Previous</button>`;
  
  const totalPages = meta.pages || 1;
  let pMin = Math.max(1, meta.page - 2);
  let pMax = Math.min(totalPages, meta.page + 2);
  if (pMin > 1) {
    html += `<button onclick="changeExplorerPage(1)" class="px-2.5 py-1 bg-white border border-slate-300 rounded hover:bg-slate-100 text-xs">1</button>`;
    if (pMin > 2) html += `<span class="px-1 text-slate-400">...</span>`;
  }
  for (let p = pMin; p <= pMax; p++) {
    const active = (p === meta.page);
    html += `<button onclick="changeExplorerPage(${p})" class="px-2.5 py-1 rounded text-xs font-semibold ${active ? 'bg-govNavy-900 text-white border border-govNavy-900' : 'bg-white border border-slate-300 hover:bg-slate-100 text-slate-700'}">${p}</button>`;
  }
  if (pMax < totalPages) {
    if (pMax < totalPages - 1) html += `<span class="px-1 text-slate-400">...</span>`;
    html += `<button onclick="changeExplorerPage(${totalPages})" class="px-2.5 py-1 bg-white border border-slate-300 rounded hover:bg-slate-100 text-xs">${totalPages}</button>`;
  }

  html += `<button onclick="changeExplorerPage(${meta.page + 1})" class="px-2.5 py-1 bg-white border border-slate-300 rounded hover:bg-slate-100 disabled:opacity-30 disabled:pointer-events-none text-xs" ${meta.page >= totalPages ? 'disabled' : ''}>Next</button>`;
  
  controls.innerHTML = html;
}

function changeExplorerPage(target) {
  if (target >= 1 && target <= totalPages) {
    loadExplorerData(target);
  }
}"""

    new_render_pag = """function renderPagination(meta) {
  const info = document.getElementById('explorerPaginationInfo');
  const controls = document.getElementById('explorerPaginationControls');
  if (!info || !controls) return;

  const maxPages = meta.pages || totalExplorerPages || 1;
  const page = meta.page || currentExplorerPage || 1;
  info.innerHTML = `Showing Page <strong class="text-govNavy-900 font-bold">${page}</strong> of <strong class="text-govNavy-900 font-bold">${maxPages}</strong> (<span class="font-mono font-semibold text-slate-700">${meta.total.toLocaleString('en-IN')}</span> Total Records in In-Memory DuckDB)`;

  let html = '';
  html += `<button onclick="changeExplorerPage(${page - 1})" class="h-8 px-3 rounded-lg bg-white hover:bg-slate-100 text-slate-700 border border-slate-300 font-semibold text-xs inline-flex items-center gap-1 transition-all duration-150 shadow-xs hover:shadow-sm active:scale-95 disabled:opacity-30 disabled:pointer-events-none disabled:shadow-none" ${page <= 1 ? 'disabled' : ''}>← Prev</button>`;

  let pMin = Math.max(1, page - 2);
  let pMax = Math.min(maxPages, page + 2);
  if (pMin > 1) {
    html += `<button onclick="changeExplorerPage(1)" class="h-8 min-w-[32px] px-2.5 rounded-lg bg-white hover:bg-slate-100 text-slate-700 border border-slate-300 font-semibold text-xs inline-flex items-center justify-center transition-all duration-150 shadow-xs hover:shadow-sm active:scale-95">1</button>`;
    if (pMin > 2) html += `<span class="h-8 px-1 inline-flex items-center justify-center text-slate-400 text-xs font-bold">…</span>`;
  }
  for (let p = pMin; p <= pMax; p++) {
    const active = (p === page);
    html += `<button onclick="changeExplorerPage(${p})" class="h-8 min-w-[32px] px-2.5 rounded-lg text-xs font-semibold inline-flex items-center justify-center transition-all duration-150 shadow-xs active:scale-95 ${active ? 'bg-govNavy-900 text-white border border-govNavy-900 shadow-sm font-bold scale-105' : 'bg-white hover:bg-slate-100 text-slate-700 border border-slate-300 hover:border-slate-400'}">${p}</button>`;
  }
  if (pMax < maxPages) {
    if (pMax < maxPages - 1) html += `<span class="h-8 px-1 inline-flex items-center justify-center text-slate-400 text-xs font-bold">…</span>`;
    html += `<button onclick="changeExplorerPage(${maxPages})" class="h-8 min-w-[32px] px-2.5 rounded-lg bg-white hover:bg-slate-100 text-slate-700 border border-slate-300 font-semibold text-xs inline-flex items-center justify-center transition-all duration-150 shadow-xs hover:shadow-sm active:scale-95">${maxPages}</button>`;
  }

  html += `<button onclick="changeExplorerPage(${page + 1})" class="h-8 px-3 rounded-lg bg-white hover:bg-slate-100 text-slate-700 border border-slate-300 font-semibold text-xs inline-flex items-center gap-1 transition-all duration-150 shadow-xs hover:shadow-sm active:scale-95 disabled:opacity-30 disabled:pointer-events-none disabled:shadow-none" ${page >= maxPages ? 'disabled' : ''}>Next →</button>`;

  controls.innerHTML = html;
}

function changeExplorerPage(target) {
  const maxPages = totalExplorerPages || 1;
  if (target >= 1 && target <= maxPages) {
    loadExplorerData(target);
  }
}"""

    if old_render_pag in html:
        html = html.replace(old_render_pag, new_render_pag)

    # 10. Update toggleOnlyDisinfected & resetExplorerFilters styling
    old_toggle_disinfected = """function toggleOnlyDisinfected() {
  onlyLgdVerified = !onlyLgdVerified;
  const btn = document.getElementById('btn-filter-disinfected');
  const label = document.getElementById('btn-filter-disinfected-label');
  if (onlyLgdVerified) {
    btn.className = 'bg-emerald-600 text-white border border-emerald-700 text-[11px] font-semibold px-2 py-1 rounded flex items-center gap-1 transition shadow-xs';
    if (label) label.innerText = 'Showing Verified LGD Only (11,742)';
  } else {
    btn.className = 'bg-emerald-50 hover:bg-emerald-100 text-emerald-700 border border-emerald-200 text-[11px] font-semibold px-2 py-1 rounded flex items-center gap-1 transition';
    if (label) label.innerText = '100% LGD Match (782 Districts)';
  }
  loadExplorerData(1);
}"""

    new_toggle_disinfected = """function toggleOnlyDisinfected() {
  onlyLgdVerified = !onlyLgdVerified;
  const btn = document.getElementById('btn-filter-disinfected');
  const label = document.getElementById('btn-filter-disinfected-label');
  if (onlyLgdVerified) {
    btn.className = 'h-9 px-3.5 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white border border-emerald-700 text-xs font-semibold inline-flex items-center gap-2 transition-all duration-200 shadow-sm active:scale-95 hover:-translate-y-0.5 active:translate-y-0 cursor-pointer';
    if (label) label.innerText = 'Showing Verified LGD Only (11,742)';
  } else {
    btn.className = 'h-9 px-3.5 rounded-lg bg-emerald-50 hover:bg-emerald-100/90 text-emerald-800 border border-emerald-300/80 text-xs font-semibold inline-flex items-center gap-2 transition-all duration-200 shadow-xs hover:shadow-sm active:scale-95 hover:-translate-y-0.5 active:translate-y-0 cursor-pointer';
    if (label) label.innerText = '100% LGD Match (782 Districts)';
  }
  loadExplorerData(1);
}"""

    if old_toggle_disinfected in html:
        html = html.replace(old_toggle_disinfected, new_toggle_disinfected)

    old_reset_filters = """function resetExplorerFilters() {
  if (document.getElementById('stateFilter')) document.getElementById('stateFilter').value = 'ALL';
  if (document.getElementById('schemeFilter')) document.getElementById('schemeFilter').value = 'ALL';
  if (document.getElementById('searchInput')) document.getElementById('searchInput').value = '';
  onlyLgdVerified = false;
  const btn = document.getElementById('btn-filter-disinfected');
  if (btn) {
    btn.className = 'bg-emerald-50 hover:bg-emerald-100 text-emerald-700 border border-emerald-200 text-[11px] font-semibold px-2 py-1 rounded flex items-center gap-1 transition';
    document.getElementById('btn-filter-disinfected-label').innerText = '100% LGD Match (782 Districts)';
  }
  loadExplorerData(1);
}"""

    new_reset_filters = """function resetExplorerFilters() {
  if (document.getElementById('stateFilter')) document.getElementById('stateFilter').value = 'ALL';
  if (document.getElementById('schemeFilter')) document.getElementById('schemeFilter').value = 'ALL';
  if (document.getElementById('searchInput')) document.getElementById('searchInput').value = '';
  onlyLgdVerified = false;
  const btn = document.getElementById('btn-filter-disinfected');
  if (btn) {
    btn.className = 'h-9 px-3.5 rounded-lg bg-emerald-50 hover:bg-emerald-100/90 text-emerald-800 border border-emerald-300/80 text-xs font-semibold inline-flex items-center gap-2 transition-all duration-200 shadow-xs hover:shadow-sm active:scale-95 hover:-translate-y-0.5 active:translate-y-0 cursor-pointer';
    document.getElementById('btn-filter-disinfected-label').innerText = '100% LGD Match (782 Districts)';
  }
  loadExplorerData(1);
}"""

    if old_reset_filters in html:
        html = html.replace(old_reset_filters, new_reset_filters)

    # 11. Subview buttons styling inside switchSubView
    old_switch_subview = """function switchSubView(view) {
  document.getElementById('subview-table-container').classList.add('hidden');
  document.getElementById('subview-cards-container').classList.add('hidden');
  document.getElementById('subview-validator-container').classList.add('hidden');

  ['btn-view-table', 'btn-view-cards', 'btn-view-validator'].forEach(id => {
    document.getElementById(id).className = 'subview-btn px-2.5 py-1 rounded text-slate-600 hover:text-slate-900';
  });

  if (view === 'table') {
    document.getElementById('subview-table-container').classList.remove('hidden');
    document.getElementById('btn-view-table').className = 'subview-btn px-2.5 py-1 rounded bg-govNavy-900 text-white font-semibold';
  } else if (view === 'cards') {
    document.getElementById('subview-cards-container').classList.remove('hidden');
    document.getElementById('btn-view-cards').className = 'subview-btn px-2.5 py-1 rounded bg-govNavy-900 text-white font-semibold';
  } else if (view === 'validator') {
    document.getElementById('subview-validator-container').classList.remove('hidden');
    document.getElementById('btn-view-validator').className = 'subview-btn px-2.5 py-1 rounded bg-govNavy-900 text-white font-semibold';
  }
}"""

    new_switch_subview = """function switchSubView(view) {
  document.getElementById('subview-table-container').classList.add('hidden');
  document.getElementById('subview-cards-container').classList.add('hidden');
  document.getElementById('subview-validator-container').classList.add('hidden');

  ['btn-view-table', 'btn-view-cards', 'btn-view-validator'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.className = 'subview-btn h-8 px-3 rounded-md text-slate-600 hover:text-slate-900 font-medium inline-flex items-center justify-center transition-all duration-150 active:scale-95';
  });

  if (view === 'table') {
    document.getElementById('subview-table-container').classList.remove('hidden');
    const el = document.getElementById('btn-view-table');
    if (el) el.className = 'subview-btn h-8 px-3 rounded-md bg-govNavy-900 text-white font-semibold inline-flex items-center justify-center transition-all duration-150 shadow-xs active:scale-95';
  } else if (view === 'cards') {
    document.getElementById('subview-cards-container').classList.remove('hidden');
    const el = document.getElementById('btn-view-cards');
    if (el) el.className = 'subview-btn h-8 px-3 rounded-md bg-govNavy-900 text-white font-semibold inline-flex items-center justify-center transition-all duration-150 shadow-xs active:scale-95';
  } else if (view === 'validator') {
    document.getElementById('subview-validator-container').classList.remove('hidden');
    const el = document.getElementById('btn-view-validator');
    if (el) el.className = 'subview-btn h-8 px-3 rounded-md bg-govNavy-900 text-white font-semibold inline-flex items-center justify-center transition-all duration-150 shadow-xs active:scale-95';
  }
}"""

    if old_switch_subview in html:
        html = html.replace(old_switch_subview, new_switch_subview)

    # 12. Write back updated file
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Successfully enhanced buttons in", path)

