# Commercial Credit Risk Scorecard & Model Monitoring Methodology

This document details the regulatory background, statistical methodology, model architecture, and monitoring governance for the **Commercial Credit Risk Scorecard & Model Monitoring Platform**.

---

## 1. Regulatory & Business Context (BCB / CIB Credit Risk)

In corporate and commercial banking (Business & Commercial Banking / Corporate & Institutional Banking), credit risk models underpin critical financial decisions:
- **Origination & Underwriting:** Automated credit decisioning and debt-capacity sizing.
- **Capital Adequacy (Basel II / III / IV):** Estimating Probability of Default (PD) for regulatory capital calculations under the Internal Ratings-Based (IRB) approach.
- **Model Risk Management (PRA SS3/18):** UK Prudential Regulation Authority expectations requiring comprehensive model validation, out-of-time benchmarking against challenger models, and systematic ongoing monitoring of population stability and calibration.

---

## 2. Dataset Architecture & Information Governance

| Attribute | Details |
|---|---|
| **Commercial Loan Portfolio** | U.S. Small Business Administration (SBA) 7(a) FOIA Loan Program (`data.sba.gov`) |
| **Cohort Window** | FY2000 – FY2009 (10 approval years) |
| **Total Facility Volume** | **604,786 closed commercial loan facilities** (excluding cancellations and active loans) |
| **Development Sample** | **249,854 loans** (FY2000–FY2004 approvals; split into 70% Train [174,897] and 30% Test [74,957]) |
| **Out-of-Time Monitoring Sample** | **354,932 loans** (FY2005–FY2009 approvals, tracking through the 2007–2008 Financial Crisis) |
| **UK Macro Benchmark** | The Insolvency Service (GOV.UK) long-run company insolvency statistics covering England & Wales (2000–2024) |
| **Target Variable** | Binary indicator: `Default = 1` (Charged Off / Loss), `Default = 0` (Paid in Full) |
| **Target Leakage Safeguard** | Variables recorded post-origination during debt recovery or liquidation (such as `CollateralInd` or workout flags) were strictly excluded from the feature set. |

---

## 3. Statistical Methodology

### 3.1 Weight of Evidence (WoE) & Information Value (IV)
Continuous and categorical features are binned into monotonic or risk-differentiated intervals. For each bin $i$:

$$\text{WoE}_i = \ln\left(\frac{\text{Distr Good}_i}{\text{Distr Bad}_i}\right)$$

$$\text{IV} = \sum_{i} \left(\text{Distr Good}_i - \text{Distr Bad}_i\right) \times \text{WoE}_i$$

- **Positive WoE:** Indicates lower risk than population average (contributes positive scorecard points).
- **Negative WoE:** Indicates elevated default risk (penalises the score).

### 3.2 Logistic Regression Scorecard Formulation
The primary production model fits a multivariable logistic regression on the WoE-transformed features:

$$\ln\left(\frac{1 - p}{p}\right) = \beta_0 + \sum_{j=1}^{m} \beta_j \times \text{WoE}_{j}$$

### 3.3 Scorecard Scaling to Points
Using standard banking scaling parameters:
- **Base Score:** 600 points at **Odds of 50:1** (Good:Bad)
- **Points to Double the Odds (PDO):** 20 points
- **Factor:** $\text{Factor} = \frac{\text{PDO}}{\ln(2)} \approx 28.8539$
- **Offset:** $\text{Offset} = \text{BaseScore} - \text{Factor} \times \ln(\text{BaseOdds}) \approx 487.123$

For characteristic $j$ and attribute bin $i$, the points contribution is:

$$\text{Points}_{j, i} = \left(\frac{\text{Offset}}{m} - \frac{\text{Factor} \times \beta_0}{m}\right) - \text{Factor} \times \beta_j \times \text{WoE}_{j, i}$$

$$\text{Total Score} = \sum_{j=1}^{m} \text{Points}_{j, i}$$

$$\text{Implied PD} = \frac{1}{1 + \exp\left(\frac{\text{Score} - \text{Offset}}{\text{Factor}}\right)}$$

---

## 4. Challenger Model Benchmark (PRA SS3/18 Expectation)

To quantify the non-linear interaction potential and test whether the explainable scorecard leaves uncaptured predictive power on the table, a **HistGradientBoostingClassifier** was trained on raw categorical and continuous variables.

| Metric | Scorecard (Logistic WoE) | Challenger (HistGradientBoosting) | Lift / Variance |
|---|---|---|---|
| **Test AUC** | **0.7916** | **0.8432** | **+0.0516** |
| **Test Gini** | **0.5833** | **0.6864** | **+0.1031** |
| **Test KS** | **0.4554** | **0.5223** | **+0.0669** |
| **Explainability** | Full additive point attribution | Complex tree ensemble (SHAP required) | Scorecard is preferred for adverse action |

---

## 5. Model Monitoring Framework (Risk Science Standards)

### 5.1 Population Stability Index (PSI)
Measures the shift in the distribution of credit scores between the baseline development population $B$ and the current monitoring cohort $A$ across 10 score deciles:

$$\text{PSI} = \sum_{k=1}^{10} \left(A_k - B_k\right) \times \ln\left(\frac{A_k}{B_k}\right)$$

- **Green ($PSI < 0.10$):** Stable population. No action required.
- **Amber ($0.10 \le PSI \le 0.25$):** Moderate drift. Increased monitoring frequency.
- **Red ($PSI > 0.25$):** Significant shift. Trigger root-cause investigation and potential recalibration.

### 5.2 Characteristic Stability Index (CSI)
Measures stability at the individual feature level, isolating *which* risk drivers (e.g. loan term, guarantee rate, revolving facility share) drove the macro score drift.

### 5.3 Calibration Monitoring ($O/E$ Ratio)
Tracks Observed Default Rate ($O$) against Expected Default Rate ($E$).
- During the 2007–2008 crisis, the $O/E$ ratio rose to **1.74x (RED)**, reflecting the macroeconomic surge in business failures. This provides clear empirical evidence of why banks apply macroeconomic stress overlays to through-the-cycle (TTC) scorecards.

---

## 6. UK Corporate Insolvency Context

To place the empirical loan outcomes into UK macroeconomic perspective, the platform incorporates official long-run company insolvency statistics from **The Insolvency Service (England & Wales)**. 

Both jurisdictions exhibit parallel cyclical distress:
- **UK Company Insolvencies peaked at 24,038 in 2009** (up +54% from 15,629 in 2007).
- **US SBA Small Business Defaults peaked at 36.95% in FY2007 approval cohorts** as recession conditions took hold.
