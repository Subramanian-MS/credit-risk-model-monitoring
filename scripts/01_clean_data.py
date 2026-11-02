"""
01_clean_data.py
Ingests and cleans raw SBA 7(a) loan outcomes (FY2000-FY2009) and UK Insolvency Service long-run statistics.
Excludes post-origination leakage fields. Splits into development (2000-2004) and out-of-time monitoring (2005-2009).
"""

import os
import json
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, 'data', 'raw')
PROC_DIR = os.path.join(BASE_DIR, 'data', 'processed')
os.makedirs(PROC_DIR, exist_ok=True)

# 1. NAICS 2-digit human-readable industry names
NAICS_NAMES = {
    '11': 'Agriculture, Forestry & Fishing',
    '21': 'Mining, Quarrying & Oil Extraction',
    '22': 'Utilities',
    '23': 'Construction',
    '31': 'Manufacturing (Food, Textiles, Apparel)',
    '32': 'Manufacturing (Wood, Paper, Chemical, Plastics)',
    '33': 'Manufacturing (Metal, Machinery, Electronics)',
    '42': 'Wholesale Trade',
    '44': 'Retail Trade (Motor, Furniture, Electronics, Food)',
    '45': 'Retail Trade (General, Clothing, Sporting, Online)',
    '48': 'Transportation & Warehousing',
    '49': 'Postal, Couriers & Warehousing',
    '51': 'Information & Media',
    '52': 'Finance & Insurance',
    '53': 'Real Estate, Rental & Leasing',
    '54': 'Professional, Scientific & Technical Services',
    '55': 'Management of Companies',
    '56': 'Administrative & Support & Waste Management',
    '61': 'Educational Services',
    '62': 'Health Care & Social Assistance',
    '71': 'Arts, Entertainment & Recreation',
    '72': 'Accommodation & Food Services',
    '81': 'Other Services (Repair, Personal, Laundry)',
    '92': 'Public Administration',
    '99': 'Other / Unclassified'
}

# Macro Economic US Regions
US_REGIONS = {
    'CT': 'Northeast', 'ME': 'Northeast', 'MA': 'Northeast', 'NH': 'Northeast', 'RI': 'Northeast', 'VT': 'Northeast',
    'NJ': 'Northeast', 'NY': 'Northeast', 'PA': 'Northeast',
    'IL': 'Midwest', 'IN': 'Midwest', 'MI': 'Midwest', 'OH': 'Midwest', 'WI': 'Midwest',
    'IA': 'Midwest', 'KS': 'Midwest', 'MN': 'Midwest', 'MO': 'Midwest', 'NE': 'Midwest', 'ND': 'Midwest', 'SD': 'Midwest',
    'DE': 'South', 'FL': 'South', 'GA': 'South', 'MD': 'South', 'NC': 'South', 'SC': 'South', 'VA': 'South', 'DC': 'South', 'WV': 'South',
    'AL': 'South', 'KY': 'South', 'MS': 'South', 'TN': 'South', 'AR': 'South', 'LA': 'South', 'OK': 'South', 'TX': 'South',
    'AZ': 'West', 'CO': 'West', 'ID': 'West', 'MT': 'West', 'NV': 'West', 'NM': 'West', 'UT': 'West', 'WY': 'West',
    'AK': 'West', 'CA': 'West', 'HI': 'West', 'OR': 'West', 'WA': 'West'
}

def clean_sba_data():
    csv_path = os.path.join(RAW_DIR, 'FOIA_7a_FY2000_FY2009.csv')
    print(f"Reading SBA loan records from {csv_path}...")

    cols = [
        'GrossApproval', 'SBAGuaranteedApproval', 'ApprovalFY', 'ProcessingMethod',
        'TermInMonths', 'NaicsCode', 'ProjectState', 'BorrState', 'BankState',
        'BusinessType', 'BusinessAge', 'LoanStatus', 'RevolverStatus', 'JobsSupported'
    ]

    df = pd.read_csv(csv_path, usecols=cols, dtype=str)
    print(f"Total raw rows: {len(df):,}")

    # Keep only completed/closed loans (Paid in Full vs Charged Off)
    df = df[df['LoanStatus'].isin(['P I F', 'CHGOFF'])].copy()
    print(f"Closed loans (PIF or CHGOFF): {len(df):,}")

    # Target variable: 1 = Default (Charged off), 0 = Repaid (Paid in full)
    df['default'] = (df['LoanStatus'] == 'CHGOFF').astype(int)
    df['fy'] = pd.to_numeric(df['ApprovalFY'], errors='coerce').fillna(2000).astype(int)

    # Financial numeric variables
    df['loan_amt'] = pd.to_numeric(df['GrossApproval'], errors='coerce').fillna(0.0)
    df['guar_amt'] = pd.to_numeric(df['SBAGuaranteedApproval'], errors='coerce').fillna(0.0)
    df['guar_pct'] = np.where(df['loan_amt'] > 0, np.clip(df['guar_amt'] / df['loan_amt'] * 100, 0, 100), 50.0).round(1)
    df['term_months'] = pd.to_numeric(df['TermInMonths'], errors='coerce').fillna(60.0).astype(int)
    df['jobs'] = pd.to_numeric(df['JobsSupported'], errors='coerce').fillna(0.0).astype(int)

    # Clean categorical features
    df['is_revolver'] = np.where(df['RevolverStatus'].str.upper() == 'Y', 'Revolving Line', 'Term Loan')
    df['same_state_bank'] = np.where(df['BorrState'].fillna('') == df['BankState'].fillna(''), 'Local Bank (Same State)', 'Out-of-State Bank')

    # Business Type
    btype_map = {
        'CORPORATION': 'Corporation',
        'INDIVIDUAL': 'Sole Proprietorship',
        'PARTNERSHIP': 'Partnership'
    }
    df['business_type'] = df['BusinessType'].map(btype_map).fillna('Corporation')

    # Business Age
    def clean_age(x):
        s = str(x)
        if 'New' in s or 'Less than 1' in s:
            return 'New (<1 Year)'
        elif 'Startup' in s:
            return 'Startup'
        elif 'Existing, 5' in s or 'Existing or more' in s:
            return 'Established (5+ Years)'
        elif '2 years' in s or '3 years' in s or '4 years' in s:
            return 'Young (1-4 Years)'
        else:
            return 'Established (5+ Years)'
    df['business_age'] = df['BusinessAge'].apply(clean_age)

    # Industry mapping
    def clean_naics(x):
        s = str(x).strip()
        if len(s) >= 2 and s[:2].isdigit():
            c2 = s[:2]
            return NAICS_NAMES.get(c2, 'Other / Unclassified')
        return 'Other / Unclassified'
    df['industry'] = df['NaicsCode'].apply(clean_naics)

    # Macro Region
    df['region'] = df['ProjectState'].map(US_REGIONS).fillna('Other')

    # Processing Method simplification
    def clean_proc(x):
        s = str(x)
        if 'Express' in s and 'Community' not in s and 'Patriot' not in s:
            return 'SBA Express'
        elif 'Preferred' in s:
            return 'Preferred Lender (PLP)'
        elif 'Low Doc' in s:
            return 'Low Documentation'
        elif 'Community' in s:
            return 'Community Express'
        elif 'General' in s or '7a' in s:
            return 'Standard 7(a)'
        else:
            return 'Other Specialised'
    df['delivery_method'] = df['ProcessingMethod'].apply(clean_proc)

    # Binning continuous variables into bank-standard intervals
    # Loan Amount Bins
    amt_bins = [-1, 25000, 50000, 100000, 250000, 500000, 100000000]
    amt_labels = ['<$25k', '$25k-$50k', '$50k-$100k', '$100k-$250k', '$250k-$500k', '>$500k']
    df['loan_amt_band'] = pd.cut(df['loan_amt'], bins=amt_bins, labels=amt_labels).astype(str)

    # Term Bins
    term_bins = [-1, 35, 60, 120, 1000]
    term_labels = ['Short (<36m)', 'Medium (36-60m)', 'Long (61-120m)', 'Real Estate / Extended (>120m)']
    df['term_band'] = pd.cut(df['term_months'], bins=term_bins, labels=term_labels).astype(str)

    # Guarantee Share Bins
    guar_bins = [-1, 50, 74.9, 80, 100]
    guar_labels = ['Low (<=50%)', 'Moderate (51-74%)', 'Standard (75-80%)', 'High (>80%)']
    df['guar_band'] = pd.cut(df['guar_pct'], bins=guar_bins, labels=guar_labels).astype(str)

    # Jobs Supported Bins
    jobs_bins = [-1, 0, 2, 5, 10, 100000]
    jobs_labels = ['0 Jobs', '1-2 Jobs', '3-5 Jobs', '6-10 Jobs', '>10 Jobs']
    df['jobs_band'] = pd.cut(df['jobs'], bins=jobs_bins, labels=jobs_labels).astype(str)

    # Select model columns
    model_cols = [
        'fy', 'default', 'loan_amt', 'guar_pct', 'term_months', 'jobs',
        'loan_amt_band', 'term_band', 'guar_band', 'jobs_band',
        'is_revolver', 'same_state_bank', 'business_type', 'business_age',
        'industry', 'region', 'delivery_method'
    ]
    cleaned = df[model_cols].copy()

    # Save to parquet or feather or compressed csv
    out_csv = os.path.join(PROC_DIR, 'cleaned_sba_loans.csv.gz')
    cleaned.to_csv(out_csv, index=False, compression='gzip')
    print(f"Cleaned SBA data saved to {out_csv} ({len(cleaned):,} rows)")

    # Print summary statistics
    print("\n--- Summary by Approval FY ---")
    summary = cleaned.groupby('fy').agg(
        total_loans=('default', 'count'),
        defaulted_loans=('default', 'sum'),
        default_rate=('default', 'mean'),
        avg_loan_amt=('loan_amt', 'mean')
    ).round({'default_rate': 4, 'avg_loan_amt': 0})
    print(summary)

    return cleaned

def clean_uk_insolvency_data():
    raw_path = os.path.join(RAW_DIR, 'uk_insolvency_longrun.csv')
    print(f"\nProcessing UK Insolvency Service statistics from {raw_path}...")
    df = pd.read_csv(raw_path)

    # Keep calendar years 2000 to 2024
    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    df = df[df['year'].between(2000, 2024)].copy()

    # Total company insolvencies in England & Wales (seasonally adjusted and non-seasonally adjusted)
    df['total_ew'] = pd.to_numeric(df['total_ew_nsa'], errors='coerce').fillna(0)
    df['cvl_ew'] = pd.to_numeric(df['cvl_ew_nsa'], errors='coerce').fillna(0)
    df['compliq_ew'] = pd.to_numeric(df['compliq_ew_nsa'], errors='coerce').fillna(0)
    df['admin_ew'] = pd.to_numeric(df['admin_ew_nsa'], errors='coerce').fillna(0)

    # Annual aggregation
    annual = df.groupby('year').agg(
        total_insolvencies=('total_ew', 'sum'),
        creditors_voluntary_liquidations=('cvl_ew', 'sum'),
        compulsory_liquidations=('compliq_ew', 'sum'),
        administrations=('admin_ew', 'sum')
    ).reset_index()

    annual['year'] = annual['year'].astype(int)
    out_json = os.path.join(PROC_DIR, 'uk_insolvency_annual.json')
    annual.to_json(out_json, orient='records', indent=2)
    print(f"Saved UK annual insolvency statistics to {out_json} (2000-2024)")
    print(annual.head(10))

if __name__ == '__main__':
    clean_sba_data()
    clean_uk_insolvency_data()
