<div align="center">

# 📊 Commercial Credit Risk Scorecard & Model Monitoring Platform

**Empirical Credit Risk Scoring, Weight of Evidence (WoE) Scorecard Architecture, Challenger Gradient Boosting, and Out-of-Time Crisis Monitoring across 604,786 Commercial Loans (FY2000–FY2009) with UK Corporate Insolvency Benchmarking**

[![Live Web Application](https://img.shields.io/badge/🔗_Live_App-View_Now-005a36?style=for-the-badge)](https://subramanian-ms.github.io/credit-risk-model-monitoring/)
[![Validation Report](https://img.shields.io/badge/Automated_Reconciliation-22_%2F_22_PASS-15803d?style=for-the-badge)](docs/Validation_Report.md)
[![Methodology](https://img.shields.io/badge/Methodology-PRA_SS3%2F18_%26_Basel_IRB-1976d2?style=for-the-badge)](docs/Methodology.md)
[![License](https://img.shields.io/badge/License-MIT-gray?style=for-the-badge)](LICENSE)

---

*How do commercial lenders balance regulatory transparency with predictive discrimination? How does an underwriting scorecard hold up when a macroeconomic crisis hits?*

</div>

## ✨ Key Capabilities & Features

| Capability | Technical Implementation |
|---|---|
| 🎯 **Interactive Risk Checker** | Instant in-browser scoring computing **Scorecard Points, 1-Year Probability of Default (PD), Risk Band (Prime to Subprime), and Credit Policy Recommendation** (Approve / Refer / Decline) |
| 🔍 **Points Breakdown & Adverse Action Explainability** | Compliant with **PRA SS3/18** and Basel transparency standards: exact points attribution contributed by each risk driver (loan term, facility size, guarantee coverage, trading track record, legal structure) |
| 📈 **Model Performance & Challenger Benchmark** | **Logistic Regression WoE Scorecard** (Test AUC: `0.7916`, Gini: `0.5833`, KS: `0.4554`) benchmarked against a **HistGradientBoosting Challenger** (Test AUC: `0.8432`, Gini: `0.6864`), highlighting the trade-off between explainability and non-linear lift |
| ⚠️ **Out-of-Time Model Monitoring (PSI / CSI)** | Multi-year model monitoring across **354,932 out-of-time loans** tracking portfolio drift through the **2007–2008 Great Financial Crisis** using **Population Stability Index (PSI)**, **Characteristic Stability Index (CSI)**, and **O/E Calibration RAG status** |
| 🏢 **Commercial Portfolio Breakdown** | Cross-tabulation of default rates across 11 industry sectors, 4 business age cohorts, facility size bands, and geographic regions comparing baseline (2000–04) to peak crisis stress (2006–08) |
| 🇬🇧 **UK Macroeconomic Context** | Benchmarking against **The Insolvency Service official company insolvency statistics for England & Wales (2000–2024)**, examining the parallel surge in corporate liquidations during economic downturns |
| 🛡️ **22 Automated Reconciliation Checks** | Complete test suite (`scripts/validate.py`) reconciling every score bin, decile distribution, PSI value, and UK statistic against underlying data (`docs/Validation_Report.md`) |
| ⚡ **Zero Server Footprint** | Pure standalone web application running client-side with zero external JavaScript dependencies — instantaneous loading on GitHub Pages |

---

## 🏛️ Regulatory Context & Model Architecture

In Business & Commercial Banking (BCB) and Corporate & Institutional Banking (CIB) risk functions, credit risk models must satisfy dual objectives:
1. **Accurate Risk Differentiation:** Rank-ordering borrowers by creditworthiness to minimize expected loss ($EL = PD \times EAD \times LGD$).
2. **Regulatory Explainability & Governance (PRA SS3/18):** Underwriters and risk committees must be able to explain *why* an applicant was declined, provide actionable feedback, and systematically monitor model stability over time.

### Scorecard Formulation
- **Base Score:** 600 points at **50:1 Odds**
- **Points to Double the Odds (PDO):** 20 points
- **Standard Formula:**

$$\text{Points}_{j, i} = \left(\frac{\text{Offset}}{m} - \frac{\text{Factor} \times \beta_0}{m}\right) - \text{Factor} \times \beta_j \times \text{WoE}_{j, i}$$

$$\text{Score} = \sum_{j=1}^{m} \text{Points}_{j, i}, \quad PD = \frac{1}{1 + \exp\left(\frac{\text{Score} - \text{Offset}}{\text{Factor}}\right)}$$

---

## 📂 Repository Structure

```
├── data/
│   ├── raw/                 # Official SBA FOIA CSV and UK Insolvency long-run CSV
│   └── processed/           # Cleaned loan records, model JSON, monitoring JSON
├── docs/
│   ├── Methodology.md       # Detailed mathematical & regulatory documentation
│   ├── Validation_Report.md # Automated 22-check reconciliation report
│   └── Data_Attribution.md  # Official data sources & open licensing
├── scripts/
│   ├── 01_clean_data.py     # Ingestion, target definition, leakage removal
│   ├── 02_train_scorecard.py# WoE/IV binning, Logistic Scorecard & Gradient Boosting
│   ├── 03_monitoring.py     # Year-by-year PSI, CSI, Gini decay, and O/E calibration
│   ├── 04_build_website.py  # Compiles JSON data payload and builds index.html
│   └── validate.py          # 22 automated reconciliation checks
├── index.html               # Production standalone web application
├── README.md                # Project documentation
└── LICENSE                  # MIT License
```

---

## 🚀 Reproducible Build Pipeline

To reproduce the modeling pipeline from raw open data:

```bash
# 1. Clean data and split into dev (2000-2004) and OOT monitoring (2005-2009)
python scripts/01_clean_data.py

# 2. Train WoE Logistic Scorecard and Challenger Gradient Boosting model
python scripts/02_train_scorecard.py

# 3. Compute annual PSI, CSI, Gini trajectories, and calibration monitoring
python scripts/03_monitoring.py

# 4. Compile web application
python scripts/04_build_website.py

# 5. Run 22 automated reconciliation checks
python scripts/validate.py
```

---

## 📖 Data Sources & Attribution

- **U.S. Small Business Administration (SBA):** 7(a) Loan Program FOIA Open Dataset (`data.sba.gov`), Public Domain.
- **The Insolvency Service (UK):** Long-run company insolvency statistics for England & Wales (`GOV.UK`), Open Government Licence v3.0.

---

<div align="center">

**Developed by [Subramanian Mathur Seetharaman](https://github.com/Subramanian-MS)**

</div>
