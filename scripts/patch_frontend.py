#!/usr/bin/env python3
"""Upgrade script for DataSetu frontend with 6 cutting-edge features."""

import os
import sys

INDEX_PATH = "datasetu/static/index.html"
API_INDEX_PATH = "api/datasetu/static/index.html"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Top Navbar: Add direct shortcuts to Map, Audit, Correlator, Webhooks
OLD_NAV_BUTTONS = """        <button class="nav-btn px-3 py-2 text-amber-300 hover:text-white bg-amber-950/60 hover:bg-amber-900 border border-amber-500/40 rounded-md transition-colors font-bold flex items-center gap-1 shadow-sm" onclick="navToTab('catalog', this)">🌐 300,000+ Datasets</button>
        <button class="nav-btn px-3 py-2 text-emerald-300 hover:text-white bg-emerald-950/60 hover:bg-emerald-900 border border-emerald-500/40 rounded-md transition-colors font-bold flex items-center gap-1 shadow-sm" onclick="navToTab('futuresync', this)">🔄 Future Sync</button>
        <button class="nav-btn px-3 py-2 text-purple-300 hover:text-white bg-purple-950/60 hover:bg-purple-900 border border-purple-500/40 rounded-md transition-colors font-bold flex items-center gap-1 shadow-sm" onclick="navToTab('ai', this)">🤖 Ask AI</button>"""

NEW_NAV_BUTTONS = """        <button class="nav-btn px-3 py-2 text-sky-300 hover:text-white bg-sky-950/60 hover:bg-sky-900 border border-sky-500/40 rounded-md transition-colors font-bold flex items-center gap-1 shadow-sm" onclick="navToTab('map', this); loadMapChoropleth();">🗺️ Bharat Map</button>
        <button class="nav-btn px-3 py-2 text-rose-300 hover:text-white bg-rose-950/60 hover:bg-rose-900 border border-rose-500/40 rounded-md transition-colors font-bold flex items-center gap-1 shadow-sm" onclick="navToTab('audit', this); loadAuditAnomalies();">🛡️ Civic Audit</button>
        <button class="nav-btn px-3 py-2 text-indigo-300 hover:text-white bg-indigo-950/60 hover:bg-indigo-900 border border-indigo-500/40 rounded-md transition-colors font-bold flex items-center gap-1 shadow-sm" onclick="navToTab('correlator', this); runCorrelator();">🔗 Correlator</button>
        <button class="nav-btn px-3 py-2 text-purple-300 hover:text-white bg-purple-950/60 hover:bg-purple-900 border border-purple-500/40 rounded-md transition-colors font-bold flex items-center gap-1 shadow-sm" onclick="navToTab('ai', this)">🤖 Ask AI</button>
        <button class="nav-btn px-3 py-2 text-amber-300 hover:text-white bg-amber-950/60 hover:bg-amber-900 border border-amber-500/40 rounded-md transition-colors font-bold flex items-center gap-1 shadow-sm" onclick="navToTab('catalog', this)">🌐 300k+ Catalog</button>
        <button class="nav-btn px-3 py-2 text-emerald-300 hover:text-white bg-emerald-950/60 hover:bg-emerald-900 border border-emerald-500/40 rounded-md transition-colors font-bold flex items-center gap-1 shadow-sm" onclick="navToTab('futuresync', this)">🔄 Future Sync</button>"""

assert OLD_NAV_BUTTONS in html, "Could not find OLD_NAV_BUTTONS"
html = html.replace(OLD_NAV_BUTTONS, NEW_NAV_BUTTONS)

# 2. Main Tab Buttons Bar
OLD_TAB_BAR = """    <div class="flex bg-slate-200/80 p-1 rounded-lg border border-slate-300 self-start md:self-auto overflow-x-auto max-w-full">
      <button id="tab-btn-explorer" class="tab-trigger px-3.5 py-1.5 rounded-md text-xs font-semibold text-govNavy-900 bg-white shadow-sm whitespace-nowrap" onclick="switchGovTab('explorer')">National Data Explorer</button>
      <button id="tab-btn-catalog" class="tab-trigger px-3.5 py-1.5 rounded-md text-xs font-semibold text-amber-700 hover:text-amber-900 hover:bg-amber-50 whitespace-nowrap flex items-center gap-1 font-bold" onclick="switchGovTab('catalog')">🌐 Universal Gateway (300k+ Datasets)</button>
      <button id="tab-btn-futuresync" class="tab-trigger px-3.5 py-1.5 rounded-md text-xs font-semibold text-emerald-700 hover:text-emerald-900 hover:bg-emerald-50 whitespace-nowrap flex items-center gap-1 font-bold" onclick="switchGovTab('futuresync')">🔄 Future Auto-Sync</button>
      <button id="tab-btn-ai" class="tab-trigger px-3.5 py-1.5 rounded-md text-xs font-semibold text-purple-700 hover:text-purple-900 hover:bg-purple-50 whitespace-nowrap flex items-center gap-1 font-bold" onclick="switchGovTab('ai')">🤖 DataSetu AI Agent</button>
      <button id="tab-btn-directory" class="tab-trigger px-3.5 py-1.5 rounded-md text-xs font-semibold text-slate-600 hover:text-govNavy-900 whitespace-nowrap" onclick="switchGovTab('directory')">🏛️ Govt Sites Directory</button>
      <button id="tab-btn-sql" class="tab-trigger px-3.5 py-1.5 rounded-md text-xs font-semibold text-slate-600 hover:text-govNavy-900 whitespace-nowrap" onclick="switchGovTab('sql')">⚡ SQL Studio</button>
      <button id="tab-btn-disinfector" class="tab-trigger px-3.5 py-1.5 rounded-md text-xs font-semibold text-slate-600 hover:text-govNavy-900 whitespace-nowrap" onclick="switchGovTab('disinfector')">Data Disinfector</button>
      <button id="tab-btn-playground" class="tab-trigger px-3.5 py-1.5 rounded-md text-xs font-semibold text-slate-600 hover:text-govNavy-900 whitespace-nowrap" onclick="switchGovTab('playground')">Bharat API Playground</button>
      <button id="tab-btn-lgd" class="tab-trigger px-3.5 py-1.5 rounded-md text-xs font-semibold text-slate-600 hover:text-govNavy-900 whitespace-nowrap" onclick="switchGovTab('lgd')">LGD Directory</button>
    </div>"""

NEW_TAB_BAR = """    <div class="flex bg-slate-200/80 p-1 rounded-lg border border-slate-300 self-start md:self-auto overflow-x-auto max-w-full">
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

assert OLD_TAB_BAR in html, "Could not find OLD_TAB_BAR"
html = html.replace(OLD_TAB_BAR, NEW_TAB_BAR)

# 3. Add Polyglot SDK tabs inside #tab-pane-playground
OLD_PLAYGROUND_CLOSE = """        <div class="bg-govNavy-950 text-slate-200 p-4 rounded-lg font-mono text-xs overflow-x-auto max-h-[300px] custom-scrollbar border border-slate-800">
          <pre id="apiResponseOutput">{
  "meta": {
    "gateway": "NIC-Bharat-API-Gateway/2.4",
    "timestamp": "2026-10-31T02:06:31Z",
    "records_count": 5,
    "latency_ms": 1.18,
    "lgd_directory_version": "2026.1"
  },
  "data": [
    { "lgd_district_code": 556, "district_name_en": "Belagavi", "district_name_indic": "ಬೆಳಗಾವಿ", "state_code": "KA", "panchayats_count": 506 },
    { "lgd_district_code": 557, "district_name_en": "Ballari", "district_name_indic": "ಬಳ್ಳಾರಿ", "state_code": "KA", "panchayats_count": 198 },
    { "lgd_district_code": 558, "district_name_en": "Bengaluru Urban", "district_name_indic": "ಬೆಂಗಳೂರು ನಗರ", "state_code": "KA", "panchayats_count": 96 }
  ]
}</pre>
        </div>
      </div>
    </div>
  </div>"""

NEW_PLAYGROUND_CLOSE = """        <div class="bg-govNavy-950 text-slate-200 p-4 rounded-lg font-mono text-xs overflow-x-auto max-h-[300px] custom-scrollbar border border-slate-800">
          <pre id="apiResponseOutput">{
  "meta": {
    "gateway": "NIC-Bharat-API-Gateway/2.4",
    "timestamp": "2026-10-31T02:06:31Z",
    "records_count": 5,
    "latency_ms": 1.18,
    "lgd_directory_version": "2026.1"
  },
  "data": [
    { "lgd_district_code": 556, "district_name_en": "Belagavi", "district_name_indic": "ಬೆಳಗಾವಿ", "state_code": "KA", "panchayats_count": 506 },
    { "lgd_district_code": 557, "district_name_en": "Ballari", "district_name_indic": "ಬಳ್ಳಾರಿ", "state_code": "KA", "panchayats_count": 198 },
    { "lgd_district_code": 558, "district_name_en": "Bengaluru Urban", "district_name_indic": "ಬೆಂಗಳೂರು ನಗರ", "state_code": "KA", "panchayats_count": 96 }
  ]
}</pre>
        </div>
      </div>

      <!-- Native Polyglot SDK Generator -->
      <div class="mt-6 border-t border-slate-200 pt-5">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-3">
          <div>
            <h4 class="text-base font-bold text-govNavy-900 flex items-center gap-2">
              <span>💻</span> Native Polyglot Client SDKs (Zero Build Overhead)
            </h4>
            <p class="text-xs text-slate-500">Production-ready, type-safe API clients generated directly from the live OpenAPI 3.1 specification.</p>
          </div>
          <div class="flex items-center gap-1 bg-slate-100 p-1 rounded-lg border border-slate-200 text-xs font-semibold">
            <button id="sdk-tab-ts" class="sdk-tab-btn px-3 py-1 rounded bg-white text-govNavy-900 shadow-xs" onclick="switchSdkTab('ts')">TypeScript / Node.js</button>
            <button id="sdk-tab-go" class="sdk-tab-btn px-3 py-1 rounded text-slate-600 hover:text-slate-900" onclick="switchSdkTab('go')">Go</button>
            <button id="sdk-tab-py" class="sdk-tab-btn px-3 py-1 rounded text-slate-600 hover:text-slate-900" onclick="switchSdkTab('py')">Python</button>
            <button id="sdk-tab-curl" class="sdk-tab-btn px-3 py-1 rounded text-slate-600 hover:text-slate-900" onclick="switchSdkTab('curl')">cURL</button>
          </div>
        </div>

        <div class="relative bg-slate-950 rounded-lg p-4 font-mono text-xs text-slate-200 border border-slate-800">
          <div class="flex items-center justify-between pb-2 mb-2 border-b border-slate-800 text-[11px] text-slate-400">
            <span id="sdkFileNameBadge" class="text-amber-300 font-bold">dataSetuClient.ts</span>
            <div class="flex items-center gap-2">
              <button class="bg-slate-800 hover:bg-slate-700 text-slate-200 px-2.5 py-1 rounded transition text-[11px]" onclick="copySdkCode()">Copy Code</button>
              <button class="bg-govNavy-800 hover:bg-govNavy-700 text-amber-300 font-bold px-3 py-1 rounded transition text-[11px] flex items-center gap-1" onclick="downloadSdkFile()">
                <span>⬇️ Download Client SDK</span>
              </button>
            </div>
          </div>
          <pre id="sdkCodeOutput" class="max-h-[260px] overflow-y-auto custom-scrollbar">// Loading SDK code...</pre>
        </div>
      </div>
    </div>
  </div>"""

assert OLD_PLAYGROUND_CLOSE in html, "Could not find OLD_PLAYGROUND_CLOSE"
html = html.replace(OLD_PLAYGROUND_CLOSE, NEW_PLAYGROUND_CLOSE)

# 4. Vernacular Voice & Audio enhancements in #tab-pane-ai
OLD_AI_INPUT = """      <!-- Prompt Input Bar -->
      <div class="mt-6 flex flex-col sm:flex-row gap-2">
        <div class="relative flex-grow">
          <input
            id="aiQueryInput"
            type="text"
            class="w-full pl-11 pr-4 py-3.5 rounded-lg bg-slate-950/85 border border-purple-400/50 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-purple-400 font-medium text-sm shadow-inner"
            placeholder="Ask anything: e.g. 'Top 10 districts by PM-KISAN in UP', 'Show tap water in Bihar', 'MGNREGA wages in Maharashtra'..."
            value="Which districts in Uttar Pradesh have the highest PM-KISAN funds?"
            onkeydown="if(event.key === 'Enter') runAiQuery();"
          />
          <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-purple-300">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
          </div>
        </div>
        <button
          id="btnRunAi"
          class="bg-gradient-to-r from-amber-500 to-saffron hover:from-amber-600 hover:to-orange-600 text-govNavy-900 font-bold px-6 py-3.5 rounded-lg flex items-center justify-center gap-2 transition shadow-lg shrink-0 active:scale-95"
          onclick="runAiQuery()"
        >
          <span>Ask DataSetu AI</span>
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
        </button>
      </div>"""

NEW_AI_INPUT = """      <!-- Vernacular Multilingual Language Pills -->
      <div class="mt-4 flex items-center gap-2 flex-wrap text-xs">
        <span class="text-purple-300 font-semibold mr-1">Query Language (भाषिणी AI):</span>
        <button class="ai-lang-pill px-2.5 py-1 rounded-full font-bold bg-amber-400 text-slate-950 shadow-xs" onclick="setAiLanguage('en', this)">English</button>
        <button class="ai-lang-pill px-2.5 py-1 rounded-full font-bold bg-white/10 hover:bg-white/20 text-purple-200 border border-white/20 font-devanagari" onclick="setAiLanguage('hi', this)">हिन्दी</button>
        <button class="ai-lang-pill px-2.5 py-1 rounded-full font-bold bg-white/10 hover:bg-white/20 text-purple-200 border border-white/20" onclick="setAiLanguage('pa', this)">ਪੰਜਾਬੀ</button>
        <button class="ai-lang-pill px-2.5 py-1 rounded-full font-bold bg-white/10 hover:bg-white/20 text-purple-200 border border-white/20 font-devanagari" onclick="setAiLanguage('mr', this)">मराठी</button>
        <button class="ai-lang-pill px-2.5 py-1 rounded-full font-bold bg-white/10 hover:bg-white/20 text-purple-200 border border-white/20" onclick="setAiLanguage('bn', this)">বাংলা</button>
        <button class="ai-lang-pill px-2.5 py-1 rounded-full font-bold bg-white/10 hover:bg-white/20 text-purple-200 border border-white/20" onclick="setAiLanguage('ta', this)">தமிழ்</button>
        <button class="ai-lang-pill px-2.5 py-1 rounded-full font-bold bg-white/10 hover:bg-white/20 text-purple-200 border border-white/20" onclick="setAiLanguage('te', this)">తెలుగు</button>
      </div>

      <!-- Prompt Input Bar with Web Speech API Mic -->
      <div class="mt-3 flex flex-col sm:flex-row gap-2">
        <div class="relative flex-grow">
          <input
            id="aiQueryInput"
            type="text"
            class="w-full pl-11 pr-14 py-3.5 rounded-lg bg-slate-950/85 border border-purple-400/50 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-purple-400 font-medium text-sm shadow-inner"
            placeholder="Ask anything: e.g. 'Top 10 districts by PM-KISAN in UP', 'Show tap water in Bihar', 'MGNREGA wages in Maharashtra'..."
            value="Which districts in Uttar Pradesh have the highest PM-KISAN funds?"
            onkeydown="if(event.key === 'Enter') runAiQuery();"
          />
          <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-purple-300">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
          </div>
          <!-- Voice Microphone Button -->
          <button
            id="btnAiVoiceMic"
            type="button"
            class="absolute inset-y-1.5 right-1.5 px-3 rounded-md bg-purple-900/60 hover:bg-purple-800 text-purple-200 border border-purple-500/30 flex items-center justify-center transition active:scale-95"
            onclick="toggleVoiceRecognition()"
            title="Click to speak (Voice Recognition in English, Hindi, Punjabi, Marathi)"
          >
            <span id="voiceMicIcon" class="text-base">🎙️</span>
          </button>
        </div>
        <button
          id="btnRunAi"
          class="bg-gradient-to-r from-amber-500 to-saffron hover:from-amber-600 hover:to-orange-600 text-govNavy-900 font-bold px-6 py-3.5 rounded-lg flex items-center justify-center gap-2 transition shadow-lg shrink-0 active:scale-95"
          onclick="runAiQuery()"
        >
          <span>Ask DataSetu AI</span>
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
        </button>
      </div>"""

assert OLD_AI_INPUT in html, "Could not find OLD_AI_INPUT"
html = html.replace(OLD_AI_INPUT, NEW_AI_INPUT)

# 5. Insert the 4 New Tab Panes before </main>
NEW_TAB_PANES = """
  <!-- TAB PANE 1: 🗺️ Bharat Geospatial Map & District Choropleth -->
  <div id="tab-pane-map" class="tab-content hidden space-y-6">
    <!-- Header Banner -->
    <div class="bg-gradient-to-r from-sky-950 via-slate-900 to-govNavy-950 text-white rounded-xl p-6 border-2 border-sky-500/40 shadow-xl relative overflow-hidden">
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div class="flex items-center gap-2 mb-2 flex-wrap">
            <span class="bg-sky-500/30 border border-sky-400 text-sky-200 text-[11px] font-bold px-2.5 py-0.5 rounded-full uppercase tracking-wider flex items-center gap-1">
              <span>🗺️</span> Pan-India Geospatial Choropleth • LGD Harmonized
            </span>
            <span class="bg-emerald-500/30 text-emerald-300 text-[11px] font-bold px-2 py-0.5 rounded-full">
              738+ Active Districts • 36 States/UTs
            </span>
          </div>
          <h3 class="text-2xl font-extrabold tracking-tight">Bharat Interactive Geospatial GIS &amp; Choropleth Engine</h3>
          <p class="text-sky-200 text-sm mt-1 max-w-3xl leading-relaxed">
            Real-time vectorized geospatial visualization of fiscal outlays, actual expenditures, citizen beneficiaries, and statutory LGD matching integrity across all 36 States and Union Territories.
          </p>
        </div>
        <div class="bg-white/10 backdrop-blur rounded-lg p-3 text-right hidden sm:block border border-white/10 shrink-0">
          <div class="text-xs text-sky-200 font-medium">GIS GeoJSON Endpoint</div>
          <div class="text-base font-mono font-bold text-amber-300">GET /v1/geojson</div>
          <div class="text-[10px] text-sky-300">RFC 7946 Standard • Leaflet/Mapbox Ready</div>
        </div>
      </div>

      <!-- Metric Selector & Quick Controls -->
      <div class="mt-6 flex flex-wrap items-center justify-between gap-4 border-t border-sky-800/60 pt-4">
        <div class="flex items-center gap-2 flex-wrap text-xs">
          <span class="text-sky-300 font-bold uppercase tracking-wider">Choropleth Heatmap Metric:</span>
          <button id="map-metric-alloc" class="map-metric-btn px-3 py-1.5 rounded font-bold bg-sky-500 text-slate-950 transition" onclick="setMapMetric('allocation')">Central Sanctioned (INR)</button>
          <button id="map-metric-spend" class="map-metric-btn px-3 py-1.5 rounded font-bold bg-sky-950/70 text-sky-200 hover:bg-sky-800 border border-sky-600/40 transition" onclick="setMapMetric('expenditure')">Actual Expenditure (INR)</button>
          <button id="map-metric-bene" class="map-metric-btn px-3 py-1.5 rounded font-bold bg-sky-950/70 text-sky-200 hover:bg-sky-800 border border-sky-600/40 transition" onclick="setMapMetric('beneficiaries')">Citizen Beneficiaries</button>
          <button id="map-metric-count" class="map-metric-btn px-3 py-1.5 rounded font-bold bg-sky-950/70 text-sky-200 hover:bg-sky-800 border border-sky-600/40 transition" onclick="setMapMetric('count')">Ingested Records Count</button>
        </div>
        <div class="text-xs text-slate-300 flex items-center gap-2">
          <span class="inline-block w-3 h-3 rounded-full bg-emerald-400 live-pulse"></span>
          <span>Vectorized In-Memory Aggregation</span>
        </div>
      </div>
    </div>

    <!-- Map Viewport & State Leaderboard Split -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
      <!-- Left: Interactive Map Visualization Container -->
      <div class="lg:col-span-8 bg-white rounded-xl shadow-md border border-slate-200 p-5 space-y-4">
        <div class="flex items-center justify-between border-b border-slate-100 pb-3 flex-wrap gap-2">
          <div>
            <h4 class="text-base font-bold text-govNavy-900 flex items-center gap-2">
              <span>🇮🇳</span> National Choropleth Map (State/UT Level)
            </h4>
            <p class="text-xs text-slate-500">Hover over any state to inspect live metrics. Click to filter National Data Explorer.</p>
          </div>
          <div class="flex items-center gap-2 text-xs">
            <span class="text-slate-400">Scale:</span>
            <div class="flex items-center gap-1 font-mono text-[10px]">
              <span class="w-3 h-3 rounded bg-sky-100 border border-slate-200"></span> <span>Low</span>
              <span class="w-3 h-3 rounded bg-sky-300"></span>
              <span class="w-3 h-3 rounded bg-sky-600"></span>
              <span class="w-3 h-3 rounded bg-govNavy-900"></span> <span>High</span>
            </div>
          </div>
        </div>

        <!-- SVG Map Container with Interactive State Cards & Dynamic Choropleth -->
        <div class="relative bg-slate-900 rounded-lg p-5 border border-slate-800 min-h-[480px] flex flex-col justify-between overflow-hidden">
          <div id="mapTooltip" class="absolute hidden z-20 pointer-events-none bg-slate-900/95 text-white border border-sky-400/60 p-3 rounded-lg shadow-2xl text-xs max-w-xs backdrop-blur">
            <!-- Populated via hover -->
          </div>

          <!-- Dynamic State Grid & Centroid Visualization -->
          <div id="indiaSvgWrapper" class="w-full my-auto py-2 grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3 max-h-[400px] overflow-y-auto custom-scrollbar p-2">
            <!-- Dynamically populated state choropleth cards with live metric scaling -->
          </div>

          <!-- Active Selected State Action Pill -->
          <div id="mapSelectedStateBar" class="bg-slate-800/90 border border-slate-700 rounded-lg p-3 flex items-center justify-between text-xs text-slate-200 mt-2">
            <div class="flex items-center gap-2">
              <span class="font-bold text-sky-400" id="mapHoverStateName">India National Summary</span>
              <span class="text-slate-400" id="mapHoverStateStats">36 States/UTs • 738 Active Districts</span>
            </div>
            <button id="mapBtnFilterState" class="bg-sky-600 hover:bg-sky-500 text-white font-bold px-3 py-1 rounded text-[11px] transition" onclick="filterExplorerFromMap()">
              Filter Explorer to this State &rarr;
            </button>
          </div>
        </div>
      </div>

      <!-- Right: Top States Ranking Leaderboard -->
      <div class="lg:col-span-4 bg-white rounded-xl shadow-md border border-slate-200 p-5 space-y-4 flex flex-col">
        <div class="border-b border-slate-100 pb-3 flex items-center justify-between">
          <h4 class="text-base font-bold text-govNavy-900 flex items-center gap-2">
            <span>🏆</span> State / UT Leaderboard
          </h4>
          <span class="text-xs font-mono font-bold text-sky-700" id="mapLeaderboardMetricTitle">Sanctioned Outlay</span>
        </div>

        <div id="mapLeaderboardList" class="divide-y divide-slate-100 overflow-y-auto max-h-[460px] custom-scrollbar flex-grow text-xs space-y-2 pr-1">
          <!-- Populated dynamically via JS -->
        </div>

        <div class="pt-3 border-t border-slate-100 text-[11px] text-slate-500 flex items-center justify-between">
          <span>Source: In-Memory DuckDB Engine</span>
          <button class="text-sky-700 hover:underline font-bold" onclick="switchGovTab('sql')">Run Custom GIS SQL &rarr;</button>
        </div>
      </div>
    </div>
  </div>

  <!-- TAB PANE 2: 🛡️ Civic Anomaly & Forensic Audit Engine -->
  <div id="tab-pane-audit" class="tab-content hidden space-y-6">
    <!-- Header Banner -->
    <div class="bg-gradient-to-r from-rose-950 via-slate-900 to-govNavy-950 text-white rounded-xl p-6 border-2 border-rose-500/50 shadow-xl relative overflow-hidden">
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div class="flex items-center gap-2 mb-2 flex-wrap">
            <span class="bg-rose-500/30 border border-rose-400 text-rose-200 text-[11px] font-bold px-2.5 py-0.5 rounded-full uppercase tracking-wider flex items-center gap-1">
              <span>🛡️</span> CAG Forensic Engine • Real-Time Anomaly Scanner
            </span>
            <span class="bg-amber-500/30 text-amber-300 text-[11px] font-bold px-2 py-0.5 rounded-full">
              Automated Fiscal Leakage &amp; Dormant Outlay Detection
            </span>
          </div>
          <h3 class="text-2xl font-extrabold tracking-tight">Civic Anomaly &amp; Forensic Audit Engine</h3>
          <p class="text-rose-200 text-sm mt-1 max-w-3xl leading-relaxed">
            Autonomous statutory monitoring modeled after the Comptroller and Auditor General (CAG) guidelines. Identifies expenditure leakages, unutilized idle funds, and low-beneficiary anomalies across all ministries.
          </p>
        </div>
        <div class="bg-white/10 backdrop-blur rounded-lg p-3 text-right hidden sm:block border border-white/10 shrink-0">
          <div class="text-xs text-rose-200 font-medium">Public Audit API</div>
          <div class="text-base font-mono font-bold text-amber-300">GET /v1/audit/anomalies</div>
          <div class="text-[10px] text-rose-300">Zero-Friction In-Memory Inspection</div>
        </div>
      </div>

      <!-- National Data Hygiene Score Meter & Summary Counters -->
      <div class="mt-6 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 border-t border-rose-800/60 pt-4">
        <div class="bg-white/10 rounded-lg p-3.5 backdrop-blur border border-white/10">
          <div class="text-xs text-rose-200 font-medium">National Civic Hygiene Score</div>
          <div class="flex items-baseline gap-2 mt-1">
            <span class="text-2xl font-black text-amber-300 font-mono" id="auditHygieneScore">--</span>
            <span class="text-xs text-rose-300">/ 100</span>
            <span class="bg-emerald-500/30 text-emerald-300 text-[10px] font-bold px-2 py-0.5 rounded font-mono" id="auditHygieneGrade">Grade A</span>
          </div>
          <div class="text-[11px] text-rose-300 mt-1" id="auditHygieneDesc">Evaluating data reliability...</div>
        </div>

        <div class="bg-white/10 rounded-lg p-3.5 backdrop-blur border border-white/10">
          <div class="text-xs text-rose-200 font-medium">Fiscal Overspend (Leakages)</div>
          <div class="text-2xl font-black text-rose-400 font-mono mt-1" id="auditLeakageCount">--</div>
          <div class="text-[11px] text-rose-300 mt-1" id="auditLeakageTotal">Total: -- Cr</div>
        </div>

        <div class="bg-white/10 rounded-lg p-3.5 backdrop-blur border border-white/10">
          <div class="text-xs text-rose-200 font-medium">Dormant Idle Funds (&lt;10% Spend)</div>
          <div class="text-2xl font-black text-amber-300 font-mono mt-1" id="auditDormantCount">--</div>
          <div class="text-[11px] text-rose-300 mt-1" id="auditDormantTotal">Total: -- Cr</div>
        </div>

        <div class="bg-white/10 rounded-lg p-3.5 backdrop-blur border border-white/10">
          <div class="text-xs text-rose-200 font-medium">Low Beneficiary Outliers</div>
          <div class="text-2xl font-black text-sky-300 font-mono mt-1" id="auditLowBeneCount">--</div>
          <div class="text-[11px] text-rose-300 mt-1" id="auditLowBeneTotal">&lt;100 beneficiaries flagged</div>
        </div>
      </div>
    </div>

    <!-- Anomaly Table and Filters -->
    <div class="bg-white rounded-xl shadow-md border border-slate-200 p-6 space-y-4">
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-100 pb-4">
        <div>
          <h4 class="text-base font-bold text-govNavy-900 flex items-center gap-2">
            <span>🚨</span> Flagged Audit Dossiers &amp; Forensic Findings
          </h4>
          <p class="text-xs text-slate-500 mt-0.5">Records filtered by statutory CAG audit thresholds. Click any row to inspect.</p>
        </div>

        <div class="flex items-center gap-2 flex-wrap text-xs">
          <button id="btn-audit-filter-all" class="px-3 py-1.5 rounded font-bold bg-govNavy-900 text-white transition" onclick="filterAuditAnomalies('ALL')">All Anomalies</button>
          <button id="btn-audit-filter-leakage" class="px-3 py-1.5 rounded font-bold bg-slate-100 text-slate-700 hover:bg-slate-200 transition" onclick="filterAuditAnomalies('FISCAL_OVERSPEND')">Fiscal Overspend</button>
          <button id="btn-audit-filter-dormant" class="px-3 py-1.5 rounded font-bold bg-slate-100 text-slate-700 hover:bg-slate-200 transition" onclick="filterAuditAnomalies('DORMANT_FUNDS')">Dormant Funds</button>
          <button id="btn-audit-filter-bene" class="px-3 py-1.5 rounded font-bold bg-slate-100 text-slate-700 hover:bg-slate-200 transition" onclick="filterAuditAnomalies('LOW_BENEFICIARY_OUTLIER')">Low Beneficiaries</button>
          <button class="bg-rose-600 hover:bg-rose-700 text-white font-bold px-3 py-1.5 rounded flex items-center gap-1 transition shadow-sm active:scale-95" onclick="exportAuditCsv()">
            <span>⬇️ Export CAG CSV</span>
          </button>
        </div>
      </div>

      <!-- Table -->
      <div class="overflow-x-auto">
        <table class="min-w-full text-left text-xs">
          <thead class="bg-slate-100 border-b border-slate-200 text-slate-700 font-bold uppercase text-[11px]">
            <tr>
              <th class="py-3 px-4">Severity / Anomaly Type</th>
              <th class="py-3 px-4">District &amp; State</th>
              <th class="py-3 px-4">Scheme &amp; Sector</th>
              <th class="py-3 px-4 text-right">Sanctioned Outlay</th>
              <th class="py-3 px-4 text-right">Actual Spend</th>
              <th class="py-3 px-4 text-right">Variance (Gap)</th>
              <th class="py-3 px-4">Forensic Risk Finding</th>
              <th class="py-3 px-4 text-right">Actions</th>
            </tr>
          </thead>
          <tbody id="auditAnomaliesTableBody" class="divide-y divide-slate-100 font-medium">
            <tr>
              <td colspan="8" class="py-8 text-center text-slate-400">Loading live civic audit anomalies from DuckDB engine...</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- TAB PANE 3: 🔗 Cross-Ministerial Dataset Correlator -->
  <div id="tab-pane-correlator" class="tab-content hidden space-y-6">
    <!-- Header Banner -->
    <div class="bg-gradient-to-r from-indigo-950 via-slate-900 to-govNavy-950 text-white rounded-xl p-6 border-2 border-indigo-500/40 shadow-xl relative overflow-hidden">
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div class="flex items-center gap-2 mb-2 flex-wrap">
            <span class="bg-indigo-500/30 border border-indigo-400 text-indigo-200 text-[11px] font-bold px-2.5 py-0.5 rounded-full uppercase tracking-wider flex items-center gap-1">
              <span>🔗</span> Statutory Local Government Directory (LGD) Cross-Join
            </span>
            <span class="bg-emerald-500/30 text-emerald-300 text-[11px] font-bold px-2 py-0.5 rounded-full">
              Sub-Millisecond Multi-Table DuckDB JOINs
            </span>
          </div>
          <h3 class="text-2xl font-extrabold tracking-tight">Cross-Ministerial Dataset Correlator</h3>
          <p class="text-indigo-200 text-sm mt-1 max-w-3xl leading-relaxed">
            Eliminates ministerial data silos. By using statutory 782-district LGD codes as canonical foreign keys, DataSetu joins disparate departmental data in real-time, computing Pearson correlation $r$ and automated policy impact synthesis.
          </p>
        </div>
        <div class="bg-white/10 backdrop-blur rounded-lg p-3 text-right hidden sm:block border border-white/10 shrink-0">
          <div class="text-xs text-indigo-200 font-medium">Correlation API</div>
          <div class="text-base font-mono font-bold text-amber-300">GET /v1/correlate</div>
          <div class="text-[10px] text-indigo-300">Sub-Millisecond In-Memory JOIN</div>
        </div>
      </div>

      <!-- Controls: Dataset X vs Dataset Y -->
      <div class="mt-6 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-3 border-t border-indigo-800/60 pt-4 text-xs">
        <div>
          <label class="block text-indigo-200 font-semibold mb-1">Primary Sector (Dataset X)</label>
          <select id="corrDatasetX" class="w-full bg-slate-900 border border-indigo-400/50 text-white rounded p-2 focus:ring-1 focus:ring-indigo-400 text-xs">
            <option value="road_transport" selected>🚗 Road Transport &amp; Highways</option>
            <option value="agriculture">🌾 Agriculture &amp; Farmers Welfare</option>
            <option value="rural_development">🛠️ Rural Development</option>
            <option value="health">🏥 Health &amp; Family Welfare</option>
            <option value="power_energy">☀️ Power &amp; Energy</option>
          </select>
        </div>
        <div>
          <label class="block text-indigo-200 font-semibold mb-1">Metric X</label>
          <select id="corrMetricX" class="w-full bg-slate-900 border border-indigo-400/50 text-white rounded p-2 focus:ring-1 focus:ring-indigo-400 text-xs">
            <option value="allocation" selected>Central Allocation (INR)</option>
            <option value="expenditure">Actual Expenditure (INR)</option>
            <option value="beneficiaries">Beneficiaries Reached</option>
          </select>
        </div>
        <div>
          <label class="block text-indigo-200 font-semibold mb-1">Secondary Sector (Dataset Y)</label>
          <select id="corrDatasetY" class="w-full bg-slate-900 border border-indigo-400/50 text-white rounded p-2 focus:ring-1 focus:ring-indigo-400 text-xs">
            <option value="rural_development" selected>🛠️ Rural Development</option>
            <option value="road_transport">🚗 Road Transport &amp; Highways</option>
            <option value="agriculture">🌾 Agriculture &amp; Farmers Welfare</option>
            <option value="health">🏥 Health &amp; Family Welfare</option>
            <option value="power_energy">☀️ Power &amp; Energy</option>
          </select>
        </div>
        <div>
          <label class="block text-indigo-200 font-semibold mb-1">Metric Y</label>
          <select id="corrMetricY" class="w-full bg-slate-900 border border-indigo-400/50 text-white rounded p-2 focus:ring-1 focus:ring-indigo-400 text-xs">
            <option value="beneficiaries" selected>Beneficiaries Reached</option>
            <option value="allocation">Central Allocation (INR)</option>
            <option value="expenditure">Actual Expenditure (INR)</option>
          </select>
        </div>
        <div class="flex items-end">
          <button class="w-full bg-gradient-to-r from-indigo-500 to-indigo-600 hover:from-indigo-600 hover:to-indigo-700 text-white font-bold py-2 rounded text-xs transition shadow-sm active:scale-95" onclick="runCorrelator()">
            Compute LGD Correlation &rarr;
          </button>
        </div>
      </div>
    </div>

    <!-- Results Banner: Correlation Badge + Automated Policy Insight -->
    <div id="correlatorResultsCard" class="bg-white rounded-xl shadow-md border border-slate-200 p-6 space-y-4">
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-100 pb-4">
        <div class="flex items-center gap-3">
          <div class="bg-indigo-50 border border-indigo-200 rounded-lg p-3 text-center min-w-[120px]">
            <div class="text-[10px] uppercase font-bold text-indigo-700">Pearson r</div>
            <div class="text-2xl font-black font-mono text-indigo-900" id="corrValue">--</div>
            <div class="text-[10px] font-bold text-emerald-700" id="corrDirection">--</div>
          </div>
          <div>
            <span class="bg-indigo-100 text-indigo-800 text-xs font-bold px-2.5 py-0.5 rounded-full" id="corrStrengthBadge">Calculating...</span>
            <h4 class="text-base font-bold text-govNavy-900 mt-1" id="corrHeading">Cross-Ministerial Alignment</h4>
            <p class="text-xs text-slate-500" id="corrSampleSize">Matched Sample Size: -- districts via LGD directory</p>
          </div>
        </div>
        <div class="text-right">
          <span class="text-xs font-mono text-slate-400" id="corrLatency">Latency: -- ms</span>
        </div>
      </div>

      <!-- Policy Narrative Synthesis -->
      <div class="bg-slate-50 rounded-lg p-4 border border-slate-200">
        <div class="text-xs font-bold text-slate-700 flex items-center gap-1.5 mb-1">
          <span>💡</span> Automated Civic Policy Synthesis
        </div>
        <p class="text-xs text-slate-600 leading-relaxed font-sans" id="corrPolicyInsight">
          Select two ministerial datasets above and click "Compute LGD Correlation" to perform an in-memory cross-table DuckDB join.
        </p>
      </div>

      <!-- Interactive Scatter Plot HTML5 Canvas -->
      <div class="border border-slate-200 rounded-lg p-4 bg-slate-900 text-slate-200">
        <div class="flex items-center justify-between mb-2">
          <span class="text-xs font-bold text-sky-400 font-mono">LGD District Multi-Table Scatter Matrix</span>
          <span class="text-[10px] text-slate-400 font-mono">Hover points to view district LGD keys</span>
        </div>
        <div class="w-full flex items-center justify-center">
          <canvas id="correlatorCanvas" width="800" height="320" class="w-full max-h-[320px] rounded"></canvas>
        </div>
      </div>
    </div>
  </div>

  <!-- TAB PANE 4: ⚡ Event-Driven Webhooks & Change Notification Simulator -->
  <div id="tab-pane-webhooks" class="tab-content hidden space-y-6">
    <!-- Header Banner -->
    <div class="bg-gradient-to-r from-amber-950 via-slate-900 to-govNavy-950 text-white rounded-xl p-6 border-2 border-amber-500/40 shadow-xl relative overflow-hidden">
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div class="flex items-center gap-2 mb-2 flex-wrap">
            <span class="bg-amber-500/30 border border-amber-400 text-amber-200 text-[11px] font-bold px-2.5 py-0.5 rounded-full uppercase tracking-wider flex items-center gap-1">
              <span>⚡</span> HMAC-SHA256 Signed • Zero-Polling Webhooks
            </span>
            <span class="bg-emerald-500/30 text-emerald-300 text-[11px] font-bold px-2 py-0.5 rounded-full">
              Event-Driven Civic Architecture
            </span>
          </div>
          <h3 class="text-2xl font-extrabold tracking-tight">Event-Driven Webhook Dispatch &amp; Notification Engine</h3>
          <p class="text-amber-200 text-sm mt-1 max-w-3xl leading-relaxed">
            Eliminates costly periodic polling. Subscribe downstream municipal systems, civic dashboards, or third-party apps to instant notifications whenever new dataset versions are synced, LGD codes are reconciled, or audit leakages are detected.
          </p>
        </div>
        <div class="bg-white/10 backdrop-blur rounded-lg p-3 text-right hidden sm:block border border-white/10 shrink-0">
          <div class="text-xs text-amber-200 font-medium">Subscriptions Endpoint</div>
          <div class="text-base font-mono font-bold text-amber-300">POST /v1/webhooks/subscribe</div>
          <div class="text-[10px] text-amber-300">Cryptographically Signed via SHA-256</div>
        </div>
      </div>
    </div>

    <!-- Webhook Registration Form and Active List Split -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
      <!-- Left: Register New Webhook -->
      <div class="lg:col-span-5 bg-white rounded-xl shadow-md border border-slate-200 p-6 space-y-4">
        <h4 class="text-base font-bold text-govNavy-900 flex items-center gap-2">
          <span>➕</span> Register Webhook Endpoint
        </h4>
        <form onsubmit="event.preventDefault(); submitWebhookSubscription();" class="space-y-3 text-xs">
          <div>
            <label class="block text-slate-700 font-semibold mb-1">Target Callback URL</label>
            <input id="webhookTargetUrl" type="url" required class="w-full border-slate-300 rounded p-2 text-xs font-mono" placeholder="https://api.mycivicapp.org/webhooks/datasetu" />
          </div>
          <div>
            <label class="block text-slate-700 font-semibold mb-1">Subscribed Event Types</label>
            <select id="webhookEventType" class="w-full border-slate-300 rounded p-2 text-xs">
              <option value="cdc.mutation">cdc.mutation (Data Updates &amp; Incremental Ingestion)</option>
              <option value="audit.leakage_detected">audit.leakage_detected (CAG Civic Audit Overspend)</option>
              <option value="district.anomaly">district.anomaly (Low Beneficiary Outlier)</option>
              <option value="*">* (All National Events)</option>
            </select>
          </div>
          <div>
            <label class="block text-slate-700 font-semibold mb-1">Secret Key (for HMAC Signature)</label>
            <input id="webhookSecret" type="text" class="w-full border-slate-300 rounded p-2 text-xs font-mono" placeholder="whsec_bharat_sandbox_key_2026" value="whsec_bharat_sandbox_key_2026" />
          </div>
          <button type="submit" class="w-full bg-govNavy-900 hover:bg-govNavy-800 text-white font-bold py-2.5 rounded text-xs transition">
            Save Webhook Subscription
          </button>
        </form>

        <!-- Active Subscriptions -->
        <div class="border-t border-slate-100 pt-3">
          <div class="flex items-center justify-between mb-2">
            <span class="text-xs font-bold text-slate-700">Active Subscriptions</span>
            <span class="text-[10px] bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-mono" id="webhookSubCountBadge">0 registered</span>
          </div>
          <div id="webhookSubscriptionsList" class="space-y-2 max-h-48 overflow-y-auto custom-scrollbar">
            <!-- Populated via JS -->
          </div>
        </div>
      </div>

      <!-- Right: Live Webhook Dispatch Simulator -->
      <div class="lg:col-span-7 bg-white rounded-xl shadow-md border border-slate-200 p-6 space-y-4">
        <div class="border-b border-slate-100 pb-3 flex items-center justify-between flex-wrap gap-2">
          <div>
            <h4 class="text-base font-bold text-govNavy-900 flex items-center gap-2">
              <span>🧪</span> Real-Time Webhook Simulator &amp; HMAC Inspector
            </h4>
            <p class="text-xs text-slate-500">Simulate an upstream government update and verify HMAC-SHA256 signature payloads.</p>
          </div>
          <button class="bg-amber-600 hover:bg-amber-700 text-white font-bold px-3 py-1.5 rounded text-xs transition flex items-center gap-1 active:scale-95" onclick="simulateWebhookDispatch()">
            <span>🚀 Dispatch Event</span>
          </button>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
          <div>
            <label class="block text-slate-600 font-semibold mb-1">Simulate Event</label>
            <select id="simEventType" class="w-full border-slate-300 rounded p-2 text-xs">
              <option value="cdc.mutation">cdc.mutation (New Road Transport Outlay)</option>
              <option value="audit.leakage_detected">audit.leakage_detected (CAG Fiscal Leakage Flag)</option>
              <option value="district.anomaly">district.anomaly (Low Beneficiary Flag)</option>
            </select>
          </div>
          <div>
            <label class="block text-slate-600 font-semibold mb-1">Simulate District</label>
            <select id="simDistrict" class="w-full border-slate-300 rounded p-2 text-xs">
              <option value="Amritsar, Punjab">Amritsar (Punjab • LGD: 30)</option>
              <option value="Varanasi, Uttar Pradesh">Varanasi (Uttar Pradesh • LGD: 198)</option>
              <option value="Pune, Maharashtra">Pune (Maharashtra • LGD: 492)</option>
              <option value="Patna, Bihar">Patna (Bihar • LGD: 231)</option>
            </select>
          </div>
        </div>

        <!-- Simulation Output Inspector -->
        <div class="space-y-2">
          <div class="flex items-center justify-between text-xs">
            <span class="font-bold text-slate-700">Simulated HTTP Request Headers</span>
            <span id="simStatusBadge" class="bg-slate-100 text-slate-600 font-mono text-[10px] px-2 py-0.5 rounded">Ready to dispatch</span>
          </div>
          <div class="bg-slate-950 text-emerald-400 p-3 rounded-lg font-mono text-[11px] overflow-x-auto border border-slate-800 space-y-1">
            <div><span class="text-slate-400">Content-Type:</span> application/json</div>
            <div><span class="text-slate-400">X-DataSetu-Event:</span> <span id="simHdrEvent" class="text-amber-300">cdc.mutation</span></div>
            <div><span class="text-slate-400">X-DataSetu-Delivery:</span> <span id="simHdrDelivery" class="text-sky-300">del_89b2f34</span></div>
            <div class="break-all"><span class="text-slate-400">X-DataSetu-Signature:</span> <span id="simHdrSig" class="text-amber-400 font-bold">sha256=...</span></div>
          </div>

          <div class="flex items-center justify-between text-xs pt-2">
            <span class="font-bold text-slate-700">Dispatched JSON Payload</span>
            <button class="text-govRed hover:underline text-[11px] font-semibold" onclick="copySimPayload()">Copy JSON</button>
          </div>
          <div class="bg-slate-950 text-slate-200 p-3 rounded-lg font-mono text-[11px] overflow-x-auto max-h-48 border border-slate-800">
            <pre id="simPayloadJson">// Click "Dispatch Event" above to fire an instant HMAC-signed webhook event</pre>
          </div>
        </div>
      </div>
    </div>
  </div>
"""

TARGET_MAIN_CLOSE = "  </main>"
assert TARGET_MAIN_CLOSE in html, "Could not find </main>"
html = html.replace(TARGET_MAIN_CLOSE, NEW_TAB_PANES + "\n  </main>")

# 6. Insert JavaScript Logic for the new features
JS_NEW_LOGIC = """
// ==========================================
// FEATURE 1: 🗺️ Bharat Geospatial Map & Choropleth
// ==========================================
let currentMapMetric = 'allocation';
let mapStatesData = [];
let selectedMapState = null;

async function loadMapChoropleth(metric = currentMapMetric) {
  currentMapMetric = metric;
  const wrapper = document.getElementById('indiaSvgWrapper');
  const lbList = document.getElementById('mapLeaderboardList');
  const lbTitle = document.getElementById('mapLeaderboardMetricTitle');
  if (!wrapper) return;

  if (lbTitle) {
    if (metric === 'allocation') lbTitle.innerText = 'Sanctioned Outlay';
    else if (metric === 'expenditure') lbTitle.innerText = 'Actual Spend';
    else if (metric === 'beneficiaries') lbTitle.innerText = 'Beneficiaries';
    else lbTitle.innerText = 'Records Count';
  }

  try {
    let metricParam = 'sum:allocation';
    if (metric === 'expenditure') metricParam = 'sum:expenditure';
    else if (metric === 'beneficiaries') metricParam = 'sum:beneficiaries';
    else if (metric === 'count') metricParam = 'count:allocation';

    const resp = await fetch(`/v1/data/summary?group_by=state&metric=${metricParam}`);
    const data = await resp.json();
    mapStatesData = (data.grouped || []).map(g => ({
      state: g.group,
      val: Number(g.metric) || 0
    })).filter(g => g.state && g.state !== 'All India');

    renderMapChoroplethCards();
  } catch (err) {
    console.error('Failed to load map choropleth:', err);
    if (wrapper) {
      wrapper.innerHTML = `<div class="col-span-full py-8 text-center text-rose-400 font-mono text-xs">Failed to load geospatial stats: ${escapeHtml(err.message)}</div>`;
    }
  }
}

function setMapMetric(m) {
  currentMapMetric = m;
  document.querySelectorAll('.map-metric-btn').forEach(b => {
    b.className = 'map-metric-btn px-3 py-1.5 rounded font-bold bg-sky-950/70 text-sky-200 hover:bg-sky-800 border border-sky-600/40 transition';
  });
  const activeBtn = document.getElementById(`map-metric-${m.slice(0, 4)}`);
  if (activeBtn) {
    activeBtn.className = 'map-metric-btn px-3 py-1.5 rounded font-bold bg-sky-500 text-slate-950 transition';
  }
  loadMapChoropleth(m);
}

function renderMapChoroplethCards() {
  const wrapper = document.getElementById('indiaSvgWrapper');
  const lbList = document.getElementById('mapLeaderboardList');
  if (!wrapper || !mapStatesData.length) return;

  const maxVal = Math.max(...mapStatesData.map(d => d.val), 1);

  // Render visual cards
  wrapper.innerHTML = mapStatesData.map(d => {
    const pct = Math.round((d.val / maxVal) * 100);
    let bgShade = 'bg-slate-800 hover:bg-slate-700';
    let textShade = 'text-sky-300';
    if (pct > 75) { bgShade = 'bg-sky-950/90 border-sky-400 hover:bg-sky-900'; textShade = 'text-amber-300'; }
    else if (pct > 40) { bgShade = 'bg-slate-800/90 border-sky-600/40 hover:bg-slate-700'; textShade = 'text-sky-200'; }

    let valDisplay = currentMapMetric === 'count'
      ? `${formatNumber(d.val)} rows`
      : currentMapMetric === 'beneficiaries'
        ? `${formatNumber(d.val)} Citizens`
        : formatIndianCurrency(d.val);

    return `
      <div 
        class="border rounded-lg p-2.5 transition cursor-pointer select-none ${bgShade} border-slate-700 flex flex-col justify-between"
        onclick="selectStateOnMap('${escapeHtml(d.state)}', '${valDisplay}')"
      >
        <div class="flex items-start justify-between gap-1">
          <span class="font-bold text-xs text-white truncate">${escapeHtml(d.state)}</span>
          <span class="text-[10px] font-mono text-slate-400">${pct}%</span>
        </div>
        <div class="mt-2">
          <div class="text-[11px] font-mono font-bold ${textShade}">${valDisplay}</div>
          <div class="w-full bg-slate-700/60 h-1.5 rounded-full mt-1.5 overflow-hidden">
            <div class="bg-gradient-to-r from-sky-500 to-amber-400 h-full rounded-full" style="width: ${Math.max(5, pct)}%"></div>
          </div>
        </div>
      </div>
    `;
  }).join('');

  // Render Leaderboard
  if (lbList) {
    lbList.innerHTML = mapStatesData.slice(0, 15).map((d, idx) => {
      let valDisplay = currentMapMetric === 'count'
        ? `${formatNumber(d.val)} recs`
        : currentMapMetric === 'beneficiaries'
          ? `${formatNumber(d.val)}`
          : formatIndianCurrency(d.val);

      return `
        <div class="py-2 flex items-center justify-between hover:bg-slate-50 px-2 rounded cursor-pointer transition" onclick="selectStateOnMap('${escapeHtml(d.state)}', '${valDisplay}')">
          <div class="flex items-center gap-2">
            <span class="font-mono text-[11px] font-bold ${idx < 3 ? 'text-amber-500' : 'text-slate-400'} w-4">#${idx + 1}</span>
            <span class="font-medium text-slate-800">${escapeHtml(d.state)}</span>
          </div>
          <span class="font-mono font-bold text-govNavy-900 text-xs">${valDisplay}</span>
        </div>
      `;
    }).join('');
  }
}

function selectStateOnMap(stateName, valDisplay) {
  selectedMapState = stateName;
  const nameEl = document.getElementById('mapHoverStateName');
  const statsEl = document.getElementById('mapHoverStateStats');
  if (nameEl) nameEl.innerText = stateName;
  if (statsEl) statsEl.innerText = `${currentMapMetric.toUpperCase()}: ${valDisplay} • Click to filter National Explorer`;
  showToast('State Selected', `Selected ${stateName}. Click "Filter Explorer to this State" to view all records.`, 'info');
}

function filterExplorerFromMap() {
  if (!selectedMapState) {
    showToast('Select State', 'Please click on any state in the map or leaderboard first.', 'warning');
    return;
  }
  const stateSel = document.getElementById('stateFilter');
  if (stateSel) {
    stateSel.value = selectedMapState;
  }
  switchGovTab('explorer');
  loadExplorerData(1);
}

// ==========================================
// FEATURE 2: 🛡️ Civic Anomaly & Audit Engine
// ==========================================
let allAuditAnomalies = [];
let currentAuditFilter = 'ALL';

async function loadAuditAnomalies() {
  const tbody = document.getElementById('auditAnomaliesTableBody');
  if (tbody) {
    tbody.innerHTML = '<tr><td colspan="8" class="py-8 text-center text-slate-400">Executing CAG forensic algorithms across in-memory records...</td></tr>';
  }

  try {
    const resp = await fetch('/v1/audit/anomalies');
    const data = await resp.json();
    if (!resp.ok) throw new Error(data.detail || 'Audit calculation failed');

    // Hygiene Score & Badges
    const sc = document.getElementById('auditHygieneScore');
    const gr = document.getElementById('auditHygieneGrade');
    const de = document.getElementById('auditHygieneDesc');
    if (sc) sc.innerText = data.hygiene_score;
    if (gr) gr.innerText = `Grade ${data.letter_grade}`;
    if (de) de.innerText = data.evaluation;

    // Counters
    const lc = document.getElementById('auditLeakageCount');
    const lt = document.getElementById('auditLeakageTotal');
    const dc = document.getElementById('auditDormantCount');
    const dt = document.getElementById('auditDormantTotal');
    const bc = document.getElementById('auditLowBeneCount');

    if (lc) lc.innerText = `${data.fiscal_leakages.count} Anomalies`;
    if (lt) lt.innerText = `Total: ₹ ${(data.fiscal_leakages.total_amount_inr / 10000000).toFixed(2)} Cr`;
    if (dc) dc.innerText = `${data.dormant_funds.count} Dormant`;
    if (dt) dt.innerText = `Idle: ₹ ${(data.dormant_funds.total_unutilized_inr / 10000000).toFixed(2)} Cr`;
    if (bc) bc.innerText = `${data.low_beneficiary_outliers.count} Outliers`;

    allAuditAnomalies = data.anomalies || [];
    renderAuditTable(allAuditAnomalies);
  } catch (err) {
    console.error('Failed to load audit data:', err);
    if (tbody) {
      tbody.innerHTML = `<tr><td colspan="8" class="py-8 text-center text-rose-500 font-semibold">Failed to load CAG forensic audit: ${escapeHtml(err.message)}</td></tr>`;
    }
  }
}

function filterAuditAnomalies(type) {
  currentAuditFilter = type;
  document.querySelectorAll('[id^="btn-audit-filter-"]').forEach(b => {
    b.className = 'px-3 py-1.5 rounded font-bold bg-slate-100 text-slate-700 hover:bg-slate-200 transition';
  });

  let btnId = 'btn-audit-filter-all';
  if (type === 'FISCAL_OVERSPEND') btnId = 'btn-audit-filter-leakage';
  else if (type === 'DORMANT_FUNDS') btnId = 'btn-audit-filter-dormant';
  else if (type === 'LOW_BENEFICIARY_OUTLIER') btnId = 'btn-audit-filter-bene';

  const activeBtn = document.getElementById(btnId);
  if (activeBtn) activeBtn.className = 'px-3 py-1.5 rounded font-bold bg-govNavy-900 text-white transition';

  const filtered = type === 'ALL'
    ? allAuditAnomalies
    : allAuditAnomalies.filter(a => a.type === type);

  renderAuditTable(filtered);
}

function renderAuditTable(list) {
  const tbody = document.getElementById('auditAnomaliesTableBody');
  if (!tbody) return;

  if (list.length === 0) {
    tbody.innerHTML = '<tr><td colspan="8" class="py-8 text-center text-slate-400">Zero anomalies match this category. CAG audit compliance satisfied.</td></tr>';
    return;
  }

  tbody.innerHTML = list.slice(0, 100).map(a => {
    const isLeakage = a.type === 'FISCAL_OVERSPEND';
    const isDormant = a.type === 'DORMANT_FUNDS';

    let sevBadge = a.severity === 'CRITICAL'
      ? '<span class="bg-rose-100 text-rose-800 border border-rose-300 px-1.5 py-0.5 rounded font-bold text-[10px]">CRITICAL</span>'
      : a.severity === 'WARNING'
        ? '<span class="bg-amber-100 text-amber-800 border border-amber-300 px-1.5 py-0.5 rounded font-bold text-[10px]">WARNING</span>'
        : '<span class="bg-sky-100 text-sky-800 border border-sky-300 px-1.5 py-0.5 rounded font-bold text-[10px]">ADVISORY</span>';

    let typeTag = isLeakage ? '🚨 Overspend Leakage' : isDormant ? '💤 Dormant Idle Fund' : '👥 Low Beneficiary';

    let gapDisplay = isLeakage
      ? `<span class="text-rose-600 font-bold font-mono">+${formatIndianCurrency(a.variance_gap_inr)}</span>`
      : isDormant
        ? `<span class="text-amber-600 font-bold font-mono">${a.utilization_rate_pct}% Spend</span>`
        : `<span class="text-slate-500 font-mono">${formatNumber(a.beneficiaries)} bene</span>`;

    return `
      <tr class="hover:bg-slate-50 transition">
        <td class="py-3 px-4">
          <div class="flex items-center gap-1.5">
            ${sevBadge}
            <span class="text-slate-700 font-semibold text-xs">${typeTag}</span>
          </div>
        </td>
        <td class="py-3 px-4">
          <div class="font-bold text-govNavy-900">${escapeHtml(a.district)}</div>
          <div class="text-[11px] text-slate-500">${escapeHtml(a.state)} <span class="text-[10px] bg-slate-100 px-1 py-0.5 rounded font-mono">LGD: ${a.lgd_district_code}</span></div>
        </td>
        <td class="py-3 px-4">
          <div class="text-xs font-semibold text-slate-800 max-w-[200px] truncate" title="${escapeHtml(a.scheme)}">${escapeHtml(a.scheme)}</div>
          <div class="text-[10px] text-slate-400">${escapeHtml(a.sector)}</div>
        </td>
        <td class="py-3 px-4 text-right font-mono text-slate-700">${formatIndianCurrency(a.allocation_inr)}</td>
        <td class="py-3 px-4 text-right font-mono text-slate-700">${formatIndianCurrency(a.expenditure_inr)}</td>
        <td class="py-3 px-4 text-right">${gapDisplay}</td>
        <td class="py-3 px-4">
          <div class="text-[11px] text-slate-600 max-w-xs leading-tight">${escapeHtml(a.finding)}</div>
        </td>
        <td class="py-3 px-4 text-right">
          <button class="bg-govNavy-900 hover:bg-govNavy-800 text-white px-2.5 py-1 rounded text-[11px] font-semibold transition" onclick="inspectDistrictFromAudit('${escapeHtml(a.district)}')">
            Inspect &rarr;
          </button>
        </td>
      </tr>
    `;
  }).join('');
}

function inspectDistrictFromAudit(district) {
  const searchInput = document.getElementById('searchInput');
  if (searchInput) searchInput.value = district;
  switchGovTab('explorer');
  loadExplorerData(1);
}

function exportAuditCsv() {
  if (!allAuditAnomalies.length) {
    showToast('No Data', 'No audit anomalies to export.', 'warning');
    return;
  }
  const headers = ['Type', 'Severity', 'State', 'District', 'LGD_Code', 'Scheme', 'Sector', 'Allocation_INR', 'Expenditure_INR', 'Variance_Gap_INR', 'Beneficiaries', 'Risk_Finding'];
  const rows = allAuditAnomalies.map(a => [
    a.type,
    a.severity,
    `"${(a.state || '').replace(/"/g, '""')}"`,
    `"${(a.district || '').replace(/"/g, '""')}"`,
    a.lgd_district_code,
    `"${(a.scheme || '').replace(/"/g, '""')}"`,
    `"${(a.sector || '').replace(/"/g, '""')}"`,
    a.allocation_inr,
    a.expenditure_inr,
    a.variance_gap_inr,
    a.beneficiaries,
    `"${(a.finding || '').replace(/"/g, '""')}"`,
  ]);

  const csvContent = [headers.join(','), ...rows.map(r => r.join(','))].join('\n');
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.setAttribute('href', url);
  link.setAttribute('download', `datasetu_cag_audit_anomalies_${Date.now()}.csv`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  showToast('Audit Exported', 'Downloaded CAG Forensic Audit CSV report successfully.', 'success');
}

// ==========================================
// FEATURE 3: 🔗 Cross-Ministerial LGD Correlator
// ==========================================
async function runCorrelator() {
  const datasetX = document.getElementById('corrDatasetX').value;
  const metricX = document.getElementById('corrMetricX').value;
  const datasetY = document.getElementById('corrDatasetY').value;
  const metricY = document.getElementById('corrMetricY').value;

  const corrValue = document.getElementById('corrValue');
  const corrDir = document.getElementById('corrDirection');
  const corrBadge = document.getElementById('corrStrengthBadge');
  const corrSample = document.getElementById('corrSampleSize');
  const corrLatency = document.getElementById('corrLatency');
  const corrPolicy = document.getElementById('corrPolicyInsight');

  if (corrValue) corrValue.innerText = '...';
  if (corrPolicy) corrPolicy.innerText = 'Executing vectorized inner-join across statutory LGD district codes in DuckDB...';

  try {
    const url = `/v1/correlate?dataset_x=${datasetX}&metric_x=${metricX}&dataset_y=${datasetY}&metric_y=${metricY}`;
    const resp = await fetch(url);
    const data = await resp.json();
    if (!resp.ok) throw new Error(data.detail || 'Correlation calculation failed');

    if (corrValue) corrValue.innerText = (data.pearson_r !== null ? data.pearson_r.toFixed(3) : 'N/A');
    if (corrDir) corrDir.innerText = `${data.direction.toUpperCase()} (${data.correlation_strength.toUpperCase()})`;
    if (corrBadge) corrBadge.innerText = `${data.correlation_strength} correlation`;
    if (corrSample) corrSample.innerText = `Sample Size: ${data.sample_size_districts} districts harmonized via LGD statutory gazetteer`;
    if (corrLatency) corrLatency.innerText = `Join Latency: ${data.latency_ms} ms`;
    if (corrPolicy) corrPolicy.innerText = data.policy_insight;

    // Draw Scatter Plot on Canvas
    drawCorrelatorScatter(data.scatter_points || [], `${datasetX} (${metricX})`, `${datasetY} (${metricY})`, data.pearson_r);
    showToast('LGD Correlation Computed', `Joined in ${data.latency_ms} ms across ${data.sample_size_districts} districts (r = ${data.pearson_r}).`, 'success');
  } catch (err) {
    console.error('Correlation error:', err);
    if (corrPolicy) corrPolicy.innerText = `Error: ${err.message}`;
    showToast('Correlator Error', err.message, 'error');
  }
}

function drawCorrelatorScatter(points, xLabel, yLabel, r) {
  const canvas = document.getElementById('correlatorCanvas');
  if (!canvas || !canvas.getContext) return;
  const ctx = canvas.getContext('2d');
  const w = canvas.width;
  const h = canvas.height;

  ctx.clearRect(0, 0, w, h);

  // Background
  ctx.fillStyle = '#0f172a';
  ctx.fillRect(0, 0, w, h);

  if (!points.length) {
    ctx.fillStyle = '#94a3b8';
    ctx.font = '12px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('No matched data points for this combination.', w / 2, h / 2);
    return;
  }

  const pad = 50;
  const xs = points.map(p => p.x);
  const ys = points.map(p => p.y);
  const minX = Math.min(...xs), maxX = Math.max(...xs) || 1;
  const minY = Math.min(...ys), maxY = Math.max(...ys) || 1;

  // Draw Grid Lines
  ctx.strokeStyle = '#1e293b';
  ctx.lineWidth = 1;
  for (let i = 0; i <= 4; i++) {
    const yLine = pad + (i / 4) * (h - 2 * pad);
    ctx.beginPath();
    ctx.moveTo(pad, yLine);
    ctx.lineTo(w - pad, yLine);
    ctx.stroke();
  }

  // Draw Points
  points.forEach(p => {
    const px = pad + ((p.x - minX) / (maxX - minX || 1)) * (w - 2 * pad);
    const py = (h - pad) - ((p.y - minY) / (maxY - minY || 1)) * (h - 2 * pad);

    ctx.fillStyle = '#38bdf8';
    ctx.beginPath();
    ctx.arc(px, py, 4.5, 0, 2 * Math.PI);
    ctx.fill();

    ctx.strokeStyle = '#0284c7';
    ctx.lineWidth = 1.5;
    ctx.stroke();
  });

  // Draw Trendline if points exist
  if (points.length > 1) {
    const p1x = pad;
    const p1y = (r >= 0) ? (h - pad) - 0.2 * (h - 2 * pad) : pad + 0.2 * (h - 2 * pad);
    const p2x = w - pad;
    const p2y = (r >= 0) ? pad + 0.2 * (h - 2 * pad) : (h - pad) - 0.2 * (h - 2 * pad);

    ctx.strokeStyle = '#fbbf24';
    ctx.lineWidth = 2;
    ctx.setLineDash([5, 5]);
    ctx.beginPath();
    ctx.moveTo(p1x, p1y);
    ctx.lineTo(p2x, p2y);
    ctx.stroke();
    ctx.setLineDash([]);
  }

  // Axes labels
  ctx.fillStyle = '#94a3b8';
  ctx.font = '10px monospace';
  ctx.textAlign = 'left';
  ctx.fillText(`X: ${xLabel}`, pad, h - 15);
  ctx.textAlign = 'right';
  ctx.fillText(`Y: ${yLabel}`, w - pad, 20);
}

// ==========================================
// FEATURE 4: ⚡ Event-Driven Webhooks & Simulator
// ==========================================
async function loadWebhooksView() {
  const listEl = document.getElementById('webhookSubscriptionsList');
  const countEl = document.getElementById('webhookSubCountBadge');
  if (!listEl) return;

  try {
    const resp = await fetch('/v1/webhooks/subscriptions');
    const data = await resp.json();
    const subs = data.subscriptions || [];

    if (countEl) countEl.innerText = `${subs.length} registered`;

    if (!subs.length) {
      listEl.innerHTML = '<div class="p-3 text-center text-slate-400 text-xs">No webhooks registered yet. Add one above.</div>';
      return;
    }

    listEl.innerHTML = subs.map(s => `
      <div class="p-2.5 rounded bg-slate-50 border border-slate-200 text-xs flex items-center justify-between">
        <div class="overflow-hidden">
          <div class="font-mono font-bold text-govNavy-900 truncate max-w-xs">${escapeHtml(s.target_url)}</div>
          <div class="text-[10px] text-slate-500">Events: <span class="bg-amber-100 text-amber-800 px-1 py-0.2 rounded font-mono">${escapeHtml(s.events.join(', '))}</span></div>
        </div>
        <span class="bg-emerald-100 text-emerald-800 text-[10px] font-bold px-1.5 py-0.5 rounded">Active</span>
      </div>
    `).join('');
  } catch (err) {
    console.error('Failed to load webhooks:', err);
  }
}

async function submitWebhookSubscription() {
  const targetUrl = document.getElementById('webhookTargetUrl').value;
  const eventType = document.getElementById('webhookEventType').value;
  const secret = document.getElementById('webhookSecret').value;

  try {
    const resp = await fetch('/v1/webhooks/subscribe', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        target_url: targetUrl,
        events: [eventType],
        secret: secret
      })
    });
    const data = await resp.json();
    if (!resp.ok) throw new Error(data.detail || 'Subscription failed');

    showToast('Webhook Registered', `Successfully subscribed ${targetUrl} to ${eventType}!`, 'success');
    document.getElementById('webhookTargetUrl').value = '';
    loadWebhooksView();
  } catch (err) {
    showToast('Subscription Error', err.message, 'error');
  }
}

let lastSimPayload = null;

async function simulateWebhookDispatch() {
  const eventType = document.getElementById('simEventType').value;
  const district = document.getElementById('simDistrict').value;
  const statusBadge = document.getElementById('simStatusBadge');
  const hdrEvent = document.getElementById('simHdrEvent');
  const hdrDelivery = document.getElementById('simHdrDelivery');
  const hdrSig = document.getElementById('simHdrSig');
  const payloadBox = document.getElementById('simPayloadJson');

  if (statusBadge) statusBadge.innerText = 'Dispatching HMAC event...';

  try {
    const resp = await fetch('/v1/webhooks/simulate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ event_type: eventType, district: district })
    });
    const data = await resp.json();
    if (!resp.ok) throw new Error(data.detail || 'Simulation failed');

    lastSimPayload = data.payload;
    if (hdrEvent) hdrEvent.innerText = data.event;
    if (hdrDelivery) hdrDelivery.innerText = data.delivery_id;
    if (hdrSig) hdrSig.innerText = data.signature;
    if (payloadBox) payloadBox.innerText = JSON.stringify(data.payload, null, 2);
    if (statusBadge) {
      statusBadge.innerText = `Dispatched in ${data.simulated_delivery_ms} ms (HTTP 200 OK)`;
      statusBadge.className = 'bg-emerald-100 text-emerald-800 font-mono text-[10px] px-2 py-0.5 rounded font-bold';
    }

    showToast('Webhook Dispatched', `HMAC-SHA256 signature generated and dispatched in ${data.simulated_delivery_ms} ms.`, 'success');
  } catch (err) {
    showToast('Simulation Error', err.message, 'error');
  }
}

function copySimPayload() {
  if (!lastSimPayload) {
    showToast('No Payload', 'Dispatch an event first to generate payload.', 'warning');
    return;
  }
  navigator.clipboard.writeText(JSON.stringify(lastSimPayload, null, 2));
  showToast('Copied', 'Webhook payload copied to clipboard.', 'info');
}

// ==========================================
// FEATURE 5: 💻 Native Polyglot SDK Generator
// ==========================================
let currentSdkTab = 'ts';
let sdkCache = {};

async function switchSdkTab(tab) {
  currentSdkTab = tab;
  document.querySelectorAll('.sdk-tab-btn').forEach(b => {
    b.className = 'sdk-tab-btn px-3 py-1 rounded text-slate-600 hover:text-slate-900';
  });
  const activeBtn = document.getElementById(`sdk-tab-${tab}`);
  if (activeBtn) activeBtn.className = 'sdk-tab-btn px-3 py-1 rounded bg-white text-govNavy-900 shadow-xs font-bold';

  const badge = document.getElementById('sdkFileNameBadge');
  const out = document.getElementById('sdkCodeOutput');

  if (tab === 'ts') {
    if (badge) badge.innerText = 'dataSetuClient.ts';
    if (!sdkCache.ts) {
      out.innerText = '// Fetching live TypeScript SDK from /v1/sdk/typescript...';
      const r = await fetch('/v1/sdk/typescript');
      sdkCache.ts = await r.text();
    }
    out.innerText = sdkCache.ts;
  } else if (tab === 'go') {
    if (badge) badge.innerText = 'client.go';
    if (!sdkCache.go) {
      out.innerText = '// Fetching live Go SDK from /v1/sdk/go...';
      const r = await fetch('/v1/sdk/go');
      sdkCache.go = await r.text();
    }
    out.innerText = sdkCache.go;
  } else if (tab === 'py') {
    if (badge) badge.innerText = 'datasetu_client.py';
    if (!sdkCache.py) {
      out.innerText = '// Fetching live Python SDK from /v1/sdk/python...';
      const r = await fetch('/v1/sdk/python');
      sdkCache.py = await r.text();
    }
    out.innerText = sdkCache.py;
  } else {
    if (badge) badge.innerText = 'cURL CLI';
    out.innerText = `# 1. Query records with DuckDB sub-millisecond filters
curl -X GET "https://datasetu-five.vercel.app/v1/data?state=Punjab&sector=Road%20Transport%20%26%20Highways&limit=5" \\
     -H "Accept: application/json"

# 2. Run Forensic CAG Audit Scanner
curl -X GET "https://datasetu-five.vercel.app/v1/audit/anomalies"

# 3. Cross-Ministerial Statutory LGD Inner JOIN
curl -X GET "https://datasetu-five.vercel.app/v1/correlate?dataset_x=road_transport&metric_x=allocation&dataset_y=rural_development&metric_y=beneficiaries"`;
  }
}

function downloadSdkFile() {
  const out = document.getElementById('sdkCodeOutput');
  const code = out ? out.innerText : '';
  let filename = 'dataSetuClient.ts';
  let mime = 'text/typescript';

  if (currentSdkTab === 'go') { filename = 'client.go'; mime = 'text/plain'; }
  else if (currentSdkTab === 'py') { filename = 'datasetu_client.py'; mime = 'text/x-python'; }
  else if (currentSdkTab === 'curl') { filename = 'query.sh'; mime = 'application/x-sh'; }

  const blob = new Blob([code], { type: mime });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  showToast('SDK Downloaded', `Saved ${filename} to your downloads.`, 'success');
}

function copySdkCode() {
  const out = document.getElementById('sdkCodeOutput');
  if (!out) return;
  navigator.clipboard.writeText(out.innerText);
  showToast('Copied', 'SDK source code copied to clipboard.', 'info');
}

// ==========================================
// FEATURE 6: 🇮🇳 Vernacular Voice & Audio Engine
// ==========================================
let currentAiLanguage = 'en';
let isVoiceListening = false;
let speechRecognizer = null;

function setAiLanguage(lang, el) {
  currentAiLanguage = lang;
  document.querySelectorAll('.ai-lang-pill').forEach(b => {
    b.className = 'ai-lang-pill px-2.5 py-1 rounded-full font-bold bg-white/10 hover:bg-white/20 text-purple-200 border border-white/20';
  });
  if (el) {
    el.className = 'ai-lang-pill px-2.5 py-1 rounded-full font-bold bg-amber-400 text-slate-950 shadow-xs';
  }
  showToast('Language Selected', `DataSetu AI synthesized responses will target '${lang}'.`, 'info');
}

function toggleVoiceRecognition() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    showToast('Voice Not Supported', 'Web Speech API is not supported in this browser. Please use Chrome/Edge.', 'warning');
    return;
  }

  const micIcon = document.getElementById('voiceMicIcon');
  const btn = document.getElementById('btnAiVoiceMic');

  if (isVoiceListening && speechRecognizer) {
    speechRecognizer.stop();
    isVoiceListening = false;
    if (micIcon) micIcon.innerText = '🎙️';
    if (btn) btn.classList.remove('bg-rose-600', 'animate-pulse');
    return;
  }

  speechRecognizer = new SpeechRecognition();
  speechRecognizer.continuous = false;
  speechRecognizer.interimResults = false;

  // Set Bhashini language tag
  if (currentAiLanguage === 'hi') speechRecognizer.lang = 'hi-IN';
  else if (currentAiLanguage === 'pa') speechRecognizer.lang = 'pa-IN';
  else if (currentAiLanguage === 'mr') speechRecognizer.lang = 'mr-IN';
  else if (currentAiLanguage === 'bn') speechRecognizer.lang = 'bn-IN';
  else if (currentAiLanguage === 'ta') speechRecognizer.lang = 'ta-IN';
  else if (currentAiLanguage === 'te') speechRecognizer.lang = 'te-IN';
  else speechRecognizer.lang = 'en-IN';

  speechRecognizer.onstart = () => {
    isVoiceListening = true;
    if (micIcon) micIcon.innerText = '🔴';
    if (btn) btn.classList.add('bg-rose-600', 'animate-pulse');
    showToast('Listening...', `Speak now in ${speechRecognizer.lang}.`, 'info');
  };

  speechRecognizer.onresult = (evt) => {
    const transcript = evt.results[0][0].transcript;
    const input = document.getElementById('aiQueryInput');
    if (input) input.value = transcript;
    showToast('Recognized', `"${transcript}"`, 'success');
    runAiQuery();
  };

  speechRecognizer.onerror = (evt) => {
    console.error('Speech recognition error:', evt.error);
    showToast('Voice Error', `Recognition error: ${evt.error}`, 'error');
  };

  speechRecognizer.onend = () => {
    isVoiceListening = false;
    if (micIcon) micIcon.innerText = '🎙️';
    if (btn) btn.classList.remove('bg-rose-600', 'animate-pulse');
  };

  speechRecognizer.start();
}

function speakAiSummary() {
  if (!window.speechSynthesis) {
    showToast('TTS Not Supported', 'Text-to-speech not supported in this browser.', 'warning');
    return;
  }
  const summaryEl = document.getElementById('aiExecutiveSummary');
  if (!summaryEl || !summaryEl.innerText) {
    showToast('No Summary', 'Execute an AI query first to synthesize summary.', 'warning');
    return;
  }

  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(summaryEl.innerText);
  if (currentAiLanguage === 'hi') utterance.lang = 'hi-IN';
  else utterance.lang = 'en-IN';
  window.speechSynthesis.speak(utterance);
  showToast('Audio Playing', 'Speaking synthesized executive brief.', 'info');
}
"""

TARGET_JS_ANCHOR = "async function runAiQuery() {"
assert TARGET_JS_ANCHOR in html, "Could not find runAiQuery"

# Also update runAiQuery to pass language: currentAiLanguage
OLD_RUN_AI = """  try {
    const resp = await fetch('/v1/ai/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question: q, max_rows: 25 })
    });"""

NEW_RUN_AI = """  try {
    const resp = await fetch('/v1/ai/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question: q, max_rows: 25, language: currentAiLanguage })
    });"""

assert OLD_RUN_AI in html, "Could not find OLD_RUN_AI"
html = html.replace(OLD_RUN_AI, NEW_RUN_AI)

# Insert the JS logic right before runAiQuery
html = html.replace(TARGET_JS_ANCHOR, JS_NEW_LOGIC + "\n" + TARGET_JS_ANCHOR)

# Write to both static files
with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)

with open(API_INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("Successfully upgraded datasetu/static/index.html and api/datasetu/static/index.html!")
