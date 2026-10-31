#!/usr/bin/env python3
"""
Updates DataSetu web portal for public open-source release:
- Removes unapproved government agency mimicry (MeitY/NIC headers).
- Adds prominent Public Beta Sandbox & Open Source Civic Tech disclaimer.
- Replaces unverified Grade A+ badges with empirical benchmark measurements (83.5% LGD match, 96.2% reliability).
- Renders warning badge in data table for records flagged with lgd_needs_review.
- Replaces fake .gov.in URLs with relative /v1/... endpoints.
- Synchronizes changes to api/datasetu/static/index.html.
"""

import shutil
from pathlib import Path

def main():
    repo_dir = Path(__file__).resolve().parent.parent
    html_path = repo_dir / "datasetu" / "static" / "index.html"
    content = html_path.read_text(encoding="utf-8")

    # 1. Update header branding
    old_hdr = (
        '        <svg class="w-4 h-5 fill-amber-400" viewBox="0 0 24 30"><path d="M12 2C10.5 2 9 3 9 4.5V6H15V4.5C15 3 13.5 2 12 2ZM6 8C5.5 8 5 8.5 5 9V11C5 12 5.8 12.8 6.7 13L6 18H8L8.6 13C9 13 9.4 12.9 9.8 12.7V17H11V8H6ZM18 8H13V17H14.2V12.7C14.6 12.9 15 13 15.4 13L16 18H18L17.3 13C18.2 12.8 19 12 19 11V9C19 8.5 18.5 8 18 8ZM8 20V22H16V20H8ZM7 23C7 24.1 7.9 25 9 25H15C16.1 25 17 24.1 17 23V22.5H7V23Z"></path></svg>\n'
        '        <span class="font-semibold text-slate-200 tracking-wide font-devanagari" id="txt-govt-brand">भारत सरकार</span>\n'
        '        <span class="text-slate-400 hidden sm:inline" id="txt-govt-en">| Government of India</span>\n'
        '      </div>\n'
        '      <div class="pl-3 hidden md:flex items-center space-x-2 text-slate-400">\n'
        '        <span id="txt-ministry" class="">Ministry of Electronics &amp; IT (MeitY)</span>\n'
        '        <span class="text-slate-600">•</span>\n'
        '        <span class="text-saffron font-medium">NIC Public Partner</span>\n'
        '      </div>'
    )

    new_hdr = (
        '        <span class="font-semibold text-slate-200 tracking-wide font-devanagari text-sm" id="txt-govt-brand">डेटासेतु DataSetu</span>\n'
        '        <span class="text-slate-400 hidden sm:inline text-xs" id="txt-govt-en">| Open Source Civic Tech</span>\n'
        '      </div>\n'
        '      <div class="pl-3 hidden md:flex items-center space-x-2 text-slate-400">\n'
        '        <span id="txt-ministry" class="bg-amber-900/60 text-amber-300 px-2 py-0.5 rounded text-[10px] font-bold">Public Beta Sandbox</span>\n'
        '        <span class="text-slate-600">•</span>\n'
        '        <span class="text-emerald-400 font-medium text-xs">Community Maintained</span>\n'
        '      </div>'
    )

    assert old_hdr in content, "Header pattern not matched"
    content = content.replace(old_hdr, new_hdr)

    # 2. Disclaimer banner below header
    old_post_hdr = "</header>\n\n<!-- Main Navigation Bar -->"
    new_post_hdr = (
        "</header>\n\n"
        "<!-- Public Release Disclaimer Banner -->\n"
        '<div class="bg-govNavy-950/95 border-b border-amber-500/30 text-amber-200/90 text-xs py-2 px-4 text-center z-30">\n'
        '  <div class="max-w-7xl mx-auto flex flex-wrap items-center justify-center gap-2">\n'
        '    <span class="bg-amber-500/20 text-amber-300 text-[10px] font-bold px-1.5 py-0.5 rounded uppercase tracking-wider">Public Beta Notice</span>\n'
        "    <span>DataSetu is an independent open-source civic tech project bridging India's open datasets to modern APIs. Not affiliated with or endorsed by NIC, MeitY, or data.gov.in. All data processed under GODL-India &amp; NDSAP.</span>\n"
        "  </div>\n"
        "</div>\n\n"
        "<!-- Main Navigation Bar -->"
    )

    assert old_post_hdr in content, "Post-header pattern not matched"
    content = content.replace(old_post_hdr, new_post_hdr)

    # 3. KPI cards (empirical benchmark numbers)
    old_kpi2 = (
        '        <span class="text-xs font-semibold text-slate-500 uppercase tracking-wide group-hover:text-amber-800">LGD Match Accuracy</span>\n'
        '        <span class="bg-amber-50 text-amber-800 text-[10px] font-bold px-1.5 py-0.5 rounded">MoPR Verified</span>\n'
        '      </div>\n'
        '      <div class="text-3xl font-extrabold text-govNavy-900 mt-1" id="kpi-lgd-rate">91.9%</div>\n'
        '      <p class="text-xs text-slate-500 mt-1 flex items-center gap-1 font-medium">\n'
        '        <span class="text-amber-600 font-bold">2,298 / 2,500</span> MoPR Census gazetteer mapped\n'
        "      </p>"
    )

    new_kpi2 = (
        '        <span class="text-xs font-semibold text-slate-500 uppercase tracking-wide group-hover:text-amber-800">Benchmark LGD Match</span>\n'
        '        <span class="bg-amber-50 text-amber-800 text-[10px] font-bold px-1.5 py-0.5 rounded">26 Ministries Tested</span>\n'
        '      </div>\n'
        '      <div class="text-3xl font-extrabold text-govNavy-900 mt-1" id="kpi-lgd-rate">83.5%</div>\n'
        '      <p class="text-xs text-slate-500 mt-1 flex items-center gap-1 font-medium">\n'
        '        <span class="text-amber-600 font-bold">21 Records</span> safely flagged for human review\n'
        "      </p>"
    )

    assert old_kpi2 in content, "KPI2 pattern not matched"
    content = content.replace(old_kpi2, new_kpi2)

    old_kpi3 = (
        '        <span class="text-xs font-semibold text-slate-500 uppercase tracking-wide group-hover:text-indiaGreen">Disinfection Scorecard</span>\n'
        '        <span class="bg-emerald-50 text-emerald-800 text-[10px] font-bold px-1.5 py-0.5 rounded">Grade A+</span>\n'
        '      </div>\n'
        '      <div class="text-3xl font-extrabold text-govNavy-900 mt-1" id="kpi-hygiene-score">98.8%</div>\n'
        '      <p class="text-xs text-slate-500 mt-1 flex items-center gap-1 font-medium">\n'
        "        CP-1252, Preamble &amp; Merged Headers Repaired\n"
        "      </p>"
    )

    new_kpi3 = (
        '        <span class="text-xs font-semibold text-slate-500 uppercase tracking-wide group-hover:text-indiaGreen">Pipeline Reliability</span>\n'
        '        <span class="bg-emerald-50 text-emerald-800 text-[10px] font-bold px-1.5 py-0.5 rounded">Measured Suite</span>\n'
        '      </div>\n'
        '      <div class="text-3xl font-extrabold text-govNavy-900 mt-1" id="kpi-hygiene-score">96.2%</div>\n'
        '      <p class="text-xs text-slate-500 mt-1 flex items-center gap-1 font-medium">\n'
        "        25 / 26 real files parsed (1 corrupt caught cleanly)\n"
        "      </p>"
    )

    assert old_kpi3 in content, "KPI3 pattern not matched"
    content = content.replace(old_kpi3, new_kpi3)

    # 4. Section subheaders & cURL text
    content = content.replace(
        '<span class="">Official Public Sandbox</span>\n        <span class="">•</span>\n        <span class="text-indiaGreen">GIGW 3.0 Standardized</span>',
        '<span class="">Open Source Public Sandbox</span>\n        <span class="">•</span>\n        <span class="text-indiaGreen">Apache 2.0 Licensed</span>'
    )

    content = content.replace(
        '"https://api.datasetu.gov.in/v1/lgd/districts?state=KA&amp;format=json"',
        '"/v1/data?state=KA&amp;limit=5"'
    )
    content = content.replace(
        'NIC Bharat Serverless Edge • Latency: 1.18 ms',
        'Vectorized DuckDB Engine • In-Memory Columnar Latency: 1.18 ms'
    )
    content = content.replace(
        '"engine": "DataSetu-MoPR-Parquet-V2"',
        '"engine": "DataSetu-Vectorized-DuckDB-v1.0"'
    )

    # 5. Open Standards Section
    old_partners = (
        '<!-- Institutional Partners Ecosystem -->\n'
        '<section class="bg-slate-100 border-t border-b border-slate-200 py-8 px-4 sm:px-8">\n'
        '  <div class="max-w-7xl mx-auto">\n'
        '    <div class="text-center mb-5">\n'
        '      <span class="text-xs font-bold uppercase tracking-widest text-slate-500">Digital Public Infrastructure Ecosystem</span>\n'
        '      <h4 class="text-sm font-semibold text-slate-700 mt-0.5">Conforming to Open Government Data Standards &amp; India Stack Architecture</h4>\n'
        '    </div>\n'
        '    <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-3 items-center">\n'
        '      <div class="bg-white p-3 rounded border border-slate-200 text-center shadow-xs flex flex-col items-center justify-center h-18">\n'
        '        <span class="font-extrabold text-govNavy-900 text-sm tracking-tight">Digital India</span>\n'
        '        <span class="text-[10px] text-saffron font-bold">पॉवर टू एम्पावर</span>\n'
        '      </div>\n'
        '      <div class="bg-white p-3 rounded border border-slate-200 text-center shadow-xs flex flex-col items-center justify-center h-18">\n'
        '        <span class="font-extrabold text-govNavy-900 text-sm tracking-tight">MeitY</span>\n'
        '        <span class="text-[10px] text-slate-500">Govt. of India</span>\n'
        '      </div>\n'
        '      <div class="bg-white p-3 rounded border border-slate-200 text-center shadow-xs flex flex-col items-center justify-center h-18">\n'
        '        <span class="font-extrabold text-govNavy-900 text-sm tracking-tight">data.gov.in</span>\n'
        '        <span class="text-[10px] text-indiaGreen font-bold">OGD Platform</span>\n'
        '      </div>\n'
        '      <div class="bg-white p-3 rounded border border-slate-200 text-center shadow-xs flex flex-col items-center justify-center h-18">\n'
        '        <span class="font-extrabold text-govNavy-900 text-sm tracking-tight">NIC</span>\n'
        '        <span class="text-[10px] text-slate-500">National Informatics</span>\n'
        '      </div>\n'
        '      <div class="bg-white p-3 rounded border border-slate-200 text-center shadow-xs flex flex-col items-center justify-center h-18">\n'
        '        <span class="font-extrabold text-govNavy-900 text-sm tracking-tight">MoPR</span>\n'
        '        <span class="text-[10px] text-slate-500">LGD Directory</span>\n'
        '      </div>\n'
        '      <div class="bg-white p-3 rounded border border-slate-200 text-center shadow-xs flex flex-col items-center justify-center h-18">\n'
        '        <span class="font-extrabold text-govNavy-900 text-sm tracking-tight">India Stack</span>\n'
        '        <span class="text-[10px] text-govRed font-bold">Open APIs</span>\n'
        '      </div>\n'
        '    </div>\n'
        '  </div>\n'
        '</section>'
    )

    new_partners = (
        '<!-- Open Standards & Data Sources Section -->\n'
        '<section class="bg-slate-100 border-t border-b border-slate-200 py-8 px-4 sm:px-8">\n'
        '  <div class="max-w-7xl mx-auto">\n'
        '    <div class="text-center mb-5">\n'
        '      <span class="text-xs font-bold uppercase tracking-widest text-slate-500">Open Standards &amp; Interoperability</span>\n'
        '      <h4 class="text-sm font-semibold text-slate-700 mt-0.5">Conforming to National Data Sharing and Accessibility Policy (NDSAP) &amp; Open Data Formats</h4>\n'
        '    </div>\n'
        '    <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-3 items-center">\n'
        '      <div class="bg-white p-3 rounded border border-slate-200 text-center shadow-xs flex flex-col items-center justify-center h-18">\n'
        '        <span class="font-extrabold text-govNavy-900 text-sm tracking-tight">GODL-India</span>\n'
        '        <span class="text-[10px] text-saffron font-bold">Open Data License</span>\n'
        '      </div>\n'
        '      <div class="bg-white p-3 rounded border border-slate-200 text-center shadow-xs flex flex-col items-center justify-center h-18">\n'
        '        <span class="font-extrabold text-govNavy-900 text-sm tracking-tight">NDSAP</span>\n'
        '        <span class="text-[10px] text-slate-500">Data Standards</span>\n'
        '      </div>\n'
        '      <div class="bg-white p-3 rounded border border-slate-200 text-center shadow-xs flex flex-col items-center justify-center h-18">\n'
        '        <span class="font-extrabold text-govNavy-900 text-sm tracking-tight">data.gov.in</span>\n'
        '        <span class="text-[10px] text-indiaGreen font-bold">OGD Source Data</span>\n'
        '      </div>\n'
        '      <div class="bg-white p-3 rounded border border-slate-200 text-center shadow-xs flex flex-col items-center justify-center h-18">\n'
        '        <span class="font-extrabold text-govNavy-900 text-sm tracking-tight">LGD Directory</span>\n'
        '        <span class="text-[10px] text-slate-500">MoPR Gazetteer</span>\n'
        '      </div>\n'
        '      <div class="bg-white p-3 rounded border border-slate-200 text-center shadow-xs flex flex-col items-center justify-center h-18">\n'
        '        <span class="font-extrabold text-govNavy-900 text-sm tracking-tight">DuckDB</span>\n'
        '        <span class="text-[10px] text-slate-500">Columnar Engine</span>\n'
        '      </div>\n'
        '      <div class="bg-white p-3 rounded border border-slate-200 text-center shadow-xs flex flex-col items-center justify-center h-18">\n'
        '        <span class="font-extrabold text-govNavy-900 text-sm tracking-tight">OpenAPI 3.1</span>\n'
        '        <span class="text-[10px] text-govRed font-bold">REST Services</span>\n'
        '      </div>\n'
        '    </div>\n'
        '  </div>\n'
        '</section>'
    )

    assert old_partners in content, "Partners section pattern not matched"
    content = content.replace(old_partners, new_partners)

    # 6. Footer Disclaimer & Links
    old_footer_claims = (
        '      <div class="">© 2026 DataSetu (डेटासेतु) • Managed in collaboration with National Informatics Centre (NIC) &amp; MeitY.</div>'
    )
    new_footer_claims = (
        '      <div class="">© 2026 DataSetu (डेटासेतु) Community • Released under Apache 2.0 • Independent open source civic tech project not affiliated with NIC or MeitY.</div>'
    )
    assert old_footer_claims in content, "Footer claim pattern not matched"
    content = content.replace(old_footer_claims, new_footer_claims)

    # 7. Language dict update
    content = content.replace(
        'govtBrand: "भारत सरकार",\n    govtEn: "| Government of India",\n    ministry: "Ministry of Electronics & Information Technology (MeitY)",',
        'govtBrand: "डेटासेतु DataSetu",\n    govtEn: "| Open Source Civic Tech",\n    ministry: "Public Beta Sandbox",'
    )
    content = content.replace(
        'govtBrand: "भारत सरकार",\n    govtEn: "| Government of India",\n    ministry: "इलेक्ट्रॉनिक्स और सूचना प्रौद्योगिकी मंत्रालय (MeitY)",',
        'govtBrand: "डेटासेतु DataSetu",\n    govtEn: "| ओपन सोर्स नागरिक तकनीक",\n    ministry: "सार्वजनिक बीटा सैंडबॉक्स",'
    )

    # 8. RenderExplorerTable: Display warning pill when lgd_needs_review is true
    old_render_lgd = (
        "    const lgdBadge = lgdCode \n"
        '      ? `<span class="bg-slate-100 hover:bg-slate-200 px-1.5 py-0.5 rounded border border-slate-200 cursor-pointer inline-flex items-center gap-1 font-mono text-[11px]" onclick="openLgdInspector(\'${distEsc}\', \'${stateEsc}\')" title="Inspect official MoPR Census Gazetteer">LGD: ${lgdCode} (${escapeHtml(lgdName)}) 🔍</span><div class="text-[10px] text-emerald-700 font-medium mt-0.5">${matchMethod} match</div>`\n'
        '      : `<span class="bg-amber-50 text-amber-800 px-1.5 py-0.5 rounded border border-amber-200 cursor-pointer inline-flex items-center gap-1 text-[11px]" onclick="openLgdInspector(\'${distEsc}\', \'${stateEsc}\')">Pending 🔍</span>`;'
    )

    new_render_lgd = (
        "    const needsReview = r['lgd_needs_review'] === true;\n"
        "    const reviewReason = r['lgd_review_reason'] || '';\n"
        "    const confTier = r['lgd_confidence_tier'] || (needsReview ? 'none' : 'high');\n\n"
        "    let lgdBadge = '';\n"
        "    let statusText = status;\n"
        "    if (needsReview) {\n"
        '      lgdBadge = `<span class="bg-amber-100 text-amber-900 border border-amber-300 px-1.5 py-0.5 rounded cursor-pointer inline-flex items-center gap-1 font-mono text-[11px]" onclick="openLgdInspector(\'${distEsc}\', \'${stateEsc}\')" title="${escapeHtml(reviewReason || \'Ambiguous match requires human review\')}">⚠️ Review: ${escapeHtml(lgdName)} 🔍</span><div class="text-[10px] text-amber-700 font-medium mt-0.5" title="${escapeHtml(reviewReason)}">${escapeHtml(reviewReason ? reviewReason.slice(0, 30) + \'...\' : \'Ambiguous\')}</div>`;\n'
        "      statusText = 'Flagged for Review';\n"
        "    } else if (lgdCode) {\n"
        '      lgdBadge = `<span class="bg-slate-100 hover:bg-slate-200 px-1.5 py-0.5 rounded border border-slate-200 cursor-pointer inline-flex items-center gap-1 font-mono text-[11px]" onclick="openLgdInspector(\'${distEsc}\', \'${stateEsc}\')" title="Inspect official LGD Directory">LGD: ${lgdCode} (${escapeHtml(lgdName)}) 🔍</span><div class="text-[10px] text-emerald-700 font-medium mt-0.5">${matchMethod} match (${confTier})</div>`;\n'
        "    } else {\n"
        '      lgdBadge = `<span class="bg-amber-50 text-amber-800 px-1.5 py-0.5 rounded border border-amber-200 cursor-pointer inline-flex items-center gap-1 text-[11px]" onclick="openLgdInspector(\'${distEsc}\', \'${stateEsc}\')">Pending 🔍</span>`;\n'
        "    }"
    )

    assert old_render_lgd in content, "old_render_lgd pattern not matched"
    content = content.replace(old_render_lgd, new_render_lgd)

    content = content.replace(
        '<span class="w-2 h-2 rounded-full bg-emerald-500 mr-1.5"></span> ${escapeHtml(status)}',
        '<span class="w-2 h-2 rounded-full ${needsReview ? "bg-amber-500" : "bg-emerald-500"} mr-1.5"></span> ${escapeHtml(statusText)}'
    )

    # 9. Update filter button label
    content = content.replace("91.9% MoPR LGD Verified", "83.5% LGD Verified (Safe Matching)")

    # 10. Update copy cURL command
    content = content.replace(
        "const curl = 'curl -X GET \"https://api.datasetu.gov.in/v1/lgd/districts?state=KA&format=json\" -H \"X-Bharat-Token: demo\"';",
        "const curl = 'curl -s \"' + window.location.origin + '/v1/data?state=KA&limit=5\" | jq .';"
    )

    html_path.write_text(content, encoding="utf-8")
    api_html_path = repo_dir / "api" / "datasetu" / "static" / "index.html"
    shutil.copyfile(html_path, api_html_path)
    print("Done! Both index.html files updated successfully.")

if __name__ == "__main__":
    main()
