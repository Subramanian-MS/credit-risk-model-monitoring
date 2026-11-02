"""
02_train_scorecard.py
Develops a standard points-based credit risk scorecard and challenger gradient boosting model
for commercial lending using Weight of Evidence (WoE) and Information Value (IV).
Calculates performance metrics (ROC/AUC, Gini, KS, Calibration) across Train, Test, and OOT cohorts.
"""

import os
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score, brier_score_loss, roc_curve

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC_DIR = os.path.join(BASE_DIR, 'data', 'processed')

FEATURE_COLS = [
    'term_band', 'loan_amt_band', 'guar_band', 'delivery_method',
    'is_revolver', 'same_state_bank', 'business_age', 'business_type',
    'industry', 'region', 'jobs_band'
]

# Standard banking scorecard scaling parameters
BASE_SCORE = 600
BASE_ODDS = 50.0  # 50:1 Odds of Good vs Bad
PDO = 20.0        # Points to Double the Odds
FACTOR = PDO / np.log(2)  # ~28.8539
OFFSET = BASE_SCORE - FACTOR * np.log(BASE_ODDS)  # ~487.123

def calculate_woe_iv(df_train, feature_col, target_col):
    """
    Computes Weight of Evidence (WoE) and Information Value (IV) for a categorical feature.
    WoE = ln(Distr_Good / Distr_Bad)
    Positive WoE = Safer (lower default rate than population average).
    """
    total_good = (df_train[target_col] == 0).sum()
    total_bad = (df_train[target_col] == 1).sum()

    grouped = df_train.groupby(feature_col)[target_col].agg(
        count='count',
        bads='sum'
    ).reset_index()

    grouped['goods'] = grouped['count'] - grouped['bads']

    # Laplace smoothing to prevent division by zero or log(0)
    grouped['distr_good'] = (grouped['goods'] + 0.5) / (total_good + 1.0)
    grouped['distr_bad'] = (grouped['bads'] + 0.5) / (total_bad + 1.0)

    grouped['woe'] = np.log(grouped['distr_good'] / grouped['distr_bad'])
    grouped['iv_component'] = (grouped['distr_good'] - grouped['distr_bad']) * grouped['woe']
    total_iv = grouped['iv_component'].sum()

    grouped['default_rate'] = (grouped['bads'] / grouped['count']).round(4)
    grouped['pct_population'] = (grouped['count'] / len(df_train)).round(4)

    return grouped, total_iv

def compute_ks(y_true, y_prob):
    """Computes Kolmogorov-Smirnov (KS) statistic."""
    fpr, tpr, _ = roc_curve(y_true, y_prob)
    ks = np.max(np.abs(tpr - fpr))
    return float(ks)

def main():
    print("Loading cleaned SBA loan dataset...")
    data_path = os.path.join(PROC_DIR, 'cleaned_sba_loans.csv.gz')
    df = pd.read_csv(data_path, compression='gzip')

    print(f"Total dataset: {len(df):,} records")
    # Split Development sample (FY2000-2004) vs Out-of-Time Monitoring sample (FY2005-2009)
    dev_df = df[df['fy'] <= 2004].copy()
    oot_df = df[df['fy'] >= 2005].copy()

    print(f"Development sample (FY2000-2004): {len(dev_df):,} loans, default rate: {dev_df['default'].mean():.2%}")
    print(f"Out-of-Time sample (FY2005-2009): {len(oot_df):,} loans, default rate: {oot_df['default'].mean():.2%}")

    # Split Dev into 70% Train, 30% Test with stratified target
    train_df, test_df = train_test_split(
        dev_df, test_size=0.30, random_state=42, stratify=dev_df['default']
    )
    print(f"Train split: {len(train_df):,} loans | Test split: {len(test_df):,} loans")

    # Calculate WoE and IV for each feature on Train set
    woe_dicts = {}
    iv_summary = {}
    woe_tables = {}

    print("\n--- Weight of Evidence (WoE) & Information Value (IV) Analysis ---")
    for feat in FEATURE_COLS:
        woe_tbl, iv = calculate_woe_iv(train_df, feat, 'default')
        iv_summary[feat] = round(float(iv), 4)
        woe_dicts[feat] = dict(zip(woe_tbl[feat], woe_tbl['woe']))
        woe_tables[feat] = woe_tbl.to_dict(orient='records')
        print(f"Feature: {feat:<18} | IV: {iv:.4f}")

    # Map WoE to train, test, and oot
    X_train_woe = pd.DataFrame()
    X_test_woe = pd.DataFrame()
    X_oot_woe = pd.DataFrame()

    for feat in FEATURE_COLS:
        mapping = woe_dicts[feat]
        X_train_woe[feat] = train_df[feat].map(mapping).fillna(0.0)
        X_test_woe[feat] = test_df[feat].map(mapping).fillna(0.0)
        X_oot_woe[feat] = oot_df[feat].map(mapping).fillna(0.0)

    y_train = train_df['default'].values
    y_test = test_df['default'].values
    y_oot = oot_df['default'].values

    # Train Logistic Regression Scorecard
    print("\nTraining Logistic Regression on WoE features...")
    lr = LogisticRegression(C=1.0, max_iter=1000, random_state=42)
    lr.fit(X_train_woe, y_train)

    intercept = float(lr.intercept_[0])
    coefs = dict(zip(FEATURE_COLS, [float(c) for c in lr.coef_[0]]))
    m = len(FEATURE_COLS)

    print(f"Logistic Intercept (Beta_0): {intercept:.4f}")
    for feat, coef in coefs.items():
        print(f"  {feat:<18} Coef: {coef:.4f}")

    # Calculate Points for each bin of each characteristic
    # Standard formula: Points = (-(coef * woe + intercept/m)) * Factor + Offset/m
    # Note: Because WoE = ln(Good/Bad), positive WoE reduces probability of default.
    # In standard scorecard: Score = Offset + Factor * ln(Odds) = Offset + Factor * (-logit)
    # Logit = intercept + sum(coef * woe)
    # So: Score = Offset - Factor * intercept - Factor * sum(coef * woe)
    # Points_j = (Offset/m - Factor * intercept / m) - Factor * coef_j * woe_j
    scorecard_points = {}
    for feat in FEATURE_COLS:
        scorecard_points[feat] = {}
        c = coefs[feat]
        for bin_row in woe_tables[feat]:
            val = bin_row[feat]
            w = bin_row['woe']
            # Points contributed by this attribute
            pts = (OFFSET / m - FACTOR * intercept / m) - FACTOR * c * w
            scorecard_points[feat][str(val)] = int(round(pts))

    # Evaluate Scorecard on Train and Test
    # In scikit-learn, predict_proba returns [P(Y=0), P(Y=1)]
    train_pred_prob = lr.predict_proba(X_train_woe)[:, 1]
    test_pred_prob = lr.predict_proba(X_test_woe)[:, 1]
    oot_pred_prob = lr.predict_proba(X_oot_woe)[:, 1]

    # Convert probability to Score: Score = Offset + Factor * ln((1-p)/p)
    train_scores = (OFFSET + FACTOR * np.log((1.0 - train_pred_prob) / np.clip(train_pred_prob, 1e-6, 1.0 - 1e-6))).round().astype(int)
    test_scores = (OFFSET + FACTOR * np.log((1.0 - test_pred_prob) / np.clip(test_pred_prob, 1e-6, 1.0 - 1e-6))).round().astype(int)
    oot_scores = (OFFSET + FACTOR * np.log((1.0 - oot_pred_prob) / np.clip(oot_pred_prob, 1e-6, 1.0 - 1e-6))).round().astype(int)

    train_auc = roc_auc_score(y_train, train_pred_prob)
    test_auc = roc_auc_score(y_test, test_pred_prob)
    oot_auc = roc_auc_score(y_oot, oot_pred_prob)

    train_gini = 2 * train_auc - 1
    test_gini = 2 * test_auc - 1
    oot_gini = 2 * oot_auc - 1

    train_ks = compute_ks(y_train, train_pred_prob)
    test_ks = compute_ks(y_test, test_pred_prob)
    oot_ks = compute_ks(y_oot, oot_pred_prob)

    print("\n=== Scorecard Performance ===")
    print(f"Train - AUC: {train_auc:.4f} | Gini: {train_gini:.4f} | KS: {train_ks:.4f}")
    print(f"Test  - AUC: {test_auc:.4f} | Gini: {test_gini:.4f} | KS: {test_ks:.4f}")
    print(f"OOT   - AUC: {oot_auc:.4f} | Gini: {oot_gini:.4f} | KS: {oot_ks:.4f}")

    # Train Challenger Model: HistGradientBoosting
    print("\nTraining Challenger Model (HistGradientBoosting)...")
    # For HGB, encode categories as integers
    X_train_cat = train_df[FEATURE_COLS].copy()
    X_test_cat = test_df[FEATURE_COLS].copy()
    X_oot_cat = oot_df[FEATURE_COLS].copy()

    cat_mappings = {}
    for feat in FEATURE_COLS:
        unique_cats = sorted(X_train_cat[feat].unique().tolist())
        cat_map = {c: i for i, c in enumerate(unique_cats)}
        cat_mappings[feat] = cat_map
        X_train_cat[feat] = X_train_cat[feat].map(cat_map).fillna(0).astype(int)
        X_test_cat[feat] = X_test_cat[feat].map(cat_map).fillna(0).astype(int)
        X_oot_cat[feat] = X_oot_cat[feat].map(cat_map).fillna(0).astype(int)

    hgb = HistGradientBoostingClassifier(
        categorical_features=[True] * len(FEATURE_COLS),
        max_iter=150,
        random_state=42
    )
    hgb.fit(X_train_cat, y_train)

    hgb_test_prob = hgb.predict_proba(X_test_cat)[:, 1]
    hgb_oot_prob = hgb.predict_proba(X_oot_cat)[:, 1]

    hgb_test_auc = roc_auc_score(y_test, hgb_test_prob)
    hgb_test_gini = 2 * hgb_test_auc - 1
    hgb_test_ks = compute_ks(y_test, hgb_test_prob)

    hgb_oot_auc = roc_auc_score(y_oot, hgb_oot_prob)
    hgb_oot_gini = 2 * hgb_oot_auc - 1
    hgb_oot_ks = compute_ks(y_oot, hgb_oot_prob)

    print("\n=== Challenger (Gradient Boosting) Performance ===")
    print(f"Test - AUC: {hgb_test_auc:.4f} | Gini: {hgb_test_gini:.4f} | KS: {hgb_test_ks:.4f}")
    print(f"OOT  - AUC: {hgb_oot_auc:.4f} | Gini: {hgb_oot_gini:.4f} | KS: {hgb_oot_ks:.4f}")

    # Build Score Decile Calibration Table on Test set
    test_eval = pd.DataFrame({
        'y': y_test,
        'prob': test_pred_prob,
        'score': test_scores
    })
    # Sort by score descending (higher score = better borrower)
    test_eval['decile'] = pd.qcut(test_eval['score'], q=10, labels=False)
    # Reverse so Decile 1 is Lowest Risk, Decile 10 is Highest Risk
    test_eval['decile'] = 10 - test_eval['decile']

    deciles = []
    total_bads = test_eval['y'].sum()
    total_goods = len(test_eval) - total_bads

    for d in range(1, 11):
        subset = test_eval[test_eval['decile'] == d]
        n = len(subset)
        bads = subset['y'].sum()
        goods = n - bads
        deciles.append({
            'decile': d,
            'count': int(n),
            'min_score': int(subset['score'].min()),
            'max_score': int(subset['score'].max()),
            'avg_score': int(subset['score'].mean()),
            'avg_pred_pd': round(float(subset['prob'].mean()), 4),
            'actual_default_rate': round(float(bads / n), 4),
            'bads': int(bads),
            'goods': int(goods),
            'bad_share': round(float(bads / total_bads), 4)
        })

    # Save detailed evaluation and model artifact
    model_output = {
        'scaling': {
            'base_score': BASE_SCORE,
            'base_odds': BASE_ODDS,
            'pdo': PDO,
            'factor': round(FACTOR, 4),
            'offset': round(OFFSET, 4),
            'intercept': round(intercept, 4)
        },
        'information_values': iv_summary,
        'feature_coefficients': {k: round(v, 4) for k, v in coefs.items()},
        'scorecard_points': scorecard_points,
        'woe_tables': woe_tables,
        'performance': {
            'scorecard': {
                'train': {'auc': round(train_auc, 4), 'gini': round(train_gini, 4), 'ks': round(train_ks, 4)},
                'test': {'auc': round(test_auc, 4), 'gini': round(test_gini, 4), 'ks': round(test_ks, 4)},
                'oot_overall': {'auc': round(oot_auc, 4), 'gini': round(oot_gini, 4), 'ks': round(oot_ks, 4)}
            },
            'challenger_gradient_boosting': {
                'test': {'auc': round(hgb_test_auc, 4), 'gini': round(hgb_test_gini, 4), 'ks': round(hgb_test_ks, 4)},
                'oot_overall': {'auc': round(hgb_oot_auc, 4), 'gini': round(hgb_oot_gini, 4), 'ks': round(hgb_oot_ks, 4)}
            }
        },
        'deciles': deciles
    }

    out_file = os.path.join(PROC_DIR, 'scorecard_model.json')
    with open(out_file, 'w') as f:
        json.dump(model_output, f, indent=2)

    print(f"\nModel output successfully exported to {out_file}")

if __name__ == '__main__':
    main()
