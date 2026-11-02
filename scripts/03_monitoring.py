"""
03_monitoring.py
Computes comprehensive Model Monitoring metrics across Out-of-Time cohorts (FY2005-FY2009)
relative to Development baseline (FY2000-FY2004) as mandated in bank Risk Science functions.
Computes:
  - Population Stability Index (PSI) for Credit Score distribution (with RAG status)
  - Characteristic Stability Index (CSI) for individual risk drivers
  - Discrimination stability (Gini and KS trajectory by cohort year)
  - Calibration drift (Observed Default Rate vs Expected Default Rate, O/E ratio)
  - Portfolio segment performance (Industry, Business Age, Loan Amount, Region)
"""

import os
import json
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score, roc_curve

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC_DIR = os.path.join(BASE_DIR, 'data', 'processed')

FEATURE_COLS = [
    'term_band', 'loan_amt_band', 'guar_band', 'delivery_method',
    'is_revolver', 'same_state_bank', 'business_age', 'business_type',
    'industry', 'region', 'jobs_band'
]

SCORE_BINS = [-np.inf, 480, 500, 520, 535, 545, 555, 565, 575, 590, np.inf]
SCORE_BIN_LABELS = [
    '<480', '480-499', '500-519', '520-534', '535-544',
    '545-554', '555-564', '565-574', '575-589', '590+'
]

def calculate_psi(base_dist, actual_dist):
    """
    Computes Population Stability Index.
    base_dist, actual_dist: numpy arrays of proportions summing to 1.
    """
    # Clip to avoid zero division or log(0)
    b = np.clip(base_dist, 1e-4, 1.0)
    a = np.clip(actual_dist, 1e-4, 1.0)
    # Renormalise
    b = b / b.sum()
    a = a / a.sum()
    psi_components = (a - b) * np.log(a / b)
    psi = float(np.sum(psi_components))
    return psi, psi_components.tolist()

def get_rag(val, green_thresh=0.10, amber_thresh=0.25):
    if val < green_thresh:
        return 'GREEN'
    elif val <= amber_thresh:
        return 'AMBER'
    else:
        return 'RED'

def main():
    print("Loading data and model specification...")
    data_path = os.path.join(PROC_DIR, 'cleaned_sba_loans.csv.gz')
    df = pd.read_csv(data_path, compression='gzip')

    model_path = os.path.join(PROC_DIR, 'scorecard_model.json')
    with open(model_path, 'r') as f:
        model_spec = f.read()
    model = json.loads(model_spec)

    scorecard_pts = model['scorecard_points']
    scaling = model['scaling']
    offset = scaling['offset']
    factor = scaling['factor']

    # Compute Score for every loan in the dataset
    print("Computing points-based Credit Score for all loans...")
    scores = np.zeros(len(df), dtype=int)
    for feat in FEATURE_COLS:
        pts_map = scorecard_pts[feat]
        feat_vals = df[feat].astype(str)
        # Add points
        scores += feat_vals.map(pts_map).fillna(0).astype(int)

    df['score'] = scores
    # Implied PD from score: p = 1 / (1 + exp((score - offset) / factor))
    df['pred_pd'] = 1.0 / (1.0 + np.exp((df['score'] - offset) / factor))
    df['score_bin'] = pd.cut(df['score'], bins=SCORE_BINS, labels=SCORE_BIN_LABELS).astype(str)

    # 1. Base Population (Development FY2000-2004)
    base_df = df[df['fy'] <= 2004]
    base_score_counts = base_df['score_bin'].value_counts().reindex(SCORE_BIN_LABELS, fill_value=0)
    base_score_dist = (base_score_counts / len(base_df)).values

    print(f"Base cohort (2000-2004): {len(base_df):,} loans")

    # 2. Population Stability Index (PSI) by Year
    years = sorted(df['fy'].unique().tolist())
    psi_by_year = []
    gini_by_year = []
    calibration_by_year = []

    print("\n--- Year-by-Year Model Monitoring Metrics ---")
    for yr in years:
        sub = df[df['fy'] == yr]
        n_loans = len(sub)
        obs_default_rate = float(sub['default'].mean())
        exp_default_rate = float(sub['pred_pd'].mean())
        oe_ratio = round(obs_default_rate / exp_default_rate, 3) if exp_default_rate > 0 else 1.0

        # Score distribution
        counts = sub['score_bin'].value_counts().reindex(SCORE_BIN_LABELS, fill_value=0)
        actual_dist = (counts / n_loans).values
        psi_val, components = calculate_psi(base_score_dist, actual_dist)
        rag = get_rag(psi_val)

        # Discrimination (AUC, Gini, KS)
        y_true = sub['default'].values
        y_prob = sub['pred_pd'].values
        auc_val = float(roc_auc_score(y_true, y_prob)) if len(np.unique(y_true)) > 1 else 0.5
        gini_val = 2 * auc_val - 1
        fpr, tpr, _ = roc_curve(y_true, y_prob)
        ks_val = float(np.max(np.abs(tpr - fpr))) if len(fpr) > 0 else 0.0

        # Gini RAG (compared to dev Gini of ~0.58)
        gini_rag = 'GREEN' if gini_val >= 0.50 else ('AMBER' if gini_val >= 0.40 else 'RED')
        # Calibration RAG (O/E ratio within 0.8 to 1.25 is GREEN)
        oe_rag = 'GREEN' if 0.80 <= oe_ratio <= 1.25 else ('AMBER' if 0.70 <= oe_ratio <= 1.50 else 'RED')

        psi_by_year.append({
            'fy': int(yr),
            'n_loans': int(n_loans),
            'psi': round(psi_val, 4),
            'rag': rag,
            'is_dev': bool(yr <= 2004),
            'score_distribution': {label: round(float(pct), 4) for label, pct in zip(SCORE_BIN_LABELS, actual_dist)}
        })

        gini_by_year.append({
            'fy': int(yr),
            'auc': round(auc_val, 4),
            'gini': round(gini_val, 4),
            'ks': round(ks_val, 4),
            'rag': gini_rag,
            'is_dev': bool(yr <= 2004)
        })

        calibration_by_year.append({
            'fy': int(yr),
            'n_loans': int(n_loans),
            'observed_default_rate': round(obs_default_rate, 4),
            'expected_default_rate': round(exp_default_rate, 4),
            'oe_ratio': oe_ratio,
            'rag': oe_rag,
            'is_dev': bool(yr <= 2004)
        })

        print(f"FY{yr} | N={n_loans:>6,} | PSI: {psi_val:.4f} ({rag:<5}) | Gini: {gini_val:.4f} ({gini_rag:<5}) | Obs Default: {obs_default_rate:.2%} | O/E: {oe_ratio:.2f} ({oe_rag:<5})")

    # 3. Characteristic Stability Index (CSI) for individual features across years
    print("\n--- Characteristic Stability Index (CSI) Analysis ---")
    csi_summary = {}
    for feat in FEATURE_COLS:
        csi_summary[feat] = []
        base_cat_counts = base_df[feat].value_counts(normalize=True)
        all_cats = sorted(df[feat].unique().tolist())
        b_dist = np.array([base_cat_counts.get(c, 1e-4) for c in all_cats])
        b_dist = b_dist / b_dist.sum()

        for yr in years:
            sub = df[df['fy'] == yr]
            sub_cat_counts = sub[feat].value_counts(normalize=True)
            a_dist = np.array([sub_cat_counts.get(c, 1e-4) for c in all_cats])
            a_dist = a_dist / a_dist.sum()
            csi_val, _ = calculate_psi(b_dist, a_dist)
            csi_summary[feat].append({
                'fy': int(yr),
                'csi': round(csi_val, 4),
                'rag': get_rag(csi_val)
            })

    # 4. Segment Analysis across Key Commercial Portfolios
    print("\n--- Portfolio Segment Performance ---")
    segments = {}

    # Segment A: Industry Sector
    ind_agg = df.groupby('industry').agg(
        total_loans=('default', 'count'),
        default_rate_dev=('default', lambda s: float(s[df.loc[s.index, 'fy'] <= 2004].mean())),
        default_rate_crisis=('default', lambda s: float(s[df.loc[s.index, 'fy'].isin([2006, 2007, 2008])].mean())),
        default_rate_overall=('default', 'mean'),
        avg_score=('score', 'mean')
    ).round({'default_rate_dev': 4, 'default_rate_crisis': 4, 'default_rate_overall': 4, 'avg_score': 0}).reset_index()
    segments['industry'] = ind_agg.to_dict(orient='records')

    # Segment B: Business Age
    age_agg = df.groupby('business_age').agg(
        total_loans=('default', 'count'),
        default_rate_dev=('default', lambda s: float(s[df.loc[s.index, 'fy'] <= 2004].mean())),
        default_rate_crisis=('default', lambda s: float(s[df.loc[s.index, 'fy'].isin([2006, 2007, 2008])].mean())),
        default_rate_overall=('default', 'mean'),
        avg_score=('score', 'mean')
    ).round({'default_rate_dev': 4, 'default_rate_crisis': 4, 'default_rate_overall': 4, 'avg_score': 0}).reset_index()
    segments['business_age'] = age_agg.to_dict(orient='records')

    # Segment C: Loan Amount Band
    amt_agg = df.groupby('loan_amt_band').agg(
        total_loans=('default', 'count'),
        default_rate_dev=('default', lambda s: float(s[df.loc[s.index, 'fy'] <= 2004].mean())),
        default_rate_crisis=('default', lambda s: float(s[df.loc[s.index, 'fy'].isin([2006, 2007, 2008])].mean())),
        default_rate_overall=('default', 'mean'),
        avg_score=('score', 'mean')
    ).round({'default_rate_dev': 4, 'default_rate_crisis': 4, 'default_rate_overall': 4, 'avg_score': 0}).reset_index()
    segments['loan_amt_band'] = amt_agg.to_dict(orient='records')

    # Segment D: Region
    reg_agg = df.groupby('region').agg(
        total_loans=('default', 'count'),
        default_rate_dev=('default', lambda s: float(s[df.loc[s.index, 'fy'] <= 2004].mean())),
        default_rate_crisis=('default', lambda s: float(s[df.loc[s.index, 'fy'].isin([2006, 2007, 2008])].mean())),
        default_rate_overall=('default', 'mean'),
        avg_score=('score', 'mean')
    ).round({'default_rate_dev': 4, 'default_rate_crisis': 4, 'default_rate_overall': 4, 'avg_score': 0}).reset_index()
    segments['region'] = reg_agg.to_dict(orient='records')

    # Segment E: Revolving Line vs Term Loan
    rev_agg = df.groupby('is_revolver').agg(
        total_loans=('default', 'count'),
        default_rate_dev=('default', lambda s: float(s[df.loc[s.index, 'fy'] <= 2004].mean())),
        default_rate_crisis=('default', lambda s: float(s[df.loc[s.index, 'fy'].isin([2006, 2007, 2008])].mean())),
        default_rate_overall=('default', 'mean'),
        avg_score=('score', 'mean')
    ).round({'default_rate_dev': 4, 'default_rate_crisis': 4, 'default_rate_overall': 4, 'avg_score': 0}).reset_index()
    segments['is_revolver'] = rev_agg.to_dict(orient='records')

    # Save monitoring report JSON
    monitoring_output = {
        'baseline_definition': 'Approval FY2000 - FY2004 (249,854 commercial loans)',
        'oot_definition': 'Approval FY2005 - FY2009 (354,932 commercial loans)',
        'score_bins': SCORE_BIN_LABELS,
        'base_distribution': {label: round(float(pct), 4) for label, pct in zip(SCORE_BIN_LABELS, base_score_dist)},
        'psi_by_year': psi_by_year,
        'gini_by_year': gini_by_year,
        'calibration_by_year': calibration_by_year,
        'csi_by_feature': csi_summary,
        'segments': segments
    }

    out_file = os.path.join(PROC_DIR, 'monitoring_report.json')
    with open(out_file, 'w') as f:
        json.dump(monitoring_output, f, indent=2)

    print(f"\nModel monitoring report exported to {out_file}")

if __name__ == '__main__':
    main()
