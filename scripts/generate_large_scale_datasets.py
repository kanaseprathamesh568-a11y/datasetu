#!/usr/bin/env python3
"""
Generates high-scale, multi-year national governance datasets across all 780+
districts of India covering 20+ flagship welfare schemes.

Generates:
1. demo/bharat_governance_master_2026.csv (10,000+ cross-sector governance master records)
2. demo/catalog/pmkisan_national_dbt.csv (Agriculture Direct Benefit Transfer)
3. demo/catalog/mgnrega_national_employment.csv (Rural Employment & Wages)
4. demo/catalog/jal_jeevan_tap_water.csv (Drinking Water Infrastructure)
5. demo/catalog/ayushman_bharat_pmjay.csv (Health & Hospitalization)
6. demo/catalog/pmay_gramin_housing.csv (Affordable Rural Housing DBT)
"""

import csv
import json
import random
from pathlib import Path

random.seed(42)

def load_all_districts():
    p = Path(__file__).resolve().parent.parent / "datasetu" / "data" / "lgd_districts.json"
    with open(p, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["districts"]

SCHEMES = [
    ("Agriculture & Farmers Welfare", "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)", 12000000, 60000000, 5000, 45000),
    ("Agriculture & Farmers Welfare", "Pradhan Mantri Fasal Bima Yojana (Crop Insurance)", 8000000, 45000000, 2000, 25000),
    ("Agriculture & Farmers Welfare", "Agriculture Infrastructure Fund (AIF)", 5000000, 30000000, 200, 1500),
    ("Rural Development", "Mahatma Gandhi National Rural Employment Guarantee Scheme (MGNREGA)", 45000000, 250000000, 15000, 120000),
    ("Rural Development", "Pradhan Mantri Awaas Yojana - Gramin (PMAY-G Housing)", 35000000, 180000000, 1200, 8500),
    ("Rural Development", "Pradhan Mantri Gram Sadak Yojana (PMGSY Road Connectivity)", 25000000, 140000000, 10, 85),
    ("Rural Development", "Deendayal Antyodaya Yojana - NRLM Self Help Groups", 15000000, 85000000, 800, 6500),
    ("Health & Family Welfare", "Ayushman Bharat - Pradhan Mantri Jan Arogya Yojana (PM-JAY)", 20000000, 120000000, 4500, 35000),
    ("Health & Family Welfare", "National Health Mission - Primary Health Infrastructure", 18000000, 95000000, 2500, 22000),
    ("Health & Family Welfare", "Pradhan Mantri Ayushman Bharat Health Infrastructure Mission", 12000000, 75000000, 150, 1200),
    ("Drinking Water & Sanitation", "Jal Jeevan Mission - Har Ghar Jal Tap Water Connectivity", 55000000, 320000000, 15000, 95000),
    ("Drinking Water & Sanitation", "Swachh Bharat Mission - Gramin Phase II (ODF Plus)", 14000000, 65000000, 8000, 45000),
    ("Education & Skill Development", "Samagra Shiksha - Integrated Public School Infrastructure", 28000000, 160000000, 12000, 85000),
    ("Education & Skill Development", "PM POSHAN - National Mid-Day Meal Nutrition Program", 16000000, 90000000, 18000, 95000),
    ("Housing & Urban Affairs", "Pradhan Mantri Awas Yojana - Urban (PMAY-U)", 30000000, 150000000, 1500, 12000),
    ("Housing & Urban Affairs", "PM Street Vendor's AtmaNirbhar Nidhi (PM SVANidhi)", 4000000, 25000000, 1200, 15000),
    ("Economy & Finance", "Pradhan Mantri Jan Dhan Yojana (Financial Inclusion DBT)", 10000000, 50000000, 8500, 65000),
    ("Economy & Finance", "Micro Units Development & Refinance Agency (MUDRA Yojana)", 22000000, 110000000, 2500, 18000),
    ("Power & Energy", "PM-KUSUM Solar Agricultural Feeder Pumps", 15000000, 80000000, 350, 3500),
    ("Women & Child Development", "Mission Poshan 2.0 Early Childhood Nutrition", 12000000, 70000000, 6500, 45000)
]

STATUSES = ["Audited & Verified", "Fund Disbursed", "In-Progress", "Completed", "Approved"]
FINANCIAL_YEARS = ["2023-24", "2024-25", "2025-26"]

def make_master_records(districts, target_count=10500):
    records = []
    
    # Ensure every single one of the 782 districts has at least 10 records across key schemes
    for d in districts:
        state_name = d["state_name"]
        dist_name = d["canonical_name"]
        
        # Pick 13 schemes per district across different years
        sampled_schemes = random.sample(SCHEMES, k=13)
        for sector, scheme, min_alloc, max_alloc, min_bene, max_bene in sampled_schemes:
            fy = random.choice(FINANCIAL_YEARS)
            alloc = round(random.uniform(min_alloc, max_alloc), 2)
            # State matching share typically 40% for general states, 10% for NE/Himalayan
            is_ne = d["state_code"] in [1, 2, 5, 11, 12, 13, 14, 15, 16, 17, 18, 37]
            state_ratio = 0.10 if is_ne else 0.40
            state_share = round(alloc * state_ratio, 2)
            expenditure = round(alloc * random.uniform(0.75, 1.05), 2)
            bene = random.randint(min_bene, max_bene)
            status = random.choice(STATUSES)
            
            records.append({
                "Administrative Units - State Name": state_name,
                "Administrative Units - District Name": dist_name,
                "Governance Portfolio - Sector Category": sector,
                "Governance Portfolio - National Flagship Scheme": scheme,
                "Financial Provisions (INR) - Central Sanctioned Allocation": alloc,
                "Financial Provisions (INR) - State Matching Share Released": state_share,
                "Execution & Audit - Actual Expenditure Incurred": expenditure,
                "Impact Metrics - Beneficiaries Reached": bene,
                "Audit & Monitoring - Performance Lifecycle Status": status,
                "Fiscal Planning - Target Financial Year": fy
            })
            
            if len(records) >= target_count:
                break
        if len(records) >= target_count:
            break
            
    # Add a few realistic historical spelling aliases for robust testing
    alias_tests = [
        ("Maharashtra", "Poona", "Economy & Finance", "Pradhan Mantri Jan Dhan Yojana (Financial Inclusion DBT)", 15000000.0, 6000000.0, 14200000.0, 25000, "Audited & Verified", "2025-26"),
        ("Karnataka", "Belgaum", "Agriculture & Farmers Welfare", "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)", 24000000.0, 9600000.0, 23500000.0, 32000, "Fund Disbursed", "2025-26"),
        ("Haryana", "Gurgaon", "Housing & Urban Affairs", "PM Street Vendor's AtmaNirbhar Nidhi (PM SVANidhi)", 8500000.0, 3400000.0, 8100000.0, 4500, "Completed", "2025-26"),
        ("West Bengal", "Calcutta", "Health & Family Welfare", "Ayushman Bharat - Pradhan Mantri Jan Arogya Yojana (PM-JAY)", 35000000.0, 14000000.0, 33500000.0, 48000, "Audited & Verified", "2025-26"),
    ]
    for st, dst, sec, sch, alc, ssh, exp, ben, sta, fy in alias_tests:
        records.append({
            "Administrative Units - State Name": st,
            "Administrative Units - District Name": dst,
            "Governance Portfolio - Sector Category": sec,
            "Governance Portfolio - National Flagship Scheme": sch,
            "Financial Provisions (INR) - Central Sanctioned Allocation": alc,
            "Financial Provisions (INR) - State Matching Share Released": ssh,
            "Execution & Audit - Actual Expenditure Incurred": exp,
            "Impact Metrics - Beneficiaries Reached": ben,
            "Audit & Monitoring - Performance Lifecycle Status": sta,
            "Fiscal Planning - Target Financial Year": fy
        })

    random.shuffle(records)
    return records

def generate_domain_dataset(districts, scheme_tuple, file_path, headers_map):
    sector, scheme, min_alloc, max_alloc, min_bene, max_bene = scheme_tuple
    rows = []
    
    for d in districts:
        state_name = d["state_name"]
        dist_name = d["canonical_name"]
        
        for fy in ["2024-25", "2025-26"]:
            alloc = round(random.uniform(min_alloc, max_alloc), 2)
            is_ne = d["state_code"] in [1, 2, 5, 11, 12, 13, 14, 15, 16, 17, 18, 37]
            state_share = round(alloc * (0.10 if is_ne else 0.40), 2)
            expenditure = round(alloc * random.uniform(0.80, 1.02), 2)
            bene = random.randint(min_bene, max_bene)
            status = random.choice(STATUSES)
            
            row = {}
            for target_col, src_val in [
                ("state", state_name),
                ("district", dist_name),
                ("scheme", scheme),
                ("financial_year", fy),
                ("sanctioned_amount_inr", alloc),
                ("state_share_inr", state_share),
                ("expenditure_inr", expenditure),
                ("beneficiaries", bene),
                ("status", status)
            ]:
                custom_hdr = headers_map.get(target_col, target_col)
                row[custom_hdr] = src_val
            rows.append(row)
            
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Generated domain catalog dataset: {file_path} ({len(rows)} rows)")

def main():
    repo_dir = Path(__file__).resolve().parent.parent
    districts = load_all_districts()
    print(f"Loaded {len(districts)} districts from official LGD gazetteer.")
    
    # 1. Generate National Master Dataset (10,000+ records)
    master_records = make_master_records(districts, target_count=10166)
    master_csv_path = repo_dir / "demo" / "bharat_governance_master_2026.csv"
    with open(master_csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(master_records[0].keys()))
        writer.writeheader()
        writer.writerows(master_records)
    print(f"Generated national master: {master_csv_path} ({len(master_records)} records)")
    
    # Copy to api/demo for serverless deployment
    api_master_csv = repo_dir / "api" / "demo" / "bharat_governance_master_2026.csv"
    api_master_csv.parent.mkdir(parents=True, exist_ok=True)
    with open(api_master_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(master_records[0].keys()))
        writer.writeheader()
        writer.writerows(master_records)
    
    # 2. Generate Domain Catalog Datasets
    catalog_dir = repo_dir / "demo" / "catalog"
    api_catalog_dir = repo_dir / "api" / "demo" / "catalog"
    
    domain_configs = [
        (
            SCHEMES[0], # PM-KISAN
            "pmkisan_national_dbt.csv",
            {"state": "State / UT", "district": "District Name", "scheme": "Central Welfare Scheme", "financial_year": "Financial Year", "sanctioned_amount_inr": "Total Income Disbursed (INR)", "state_share_inr": "State Supplementary Top-Up", "expenditure_inr": "Direct Bank Settlement Total", "beneficiaries": "Farmer Beneficiaries Paid", "status": "DBT Gateway Audit Status"}
        ),
        (
            SCHEMES[3], # MGNREGA
            "mgnrega_national_employment.csv",
            {"state": "State", "district": "District", "scheme": "Scheme", "financial_year": "Fiscal Year", "sanctioned_amount_inr": "Wage Fund Sanctioned", "state_share_inr": "Material Component State Share", "expenditure_inr": "Total Wage Disbursed", "beneficiaries": "Active Muster Roll Workers", "status": "Social Audit Status"}
        ),
        (
            SCHEMES[10], # Jal Jeevan Mission
            "jal_jeevan_tap_water.csv",
            {"state": "State / UT Name", "district": "District", "scheme": "Mission Name", "financial_year": "Implementation Year", "sanctioned_amount_inr": "Sanctioned Tap Pipeline Outlay", "state_share_inr": "State Matching Fund", "expenditure_inr": "Actual Infrastructure Spend", "beneficiaries": "FHTC Tap Connections Provided", "status": "Water Quality Lab Clearance"}
        ),
        (
            SCHEMES[7], # Ayushman Bharat PM-JAY
            "ayushman_bharat_pmjay.csv",
            {"state": "State", "district": "District", "scheme": "Health Mission", "financial_year": "Policy Year", "sanctioned_amount_inr": "Pre-Authorized Medical Claims", "state_share_inr": "SHA State Health Insurance Share", "expenditure_inr": "Hospital Reimbursements Cleared", "beneficiaries": "In-Patient Treatments Covered", "status": "National Health Authority Approval"}
        ),
        (
            SCHEMES[4], # PMAY-G Housing
            "pmay_gramin_housing.csv",
            {"state": "State / UT", "district": "District Name", "scheme": "Rural Housing Scheme", "financial_year": "Sanction Cycle", "sanctioned_amount_inr": "Housing Subsidy Allocation", "state_share_inr": "State Co-Financing Share", "expenditure_inr": "AwaasSoft Disbursed Amount", "beneficiaries": "Pucca Houses Constructed", "status": "Geo-Tagged Inspection Verification"}
        ),
    ]
    
    for scheme_tuple, filename, hdr_map in domain_configs:
        generate_domain_dataset(districts, scheme_tuple, catalog_dir / filename, hdr_map)
        generate_domain_dataset(districts, scheme_tuple, api_catalog_dir / filename, hdr_map)
        
    print("All large-scale datasets generated successfully!")

if __name__ == "__main__":
    main()
