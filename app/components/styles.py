"""
Dashboard Styling Module
=========================
Professional Industrial AI Command Center theme for Streamlit.
Designed to look like an enterprise industrial telemetry & health monitoring platform.
"""

def get_custom_css() -> str:
    """Return the complete custom CSS for the dashboard."""
    return """
    <style>
    /* ================================================================
       GLOBAL STYLES — Enterprise Industrial AI Theme v3.0
       ================================================================ */

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

    :root {
        --bg-main: #090d16;
        --bg-sidebar: #060910;
        --bg-card: #111827;
        --bg-card-hover: #1f2937;
        --border-subtle: #1f2937;
        --border-medium: #374151;
        
        --text-primary: #f3f4f6;
        --text-secondary: #9ca3af;
        --text-muted: #6b7280;
        
        --status-normal: #10b981;
        --status-warning: #f59e0b;
        --status-danger: #ef4444;
        --status-info: #3b82f6;
        
        --radius-sm: 4px;
        --radius-md: 6px;
        --radius-lg: 8px;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: var(--bg-main) !important;
        color: var(--text-primary) !important;
    }

    code, pre, .mono-text {
        font-family: 'JetBrains Mono', monospace !important;
    }

    .stApp {
        background: var(--bg-main) !important;
    }

    .main .block-container {
        padding-top: 1.25rem !important;
        padding-bottom: 2rem !important;
        max-width: 1440px !important;
    }

    /* Hide Streamlit Auto-Generated Multi-Page Navigation Links */
    div[data-testid="stSidebarNav"], nav[data-testid="stSidebarNav"] {
        display: none !important;
    }

    /* Sidebar Navigation */
    section[data-testid="stSidebar"] {
        background: var(--bg-sidebar) !important;
        border-right: 1px solid var(--border-subtle) !important;
    }

    section[data-testid="stSidebar"] .stRadio > div {
        gap: 3px !important;
    }

    section[data-testid="stSidebar"] .stRadio > div > label {
        padding: 10px 14px !important;
        border-radius: var(--radius-md) !important;
        transition: all 0.15s ease !important;
        cursor: pointer !important;
        background: transparent !important;
        border-left: 3px solid transparent !important;
        font-weight: 500 !important;
        font-size: 0.88rem !important;
        color: var(--text-secondary) !important;
    }

    section[data-testid="stSidebar"] .stRadio > div > label:hover {
        background: rgba(255, 255, 255, 0.04) !important;
        color: var(--text-primary) !important;
    }

    section[data-testid="stSidebar"] .stRadio > div > label[data-checked="true"],
    section[data-testid="stSidebar"] .stRadio > div > label:has(input:checked) {
        background: rgba(59, 130, 246, 0.1) !important;
        border-left-color: var(--status-info) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
    }

    /* Headers */
    h1, h2, h3, h4, h5 {
        color: var(--text-primary) !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }

    h1 { font-size: 1.8rem !important; }
    h2 { font-size: 1.4rem !important; }
    h3 { font-size: 1.1rem !important; }

    /* KPI Cards */
    .kpi-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: var(--radius);
        padding: 18px 20px;
        box-shadow: var(--shadow-card);
        transition: all 0.25s ease;
        position: relative;
        overflow: hidden;
    }

    .kpi-card:hover {
        border-color: var(--border-glow);
        transform: translateY(-2px);
    }

    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 3px;
        background: var(--gradient-blue);
    }

    .kpi-card.kpi-blue::before { background: var(--gradient-blue); }
    .kpi-card.kpi-green::before { background: var(--gradient-success); }
    .kpi-card.kpi-red::before { background: var(--gradient-danger); }
    .kpi-card.kpi-purple::before { background: linear-gradient(135deg, #8b5cf6, #a78bfa); }
    .kpi-card.kpi-cyan::before { background: linear-gradient(135deg, #06b6d4, #38bdf8); }

    .kpi-card .kpi-label {
        font-size: 0.72rem;
        font-weight: 600;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 6px;
    }

    .kpi-card .kpi-value {
        font-size: 1.75rem;
        font-weight: 800;
        color: var(--text-primary);
        line-height: 1.2;
    }

    .kpi-card .kpi-subtitle {
        font-size: 0.75rem;
        color: var(--text-secondary);
        margin-top: 6px;
    }

    /* Risk Badges */
    .risk-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    .risk-low {
        background: rgba(16, 185, 129, 0.12);
        color: var(--accent-green);
        border: 1px solid rgba(16, 185, 129, 0.3);
    }

    .risk-moderate {
        background: rgba(245, 158, 11, 0.12);
        color: var(--accent-yellow);
        border: 1px solid rgba(245, 158, 11, 0.3);
    }

    .risk-high {
        background: rgba(249, 115, 22, 0.12);
        color: var(--accent-orange);
        border: 1px solid rgba(249, 115, 22, 0.3);
    }

    .risk-critical {
        background: rgba(239, 68, 68, 0.15);
        color: var(--accent-red);
        border: 1px solid rgba(239, 68, 68, 0.4);
    }

    /* Section Container Cards */
    .section-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-lg);
        padding: 22px 24px;
        margin-bottom: 20px;
    }

    /* Banner Header */
    .header-banner {
        background: linear-gradient(135deg, #111726 0%, #0d121d 100%);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-lg);
        padding: 24px 28px;
        margin-bottom: 24px;
        position: relative;
    }

    .header-banner h1 {
        margin: 0 !important;
        font-size: 1.5rem !important;
    }

    .header-banner p {
        color: var(--text-secondary);
        font-size: 0.85rem;
        margin: 4px 0 0 0;
    }

    .header-banner .header-meta {
        font-size: 0.7rem;
        color: var(--text-muted);
        margin-top: 8px;
    }

    /* Custom Alert Banner */
    .alert-banner {
        background: rgba(239, 68, 68, 0.08);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: var(--radius);
        padding: 16px 20px;
        margin: 12px 0 20px 0;
    }

    .alert-banner .alert-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: var(--accent-red);
        margin-bottom: 4px;
    }

    .alert-banner .alert-text {
        font-size: 0.85rem;
        color: var(--text-primary);
    }

    /* Recommendation Card */
    .rec-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid var(--border-color);
        border-left: 4px solid var(--accent-blue);
        border-radius: var(--radius-sm);
        padding: 14px 18px;
        margin-bottom: 12px;
    }

    .rec-card.rec-critical { border-left-color: var(--accent-red); }
    .rec-card.rec-high { border-left-color: var(--accent-orange); }
    .rec-card.rec-medium { border-left-color: var(--accent-yellow); }
    .rec-card.rec-low { border-left-color: var(--accent-green); }

    /* Footer */
    .footer {
        text-align: center;
        padding: 20px;
        margin-top: 40px;
        border-top: 1px solid var(--border-color);
        color: var(--text-muted);
        font-size: 0.75rem;
    }

    /* Hide Streamlit Branding */
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
    """Generate HTML for a KPI card."""
    return f"""
    <div class="kpi-card kpi-{variant}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-subtitle">{subtitle}</div>
    </div>
    """

def render_risk_badge(category: str) -> str:
    """Generate HTML for a risk badge."""
    css_class = "risk-low"
    cat_upper = category.upper()
    if "MODERATE" in cat_upper:
        css_class = "risk-moderate"
    elif "HIGH" in cat_upper and "CRITICAL" not in cat_upper:
        css_class = "risk-high"
    elif "CRITICAL" in cat_upper:
        css_class = "risk-critical"

    return f'<span class="risk-badge {css_class}">{category}</span>'

def render_header_banner(title: str, subtitle: str, meta: str = "") -> str:
    """Generate HTML for the page header banner."""
    meta_html = f'<div class="header-meta">{meta}</div>' if meta else ""
    return f"""
    <div class="header-banner">
        <h1>{title}</h1>
        <p>{subtitle}</p>
        {meta_html}
    </div>
    """

def render_status_badge(text: str, status: str = "info") -> str:
    """Generate HTML for a status badge."""
    return f'<span class="status-badge status-{status}">{text}</span>'

def render_validation_item(text: str, is_valid: bool = True) -> str:
    """Generate HTML for validation item in data check."""
    icon = "✅" if is_valid else "⚠️"
    color = "var(--accent-green)" if is_valid else "var(--accent-yellow)"
    return f'<div style="margin: 4px 0; font-size: 0.88rem;"><span style="color:{color};">{icon}</span> {text}</div>'

__all__ = [
    "get_custom_css",
    "render_kpi_card",
    "render_risk_badge",
    "render_header_banner",
    "render_status_badge",
    "render_validation_item",
]
