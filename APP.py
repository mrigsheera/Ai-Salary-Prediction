import streamlit as st
import requests

# ─── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Salary Predictor",
    page_icon="💼",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: #05091A !important;
    color: #E2E8F5 !important;
}
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse at 20% 30%, rgba(124,58,237,0.18) 0%, transparent 55%),
        radial-gradient(ellipse at 80% 10%, rgba(59,130,246,0.14) 0%, transparent 55%),
        radial-gradient(ellipse at 60% 80%, rgba(26,86,219,0.10) 0%, transparent 55%),
        #05091A !important;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { display: none !important; }
#MainMenu { display: none !important; }
footer { display: none !important; }

h1, h2, h3, h4 { font-family: 'Syne', sans-serif !important; }
p, label, span, div { font-family: 'DM Sans', sans-serif !important; }

.block-container { max-width: 780px !important; padding: 0 1.5rem 3rem !important; }

/* Navbar */
.navbar { display:flex; align-items:center; justify-content:space-between; padding:1.1rem 0 2rem; border-bottom:1px solid rgba(255,255,255,0.06); margin-bottom:0.5rem; }
.navbar-logo { display:flex; align-items:center; gap:10px; }
.logo-icon { width:34px; height:34px; background:linear-gradient(135deg,#7C3AED,#3B82F6); border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:15px; position:relative; }
.logo-dot { position:absolute; top:-3px; right:-3px; width:9px; height:9px; background:#A78BFA; border-radius:50%; border:2px solid #05091A; animation:pulse-dot 2s ease-in-out infinite; }
@keyframes pulse-dot { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.5;transform:scale(0.8)} }
.logo-text { font-family:'Syne',sans-serif !important; font-weight:700; font-size:1rem; color:#fff; letter-spacing:-0.02em; }
.navbar-links { display:flex; align-items:center; gap:8px; }
.nav-link { display:inline-flex; align-items:center; gap:6px; padding:7px 14px; border-radius:10px; font-family:'DM Sans',sans-serif !important; font-size:0.82rem; font-weight:500; color:#94A3C8; text-decoration:none; border:1px solid rgba(255,255,255,0.06); background:rgba(255,255,255,0.03); }

/* Hero */
.hero { text-align:center; padding:3.5rem 0 2.5rem; }
.hero-badge { display:inline-flex; align-items:center; gap:8px; padding:7px 16px; border-radius:50px; background:rgba(124,58,237,0.1); border:1px solid rgba(124,58,237,0.25); font-family:'JetBrains Mono',monospace !important; font-size:0.72rem; color:#A78BFA; margin-bottom:1.4rem; letter-spacing:0.02em; }
.badge-dot { width:7px; height:7px; background:#8B5CF6; border-radius:50%; animation:pulse-dot 2s ease-in-out infinite; }
.hero-title { font-family:'Syne',sans-serif !important; font-size:clamp(2.6rem,6vw,4rem) !important; font-weight:800 !important; line-height:1.1 !important; letter-spacing:-0.03em !important; color:#fff !important; margin:0 0 1rem !important; }
.gradient-text { background:linear-gradient(135deg,#60A5FA 0%,#8B5CF6 50%,#A78BFA 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
.hero-sub { font-size:1.05rem; color:#94A3C8; max-width:520px; margin:0 auto 1.8rem; line-height:1.6; font-weight:300; }
.model-pills { display:flex; flex-wrap:wrap; align-items:center; justify-content:center; gap:8px; margin-bottom:1.5rem; }
.model-pill { display:inline-flex; align-items:center; gap:6px; padding:5px 12px; border-radius:50px; font-family:'JetBrains Mono',monospace !important; font-size:0.72rem; font-weight:500; }
.pill-rf { background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.2); color:#6EE7B7; }
.pill-gb { background:rgba(59,130,246,0.1); border:1px solid rgba(59,130,246,0.2); color:#93C5FD; }
.pill-et { background:rgba(139,92,246,0.1); border:1px solid rgba(139,92,246,0.2); color:#C4B5FD; }
.pill-dot { width:6px; height:6px; border-radius:50%; }
.pill-rf .pill-dot { background:#10B981; }
.pill-gb .pill-dot { background:#3B82F6; }
.pill-et .pill-dot { background:#8B5CF6; }
.stat-row { display:flex; flex-wrap:wrap; align-items:center; justify-content:center; gap:10px; }
.stat-badge { display:inline-flex; align-items:center; gap:8px; padding:8px 16px; border-radius:12px; background:rgba(15,32,64,0.6); border:1px solid rgba(255,255,255,0.06); }
.stat-value { font-family:'Syne',sans-serif !important; font-size:1rem; font-weight:700; background:linear-gradient(135deg,#60A5FA,#8B5CF6); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
.stat-label { font-size:0.78rem; color:#64748B; }

/* Divider */
.section-divider { display:flex; align-items:center; gap:12px; margin:0.5rem 0 1.5rem; }
.divider-line { flex:1; height:1px; background:rgba(255,255,255,0.06); }
.divider-text { font-family:'Syne',sans-serif !important; font-size:0.7rem; font-weight:600; text-transform:uppercase; letter-spacing:0.12em; color:#475569; }

/* Form card */
.form-card { background:rgba(10,22,48,0.55); border:1px solid rgba(255,255,255,0.07); border-radius:20px; padding:2rem 2rem 1.5rem; position:relative; overflow:hidden; backdrop-filter:blur(12px); }
.form-header { display:flex; align-items:center; gap:12px; margin-bottom:1.6rem; }
.form-icon { width:38px; height:38px; background:linear-gradient(135deg,#7C3AED,#2563EB); border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:17px; }
.form-title { font-family:'Syne',sans-serif !important; font-size:1rem; font-weight:700; color:#fff; margin:0; }
.form-sub { font-size:0.78rem; color:#64748B; margin:2px 0 0; }

/* Streamlit widgets */
[data-testid="stSelectbox"] label, [data-testid="stNumberInput"] label {
    font-family:'Syne',sans-serif !important; font-size:0.68rem !important; font-weight:600 !important;
    text-transform:uppercase !important; letter-spacing:0.1em !important; color:#64748B !important; margin-bottom:6px !important;
}
[data-testid="stSelectbox"] > div > div, [data-testid="stNumberInput"] input {
    background:rgba(5,15,35,0.7) !important; border:1px solid rgba(255,255,255,0.08) !important;
    border-radius:12px !important; color:#CBD5E1 !important; font-family:'DM Sans',sans-serif !important; font-size:0.88rem !important;
}
[data-testid="stSelectbox"] > div > div:hover { border-color:rgba(139,92,246,0.35) !important; }
[data-testid="stSelectbox"] > div > div:focus-within { border-color:rgba(139,92,246,0.6) !important; box-shadow:0 0 0 3px rgba(139,92,246,0.1) !important; }
[data-testid="stSelectbox"] ul { background:#0D1B38 !important; border:1px solid rgba(255,255,255,0.08) !important; border-radius:12px !important; }
[data-testid="stSelectbox"] ul li:hover { background:rgba(139,92,246,0.15) !important; }

/* Button */
[data-testid="stButton"] button {
    width:100% !important; padding:14px 24px !important; border-radius:14px !important;
    background:linear-gradient(135deg,#7C3AED 0%,#6D28D9 40%,#2563EB 100%) !important;
    border:none !important; color:#fff !important; font-family:'Syne',sans-serif !important;
    font-size:1rem !important; font-weight:700 !important; cursor:pointer !important;
    box-shadow:0 4px 24px rgba(124,58,237,0.3) !important; margin-top:0.5rem !important;
    transition:all 0.25s ease !important;
}
[data-testid="stButton"] button:hover { transform:translateY(-1px) !important; box-shadow:0 8px 36px rgba(124,58,237,0.45) !important; filter:brightness(1.08) !important; }

/* Result card */
.result-card { border-radius:20px; overflow:hidden; margin-top:1.6rem; animation:slideUp 0.5s cubic-bezier(0.16,1,0.3,1) forwards; }
@keyframes slideUp { from{opacity:0;transform:translateY(20px)} to{opacity:1;transform:translateY(0)} }
.result-inner { background:rgba(10,22,48,0.7); border:1px solid rgba(255,255,255,0.08); border-top:none; border-radius:0 0 20px 20px; padding:1.6rem 2rem 1.8rem; }
.result-accent { height:4px; width:100%; border-radius:20px 20px 0 0; }
.result-header { display:flex; align-items:center; justify-content:space-between; margin-bottom:1.2rem; }
.result-label-row { display:flex; align-items:center; gap:10px; }
.result-icon { width:30px; height:30px; border-radius:9px; display:flex; align-items:center; justify-content:center; font-size:14px; }
.result-label { font-family:'Syne',sans-serif !important; font-size:0.7rem; font-weight:600; text-transform:uppercase; letter-spacing:0.12em; color:#64748B; }
.result-tag { display:inline-flex; align-items:center; gap:6px; padding:4px 10px; border-radius:50px; background:rgba(139,92,246,0.12); border:1px solid rgba(139,92,246,0.2); font-family:'JetBrains Mono',monospace !important; font-size:0.68rem; color:#A78BFA; }
.salary-display { margin-bottom:1.4rem; }
.salary-amount { font-family:'Syne',sans-serif !important; font-size:clamp(3rem,8vw,4.2rem) !important; font-weight:800 !important; line-height:1 !important; background:linear-gradient(135deg,#60A5FA 0%,#8B5CF6 50%,#A78BFA 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; letter-spacing:-0.04em !important; }
.salary-currency { font-family:'JetBrains Mono',monospace !important; font-size:0.8rem; color:#475569; margin-left:4px; vertical-align:super; }
.band-row { display:flex; align-items:center; gap:10px; margin-bottom:1.2rem; }
.band-pill { display:inline-flex; align-items:center; padding:5px 14px; border-radius:50px; font-family:'Syne',sans-serif !important; font-size:0.75rem; font-weight:700; color:#fff; }
.band-note { font-size:0.75rem; color:#475569; }
.progress-section { margin-bottom:1.2rem; }
.progress-labels { display:flex; justify-content:space-between; font-family:'JetBrains Mono',monospace !important; font-size:0.68rem; color:#334155; margin-bottom:6px; }
.progress-track { height:6px; border-radius:999px; background:rgba(255,255,255,0.05); overflow:hidden; }
.progress-bar { height:100%; border-radius:999px; }
.result-note { font-size:0.75rem; line-height:1.5; color:#334155; border-top:1px solid rgba(255,255,255,0.05); padding-top:1rem; margin-top:0.2rem; }

/* Error */
.error-card { display:flex; align-items:flex-start; gap:12px; padding:14px 16px; border-radius:14px; background:rgba(239,68,68,0.07); border:1px solid rgba(239,68,68,0.2); margin-top:1rem; }
.error-icon { font-size:1.1rem; margin-top:1px; }
.error-title { font-size:0.85rem; font-weight:600; color:#FCA5A5; margin:0 0 3px; }
.error-note { font-size:0.75rem; color:#7F1D1D; margin:0; }

/* Info cards */
.info-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-top:1.5rem; }
@media(max-width:600px){.info-grid{grid-template-columns:1fr}}
.info-card { padding:18px; border-radius:16px; background:rgba(10,22,48,0.4); border:1px solid rgba(255,255,255,0.06); transition:all 0.2s ease; }
.info-card:hover { border-color:rgba(139,92,246,0.2); background:rgba(15,32,64,0.5); transform:translateY(-2px); }
.info-emoji { font-size:1.4rem; margin-bottom:10px; }
.info-title { font-family:'Syne',sans-serif !important; font-size:0.82rem; font-weight:700; color:#E2E8F5; margin-bottom:5px; }
.info-desc { font-size:0.75rem; color:#475569; line-height:1.5; }

/* Footer */
.footer { border-top:1px solid rgba(255,255,255,0.05); margin-top:2.5rem; padding:1.4rem 0; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px; }
.footer-logo { display:flex; align-items:center; gap:8px; }
.footer-logo-icon { width:22px; height:22px; background:linear-gradient(135deg,#7C3AED,#3B82F6); border-radius:7px; display:flex; align-items:center; justify-content:center; font-size:10px; }
.footer-brand { font-family:'Syne',sans-serif !important; font-size:0.8rem; font-weight:600; color:#475569; }
.footer-center { font-size:0.75rem; color:#334155; text-align:center; }
.footer-tags { display:flex; gap:6px; }
.footer-tag { font-family:'JetBrains Mono',monospace !important; font-size:0.68rem; padding:3px 8px; border-radius:6px; background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.06); color:#475569; }
</style>
""", unsafe_allow_html=True)

# ─── Data ─────────────────────────────────────────────────────────────────────
WORK_YEARS = [2024, 2023, 2022, 2021, 2020]

EXPERIENCE_LEVELS = {
    "EN – Entry Level / Junior":      "EN",
    "MI – Mid Level / Intermediate":  "MI",
    "SE – Senior Level / Expert":     "SE",
    "EX – Executive / Director":      "EX",
}

EMPLOYMENT_TYPES = {
    "FT – Full Time": "FT",
    "PT – Part Time": "PT",
    "CT – Contract":  "CT",
    "FL – Freelance": "FL",
}

JOB_TITLES = sorted([
    "Data Scientist", "Data Engineer", "Data Analyst",
    "Machine Learning Engineer", "Research Scientist",
    "Data Science Manager", "Applied Scientist", "Data Architect",
    "BI Data Analyst", "ML Engineer", "Head of Data",
    "Director of Data Science", "Data Science Lead",
    "Principal Data Scientist", "Staff Data Scientist",
    "Analytics Engineer", "Data Manager",
    "Computer Vision Engineer", "NLP Engineer",
    "Cloud Data Engineer", "Business Data Analyst", "Data Specialist",
])

REMOTE_RATIOS = {
    "0% – Fully On-site":  0,
    "50% – Hybrid":        50,
    "100% – Fully Remote": 100,
}

COMPANY_SIZES = {
    "S – Small  (< 50 employees)":   "S",
    "M – Medium (50–250 employees)": "M",
    "L – Large  (250+ employees)":   "L",
}

COUNTRIES = {
    "🇺🇸 United States": "US", "🇬🇧 United Kingdom": "GB",
    "🇨🇦 Canada": "CA",        "🇩🇪 Germany": "DE",
    "🇫🇷 France": "FR",        "🇮🇳 India": "IN",
    "🇦🇺 Australia": "AU",     "🇪🇸 Spain": "ES",
    "🇳🇱 Netherlands": "NL",   "🇧🇷 Brazil": "BR",
    "🇸🇬 Singapore": "SG",     "🇯🇵 Japan": "JP",
    "🇵🇹 Portugal": "PT",      "🇮🇹 Italy": "IT",
    "🇨🇭 Switzerland": "CH",   "🇸🇪 Sweden": "SE",
    "🇵🇱 Poland": "PL",        "🇲🇽 Mexico": "MX",
}

def get_salary_band(salary):
    if salary < 60_000:
        return ("Entry Level",       "linear-gradient(135deg,#10B981,#059669)")
    elif salary < 100_000:
        return ("Mid Level",         "linear-gradient(135deg,#3B82F6,#0EA5E9)")
    elif salary < 150_000:
        return ("Senior Level",      "linear-gradient(135deg,#8B5CF6,#7C3AED)")
    else:
        return ("Principal / Staff", "linear-gradient(135deg,#F59E0B,#EF4444)")

# ─── Navbar ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="navbar">
  <div class="navbar-logo">
    <div class="logo-icon">🧠<div class="logo-dot"></div></div>
    <span class="logo-text">AI Salary Predictor</span>
  </div>
  <div class="navbar-links">
    <a class="nav-link" href="https://github.com" target="_blank">⭐ GitHub</a>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-badge"><div class="badge-dot"></div>Ensemble ML · RF + GB + ET · Voting Regressor</div>
  <h1 class="hero-title">AI Powered <span class="gradient-text">Salary</span><br>Prediction</h1>
  <p class="hero-sub">Predict employee compensation using machine learning ensemble models trained on real-world data science salary datasets.</p>
  <div class="model-pills">
    <span class="model-pill pill-rf"><span class="pill-dot"></span>Random Forest</span>
    <span class="model-pill pill-gb"><span class="pill-dot"></span>Gradient Boosting</span>
    <span class="model-pill pill-et"><span class="pill-dot"></span>Extra Trees</span>
  </div>
  <div class="stat-row">
    <div class="stat-badge"><span class="stat-value">3</span><span class="stat-label">Models</span></div>
    <div class="stat-badge"><span class="stat-value">Voting</span><span class="stat-label">Regressor</span></div>
    <div class="stat-badge"><span class="stat-value">8</span><span class="stat-label">Features</span></div>
    <div class="stat-badge"><span class="stat-value">USD</span><span class="stat-label">Output</span></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── Divider ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-divider">
  <div class="divider-line"></div>
  <span class="divider-text">Configure Prediction</span>
  <div class="divider-line"></div>
</div>
""", unsafe_allow_html=True)

# ─── Form header card ─────────────────────────────────────────────────────────
st.markdown("""
<div class="form-card">
  <div class="form-header">
    <div class="form-icon">📊</div>
    <div>
      <div class="form-title">Employee Profile</div>
      <div class="form-sub">Fill in the attributes below to generate a salary prediction</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── Inputs ───────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2, gap="medium")

with col1:
    work_year    = st.selectbox("Work Year",          WORK_YEARS, index=1)
    exp_label    = st.selectbox("Experience Level",   list(EXPERIENCE_LEVELS.keys()), index=2)
    emp_label    = st.selectbox("Employment Type",    list(EMPLOYMENT_TYPES.keys()),  index=0)
    job_title    = st.selectbox("Job Title",          JOB_TITLES, index=JOB_TITLES.index("Data Scientist"))

with col2:
    res_label    = st.selectbox("Employee Residence", list(COUNTRIES.keys()),         index=0)
    remote_label = st.selectbox("Remote Ratio",       list(REMOTE_RATIOS.keys()),     index=2)
    loc_label    = st.selectbox("Company Location",   list(COUNTRIES.keys()),         index=0)
    size_label   = st.selectbox("Company Size",       list(COMPANY_SIZES.keys()),     index=1)

# ─── Predict button ───────────────────────────────────────────────────────────
predict_clicked = st.button("⚡  Predict Salary", use_container_width=True)

# ─── Prediction logic ─────────────────────────────────────────────────────────
if predict_clicked:
    payload = {
        "work_year":          int(work_year),
        "experience_level":   EXPERIENCE_LEVELS[exp_label],
        "employment_type":    EMPLOYMENT_TYPES[emp_label],
        "job_title":          job_title,
        "employee_residence": COUNTRIES[res_label],
        "remote_ratio":       REMOTE_RATIOS[remote_label],
        "company_location":   COUNTRIES[loc_label],
        "company_size":       COMPANY_SIZES[size_label],
    }

    with st.spinner("AI model is predicting salary..."):
        try:
            response = requests.post(
                "http://localhost:5000/predict",
                json=payload,
                timeout=10,
            )
            response.raise_for_status()
            data   = response.json()
            salary = data.get("predicted_salary") or data.get("salary") or data

            if isinstance(salary, (int, float)):
                band_name, band_grad = get_salary_band(salary)
                pct = min(int((salary / 300_000) * 100), 100)

                st.markdown(f"""
<div class="result-card">
  <div class="result-accent" style="background:{band_grad}"></div>
  <div class="result-inner">
    <div class="result-header">
      <div class="result-label-row">
        <div class="result-icon" style="background:{band_grad}">📈</div>
        <span class="result-label">Predicted Salary</span>
      </div>
      <span class="result-tag">✦ Prediction Ready</span>
    </div>
    <div class="salary-display">
      <span class="salary-amount">${salary:,.0f}</span>
      <span class="salary-currency">USD / yr</span>
    </div>
    <div class="band-row">
      <span class="band-pill" style="background:{band_grad}">{band_name}</span>
      <span class="band-note">Based on submitted attributes</span>
    </div>
    <div class="progress-section">
      <div class="progress-labels"><span>$30k</span><span>$300k+</span></div>
      <div class="progress-track">
        <div class="progress-bar" style="width:{pct}%;background:{band_grad}"></div>
      </div>
    </div>
    <p class="result-note">
      Estimated using a Voting Regressor ensemble of Random Forest,
      Gradient Boosting &amp; Extra Trees — trained on real-world data science compensation data.
    </p>
  </div>
</div>
""", unsafe_allow_html=True)

            else:
                st.error("Unexpected response format from the API.")

        except requests.exceptions.ConnectionError:
            st.markdown("""
<div class="error-card">
  <div class="error-icon">✕</div>
  <div>
    <p class="error-title">Cannot connect to prediction API</p>
    <p class="error-note">Make sure the Flask server is running at http://localhost:5000</p>
  </div>
</div>
""", unsafe_allow_html=True)

        except requests.exceptions.Timeout:
            st.markdown("""
<div class="error-card">
  <div class="error-icon">⏱</div>
  <div>
    <p class="error-title">Request timed out</p>
    <p class="error-note">The API took too long to respond. Try again in a moment.</p>
  </div>
</div>
""", unsafe_allow_html=True)

        except Exception as e:
            st.markdown(f"""
<div class="error-card">
  <div class="error-icon">⚠</div>
  <div>
    <p class="error-title">Prediction failed</p>
    <p class="error-note">{str(e)}</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── Info cards ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="info-grid">
  <div class="info-card">
    <div class="info-emoji">⚡</div>
    <div class="info-title">Fast Inference</div>
    <div class="info-desc">Sub-second predictions powered by pre-trained ensemble models.</div>
  </div>
  <div class="info-card">
    <div class="info-emoji">🎯</div>
    <div class="info-title">High Accuracy</div>
    <div class="info-desc">Trained on thousands of real data science compensation records.</div>
  </div>
  <div class="info-card">
    <div class="info-emoji">🌍</div>
    <div class="info-title">Global Data</div>
    <div class="info-desc">Covers 50+ countries, all experience levels and job titles.</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  <div class="footer-logo">
    <div class="footer-logo-icon">🧠</div>
    <span class="footer-brand">AI Salary Predictor</span>
  </div>
  <div class="footer-center">
    Powered by Ensemble Machine Learning Model &nbsp;·&nbsp; Built with Streamlit
  </div>
  <div class="footer-tags">
    <span class="footer-tag">RF</span>
    <span class="footer-tag">GB</span>
    <span class="footer-tag">ET</span>
  </div>
</div>
""", unsafe_allow_html=True)