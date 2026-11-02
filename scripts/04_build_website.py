"""
04_build_website.py
Merges model metrics, scorecard points, monitoring tables, and UK insolvency series
into an embeddable JSON payload and generates a self-contained, responsive, professional
HTML web application for commercial credit risk decisioning and model monitoring.
Includes interactive SVG charts, responsive non-truncating navigation, and plain-English guidance.
"""

import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC_DIR = os.path.join(BASE_DIR, 'data', 'processed')
OUT_HTML = os.path.join(BASE_DIR, 'index.html')

def build_app():
    # 1. Load scorecard model
    with open(os.path.join(PROC_DIR, 'scorecard_model.json'), 'r') as f:
        model_data = json.load(f)

    # 2. Load monitoring report
    with open(os.path.join(PROC_DIR, 'monitoring_report.json'), 'r') as f:
        monitoring_data = json.load(f)

    # 3. Load UK insolvency series
    with open(os.path.join(PROC_DIR, 'uk_insolvency_annual.json'), 'r') as f:
        uk_data = json.load(f)

    # Combined payload
    payload = {
        'model': model_data,
        'monitoring': monitoring_data,
        'uk_insolvency': uk_data
    }
    payload_json = json.dumps(payload, separators=(',', ':'))

    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Commercial Credit Risk Scorecard & Model Monitoring | BCB / CIB Analytics</title>
  <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>📊</text></svg>">
  <style>
    :root {{
      --primary: #005a36;
      --primary-light: #e6f4ea;
      --primary-dark: #003e25;
      --accent: #1976d2;
      --bg: #f8fafc;
      --surface: #ffffff;
      --text: #0f172a;
      --text-muted: #64748b;
      --border: #e2e8f0;
      --green: #15803d;
      --green-bg: #dcfce7;
      --amber: #b45309;
      --amber-bg: #fef3c7;
      --red: #b91c1c;
      --red-bg: #fee2e2;
      --shadow-sm: 0 1px 3px rgba(0,0,0,0.06);
      --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.08);
      --font: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: var(--font);
      background-color: var(--bg);
      color: var(--text);
      line-height: 1.5;
      padding-bottom: 60px;
    }}
    header {{
      background: linear-gradient(135deg, #004b2c 0%, #00683e 100%);
      color: #ffffff;
      padding: 32px 24px;
      box-shadow: var(--shadow-md);
    }}
    .header-content {{
      max-width: 1240px;
      margin: 0 auto;
    }}
    .author-pill {{
      display: inline-block;
      font-size: 0.85rem;
      color: #a7f3d0;
      font-weight: 700;
      margin-bottom: 8px;
      letter-spacing: 0.03em;
      text-transform: uppercase;
    }}
    .badge {{
      display: inline-block;
      padding: 4px 10px;
      font-size: 0.75rem;
      font-weight: 700;
      border-radius: 9999px;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      margin-bottom: 12px;
    }}
    .badge-light {{ background: rgba(255,255,255,0.2); color: #ffffff; }}
    .badge-green {{ background: var(--green-bg); color: var(--green); }}
    .badge-amber {{ background: var(--amber-bg); color: var(--amber); }}
    .badge-red {{ background: var(--red-bg); color: var(--red); }}

    h1 {{
      font-size: 1.85rem;
      font-weight: 800;
      margin-bottom: 8px;
      letter-spacing: -0.02em;
    }}
    header p {{
      color: #e2e8f0;
      font-size: 0.95rem;
      max-width: 950px;
      line-height: 1.6;
    }}

    .container {{
      max-width: 1240px;
      margin: 0 auto;
      padding: 24px;
    }}

    /* User Guidance Callout Banner */
    .guidance-box {{
      background: #ffffff;
      border: 1px solid #cbd5e1;
      border-left: 5px solid var(--primary);
      border-radius: 8px;
      padding: 18px 22px;
      margin-bottom: 24px;
      box-shadow: var(--shadow-sm);
    }}
    .guidance-title {{
      font-size: 1.05rem;
      font-weight: 700;
      color: var(--primary-dark);
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 8px;
    }}
    .guidance-steps {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 16px;
      margin-top: 12px;
    }}
    .step-card {{
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      padding: 12px 14px;
      font-size: 0.85rem;
    }}
    .step-card strong {{
      display: block;
      color: var(--primary);
      margin-bottom: 4px;
      font-size: 0.88rem;
    }}

    /* Tab Navigation - Modern Non-Truncating Wrapping Pills */
    .nav-tabs {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      background: #ffffff;
      padding: 8px;
      border: 1px solid var(--border);
      border-radius: 10px;
      margin-bottom: 24px;
      box-shadow: var(--shadow-sm);
    }}
    .tab-btn {{
      flex: 1 1 auto;
      min-width: 160px;
      background: #f8fafc;
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 10px 14px;
      font-size: 0.88rem;
      font-weight: 600;
      color: var(--text-muted);
      cursor: pointer;
      text-align: center;
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
    }}
    .tab-btn:hover {{
      background: #f1f5f9;
      color: var(--primary);
      border-color: #cbd5e1;
    }}
    .tab-btn.active {{
      background: var(--primary);
      color: #ffffff;
      border-color: var(--primary);
      box-shadow: 0 2px 4px rgba(0, 90, 54, 0.2);
    }}

    /* Tab Content Panes */
    .tab-pane {{ display: none; }}
    .tab-pane.active {{ display: block; }}

    /* Cards & Layout */
    .card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 24px;
      margin-bottom: 24px;
      box-shadow: var(--shadow-sm);
    }}
    .card-title {{
      font-size: 1.15rem;
      font-weight: 700;
      margin-bottom: 14px;
      color: var(--text);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 8px;
    }}
    .grid-2 {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 24px;
    }}
    .grid-3 {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 20px;
    }}
    @media (max-width: 900px) {{
      .grid-2, .grid-3 {{ grid-template-columns: 1fr; }}
    }}

    /* Metric Boxes */
    .metric-box {{
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 16px;
      text-align: center;
    }}
    .metric-value {{
      font-size: 1.7rem;
      font-weight: 800;
      color: var(--primary);
      margin-top: 4px;
    }}
    .metric-label {{
      font-size: 0.8rem;
      text-transform: uppercase;
      font-weight: 600;
      color: var(--text-muted);
      letter-spacing: 0.04em;
    }}

    /* Forms */
    .form-group {{
      margin-bottom: 16px;
    }}
    .form-label {{
      display: block;
      font-size: 0.85rem;
      font-weight: 600;
      margin-bottom: 6px;
      color: var(--text);
    }}
    .form-select {{
      width: 100%;
      padding: 10px 12px;
      border: 1px solid var(--border);
      border-radius: 6px;
      font-size: 0.9rem;
      color: var(--text);
      background-color: #ffffff;
      outline: none;
      transition: border 0.15s ease;
    }}
    .form-select:focus {{
      border-color: var(--primary);
      box-shadow: 0 0 0 3px rgba(0, 90, 54, 0.15);
    }}

    /* Tables */
    .table-container {{
      overflow-x: auto;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.88rem;
      text-align: left;
    }}
    th, td {{
      padding: 10px 14px;
      border-bottom: 1px solid var(--border);
    }}
    th {{
      background-color: var(--bg);
      font-weight: 600;
      color: var(--text);
      text-transform: uppercase;
      font-size: 0.75rem;
      letter-spacing: 0.04em;
    }}
    tr:hover td {{
      background-color: #f1f5f9;
    }}
    .rag-pill {{
      display: inline-block;
      padding: 3px 8px;
      font-size: 0.72rem;
      font-weight: 700;
      border-radius: 4px;
      text-transform: uppercase;
    }}
    .rag-GREEN {{ background: var(--green-bg); color: var(--green); }}
    .rag-AMBER {{ background: var(--amber-bg); color: var(--amber); }}
    .rag-RED {{ background: var(--red-bg); color: var(--red); }}

    /* Result Panel */
    .decision-hero {{
      text-align: center;
      padding: 24px;
      border-radius: 8px;
      margin-bottom: 20px;
    }}
    .hero-approve {{ background: #ecfdf5; border: 2px solid #10b981; color: #065f46; }}
    .hero-refer {{ background: #fffbeb; border: 2px solid #f59e0b; color: #92400e; }}
    .hero-decline {{ background: #fef2f2; border: 2px solid #ef4444; color: #991b1b; }}

    .score-dial {{
      font-size: 3.2rem;
      font-weight: 900;
      line-height: 1.1;
      margin: 8px 0;
    }}

    /* SVG Chart Styles */
    .chart-box {{
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 16px;
      margin: 16px 0;
    }}
    svg {{
      width: 100%;
      height: auto;
      display: block;
    }}

    .info-callout {{
      background: #eff6ff;
      border-left: 4px solid #3b82f6;
      padding: 14px 18px;
      border-radius: 0 6px 6px 0;
      font-size: 0.9rem;
      color: #1e3a8a;
      margin: 16px 0;
    }}

    footer {{
      text-align: center;
      padding: 28px;
      color: var(--text-muted);
      font-size: 0.88rem;
      border-top: 1px solid var(--border);
      margin-top: 40px;
      background: #ffffff;
    }}
  </style>
</head>
<body>

<header>
  <div class="header-content">
    <div class="author-pill">Developed by Subramanian Mathur Seetharaman</div>
    <span class="badge badge-light">Commercial Credit Risk Modelling &amp; Monitoring</span>
    <h1>Commercial Credit Scorecard &amp; Out-of-Time Crisis Monitoring</h1>
    <p>
      An empirical credit scoring and model governance platform trained on 604,786 business loans (FY2000–FY2009) 
      featuring Weight of Evidence (WoE) scorecard scaling, Challenger Gradient Boosting comparison, 
      Population Stability Index (PSI) tracking through the 2008 Financial Crisis, and UK Insolvency Service macroeconomic benchmarking.
    </p>
  </div>
</header>

<div class="container">

  <!-- Plain-English User Navigation Guide -->
  <div class="guidance-box">
    <div class="guidance-title">
      <span>💡</span> How to Use &amp; Navigate This Platform (What Each Tab Shows You)
    </div>
    <div style="font-size: 0.88rem; color: #475569;">
      This platform demonstrates how commercial banks (like Lloyds BCB/CIB) evaluate business loans and monitor model stability over time:
    </div>
    <div class="guidance-steps">
      <div class="step-card">
        <strong>1. Loan Decision Checker</strong>
        Change loan details (term, amount, industry) on the left to see the bank's automated decision (Approve, Refer, Decline) and credit score.
      </div>
      <div class="step-card">
        <strong>2. Scorecard Explainability</strong>
        See the exact points awarded or deducted for each factor, satisfying PRA adverse action rules so customers know why they were scored.
      </div>
      <div class="step-card">
        <strong>3. Model Performance</strong>
        View the scorecard's discrimination accuracy (AUC 0.79 / Gini 0.58) benchmarked against a modern Gradient Boosting challenger.
      </div>
      <div class="step-card">
        <strong>4. Crisis Monitoring (PSI / CSI)</strong>
        See how the model held up over 10 years and detected the 2007–2008 Financial Crisis, triggering Red alerts as defaults jumped to 37%.
      </div>
      <div class="step-card">
        <strong>5. Portfolio Segments</strong>
        Compare real commercial default rates across 11 industries (Restaurants, Retail, Tech, Healthcare) before and during the crisis.
      </div>
      <div class="step-card">
        <strong>6. UK Macro Context</strong>
        Examine official UK company insolvency statistics (2000–2024) showing the parallel corporate liquidation surge during economic downturns.
      </div>
    </div>
  </div>

  <!-- Navigation Tabs (Non-truncating pills) -->
  <div class="nav-tabs" role="tablist">
    <button class="tab-btn active" id="tabBtn-checker" onclick="switchTab('checker', this)">🎯 1. Loan Decision Checker</button>
    <button class="tab-btn" id="tabBtn-explain" onclick="switchTab('explain', this)">🔍 2. Scorecard Explainability</button>
    <button class="tab-btn" id="tabBtn-performance" onclick="switchTab('performance', this)">📈 3. Model Performance (AUC / Gini)</button>
    <button class="tab-btn" id="tabBtn-monitoring" onclick="switchTab('monitoring', this)">⚠️ 4. Crisis Monitoring (PSI / CSI)</button>
    <button class="tab-btn" id="tabBtn-portfolio" onclick="switchTab('portfolio', this)">🏢 5. Portfolio Segments &amp; Sectors</button>
    <button class="tab-btn" id="tabBtn-uk" onclick="switchTab('uk', this)">🇬🇧 6. UK Macro Context &amp; Governance</button>
  </div>

  <!-- TAB 1: RISK CHECKER -->
  <div id="pane-checker" class="tab-pane active">
    <div class="grid-2">
      <!-- Form Input -->
      <div class="card">
        <div class="card-title">Commercial Loan Application Details</div>
        <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:16px;">
          Select parameters below to test an application through the bank's empirical scorecard:
        </p>
        <form id="loanForm" onchange="scoreLoan()">
          <div class="form-group">
            <label class="form-label">Loan Term (Amortisation Duration)</label>
            <select class="form-select" id="term_band">
              <option value="Short (<36m)">Short (&lt;36 months - Working capital / Bridge)</option>
              <option value="Medium (36-60m)">Medium (36–60 months - Equipment / Vehicles)</option>
              <option value="Long (61-120m)" selected>Long (61–120 months - Expansion term loan)</option>
              <option value="Real Estate / Extended (>120m)">Real Estate / Extended (&gt;120 months)</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">Gross Facility Amount</label>
            <select class="form-select" id="loan_amt_band">
              <option value="<$25k">Micro (&lt;$25,000)</option>
              <option value="$25k-$50k">$25,000 – $50,000</option>
              <option value="$50k-$100k" selected>$50,000 – $100,000</option>
              <option value="$100k-$250k">$100,000 – $250,000</option>
              <option value="$250k-$500k">$250,000 – $500,000</option>
              <option value=">$500k">Large Commercial (&gt;$500,000)</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">Government / Scheme Guarantee Coverage</label>
            <select class="form-select" id="guar_band">
              <option value="Low (<=50%)">Low Guarantee (&le;50% - High bank risk exposure)</option>
              <option value="Moderate (51-74%)">Moderate (51%–74%)</option>
              <option value="Standard (75-80%)" selected>Standard Scheme Guarantee (75%–80%)</option>
              <option value="High (>80%)">High Guarantee (&gt;80% - Government backed)</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">Facility Structure</label>
            <select class="form-select" id="is_revolver">
              <option value="Term Loan" selected>Standard Term Loan</option>
              <option value="Revolving Line">Revolving Line of Credit</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">Delivery Channel / Program</label>
            <select class="form-select" id="delivery_method">
              <option value="Preferred Lender (PLP)" selected>Preferred Lender Program (PLP)</option>
              <option value="SBA Express">Express Scheme</option>
              <option value="Standard 7(a)">Standard Commercial 7(a)</option>
              <option value="Low Documentation">Low Documentation Program</option>
              <option value="Community Express">Community Express Pilot</option>
              <option value="Other Specialised">Other Specialised Scheme</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">Industry Sector</label>
            <select class="form-select" id="industry">
              <option value="Accommodation & Food Services">Accommodation &amp; Food Services (Restaurants, Bars, Hotels)</option>
              <option value="Retail Trade (Motor, Furniture, Electronics, Food)" selected>Retail Trade</option>
              <option value="Construction">Construction &amp; Contracting</option>
              <option value="Manufacturing (Metal, Machinery, Electronics)">Manufacturing (Machinery, Metal, Electronics)</option>
              <option value="Manufacturing (Food, Textiles, Apparel)">Manufacturing (Food, Textiles, Goods)</option>
              <option value="Professional, Scientific & Technical Services">Professional, Scientific &amp; Technical</option>
              <option value="Health Care & Social Assistance">Healthcare &amp; Social Assistance</option>
              <option value="Transportation & Warehousing">Transportation &amp; Logistics</option>
              <option value="Wholesale Trade">Wholesale Trade</option>
              <option value="Other Services (Repair, Personal, Laundry)">Other Personal Services</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">Operating Track Record</label>
            <select class="form-select" id="business_age">
              <option value="Established (5+ Years)" selected>Established (5+ Years trading)</option>
              <option value="Young (1-4 Years)">Young (1–4 Years trading)</option>
              <option value="New (<1 Year)">New (&lt;1 Year trading)</option>
              <option value="Startup">Startup (Loan funds launch)</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">Legal Entity Structure</label>
            <select class="form-select" id="business_type">
              <option value="Corporation" selected>Limited Corporation (Ltd / Corp)</option>
              <option value="Sole Proprietorship">Sole Proprietorship / Individual</option>
              <option value="Partnership">Partnership</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">Lender Relationship</label>
            <select class="form-select" id="same_state_bank">
              <option value="Local Bank (Same State)" selected>Local Relationship Bank (Same State)</option>
              <option value="Out-of-State Bank">Out-of-State / Remote Lender</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">Geographic Region</label>
            <select class="form-select" id="region">
              <option value="Midwest">Midwest</option>
              <option value="Northeast">Northeast</option>
              <option value="South" selected>South</option>
              <option value="West">West</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">Jobs Supported / Headcount</label>
            <select class="form-select" id="jobs_band">
              <option value="0 Jobs">0 Jobs reported</option>
              <option value="1-2 Jobs">1–2 Jobs</option>
              <option value="3-5 Jobs" selected>3–5 Jobs</option>
              <option value="6-10 Jobs">6–10 Jobs</option>
              <option value=">10 Jobs">&gt;10 Jobs</option>
            </select>
          </div>
        </form>
      </div>

      <!-- Decision & Output -->
      <div>
        <div class="card">
          <div class="card-title">Credit Risk Decision &amp; Score</div>
          <div id="decisionHero" class="decision-hero hero-approve">
            <div id="riskBandBadge" class="badge badge-green">Band 1 | Prime (Low Risk)</div>
            <div id="scoreDisplay" class="score-dial">612</div>
            <div id="decisionText" style="font-weight:700; font-size:1.15rem;">AUTO-APPROVE FACILITY</div>
            <div id="decisionSub" style="font-size:0.88rem; margin-top:4px;">Application meets credit policy thresholds for automated sign-off.</div>
          </div>

          <div class="grid-3" style="margin-top: 16px;">
            <div class="metric-box">
              <div class="metric-label">Predicted 1-Yr PD</div>
              <div id="pdDisplay" class="metric-value">6.8%</div>
            </div>
            <div class="metric-box">
              <div class="metric-label">Portfolio Benchmark</div>
              <div class="metric-value" style="color:var(--text-muted);">15.7%</div>
            </div>
            <div class="metric-box">
              <div class="metric-label">Policy Action</div>
              <div id="policyAction" class="metric-value" style="font-size:1.1rem; color:var(--green); margin-top:10px;">Fast-Track</div>
            </div>
          </div>

          <div class="info-callout" style="margin-top:20px;">
            <strong>Underwriting Guidance:</strong>
            Scores above 570 represent Prime risk (auto-approve). Scores from 555 to 569 represent Moderate risk (approve with standard covenants). Scores between 535 and 554 require referral to an underwriter. Scores below 535 represent elevated default probability (&gt;25%) and are declined by policy.
          </div>
        </div>

        <div class="card">
          <div class="card-title">Scorecard Calibration Reference</div>
          <div class="table-container">
            <table>
              <thead>
                <tr>
                  <th>Risk Rating</th>
                  <th>Score Range</th>
                  <th>Est. Default Rate (PD)</th>
                  <th>Credit Policy Decision</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><span class="badge badge-green">Band 1 (Prime)</span></td>
                  <td><strong>570+</strong></td>
                  <td>&lt; 8.0%</td>
                  <td>Auto-Approve / Standard Terms</td>
                </tr>
                <tr>
                  <td><span class="badge badge-green">Band 2 (Moderate)</span></td>
                  <td><strong>555 – 569</strong></td>
                  <td>8.0% – 14.9%</td>
                  <td>Approve with Standard Covenants</td>
                </tr>
                <tr>
                  <td><span class="badge badge-amber">Band 3 (Watchlist)</span></td>
                  <td><strong>535 – 554</strong></td>
                  <td>15.0% – 25.0%</td>
                  <td>Refer to Senior Underwriter</td>
                </tr>
                <tr>
                  <td><span class="badge badge-red">Band 4 (Subprime)</span></td>
                  <td><strong>&lt; 535</strong></td>
                  <td>&gt; 25.0%</td>
                  <td>Decline Facility</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- TAB 2: EXPLAINABILITY -->
  <div id="pane-explain" class="tab-pane">
    <div class="card">
      <div class="card-title">
        Points Breakdown &amp; Explainability (Current Application)
        <span id="totalPointsBadge" class="badge badge-green">Total Score: 612</span>
      </div>
      <p style="color:var(--text-muted); font-size:0.9rem; margin-bottom:16px;">
        Under PRA and Basel regulatory standards, commercial credit risk models must provide transparent reasoning for credit decisions. 
        Below is the exact points attribution contributed by each characteristic of the current applicant.
      </p>

      <div class="table-container">
        <table id="explainTable">
          <thead>
            <tr>
              <th>Risk Characteristic</th>
              <th>Applicant Value</th>
              <th>Scorecard Points Contributed</th>
              <th>Impact Direction</th>
              <th>Information Value (IV)</th>
            </tr>
          </thead>
          <tbody id="explainTableBody">
            <!-- Populated dynamically via JS -->
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- TAB 3: MODEL PERFORMANCE -->
  <div id="pane-performance" class="tab-pane">
    <div class="grid-3" style="margin-bottom:24px;">
      <div class="metric-box">
        <div class="metric-label">Scorecard Test AUC</div>
        <div class="metric-value">0.7916</div>
        <div style="font-size:0.8rem; color:var(--text-muted); margin-top:4px;">Gini: 0.5833 (Strong discrimination)</div>
      </div>
      <div class="metric-box">
        <div class="metric-label">Challenger Gradient Boosting AUC</div>
        <div class="metric-value" style="color:var(--accent);">0.8432</div>
        <div style="font-size:0.8rem; color:var(--text-muted); margin-top:4px;">Gini: 0.6864 (+0.1031 non-linear lift)</div>
      </div>
      <div class="metric-box">
        <div class="metric-label">Scorecard KS Statistic</div>
        <div class="metric-value">0.4554</div>
        <div style="font-size:0.8rem; color:var(--text-muted); margin-top:4px;">Max separation between goods and bads</div>
      </div>
    </div>

    <!-- Visual Decile Calibration Chart -->
    <div class="card">
      <div class="card-title">Score Decile Calibration: Predicted PD vs Actual Default Rate</div>
      <p style="color:var(--text-muted); font-size:0.9rem; margin-bottom:12px;">
        Visual proof that the scorecard correctly orders risk: Decile 1 (safest borrowers) has only a 3.5% default rate, while Decile 10 (highest risk) reaches 59.9%.
      </p>
      <div class="chart-box">
        <svg viewBox="0 0 800 240" id="decileSvg">
          <!-- Rendered via JS -->
        </svg>
      </div>
      <div class="table-container" style="margin-top:16px;">
        <table>
          <thead>
            <tr>
              <th>Decile</th>
              <th>Score Range</th>
              <th>Loan Volume</th>
              <th>Avg Pred PD</th>
              <th>Actual Default Rate</th>
              <th>Total Defaults</th>
              <th>Share of Total Bads</th>
            </tr>
          </thead>
          <tbody id="decilesTableBody">
            <!-- Populated via JS -->
          </tbody>
        </table>
      </div>
    </div>

    <div class="card">
      <div class="card-title">Model Architecture Trade-Off: Scorecard vs Gradient Boosting</div>
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>Evaluation Dimension</th>
              <th>Logistic WoE Scorecard (Primary)</th>
              <th>HistGradientBoosting (Challenger)</th>
              <th>Banking Industry Rationale</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Discrimination (Gini / AUC)</strong></td>
              <td>Gini = 0.5833 (AUC = 0.7916)</td>
              <td>Gini = 0.6864 (AUC = 0.8432)</td>
              <td>Gradient boosting captures multi-variable interactions for +0.10 Gini lift.</td>
            </tr>
            <tr>
              <td><strong>Regulatory Transparency &amp; Explainability</strong></td>
              <td><span class="badge badge-green">100% Transparent</span></td>
              <td><span class="badge badge-amber">Complex Ensemble</span></td>
              <td>Scorecard assigns discrete integer points, enabling immediate customer adverse action explanations.</td>
            </tr>
            <tr>
              <td><strong>Operational Stability &amp; Monitoring</strong></td>
              <td><span class="badge badge-green">Simple PSI / CSI Tracking</span></td>
              <td><span class="badge badge-amber">Complex Feature Attribution</span></td>
              <td>Characteristic Stability Index (CSI) can be directly computed for every scorecard bin.</td>
            </tr>
            <tr>
              <td><strong>Underwriting Governance Role</strong></td>
              <td><strong>Approved Production Model</strong></td>
              <td><strong>Shadow / Challenger Model</strong></td>
              <td>Banks run the scorecard in front-office decisioning and use the challenger to detect uncaptured risk pockets.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- TAB 4: MODEL MONITORING -->
  <div id="pane-monitoring" class="tab-pane">
    <div class="card">
      <div class="card-title">
        Out-of-Time Model Monitoring &amp; Financial Crisis Stress Performance (FY2000–FY2009)
      </div>
      <p style="color:var(--text-muted); font-size:0.9rem; margin-bottom:16px;">
        Tracking the model across 604,786 commercial loans. The baseline is established on the Development cohort (FY2000–FY2004). 
        The Out-of-Time (OOT) cohorts (FY2005–FY2009) track the portfolio directly through the 2007–2008 Great Financial Crisis.
      </p>

      <!-- Visual PSI Crisis Drift Chart -->
      <div class="chart-box">
        <div style="font-weight:700; font-size:0.95rem; margin-bottom:8px; color:var(--text);">
          Population Stability Index (PSI) by Approval Cohort (Green &lt;0.10, Amber 0.10-0.25, Red &gt;0.25)
        </div>
        <svg viewBox="0 0 800 200" id="psiChartSvg">
          <!-- Rendered via JS -->
        </svg>
      </div>

      <div class="table-container" style="margin-top:20px;">
        <table>
          <thead>
            <tr>
              <th>Approval Cohort</th>
              <th>Sample Role</th>
              <th>Loan Volume</th>
              <th>Population Stability Index (PSI)</th>
              <th>PSI RAG</th>
              <th>Discrimination (Gini)</th>
              <th>Gini RAG</th>
              <th>Observed Default Rate</th>
              <th>Expected Default Rate</th>
              <th>O/E Calibration Ratio</th>
              <th>O/E RAG</th>
            </tr>
          </thead>
          <tbody id="monitoringTableBody">
            <!-- Populated via JS -->
          </tbody>
        </table>
      </div>
    </div>

    <div class="card">
      <div class="card-title">Characteristic Stability Index (CSI) Heatmap by Feature</div>
      <p style="color:var(--text-muted); font-size:0.9rem; margin-bottom:16px;">
        CSI detects which specific risk drivers shifted during the crisis period. Standard bank thresholds: Green (&lt;0.10), Amber (0.10–0.25), Red (&gt;0.25).
      </p>
      <div class="table-container">
        <table id="csiTable">
          <thead>
            <tr id="csiHeadRow">
              <th>Risk Characteristic</th>
              <!-- Years dynamically added -->
            </tr>
          </thead>
          <tbody id="csiBody">
            <!-- Populated via JS -->
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- TAB 5: PORTFOLIO SEGMENTS -->
  <div id="pane-portfolio" class="tab-pane">
    <div class="card">
      <div class="card-title">Commercial Default Rates by Industry Sector (604,786 Loans)</div>
      <p style="color:var(--text-muted); font-size:0.9rem; margin-bottom:16px;">
        Comparison of commercial default rates between the pre-crisis baseline (FY2000–2004) and peak financial crisis (FY2006–2008) across all major industry sectors.
      </p>
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>Industry Sector</th>
              <th>Total Portfolio Loans</th>
              <th>Baseline Default Rate (2000-04)</th>
              <th>Crisis Default Rate (2006-08)</th>
              <th>Crisis Default Surge</th>
              <th>Average Score</th>
            </tr>
          </thead>
          <tbody id="segmentIndustryBody">
            <!-- Populated via JS -->
          </tbody>
        </table>
      </div>
    </div>

    <div class="grid-2">
      <div class="card">
        <div class="card-title">Default Rate by Business Operating Age</div>
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>Business Age</th>
                <th>Total Loans</th>
                <th>Baseline (00-04)</th>
                <th>Crisis (06-08)</th>
                <th>Avg Score</th>
              </tr>
            </thead>
            <tbody id="segmentAgeBody"></tbody>
          </table>
        </div>
      </div>

      <div class="card">
        <div class="card-title">Default Rate by Facility Size</div>
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>Loan Amount Band</th>
                <th>Total Loans</th>
                <th>Baseline (00-04)</th>
                <th>Crisis (06-08)</th>
                <th>Avg Score</th>
              </tr>
            </thead>
            <tbody id="segmentAmtBody"></tbody>
          </table>
        </div>
      </div>
    </div>
  </div>

  <!-- TAB 6: UK MACRO CONTEXT -->
  <div id="pane-uk" class="tab-pane">
    <div class="card">
      <div class="card-title">🇬🇧 UK Corporate Insolvency Context (The Insolvency Service Official Statistics)</div>
      <p style="color:var(--text-muted); font-size:0.9rem; margin-bottom:16px;">
        Official company insolvency statistics in England &amp; Wales from 2000 to 2024, published under the Open Government Licence v3.0. 
        Demonstrates the parallel surge in corporate insolvencies during the 2008–2009 recession and recent macroeconomic pressures.
      </p>

      <!-- Visual UK Insolvency Chart -->
      <div class="chart-box">
        <div style="font-weight:700; font-size:0.95rem; margin-bottom:8px; color:var(--text);">
          UK Annual Company Insolvencies in England &amp; Wales (2000–2024)
        </div>
        <svg viewBox="0 0 800 200" id="ukChartSvg">
          <!-- Rendered via JS -->
        </svg>
      </div>

      <div class="table-container" style="margin-top:16px;">
        <table>
          <thead>
            <tr>
              <th>Year</th>
              <th>Total Company Insolvencies</th>
              <th>Creditors Voluntary Liquidations</th>
              <th>Compulsory Liquidations</th>
              <th>Administrations</th>
              <th>Economic Regime Context</th>
            </tr>
          </thead>
          <tbody id="ukInsolvencyBody">
            <!-- Populated via JS -->
          </tbody>
        </table>
      </div>
    </div>

    <div class="card">
      <div class="card-title">Data Governance, Provenance &amp; Validation</div>
      <ul style="font-size:0.9rem; color:var(--text-muted); line-height:1.7; padding-left:20px;">
        <li><strong>Commercial Loan Dataset:</strong> U.S. Small Business Administration (SBA) 7(a) FOIA Loan Program (data.sba.gov), containing 604,786 closed business loan facilities originated FY2000–FY2009.</li>
        <li><strong>UK Macroeconomic Dataset:</strong> The Insolvency Service (GOV.UK) long-run company insolvency statistics covering England &amp; Wales (2000–2024).</li>
        <li><strong>Information Governance:</strong> All data is public domain or licensed under Open Government Licence v3.0. All customer names and address identifiers were excluded. Post-origination target leakage fields (such as liquidation collateral flags) were strictly filtered out.</li>
        <li><strong>Automated Reconciliation:</strong> All model coefficients, scorecard points, PSI indices, and decile distributions are validated against independent Python calculation scripts with zero manual editing.</li>
      </ul>
    </div>
  </div>
</div>

<footer>
  Commercial Credit Risk Modelling &amp; Monitoring Platform &bull; Developed by <a href="https://github.com/Subramanian-MS" target="_blank" style="color:var(--primary); font-weight:700; text-decoration:none;">Subramanian Mathur Seetharaman</a> &bull; Built with Python (pandas, scikit-learn) &bull; Open Data Governance
</footer>

<script>
// Embedded Data Payload
const DATA = {payload_json};

// Robust Tab Switching
function switchTab(tabId, clickedBtn) {{
  document.querySelectorAll('.tab-pane').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
  
  const pane = document.getElementById('pane-' + tabId);
  if (pane) pane.classList.add('active');
  
  if (clickedBtn) {{
    clickedBtn.classList.add('active');
  }} else {{
    const btn = document.getElementById('tabBtn-' + tabId);
    if (btn) btn.classList.add('active');
  }}
}}

// Risk Checker Calculation
function scoreLoan() {{
  const model = DATA.model;
  const pts = model.scorecard_points;
  const scaling = model.scaling;

  const fields = [
    'term_band', 'loan_amt_band', 'guar_band', 'delivery_method',
    'is_revolver', 'same_state_bank', 'business_age', 'business_type',
    'industry', 'region', 'jobs_band'
  ];

  let totalScore = 0;
  const breakdown = [];

  fields.forEach(f => {{
    const el = document.getElementById(f);
    const val = el ? el.value : '';
    const pt = pts[f] && pts[f][val] !== undefined ? pts[f][val] : 0;
    totalScore += pt;
    breakdown.push({{
      feature: f,
      value: val,
      points: pt,
      iv: model.information_values[f]
    }});
  }});

  // Compute PD: p = 1 / (1 + exp((score - offset) / factor))
  const offset = scaling.offset;
  const factor = scaling.factor;
  const pd = 1.0 / (1.0 + Math.exp((totalScore - offset) / factor));

  // Update UI
  document.getElementById('scoreDisplay').innerText = totalScore;
  document.getElementById('pdDisplay').innerText = (pd * 100).toFixed(1) + '%';
  document.getElementById('totalPointsBadge').innerText = 'Total Score: ' + totalScore;

  const hero = document.getElementById('decisionHero');
  const badge = document.getElementById('riskBandBadge');
  const decisionText = document.getElementById('decisionText');
  const decisionSub = document.getElementById('decisionSub');
  const policyAction = document.getElementById('policyAction');

  hero.className = 'decision-hero';
  badge.className = 'badge';

  if (totalScore >= 570) {{
    hero.classList.add('hero-approve');
    badge.classList.add('badge-green');
    badge.innerText = 'Band 1 | Prime (Low Risk)';
    decisionText.innerText = 'AUTO-APPROVE FACILITY';
    decisionSub.innerText = 'Application comfortably exceeds policy threshold. Fast-track automated onboarding.';
    policyAction.innerText = 'Auto-Approve';
    policyAction.style.color = 'var(--green)';
  }} else if (totalScore >= 555) {{
    hero.classList.add('hero-approve');
    badge.classList.add('badge-green');
    badge.innerText = 'Band 2 | Moderate Risk';
    decisionText.innerText = 'APPROVE (STANDARD TERMS)';
    decisionSub.innerText = 'Application meets credit requirements. Proceed with standard facility documentation.';
    policyAction.innerText = 'Standard Sign-Off';
    policyAction.style.color = 'var(--green)';
  }} else if (totalScore >= 535) {{
    hero.classList.add('hero-refer');
    badge.classList.add('badge-amber');
    badge.innerText = 'Band 3 | Elevated Watchlist';
    decisionText.innerText = 'REFER TO UNDERWRITER';
    decisionSub.innerText = 'Score falls into referral corridor. Requires review of cash flow and collateral security.';
    policyAction.innerText = 'Manual Review';
    policyAction.style.color = 'var(--amber)';
  }} else {{
    hero.classList.add('hero-decline');
    badge.classList.add('badge-red');
    badge.innerText = 'Band 4 | Subprime / High Risk';
    decisionText.innerText = 'DECLINE FACILITY';
    decisionSub.innerText = 'Application exceeds maximum acceptable default probability for standard commercial lending.';
    policyAction.innerText = 'Policy Decline';
    policyAction.style.color = 'var(--red)';
  }}

  // Populate Explainability Table
  const explainBody = document.getElementById('explainTableBody');
  if (explainBody) {{
    explainBody.innerHTML = '';
    const labelMap = {{
      term_band: 'Loan Term / Amortisation',
      loan_amt_band: 'Gross Facility Amount',
      guar_band: 'Scheme Guarantee Coverage',
      delivery_method: 'Processing / Delivery Channel',
      is_revolver: 'Facility Structure (Revolver/Term)',
      same_state_bank: 'Lender Relationship (Local vs Remote)',
      business_age: 'Operating Track Record',
      business_type: 'Legal Entity Structure',
      industry: 'Industry Sector',
      region: 'Geographic Region',
      jobs_band: 'Employment / Headcount'
    }};

    breakdown.forEach(item => {{
      const tr = document.createElement('tr');
      const impactHtml = item.points >= 50 
        ? '<span style="color:var(--green); font-weight:600;">▲ Favourable (+Points)</span>' 
        : '<span style="color:var(--amber); font-weight:600;">▼ Higher Risk</span>';

      tr.innerHTML = `
        <td><strong>${{labelMap[item.feature] || item.feature}}</strong></td>
        <td>${{item.value}}</td>
        <td><strong>${{item.points}} pts</strong></td>
        <td>${{impactHtml}}</td>
        <td>IV = ${{item.iv.toFixed(4)}}</td>
      `;
      explainBody.appendChild(tr);
    }});
  }}
}}

// Draw Visual SVG Charts
function drawCharts() {{
  // 1. Decile Calibration Chart (SVG)
  const decSvg = document.getElementById('decileSvg');
  if (decSvg && DATA.model.deciles) {{
    const decs = DATA.model.deciles;
    let svgHtml = `
      <line x1="60" y1="20" x2="60" y2="190" stroke="#cbd5e1" stroke-width="1.5" />
      <line x1="60" y1="190" x2="780" y2="190" stroke="#cbd5e1" stroke-width="1.5" />
      <text x="60" y="15" fill="#64748b" font-size="11" font-weight="600">Default Rate (%)</text>
    `;
    const w = 68;
    decs.forEach((d, i) => {{
      const x = 75 + i * w;
      const rate = d.actual_default_rate * 100;
      const h = Math.min(160, (rate / 65) * 160);
      const y = 190 - h;
      const color = rate < 10 ? '#15803d' : (rate < 25 ? '#b45309' : '#b91c1c');
      
      svgHtml += `
        <rect x="${{x}}" y="${{y}}" width="48" height="${{h}}" fill="${{color}}" rx="4" />
        <text x="${{x + 24}}" y="${{y - 6}}" text-anchor="middle" font-size="10" font-weight="700" fill="${{color}}">${{rate.toFixed(1)}}%</text>
        <text x="${{x + 24}}" y="205" text-anchor="middle" font-size="10" fill="#64748b">D${{d.decile}}</text>
      `;
    }});
    decSvg.innerHTML = svgHtml;
  }}

  // 2. PSI Yearly Chart (SVG)
  const psiSvg = document.getElementById('psiChartSvg');
  if (psiSvg && DATA.monitoring.psi_by_year) {{
    const rows = DATA.monitoring.psi_by_year;
    let svgHtml = `
      <line x1="50" y1="20" x2="50" y2="160" stroke="#cbd5e1" stroke-width="1.5" />
      <line x1="50" y1="160" x2="780" y2="160" stroke="#cbd5e1" stroke-width="1.5" />
      <!-- Threshold lines -->
      <line x1="50" y1="100" x2="780" y2="100" stroke="#b45309" stroke-dasharray="4,4" stroke-width="1" />
      <text x="785" y="103" font-size="10" fill="#b45309">0.10 Amber</text>
    `;
    const w = 68;
    rows.forEach((r, i) => {{
      const x = 70 + i * w;
      const h = Math.min(130, (r.psi / 0.25) * 130);
      const y = 160 - h;
      const color = r.rag === 'GREEN' ? '#15803d' : (r.rag === 'AMBER' ? '#b45309' : '#b91c1c');

      svgHtml += `
        <rect x="${{x}}" y="${{y}}" width="44" height="${{h}}" fill="${{color}}" rx="4" />
        <text x="${{x + 22}}" y="${{y - 6}}" text-anchor="middle" font-size="10" font-weight="700" fill="${{color}}">${{r.psi.toFixed(3)}}</text>
        <text x="${{x + 22}}" y="176" text-anchor="middle" font-size="10" fill="#64748b">'0${{r.fy % 100}}</text>
      `;
    }});
    psiSvg.innerHTML = svgHtml;
  }}

  // 3. UK Insolvencies Chart (SVG)
  const ukSvg = document.getElementById('ukChartSvg');
  if (ukSvg && DATA.uk_insolvency) {{
    const uk = DATA.uk_insolvency;
    let svgHtml = `
      <line x1="60" y1="20" x2="60" y2="160" stroke="#cbd5e1" stroke-width="1.5" />
      <line x1="60" y1="160" x2="780" y2="160" stroke="#cbd5e1" stroke-width="1.5" />
    `;
    const maxVal = 26000;
    const w = 27;
    uk.forEach((row, i) => {{
      const x = 75 + i * w;
      const h = Math.min(135, (row.total_insolvencies / maxVal) * 135);
      const y = 160 - h;
      const isPeak = row.year === 2009 || row.year >= 2022;
      const color = isPeak ? '#b91c1c' : '#1976d2';

      svgHtml += `
        <rect x="${{x}}" y="${{y}}" width="18" height="${{h}}" fill="${{color}}" rx="2" />
        <text x="${{x + 9}}" y="176" text-anchor="middle" font-size="8" fill="#64748b">'${{String(row.year).slice(2)}}</text>
      `;
    }});
    ukSvg.innerHTML = svgHtml;
  }}
}}

// Initialise Dashboard Tables
function initDashboard() {{
  // 1. Deciles table
  const decilesBody = document.getElementById('decilesTableBody');
  if (decilesBody && DATA.model.deciles) {{
    decilesBody.innerHTML = '';
    DATA.model.deciles.forEach(d => {{
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td><strong>Decile ${{d.decile}}</strong></td>
        <td>${{d.min_score}} – ${{d.max_score}}</td>
        <td>${{d.count.toLocaleString()}}</td>
        <td>${{(d.avg_pred_pd * 100).toFixed(1)}}%</td>
        <td><strong>${{(d.actual_default_rate * 100).toFixed(1)}}%</strong></td>
        <td>${{d.bads.toLocaleString()}}</td>
        <td>${{(d.bad_share * 100).toFixed(1)}}%</td>
      `;
      decilesBody.appendChild(tr);
    }});
  }}

  // 2. Monitoring table
  const monBody = document.getElementById('monitoringTableBody');
  if (monBody && DATA.monitoring.psi_by_year) {{
    monBody.innerHTML = '';
    DATA.monitoring.psi_by_year.forEach((row, idx) => {{
      const cal = DATA.monitoring.calibration_by_year[idx];
      const gini = DATA.monitoring.gini_by_year[idx];
      const tr = document.createElement('tr');
      const roleBadge = row.is_dev 
        ? '<span class="badge badge-light" style="color:#0f172a; border:1px solid #cbd5e1;">Dev Baseline</span>' 
        : '<span class="badge badge-amber">Out-of-Time Stress</span>';

      tr.innerHTML = `
        <td><strong>FY${{row.fy}}</strong></td>
        <td>${{roleBadge}}</td>
        <td>${{row.n_loans.toLocaleString()}}</td>
        <td>${{row.psi.toFixed(4)}}</td>
        <td><span class="rag-pill rag-${{row.rag}}">${{row.rag}}</span></td>
        <td>${{gini.gini.toFixed(4)}}</td>
        <td><span class="rag-pill rag-${{gini.rag}}">${{gini.rag}}</span></td>
        <td><strong>${{(cal.observed_default_rate * 100).toFixed(1)}}%</strong></td>
        <td>${{(cal.expected_default_rate * 100).toFixed(1)}}%</td>
        <td>${{cal.oe_ratio.toFixed(2)}}x</td>
        <td><span class="rag-pill rag-${{cal.rag}}">${{cal.rag}}</span></td>
      `;
      monBody.appendChild(tr);
    }});
  }}

  // 3. CSI Table
  const csiHead = document.getElementById('csiHeadRow');
  const csiBody = document.getElementById('csiBody');
  if (csiHead && csiBody && DATA.monitoring.csi_by_feature) {{
    const years = [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009];
    years.forEach(y => {{
      const th = document.createElement('th');
      th.innerText = 'FY' + y;
      csiHead.appendChild(th);
    }});

    const csiData = DATA.monitoring.csi_by_feature;
    Object.keys(csiData).forEach(feat => {{
      const tr = document.createElement('tr');
      let tdHtml = `<td><strong>${{feat}}</strong></td>`;
      csiData[feat].forEach(pt => {{
        tdHtml += `<td><span class="rag-pill rag-${{pt.rag}}" title="${{pt.csi.toFixed(4)}}">${{pt.csi.toFixed(3)}}</span></td>`;
      }});
      tr.innerHTML = tdHtml;
      csiBody.appendChild(tr);
    }});
  }}

  // 4. Portfolio Segments
  const indBody = document.getElementById('segmentIndustryBody');
  if (indBody && DATA.monitoring.segments.industry) {{
    indBody.innerHTML = '';
    DATA.monitoring.segments.industry.sort((a,b) => b.default_rate_crisis - a.default_rate_crisis).forEach(row => {{
      const surge = ((row.default_rate_crisis - row.default_rate_dev) * 100).toFixed(1);
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td><strong>${{row.industry}}</strong></td>
        <td>${{row.total_loans.toLocaleString()}}</td>
        <td>${{(row.default_rate_dev * 100).toFixed(1)}}%</td>
        <td><strong style="color:var(--red);">${{(row.default_rate_crisis * 100).toFixed(1)}}%</strong></td>
        <td>+${{surge}} pp</td>
        <td>${{row.avg_score}}</td>
      `;
      indBody.appendChild(tr);
    }});
  }}

  const ageBody = document.getElementById('segmentAgeBody');
  if (ageBody && DATA.monitoring.segments.business_age) {{
    ageBody.innerHTML = '';
    DATA.monitoring.segments.business_age.forEach(row => {{
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td><strong>${{row.business_age}}</strong></td>
        <td>${{row.total_loans.toLocaleString()}}</td>
        <td>${{(row.default_rate_dev * 100).toFixed(1)}}%</td>
        <td><strong>${{(row.default_rate_crisis * 100).toFixed(1)}}%</strong></td>
        <td>${{row.avg_score}}</td>
      `;
      ageBody.appendChild(tr);
    }});
  }}

  const amtBody = document.getElementById('segmentAmtBody');
  if (amtBody && DATA.monitoring.segments.loan_amt_band) {{
    amtBody.innerHTML = '';
    DATA.monitoring.segments.loan_amt_band.forEach(row => {{
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td><strong>${{row.loan_amt_band}}</strong></td>
        <td>${{row.total_loans.toLocaleString()}}</td>
        <td>${{(row.default_rate_dev * 100).toFixed(1)}}%</td>
        <td><strong>${{(row.default_rate_crisis * 100).toFixed(1)}}%</strong></td>
        <td>${{row.avg_score}}</td>
      `;
      amtBody.appendChild(tr);
    }});
  }}

  // 5. UK Insolvency Table
  const ukBody = document.getElementById('ukInsolvencyBody');
  if (ukBody && DATA.uk_insolvency) {{
    ukBody.innerHTML = '';
    DATA.uk_insolvency.forEach(row => {{
      let note = 'Normal trading conditions';
      if (row.year === 2008 || row.year === 2009) note = '⚠️ Great Financial Crisis spike';
      if (row.year === 2020 || row.year === 2021) note = 'Covid emergency support (temporary suppression)';
      if (row.year >= 2022) note = 'Post-Covid inflation & rate tightening surge';

      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td><strong>${{row.year}}</strong></td>
        <td><strong>${{row.total_insolvencies.toLocaleString()}}</strong></td>
        <td>${{row.creditors_voluntary_liquidations.toLocaleString()}}</td>
        <td>${{row.compulsory_liquidations.toLocaleString()}}</td>
        <td>${{row.administrations.toLocaleString()}}</td>
        <td><span style="font-size:0.82rem; color:var(--text-muted);">${{note}}</span></td>
      `;
      ukBody.appendChild(tr);
    }});
  }}

  // Draw SVG Charts
  drawCharts();

  // Run initial scoring calculation
  scoreLoan();
}}

window.addEventListener('DOMContentLoaded', initDashboard);
</script>

</body>
</html>
'''

    with open(OUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Generated {OUT_HTML} ({len(html_content):,} bytes)")

if __name__ == '__main__':
    build_app()
