#!/usr/bin/env python3
"""Generate a comprehensive multi-ministry benchmark dataset suite for DataSetu.

Creates 26 files covering:
- 20 realistic ministry datasets (Agriculture, Health, Education, Finance, Rural Dev, etc.)
- 4 deliberately 'ugly' real-world datasets (Windows CP-1252 quotes, long preambles, split headers)
- 2 intentional failure test cases (non-tabular prose, corrupted empty file) to test honest error reporting.
"""

from pathlib import Path

BENCHMARK_DIR = Path(__file__).resolve().parent.parent / "benchmark" / "datasets"
BENCHMARK_DIR.mkdir(parents=True, exist_ok=True)

# 1. MoA PM-KISAN (CP-1252 encoding, Lakhs units, Indian commas)
moa_data = """# Ministry of Agriculture and Farmers Welfare
# Scheme: Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) - State/District Disbursals
# Generated: 2024-08-15 | Units: INR Lakhs
"State Name","District Name","Beneficiary Farmers Reached","Q1 Allocation (Rs. Lakhs)","Actual Direct Benefit Transferred","Verification Status"
"Karnataka","Bengaluru Urban","45,210","Rs. 904.20 Lakhs","890.50 Lakhs","Verified"
"Karnataka","Mysuru","1,24,500","Rs. 2,490.00 Lakhs","2,480.10 Lakhs","Verified"
"Maharashtra","Poona","2,10,340","Rs. 4,206.80 Lakhs","4,190.00 Lakhs","Verified"
"Maharashtra","Nagpur","1,85,900","Rs. 3,718.00 Lakhs","3,700.50 Lakhs","Verified"
"Haryana","Gurgaon","58,400","Rs. 1,168.00 Lakhs","1,150.00 Lakhs","Verified"
"Uttar Pradesh","Lucknow","3,12,000","Rs. 6,240.00 Lakhs","6,200.00 Lakhs","Verified"
"Gujarat","Ahmedabad","1,95,000","Rs. 3,900.00 Lakhs","3,880.00 Lakhs","Verified"
"Himachal Pradesh","Shimla","74,300","Rs. 1,486.00 Lakhs","1,480.00 Lakhs","Verified"
"West Bengal","Calcutta","12,400","Rs. 248.00 Lakhs","240.00 Lakhs","Audited"
"Tamil Nadu","Chennai","8,500","Rs. 170.00 Lakhs","165.00 Lakhs","Verified"
"""
with open(BENCHMARK_DIR / "moa_pmkisan_disbursement_2024.csv", "wb") as f:
    f.write(moa_data.encode("cp1252"))

# 2. MoRD MGNREGA (3 preamble rows, merged headers, Crores, negatives)
mord_data = """Government of India - Ministry of Rural Development
National Rural Employment Guarantee Act (MGNREGA) Performance Audit 2023-24
Data Source: nrega.nic.in Report R7.2 | Generated: 12-01-2024
Administrative Units	Administrative Units	Financial Outlay	Financial Outlay	Work Progress
State	District	Central Sanction (Cr)	State Matching Share (Cr)	Person Days Generated
Rajasthan	Jaipur	145.50 Crores	16.20 Crores	45,80,200
Rajasthan	Jodhpur	112.00 Crores	12.40 Crores	38,20,100
Madhya Pradesh	Bhopal	98.40 Crores	10.90 Crores	31,45,000
Madhya Pradesh	Indore	85.20 Crores	9.50 Crores	28,90,000
Bihar	Patna	165.80 Crores	18.40 Crores	54,20,000
Bihar	Gaya	132.50 Crores	14.70 Crores	42,10,000
Odisha	Bhubaneswar	78.90 Crores	8.70 Crores	24,50,000
Chhattisgarh	Raipur	94.20 Crores	10.50 Crores	30,10,000
"""
with open(BENCHMARK_DIR / "mord_mgnrega_wages_2023.csv", "w", encoding="utf-8") as f:
    f.write(mord_data)

# 3. MoHFW Ayushman Bharat (Parentheses accounting negatives, Nil sentinels)
mohfw_data = """"State","District","Hospitals Empanelled","Golden Cards Issued","Pre-auth Claims Amount (INR)","Outstanding Balance (INR)"
"Karnataka","Belgaum","142","12,40,500","1,45,20,000","Nil"
"Maharashtra","Thane","310","28,90,000","3,80,50,000","(45,000)"
"Gujarat","Surat","245","21,40,000","2,95,000","(1,20,000)"
"Delhi","New Delhi","180","8,90,000","4,12,00,000","Nil"
"Assam","Kamrup","89","6,50,000","78,90,000","NA"
"Kerala","Ernakulam","165","14,20,000","1,89,00,000","-"
"Punjab","Ludhiana","128","11,10,000","1,35,00,000","Nil"
"Telangana","Hyderabad","290","26,40,000","3,45,00,000","(80,000)"
"""
with open(BENCHMARK_DIR / "mohfw_ayushman_empanelment_2025.csv", "w", encoding="utf-8") as f:
    f.write(mohfw_data)

# 4. Jal Shakti JJM (Footnote asterisks, percentages, lakhs)
jalshakti_data = """"State / UT","District","Total Rural Households","Tap Water Provided*","Coverage Percentage*","Funds Allocated (Rs. Lakhs)"
"Gujarat","Gandhinagar","2,10,000","2,10,000","100.0%*","₹ 450.00 Lakhs"
"Haryana","Ambala","1,85,000","1,85,000","100.0%*","₹ 380.00 Lakhs"
"Punjab","Amritsar","3,40,000","3,25,000","95.6%*","₹ 710.00 Lakhs"
"Rajasthan","Kota","1,95,000","1,45,000","74.4%*","₹ 820.00 Lakhs"
"Uttar Pradesh","Varanasi","4,12,000","3,10,000","75.2%*","₹ 1,250.00 Lakhs"
"Karnataka","Dharwad","2,45,000","2,15,000","87.8%*","₹ 590.00 Lakhs"
"Madhya Pradesh","Gwalior","2,80,000","2,05,000","73.2%*","₹ 890.00 Lakhs"
"""
with open(BENCHMARK_DIR / "jalshakti_jjm_tap_coverage_2024.csv", "w", encoding="utf-8") as f:
    f.write(jalshakti_data)

# 5. Ministry of Education Samagra Shiksha
moe_data = """"State","District","Schools Sanctioned","ICT Labs Installed","Teacher Training Outlay (Rs. Lakhs)","Textbook Subsidy (Rs.)"
"Maharashtra","Pune","4,850","4,200","145.80 Lakhs","12,50,000"
"Tamil Nadu","Coimbatore","3,400","3,150","98.40 Lakhs","9,80,000"
"Karnataka","Mysuru","3,120","2,890","89.50 Lakhs","8,40,000"
"Rajasthan","Jaipur","5,200","4,600","162.00 Lakhs","15,20,000"
"Uttar Pradesh","Kanpur Nagar","4,900","3,800","135.00 Lakhs","13,90,000"
"West Bengal","North 24 Parganas","5,600","4,900","175.50 Lakhs","16,40,000"
"""
with open(BENCHMARK_DIR / "moe_samagra_shiksha_allocations_2023.csv", "w", encoding="utf-8") as f:
    f.write(moe_data)

# 6. Ministry of Finance 15th FC Grants
mof_data = """"State","District / ULB","Rural Local Body Untied Grant (Cr)","Health Sector Grant (Cr)","Total Release (Rs.)"
"Andhra Pradesh","Visakhapatnam","145.20 Crores","32.50 Crores","1,77,70,00,000"
"Telangana","Hyderabad","210.80 Crores","45.00 Crores","2,55,80,00,000"
"Karnataka","Bengaluru Urban","320.50 Crores","68.00 Crores","3,88,50,00,000"
"Maharashtra","Mumbai City","410.00 Crores","95.00 Crores","5,05,00,000"
"Gujarat","Surat","185.40 Crores","38.20 Crores","2,23,60,00,000"
"""
with open(BENCHMARK_DIR / "mof_fifteenth_fc_grants_2022.csv", "w", encoding="utf-8") as f:
    f.write(mof_data)

# 7. MoRTH PMGSY Road Connectivity
morth_data = """"State","District","Habitations Connected","Road Length Constructed (Km)","Total Expenditure (Rs. Lakhs)"
"Himachal Pradesh","Kangra","245","480.50 Km","₹ 12,450.00 Lakhs"
"Uttarakhand","Dehradun","189","345.20 Km","₹ 9,120.00 Lakhs"
"Jammu and Kashmir","Srinagar","112","210.00 Km","₹ 6,400.00 Lakhs"
"Assam","Dibrugarh","310","520.80 Km","₹ 14,200.00 Lakhs"
"Odisha","Mayurbhanj","420","710.40 Km","₹ 18,900.00 Lakhs"
"""
with open(BENCHMARK_DIR / "morth_pmgsy_road_connectivity_2024.csv", "w", encoding="utf-8") as f:
    f.write(morth_data)

# 8. Ministry of Power RDSS Feeder Solarization
mop_data = """"State","District","Feeders Segregated","Agricultural Solar Pumps Installed","Capacity (MW)","Subsidy Released (Cr)"
"Rajasthan","Jaipur","340","4,500","45.0 MW","125.00 Crores"
"Gujarat","Rajkot","290","3,800","38.0 MW","105.50 Crores"
"Maharashtra","Nashik","410","5,200","52.0 MW","148.00 Crores"
"Madhya Pradesh","Indore","280","3,400","34.0 MW","95.00 Crores"
"Haryana","Hisar","210","2,900","29.0 MW","82.40 Crores"
"""
with open(BENCHMARK_DIR / "mop_rdss_feeder_metering_2025.csv", "w", encoding="utf-8") as f:
    f.write(mop_data)

# 9. WCD Poshan Abhiyaan
wcd_data = """"State","District","Anganwadi Centers Active","Children Monitored","Severe Malnutrition Rate","Incentive Grant (Rs. Lakhs)"
"Bihar","Patna","3,420","1,85,000","4.2%","₹ 45.00 Lakhs"
"Jharkhand","Ranchi","2,150","1,12,000","5.1%","₹ 32.50 Lakhs"
"Odisha","Cuttack","2,890","1,45,000","3.8%","₹ 38.00 Lakhs"
"Madhya Pradesh","Bhopal","2,400","1,25,000","4.5%","₹ 35.00 Lakhs"
"Uttar Pradesh","Varanasi","3,800","2,10,000","4.9%","₹ 52.00 Lakhs"
"""
with open(BENCHMARK_DIR / "wcd_poshan_abhiyaan_indicators_2023.csv", "w", encoding="utf-8") as f:
    f.write(wcd_data)

# 10. Ministry of Tribal Affairs (TSP Special Assistance)
mot_data = """"State","District","Tribal Population Covered","Livelihood Clusters Funded","Central Allocation (Rs. Lakhs)"
"Odisha","Mayurbhanj","5,80,000","45","₹ 2,450.00 Lakhs"
"Jharkhand","Ranchi","4,20,000","38","₹ 1,890.00 Lakhs"
"Chhattisgarh","Bastar","3,90,000","32","₹ 1,650.00 Lakhs"
"Madhya Pradesh","Jhabua","4,50,000","40","₹ 1,980.00 Lakhs"
"Gujarat","Dangs","2,10,000","22","₹ 980.00 Lakhs"
"""
with open(BENCHMARK_DIR / "mot_tribal_special_central_assistance_2024.csv", "w", encoding="utf-8") as f:
    f.write(mot_data)

# 11-20: Other Ministry Data files
for code, name, unit, val in [
    ("mospi_cpi_rural_urban_index_2025", "MoSPI Inflation Index", "Index Points", "182.4"),
    ("moefcc_national_clean_air_programme_2024", "MoEFCC NCAP Smog Mitigation", "₹ Lakhs", "450.00 Lakhs"),
    ("moca_udan_regional_connectivity_2023", "MoCA UDAN Air Route Viability", "Crores", "12.50 Crores"),
    ("mopng_pmuy_ujjwala_connections_2022", "MoPNG PMUY LPG Cylinder Release", "Lakhs", "4.85 Lakhs"),
    ("mohua_pm_svanidhi_street_vendors_2024", "MoHUA PMSVANidhi Vendor Loans", "Rs.", "15,40,000"),
    ("msme_pmegp_margin_money_2025", "MSME PMEGP Margin Money Subsidy", "₹ Lakhs", "245.00 Lakhs"),
    ("dopt_civil_service_cadre_strength_2023", "DoPT District Cadre Sanction", "Officers", "14"),
    ("meity_digital_india_csc_centers_2024", "MeitY Common Service Centers", "Kiosks", "420"),
    ("mha_disaster_response_sdrf_releases_2024", "MHA SDRF Disaster Relief", "Crores", "85.00 Crores"),
    ("dae_atomic_energy_research_grants_2022", "DAE Research Laboratory Grants", "Lakhs", "120.00 Lakhs"),
]:
    content = f""""State","District","Scheme Indicator","Sanctioned Metric ({unit})","Expenditure Status"
"Karnataka","Bengaluru Urban","{name}","{val}","Completed"
"Maharashtra","Pune","{name}","{val}","Audited"
"Tamil Nadu","Chennai","{name}","{val}","Completed"
"Telangana","Hyderabad","{name}","{val}","In Progress"
"Gujarat","Ahmedabad","{name}","{val}","Completed"
"""
    with open(BENCHMARK_DIR / f"{code}.csv", "w", encoding="utf-8") as f:
        f.write(content)

# 21. Tricky Cases: Same-named districts across states (Testing Safe Disambiguation)
tricky_data = """"State","District","Central Fund (Lakhs)"
"Himachal Pradesh","Bilaspur","₹ 450.00 Lakhs"
"Chhattisgarh","Bilaspur","₹ 820.00 Lakhs"
"Haryana","Gurgaon","₹ 310.00 Lakhs"
"Karnataka","Belgaum","₹ 590.00 Lakhs"
"West Bengal","Calcutta","₹ 240.00 Lakhs"
"""
with open(BENCHMARK_DIR / "tricky_ambiguous_districts_2024.csv", "w", encoding="utf-8") as f:
    f.write(tricky_data)

# 22. Tricky Cases: Ambiguous districts WITHOUT state hints (Must flag needs_review=True!)
ambiguous_no_hint = """"District","Amount"
"Bilaspur","1000"
"Bengaluru Urban","2000"
"Pune","3000"
"""
with open(BENCHMARK_DIR / "tricky_unhinted_ambiguity_2024.csv", "w", encoding="utf-8") as f:
    f.write(ambiguous_no_hint)

# 23. Ugly File: Corrupted CP-1252 with smart quotes and em-dashes
ugly_cp1252 = (
    "# Government of India — Internal Report (CP-1252)\n"
    "# Notes: “Provisional Figures” — Subject to Audit\n"
    '"State Name","District Name","Grant Allocation"\n'
    '"Maharashtra","Pune","Rs. 12,45.50 Lakhs*"\n'
    '"Karnataka","Bengaluru Urban","Rs. 18,90.00 Lakhs*"\n'
)
with open(BENCHMARK_DIR / "ugly_corrupted_encoding_quotes_2021.csv", "wb") as f:
    f.write(ugly_cp1252.encode("cp1252"))

# 24. Ugly File: 6 preamble banner rows before table
ugly_preamble = """REPORT NO: GOI-MOH-2020-09
MINISTRY OF HEALTH & FAMILY WELFARE
DATA RETRIEVED FROM NATIONAL PORTAL ARCHIVE
CONFIDENTIAL DRAFT - FOR EVALUATION ONLY
DATE: 2020-11-04
==================================================
State,District,Clinics Established,Doctors Assigned
Kerala,Ernakulam,45,120
Karnataka,Mysuru,38,98
Tamil Nadu,Coimbatore,52,140
"""
with open(BENCHMARK_DIR / "ugly_excessive_preamble_notes_2020.csv", "w", encoding="utf-8") as f:
    f.write(ugly_preamble)

# 25. Intentional Failure Case: Non-tabular prose text
with open(BENCHMARK_DIR / "failure_case_non_tabular_prose.txt", "w", encoding="utf-8") as f:
    f.write(
        "This is an annual narrative overview document.\n"
        "No structured tabular records exist in this text.\n"
        "The committee met on Wednesday to discuss allocations.\n"
        "Meeting adjourned at 5 PM.\n"
    )

# 26. Intentional Failure Case: Empty 0-byte file
with open(BENCHMARK_DIR / "failure_case_corrupt_empty_file.csv", "w", encoding="utf-8") as f:
    pass

print(f"Successfully generated 26 diverse benchmark datasets in {BENCHMARK_DIR}")
