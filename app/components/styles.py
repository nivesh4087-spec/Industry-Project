"""
Dashboard Styling Module
=========================
Professional Industrial AI Command Center theme for Streamlit.

Design language:
- Dark professional theme with steel-blue accents
- Clean typography
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
       GLOBAL STYLES — Industrial AI Command Center Theme
       ================================================================ */

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Root variables */
    :root {
        --bg-primary: #0a0e17;
        --bg-secondary: #111827;
        --bg-card: #1a2332;
        --bg-card-hover: #1f2b3d;
        --border-color: #2a3a4e;
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
        --shadow-card: 0 4px 24px rgba(0, 0, 0, 0.3);
        --shadow-glow: 0 0 20px rgba(59, 130, 246, 0.15);
        --radius: 12px;
        --radius-sm: 8px;
    }

    /* Global font */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* Main background */
    .stApp {
        background: var(--bg-primary) !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: var(--bg-secondary) !important;
        border-right: 1px solid var(--border-color) !important;
    }

    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li,
    section[data-testid="stSidebar"] label {
        color: var(--text-secondary) !important;
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
       KPI CARDS
       ================================================================ */

    .kpi-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: var(--radius);
        padding: 20px 24px;
        box-shadow: var(--shadow-card);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .kpi-card:hover {
        border-color: var(--accent-blue);
        box-shadow: var(--shadow-glow);
        transform: translateY(-2px);
    }

    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--gradient-blue);
    }

    .kpi-card .kpi-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 6px;
    }

    .kpi-card .kpi-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: var(--text-primary);
        line-height: 1.1;
    }

    .kpi-card .kpi-subtitle {
        font-size: 0.8rem;
        color: var(--text-muted);
        margin-top: 6px;
    }

    /* KPI color variants */
    .kpi-card.kpi-blue::before { background: var(--gradient-blue); }
    .kpi-card.kpi-green::before { background: var(--gradient-success); }
    .kpi-card.kpi-red::before { background: var(--gradient-danger); }
    .kpi-card.kpi-purple::before { background: linear-gradient(135deg, #8b5cf6, #a78bfa); }
    .kpi-card.kpi-cyan::before { background: linear-gradient(135deg, #06b6d4, #22d3ee); }

    /* ================================================================
       RISK BADGES
       ================================================================ */

    .risk-badge {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    .risk-low {
        background: rgba(34, 197, 94, 0.15);
        color: var(--accent-green);
        border: 1px solid rgba(34, 197, 94, 0.3);
    }

    .risk-moderate {
        background: rgba(234, 179, 8, 0.15);
        color: var(--accent-yellow);
        border: 1px solid rgba(234, 179, 8, 0.3);
    }

    .risk-high {
        background: rgba(249, 115, 22, 0.15);
        color: var(--accent-orange);
        border: 1px solid rgba(249, 115, 22, 0.3);
    }

    .risk-critical {
        background: rgba(239, 68, 68, 0.15);
        color: var(--accent-red);
        border: 1px solid rgba(239, 68, 68, 0.3);
    }

    /* ================================================================
       SECTION CARDS
       ================================================================ */

    .section-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: var(--radius);
        padding: 24px;
        margin-bottom: 16px;
        box-shadow: var(--shadow-card);
    }

    .section-title {
        font-size: 1rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 16px;
        padding-bottom: 8px;
        border-bottom: 1px solid var(--border-color);
    }

    /* ================================================================
       ALERT / WARNING BANNER
       ================================================================ */

    .alert-banner {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(249, 115, 22, 0.1));
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: var(--radius);
        padding: 16px 20px;
        margin: 12px 0;
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
       TABLE STYLES
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
    }

    .stDataFrame td {
        color: var(--text-secondary) !important;
        border-color: var(--border-color) !important;
    }

    /* ================================================================
       BUTTONS
       ================================================================ */

    .stButton > button {
        background: var(--gradient-blue) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--radius-sm) !important;
        font-weight: 600 !important;
        padding: 8px 24px !important;
        transition: all 0.3s ease !important;
    }

    .stButton > button:hover {
        box-shadow: var(--shadow-glow) !important;
        transform: translateY(-1px) !important;
    }

    /* ================================================================
       INPUT ELEMENTS
       ================================================================ */

    .stNumberInput input,
    .stSelectbox select,
    .stTextInput input {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text-primary) !important;
    }

    /* ================================================================
       TABS
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
    }

    .stTabs [aria-selected="true"] {
        background: var(--accent-blue) !important;
        color: white !important;
    }

    /* ================================================================
       METRICS
       ================================================================ */

    [data-testid="stMetric"] {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: var(--radius);
        padding: 16px;
    }

    [data-testid="stMetricLabel"] {
        color: var(--text-muted) !important;
    }

    [data-testid="stMetricValue"] {
        color: var(--text-primary) !important;
    }

    /* ================================================================
       DISCLAIMER
       ================================================================ */

    .disclaimer {
        background: rgba(59, 130, 246, 0.08);
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: var(--radius-sm);
        padding: 12px 16px;
        font-size: 0.75rem;
        color: var(--text-muted);
        margin-top: 12px;
    }

    /* ================================================================
       HEADER BANNER
       ================================================================ */

    .header-banner {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        border: 1px solid var(--border-color);
        border-radius: var(--radius);
        padding: 24px 28px;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }

    .header-banner::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--gradient-blue);
    }

    .header-banner h1 {
        margin: 0 !important;
        font-size: 1.6rem !important;
    }

    .header-banner p {
        color: var(--text-muted);
        font-size: 0.85rem;
        margin: 6px 0 0 0;
    }

    /* ================================================================
       RECOMMENDATION CARD
       ================================================================ */

    .rec-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-left: 4px solid var(--accent-blue);
        border-radius: var(--radius-sm);
        padding: 14px 18px;
        margin-bottom: 10px;
    }

    .rec-card.rec-critical { border-left-color: var(--accent-red); }
    .rec-card.rec-high { border-left-color: var(--accent-orange); }
    .rec-card.rec-medium { border-left-color: var(--accent-yellow); }
    .rec-card.rec-low { border-left-color: var(--accent-green); }

    /* ================================================================
       FOOTER
       ================================================================ */

    .footer {
        text-align: center;
        padding: 20px;
        margin-top: 40px;
        border-top: 1px solid var(--border-color);
        color: var(--text-muted);
        font-size: 0.75rem;
    }

    /* ================================================================
       SCROLLBAR
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


def render_header_banner(title: str, subtitle: str) -> str:
    """Generate HTML for the page header banner.

    Args:
        title: Main title.
        subtitle: Subtitle description.

    Returns:
        HTML string.
    """
    return f"""
    <div class="header-banner">
        <h1>🏭 {title}</h1>
        <p>{subtitle}</p>
    </div>
    """
