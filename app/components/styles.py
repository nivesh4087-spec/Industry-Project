"""
Dashboard Styling Module
=========================
Professional Industrial AI Command Center theme for Streamlit.

Design language:
- Dark professional theme with steel-blue accents
- Glassmorphism effects
- Animated micro-interactions
- Modern card-based layout
- Status indicators and risk badges
"""


def get_custom_css() -> str:
    """Return the complete custom CSS for the dashboard.

    Returns:
        CSS string to inject via st.markdown.
    """
    return """
    <style>
    /* ================================================================
       GLOBAL STYLES — Industrial AI Command Center Theme v2.0
       ================================================================ */

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Root variables */
    :root {
        --bg-primary: #0a0e17;
        --bg-secondary: #111827;
        --bg-card: #1a2332;
        --bg-card-hover: #1f2b3d;
        --bg-glass: rgba(26, 35, 50, 0.7);
        --border-color: #2a3a4e;
        --border-glow: rgba(59, 130, 246, 0.4);
        --text-primary: #e2e8f0;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
        --accent-blue: #3b82f6;
        --accent-cyan: #06b6d4;
        --accent-green: #22c55e;
        --accent-yellow: #eab308;
        --accent-orange: #f97316;
        --accent-red: #ef4444;
        --accent-purple: #8b5cf6;
        --gradient-blue: linear-gradient(135deg, #3b82f6, #06b6d4);
        --gradient-danger: linear-gradient(135deg, #ef4444, #f97316);
        --gradient-success: linear-gradient(135deg, #22c55e, #06b6d4);
        --gradient-purple: linear-gradient(135deg, #8b5cf6, #a78bfa);
        --gradient-mesh: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
        --shadow-card: 0 4px 24px rgba(0, 0, 0, 0.3);
        --shadow-glow: 0 0 20px rgba(59, 130, 246, 0.15);
        --shadow-glow-strong: 0 0 30px rgba(59, 130, 246, 0.25);
        --shadow-elevation: 0 8px 32px rgba(0, 0, 0, 0.4);
        --radius: 12px;
        --radius-sm: 8px;
        --radius-lg: 16px;
        --radius-xl: 20px;
        --transition-fast: 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        --transition-smooth: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        --transition-bounce: 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    }

    /* ================================================================
       ANIMATIONS
       ================================================================ */

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }

    @keyframes pulseGlow {
        0%, 100% { box-shadow: 0 0 8px rgba(59, 130, 246, 0.1); }
        50% { box-shadow: 0 0 20px rgba(59, 130, 246, 0.25); }
    }

    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    @keyframes borderGlow {
        0%, 100% { border-color: rgba(59, 130, 246, 0.2); }
        50% { border-color: rgba(59, 130, 246, 0.5); }
    }

    /* Global font */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* Main background */
    .stApp {
        background: var(--bg-primary) !important;
    }

    /* Main content area — fade in animation */
    .main .block-container {
        animation: fadeIn 0.5s ease-out;
    }

    /* ================================================================
       SIDEBAR — Premium Styling
       ================================================================ */

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1321 0%, #111827 40%, #0d1321 100%) !important;
        border-right: 1px solid var(--border-color) !important;
        box-shadow: 4px 0 24px rgba(0, 0, 0, 0.3);
    }

    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li,
    section[data-testid="stSidebar"] label {
        color: var(--text-secondary) !important;
    }

    /* Sidebar radio buttons — styled as nav items */
    section[data-testid="stSidebar"] .stRadio > div {
        gap: 2px !important;
    }

    section[data-testid="stSidebar"] .stRadio > div > label {
        padding: 10px 16px !important;
        border-radius: var(--radius-sm) !important;
        transition: var(--transition-smooth) !important;
        cursor: pointer !important;
        border-left: 3px solid transparent !important;
    }

    section[data-testid="stSidebar"] .stRadio > div > label:hover {
        background: rgba(59, 130, 246, 0.08) !important;
        border-left-color: rgba(59, 130, 246, 0.4) !important;
    }

    section[data-testid="stSidebar"] .stRadio > div > label[data-checked="true"],
    section[data-testid="stSidebar"] .stRadio > div > label:has(input:checked) {
        background: rgba(59, 130, 246, 0.12) !important;
        border-left-color: var(--accent-blue) !important;
    }

    /* Headers */
    h1, h2, h3, h4, h5 {
        color: var(--text-primary) !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }

    h1 { font-size: 2rem !important; }
    h2 { font-size: 1.5rem !important; }
    h3 { font-size: 1.2rem !important; }

    /* Paragraph text */
    p, li, span, div {
        color: var(--text-secondary);
    }

    /* ================================================================
       KPI CARDS — Premium with Animations
       ================================================================ */

    .kpi-card {
        background: var(--bg-glass);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid var(--border-color);
        border-radius: var(--radius);
        padding: 20px 24px;
        box-shadow: var(--shadow-card);
        transition: var(--transition-smooth);
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.6s ease-out both;
    }

    .kpi-card:hover {
        border-color: var(--border-glow);
        box-shadow: var(--shadow-glow-strong);
        transform: translateY(-3px);
    }

    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--gradient-blue);
        transition: height var(--transition-smooth);
    }

    .kpi-card:hover::before {
        height: 4px;
    }

    /* Subtle shimmer overlay on hover */
    .kpi-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.03), transparent);
        transition: left 0.6s ease;
    }
    .kpi-card:hover::after {
        left: 100%;
    }

    .kpi-card .kpi-label {
        font-size: 0.7rem;
        font-weight: 600;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 8px;
    }

    .kpi-card .kpi-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: var(--text-primary);
        line-height: 1.1;
        letter-spacing: -0.02em;
    }

    .kpi-card .kpi-subtitle {
        font-size: 0.78rem;
        color: var(--text-muted);
        margin-top: 8px;
        line-height: 1.3;
    }

    /* KPI color variants */
    .kpi-card.kpi-blue::before { background: var(--gradient-blue); }
    .kpi-card.kpi-green::before { background: var(--gradient-success); }
    .kpi-card.kpi-red::before { background: var(--gradient-danger); }
    .kpi-card.kpi-purple::before { background: var(--gradient-purple); }
    .kpi-card.kpi-cyan::before { background: linear-gradient(135deg, #06b6d4, #22d3ee); }

    /* Animation stagger for KPI cards in columns */
    [data-testid="stHorizontalBlock"] > div:nth-child(1) .kpi-card { animation-delay: 0s; }
    [data-testid="stHorizontalBlock"] > div:nth-child(2) .kpi-card { animation-delay: 0.08s; }
    [data-testid="stHorizontalBlock"] > div:nth-child(3) .kpi-card { animation-delay: 0.16s; }
    [data-testid="stHorizontalBlock"] > div:nth-child(4) .kpi-card { animation-delay: 0.24s; }
    [data-testid="stHorizontalBlock"] > div:nth-child(5) .kpi-card { animation-delay: 0.32s; }

    /* ================================================================
       RISK BADGES — Pill Style
       ================================================================ */

    .risk-badge {
        display: inline-block;
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        transition: var(--transition-fast);
    }

    .risk-low {
        background: rgba(34, 197, 94, 0.12);
        color: var(--accent-green);
        border: 1px solid rgba(34, 197, 94, 0.25);
    }

    .risk-moderate {
        background: rgba(234, 179, 8, 0.12);
        color: var(--accent-yellow);
        border: 1px solid rgba(234, 179, 8, 0.25);
    }

    .risk-high {
        background: rgba(249, 115, 22, 0.12);
        color: var(--accent-orange);
        border: 1px solid rgba(249, 115, 22, 0.25);
    }

    .risk-critical {
        background: rgba(239, 68, 68, 0.12);
        color: var(--accent-red);
        border: 1px solid rgba(239, 68, 68, 0.25);
        animation: pulseGlow 2s infinite;
    }

    /* ================================================================
       SECTION CARDS — Glassmorphism
       ================================================================ */

    .section-card {
        background: var(--bg-glass);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-lg);
        padding: 24px 28px;
        margin-bottom: 16px;
        box-shadow: var(--shadow-card);
        transition: var(--transition-smooth);
        animation: fadeInUp 0.5s ease-out both;
    }

    .section-card:hover {
        border-color: rgba(59, 130, 246, 0.2);
        box-shadow: var(--shadow-glow);
    }

    .section-title {
        font-size: 1rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 16px;
        padding-bottom: 10px;
        border-bottom: 1px solid var(--border-color);
    }

    /* ================================================================
       ALERT / WARNING BANNER
       ================================================================ */

    .alert-banner {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.08), rgba(249, 115, 22, 0.08));
        border: 1px solid rgba(239, 68, 68, 0.25);
        border-radius: var(--radius);
        padding: 16px 20px;
        margin: 12px 0;
        animation: fadeIn 0.4s ease-out;
    }

    .alert-banner .alert-title {
        font-size: 1rem;
        font-weight: 700;
        color: var(--accent-red);
        margin-bottom: 6px;
    }

    .alert-banner .alert-text {
        font-size: 0.85rem;
        color: var(--text-secondary);
    }

    /* ================================================================
       GAUGE / PROGRESS
       ================================================================ */

    .risk-gauge {
        text-align: center;
        padding: 20px;
    }

    .risk-gauge .gauge-value {
        font-size: 3.5rem;
        font-weight: 800;
        line-height: 1;
    }

    .risk-gauge .gauge-label {
        font-size: 0.85rem;
        color: var(--text-muted);
        margin-top: 6px;
        font-weight: 500;
    }

    /* ================================================================
       TABLE STYLES — Premium
       ================================================================ */

    .stDataFrame {
        border-radius: var(--radius) !important;
        overflow: hidden !important;
    }

    .stDataFrame table {
        background: var(--bg-card) !important;
    }

    .stDataFrame th {
        background: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        font-size: 0.8rem !important;
        letter-spacing: 0.02em;
    }

    .stDataFrame td {
        color: var(--text-secondary) !important;
        border-color: var(--border-color) !important;
        transition: background var(--transition-fast);
    }

    .stDataFrame tr:hover td {
        background: rgba(59, 130, 246, 0.05) !important;
    }

    /* ================================================================
       BUTTONS — Gradient with Glow
       ================================================================ */

    .stButton > button {
        background: var(--gradient-blue) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--radius-sm) !important;
        font-weight: 600 !important;
        padding: 10px 28px !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.01em;
        transition: var(--transition-smooth) !important;
        position: relative;
        overflow: hidden;
    }

    .stButton > button:hover {
        box-shadow: var(--shadow-glow-strong) !important;
        transform: translateY(-2px) !important;
    }

    .stButton > button:active {
        transform: translateY(0) !important;
    }

    /* ================================================================
       INPUT ELEMENTS — Refined
       ================================================================ */

    .stNumberInput input,
    .stSelectbox select,
    .stTextInput input {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text-primary) !important;
        transition: var(--transition-fast) !important;
    }

    .stNumberInput input:focus,
    .stSelectbox select:focus,
    .stTextInput input:focus {
        border-color: var(--accent-blue) !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
    }

    /* ================================================================
       TABS — Premium
       ================================================================ */

    .stTabs [data-baseweb="tab-list"] {
        background: var(--bg-secondary);
        border-radius: var(--radius);
        padding: 4px;
        gap: 4px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: var(--radius-sm);
        color: var(--text-secondary);
        font-weight: 500;
        transition: var(--transition-smooth);
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(59, 130, 246, 0.08);
    }

    .stTabs [aria-selected="true"] {
        background: var(--accent-blue) !important;
        color: white !important;
    }

    /* ================================================================
       METRICS — Premium Cards
       ================================================================ */

    [data-testid="stMetric"] {
        background: var(--bg-glass);
        backdrop-filter: blur(12px);
        border: 1px solid var(--border-color);
        border-radius: var(--radius);
        padding: 18px;
        transition: var(--transition-smooth);
    }

    [data-testid="stMetric"]:hover {
        border-color: rgba(59, 130, 246, 0.3);
        box-shadow: var(--shadow-glow);
    }

    [data-testid="stMetricLabel"] {
        color: var(--text-muted) !important;
        font-size: 0.75rem !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    [data-testid="stMetricValue"] {
        color: var(--text-primary) !important;
        font-weight: 800 !important;
    }

    /* ================================================================
       FILE UPLOADER — Premium Dropzone
       ================================================================ */

    [data-testid="stFileUploader"] {
        animation: fadeInUp 0.5s ease-out both;
    }

    [data-testid="stFileUploader"] > div {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.04), rgba(6, 182, 212, 0.04)) !important;
        border: 2px dashed rgba(59, 130, 246, 0.3) !important;
        border-radius: var(--radius-lg) !important;
        padding: 32px !important;
        transition: var(--transition-smooth) !important;
    }

    [data-testid="stFileUploader"] > div:hover {
        border-color: var(--accent-blue) !important;
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.08), rgba(6, 182, 212, 0.08)) !important;
        box-shadow: var(--shadow-glow) !important;
    }

    /* ================================================================
       EXPANDERS — Styled
       ================================================================ */

    .streamlit-expanderHeader {
        background: var(--bg-card) !important;
        border-radius: var(--radius-sm) !important;
        font-weight: 600 !important;
        color: var(--text-primary) !important;
    }

    /* ================================================================
       PROGRESS BAR
       ================================================================ */

    .stProgress > div > div {
        background: var(--gradient-blue) !important;
        border-radius: 4px;
    }

    /* ================================================================
       DISCLAIMER
       ================================================================ */

    .disclaimer {
        background: rgba(59, 130, 246, 0.06);
        border: 1px solid rgba(59, 130, 246, 0.15);
        border-radius: var(--radius-sm);
        padding: 14px 18px;
        font-size: 0.75rem;
        color: var(--text-muted);
        margin-top: 12px;
        backdrop-filter: blur(8px);
    }

    /* ================================================================
       HEADER BANNER — Animated Gradient
       ================================================================ */

    .header-banner {
        background: var(--gradient-mesh);
        background-size: 200% 200%;
        animation: gradientShift 8s ease infinite;
        border: 1px solid var(--border-color);
        border-radius: var(--radius-lg);
        padding: 28px 32px;
        margin-bottom: 28px;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(12px);
    }

    .header-banner::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--gradient-blue);
        background-size: 200% 100%;
        animation: shimmer 3s linear infinite;
    }

    .header-banner::after {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 200px;
        height: 100%;
        background: radial-gradient(ellipse at right, rgba(59, 130, 246, 0.06), transparent);
        pointer-events: none;
    }

    .header-banner h1 {
        margin: 0 !important;
        font-size: 1.6rem !important;
        animation: slideInLeft 0.6s ease-out;
    }

    .header-banner p {
        color: var(--text-muted);
        font-size: 0.85rem;
        margin: 6px 0 0 0;
        animation: slideInLeft 0.6s ease-out 0.1s both;
    }

    .header-banner .header-meta {
        font-size: 0.7rem;
        color: var(--text-muted);
        margin-top: 10px;
        opacity: 0.7;
        animation: fadeIn 1s ease-out 0.3s both;
    }

    /* ================================================================
       RECOMMENDATION CARD — Enhanced
       ================================================================ */

    .rec-card {
        background: var(--bg-glass);
        backdrop-filter: blur(8px);
        border: 1px solid var(--border-color);
        border-left: 4px solid var(--accent-blue);
        border-radius: var(--radius-sm);
        padding: 16px 20px;
        margin-bottom: 10px;
        transition: var(--transition-smooth);
    }

    .rec-card:hover {
        transform: translateX(4px);
        box-shadow: var(--shadow-glow);
    }

    .rec-card.rec-critical { border-left-color: var(--accent-red); }
    .rec-card.rec-high { border-left-color: var(--accent-orange); }
    .rec-card.rec-medium { border-left-color: var(--accent-yellow); }
    .rec-card.rec-low { border-left-color: var(--accent-green); }

    /* ================================================================
       UPLOAD ZONE — Custom Styled
       ================================================================ */

    .upload-zone {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.04), rgba(139, 92, 246, 0.04));
        border: 2px dashed rgba(59, 130, 246, 0.3);
        border-radius: var(--radius-xl);
        padding: 40px;
        text-align: center;
        transition: var(--transition-smooth);
        animation: fadeInUp 0.5s ease-out both;
    }

    .upload-zone:hover {
        border-color: var(--accent-blue);
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.08), rgba(139, 92, 246, 0.08));
        box-shadow: var(--shadow-glow);
    }

    .upload-zone .upload-icon {
        font-size: 3rem;
        margin-bottom: 12px;
        display: block;
    }

    .upload-zone .upload-text {
        font-size: 1rem;
        font-weight: 600;
        color: var(--text-primary);
    }

    .upload-zone .upload-hint {
        font-size: 0.8rem;
        color: var(--text-muted);
        margin-top: 6px;
    }

    /* ================================================================
       STATUS BADGES
       ================================================================ */

    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.03em;
    }

    .status-success {
        background: rgba(34, 197, 94, 0.12);
        color: var(--accent-green);
        border: 1px solid rgba(34, 197, 94, 0.2);
    }

    .status-error {
        background: rgba(239, 68, 68, 0.12);
        color: var(--accent-red);
        border: 1px solid rgba(239, 68, 68, 0.2);
    }

    .status-pending {
        background: rgba(234, 179, 8, 0.12);
        color: var(--accent-yellow);
        border: 1px solid rgba(234, 179, 8, 0.2);
    }

    .status-info {
        background: rgba(59, 130, 246, 0.12);
        color: var(--accent-blue);
        border: 1px solid rgba(59, 130, 246, 0.2);
    }

    /* ================================================================
       VALIDATION CHECKLIST
       ================================================================ */

    .validation-item {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px 16px;
        border-radius: var(--radius-sm);
        margin-bottom: 6px;
        font-size: 0.85rem;
        transition: var(--transition-fast);
    }

    .validation-pass {
        background: rgba(34, 197, 94, 0.06);
        border: 1px solid rgba(34, 197, 94, 0.15);
        color: var(--accent-green);
    }

    .validation-fail {
        background: rgba(239, 68, 68, 0.06);
        border: 1px solid rgba(239, 68, 68, 0.15);
        color: var(--accent-red);
    }

    .validation-warn {
        background: rgba(234, 179, 8, 0.06);
        border: 1px solid rgba(234, 179, 8, 0.15);
        color: var(--accent-yellow);
    }

    /* ================================================================
       FOOTER — Gradient Separator
       ================================================================ */

    .footer {
        text-align: center;
        padding: 24px;
        margin-top: 48px;
        border-top: 1px solid transparent;
        border-image: var(--gradient-blue) 1;
        color: var(--text-muted);
        font-size: 0.75rem;
        animation: fadeIn 1s ease-out;
    }

    .footer a {
        color: var(--accent-blue);
        text-decoration: none;
    }

    /* ================================================================
       SCROLLBAR — Subtle
       ================================================================ */

    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }

    ::-webkit-scrollbar-track {
        background: var(--bg-primary);
    }

    ::-webkit-scrollbar-thumb {
        background: var(--border-color);
        border-radius: 3px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--accent-blue);
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """


def render_kpi_card(
    label: str,
    value: str,
    subtitle: str = "",
    variant: str = "blue",
) -> str:
    """Generate HTML for a KPI card.

    Args:
        label: Card label (small text above value).
        value: Main value to display.
        subtitle: Optional subtitle below value.
        variant: Color variant (blue, green, red, purple, cyan).

    Returns:
        HTML string.
    """
    return f"""
    <div class="kpi-card kpi-{variant}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-subtitle">{subtitle}</div>
    </div>
    """


def render_risk_badge(category: str) -> str:
    """Generate HTML for a risk badge.

    Args:
        category: Risk category label (e.g., "CRITICAL RISK").

    Returns:
        HTML string.
    """
    css_class = "risk-low"
    if "MODERATE" in category.upper():
        css_class = "risk-moderate"
    elif "HIGH" in category.upper():
        css_class = "risk-high"
    elif "CRITICAL" in category.upper():
        css_class = "risk-critical"

    return f'<span class="risk-badge {css_class}">{category}</span>'


def render_header_banner(title: str, subtitle: str, meta: str = "") -> str:
    """Generate HTML for the page header banner.

    Args:
        title: Main title.
        subtitle: Subtitle description.
        meta: Optional metadata line (e.g., timestamp).

    Returns:
        HTML string.
    """
    meta_html = f'<div class="header-meta">{meta}</div>' if meta else ""
    return f"""
    <div class="header-banner">
        <h1>🏭 {title}</h1>
        <p>{subtitle}</p>
        {meta_html}
    </div>
    """


def render_status_badge(text: str, status: str = "info") -> str:
    """Generate HTML for a status badge.

    Args:
        text: Badge text.
        status: One of 'success', 'error', 'pending', 'info'.

    Returns:
        HTML string.
    """
    return f'<span class="status-badge status-{status}">{text}</span>'


def render_validation_item(text: str, passed: bool) -> str:
    """Generate HTML for a validation checklist item.

    Args:
        text: Validation description.
        passed: Whether the validation passed.

    Returns:
        HTML string.
    """
    css_class = "validation-pass" if passed else "validation-fail"
    icon = "✅" if passed else "❌"
    return f"""
    <div class="validation-item {css_class}">
        <span>{icon}</span>
        <span>{text}</span>
    </div>
    """
