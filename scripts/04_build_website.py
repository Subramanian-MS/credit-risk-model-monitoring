"""
04_build_website.py
Merges model metrics, scorecard points, monitoring tables, and UK insolvency series
into an embeddable JSON payload and generates a self-contained, responsive, professional
HTML web application for commercial credit risk decisioning and model monitoring.
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
      max-width: 1200px;
      margin: 0 auto;
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
      font-weight: 700;
      margin-bottom: 8px;
      letter-spacing: -0.02em;
    }}
    header p {{
      color: #e2e8f0;
      font-size: 0.95rem;
      max-width: 900px;
    }}

    .container {{
      max-width: 1200px;
      margin: 0 auto;
      padding: 24px;
    }}

    /* Tab Navigation */
    .nav-tabs {{
      display: flex;
      gap: 6px;
      border-bottom: 2px solid var(--border);
      margin-bottom: 24px;
      overflow-x: auto;
      scrollbar-width: none;
    }}
    .nav-tabs::-webkit-scrollbar {{ display: none; }}
    .tab-btn {{
      background: none;
      border: none;
      padding: 12px 18px;
      font-size: 0.92rem;
      font-weight: 600;
      color: var(--text-muted);
      cursor: pointer;
      border-bottom: 3px solid transparent;
      margin-bottom: -2px;
      white-space: nowrap;
      transition: all 0.2s ease;
    }}
    .tab-btn:hover {{ color: var(--primary); }}
    .tab-btn.active {{
      color: var(--primary);
      border-bottom-color: var(--primary);
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
    .grid-4 {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
    }}
    @media (max-width: 900px) {{
      .grid-2, .grid-3, .grid-4 {{ grid-template-columns: 1fr; }}
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
    .form-select, .form-input {{
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
    .form-select:focus, .form-input:focus {{
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

    /* SVG Charts */
    .chart-container {{
      width: 100%;
      margin: 16px 0;
    }}
    svg {{
      width: 100%;
      height: auto;
      font-family: var(--font);
    }}
    .grid-line {{ stroke: #e2e8f0; stroke-dasharray: 4,4; stroke-width: 1; }}
    .axis-text {{ font-size: 11px; fill: #64748b; }}
    .legend-text {{ font-size: 12px; fill: #334155; }}

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
      padding: 24px;
      color: var(--text-muted);
      font-size: 0.85rem;
      border-top: 1px solid var(--border);
      margin-top: 40px;
    }}
  </style>
</head>
<body>

<header>
  <div class="header-content">
    <div style="font-size: 0.88rem; color: #a7f3d0; margin-bottom: 6px; font-weight: 600; letter-spacing: 0.02em;">Developed by Subramanian Mathur Seetharaman</div>
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
  <!-- Tabs -->
  <div class="nav-tabs" role="tablist">
    <button class="tab-btn active" onclick="showTab('checker')">🎯 Risk Checker</button>
    <button class="tab-btn" onclick="showTab('explain')">🔍 Scorecard Explainability</button>
    <button class="tab-btn" onclick="showTab('performance')">📈 Model Performance & Comparison</button>
    <button class="tab-btn" onclick="showTab('monitoring')">⚠️ Out-of-Time Monitoring (PSI / CSI)</button>
    <button class="tab-btn" onclick="showTab('portfolio')">🏢 Portfolio Segments</button>
    <button class="tab-btn" onclick="showTab('uk')">🇬🇧 UK Macro Context & Governance</button>
  </div>

  <!-- TAB 1: RISK CHECKER -->
  <div id="pane-checker" class="tab-pane active">
    <div class="grid-2">
      <!-- Form Input -->
      <div class="card">
        <div class="card-title">Business Loan Application Details</div>
        <form id="loanForm" onchange="scoreLoan()">
          <div class="form-group">
            <label class="form-label">Loan Term (Duration)</label>
            <select class="form-select" id="term_band">
              <option value="Short (<36m)">Short (<36 months - Working capital / Bridge)</option>
              <option value="Medium (36-60m)">Medium (36–60 months - Equipment / Vehicles)</option>
              <option value="Long (61-120m)" selected>Long (61–120 months - Expansion term loan)</option>
              <option value="Real Estate / Extended (>120m)">Real Estate / Extended (>120 months)</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">Gross Facility Amount</label>
            <select class="form-select" id="loan_amt_band">
              <option value="<$25k">Micro (<$25,000)</option>
              <option value="$25k-$50k">$25,000 – $50,000</option>
              <option value="$50k-$100k" selected>$50,000 – $100,000</option>
              <option value="$100k-$250k">$100,000 – $250,000</option>
              <option value="$250k-$500k">$250,000 – $500,000</option>
              <option value=">$500k">Large Commercial (>$500,000)</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">SBA / Scheme Guarantee Coverage</label>
            <select class="form-select" id="guar_band">
              <option value="Low (<=50%)">Low Guarantee (<=50% - High bank risk)</option>
              <option value="Moderate (51-74%)">Moderate (51%–74%)</option>
              <option value="Standard (75-80%)" selected>Standard Scheme Guarantee (75%–80%)</option>
              <option value="High (>80%)">High Guarantee (>80% - Government backed)</option>
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
            <label class="form-label">Origination / Delivery Method</label>
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
            <label class="form-label">Industry Sector (NAICS)</label>
            <select class="form-select" id="industry">
              <option value="Accommodation & Food Services">Accommodation & Food Services (Restaurants, Bars, Hotels)</option>
              <option value="Retail Trade (Motor, Furniture, Electronics, Food)" selected>Retail Trade</option>
              <option value="Construction">Construction & Contracting</option>
              <option value="Manufacturing (Metal, Machinery, Electronics)">Manufacturing (Machinery, Metal, Electronics)</option>
              <option value="Manufacturing (Food, Textiles, Apparel)">Manufacturing (Food, Textiles, Goods)</option>
              <option value="Professional, Scientific & Technical Services">Professional, Scientific & Technical</option>
              <option value="Health Care & Social Assistance">Healthcare & Social Services</option>
              <option value="Transportation & Warehousing">Transportation & Logistics</option>
              <option value="Wholesale Trade">Wholesale Trade</option>
              <option value="Other Services (Repair, Personal, Laundry)">Other Personal Services</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">Business Operating Track Record</label>
            <select class="form-select" id="business_age">
              <option value="Established (5+ Years)" selected>Established (5+ Years trading)</option>
              <option value="Young (1-4 Years)">Young (1–4 Years trading)</option>
              <option value="New (<1 Year)">New (<1 Year trading)</option>
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
            <label class="form-label">Lending Relationship</label>
            <select class="form-select" id="same_state_bank">
              <option value="Local Bank (Same State)" selected>Local Relationship Bank (Same State)</option>
              <option value="Out-of-State Bank">Out-of-State / National Remote Lender</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">Project Geographic Region</label>
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
              <option value=">10 Jobs">>10 Jobs</option>
            </select>
          </div>
        </form>
      </div>

      <!-- Decision & Output -->
      <div>
        <div class="card">
          <div class="card-title">Credit Risk Decision & Score</div>
          <div id="decisionHero" class="decision-hero hero-approve">
            <div id="riskBandBadge" class="badge badge-green">Low Risk | Prime Band</div>
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
              <div class="metric-label">Benchmark Default</div>
              <div class="metric-value" style="color:var(--text-muted);">15.7%</div>
            </div>
            <div class="metric-box">
              <div class="metric-label">Policy Action</div>
              <div id="policyAction" class="metric-value" style="font-size:1.1rem; color:var(--green); margin-top:10px;">Fast-Track</div>
            </div>
          </div>

          <div class="info-callout" style="margin-top:20px;">
            <strong>Underwriting Guidance:</strong>
            Scores above 565 indicate acceptable risk for standard pricing. Facilities scoring between 540 and 564 require secondary review by a commercial underwriter. Scores below 540 fall into elevated risk bands requiring enhanced security or decline.
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
        Points Breakdown & Explainability (Current Application)
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

    <div class="card">
      <div class="card-title">Score Decile Calibration (Test Sample - 74,957 loans)</div>
      <p style="color:var(--text-muted); font-size:0.9rem; margin-bottom:16px;">
        Deciles ranked from Lowest Risk (Decile 1) to Highest Risk (Decile 10). Demonstrates monotonic risk ordering and tight calibration between predicted PD and observed default rates.
      </p>
      <div class="table-container">
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
              <td>Gradient boosting captures complex multi-variable interactions for +0.10 Gini lift.</td>
            </tr>
            <tr>
              <td><strong>Regulatory Transparency & Explainability</strong></td>
              <td><span class="badge badge-green">100% Transparent</span></td>
              <td><span class="badge badge-amber">Opaque / Complex Ensemble</span></td>
              <td>Scorecard assigns discrete points to each bin, enabling immediate customer adverse action explanations.</td>
            </tr>
            <tr>
              <td><strong>Operational Stability & Monitoring</strong></td>
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
        Out-of-Time Model Monitoring & Financial Crisis Stress Performance (FY2000–FY2009)
      </div>
      <p style="color:var(--text-muted); font-size:0.9rem; margin-bottom:16px;">
        Tracking the model across 604,786 commercial loans. The baseline is established on the Development cohort (FY2000–FY2004). 
        The Out-of-Time (OOT) cohorts (FY2005–FY2009) track the portfolio directly through the 2007–2008 Great Financial Crisis.
      </p>

      <div class="table-container">
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
      <div class="card-title">Commercial Default Rates by Industry Sector</div>
      <p style="color:var(--text-muted); font-size:0.9rem; margin-bottom:16px;">
        Comparison of default rates between the pre-crisis baseline (FY2000–2004) and peak financial crisis (FY2006–2008).
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
        <div class="card-title">Default Rate by Business Age</div>
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>Business Age</th>
                <th>Loans</th>
                <th>Baseline</th>
                <th>Crisis (06-08)</th>
                <th>Avg Score</th>
              </tr>
            </thead>
            <tbody id="segmentAgeBody"></tbody>
          </table>
        </div>
      </div>

      <div class="card">
        <div class="card-title">Default Rate by Loan Facility Size</div>
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>Loan Amount Band</th>
                <th>Loans</th>
                <th>Baseline</th>
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
        Official company insolvency statistics in England & Wales from 2000 to 2024, published under the Open Government Licence v3.0. 
        Demonstrates the parallel surge in corporate insolvencies during the 2008–2009 recession and recent macroeconomic pressures.
      </p>
      <div class="table-container">
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
      <div class="card-title">Data Governance, Provenance & Validation</div>
      <ul style="font-size:0.9rem; color:var(--text-muted); line-height:1.7; padding-left:20px;">
        <li><strong>Commercial Loan Dataset:</strong> U.S. Small Business Administration (SBA) 7(a) FOIA Loan Program (data.sba.gov), containing 604,786 closed business loan facilities originated FY2000–FY2009.</li>
        <li><strong>UK Macroeconomic Dataset:</strong> The Insolvency Service (GOV.UK) long-run company insolvency statistics covering England & Wales (2000–2024).</li>
        <li><strong>Information Governance:</strong> All data is public domain or licensed under Open Government Licence v3.0. All customer names and address identifiers were excluded. Post-origination target leakage fields (such as liquidation collateral flags) were strictly filtered out.</li>
        <li><strong>Automated Reconciliation:</strong> All model coefficients, scorecard points, PSI indices, and decile distributions are validated against independent Python calculation scripts with zero manual editing.</li>
      </ul>
    </div>
  </div>
</div>

<footer>
  Commercial Credit Risk Modelling &amp; Monitoring Platform &bull; Developed by <a href="https://github.com/Subramanian-MS" target="_blank" style="color:var(--primary); font-weight:600; text-decoration:none;">Subramanian Mathur Seetharaman</a> &bull; Built with Python (pandas, scikit-learn) &bull; Open Data Governance
</footer>

<script>
// Embedded Data Payload
const DATA = {payload_json};

function showTab(tabId) {{
  document.querySelectorAll('.tab-pane').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
  document.getElementById('pane-' + tabId).classList.add('active');
  event.target.classList.add('active');
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
    const val = document.getElementById(f).value;
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
