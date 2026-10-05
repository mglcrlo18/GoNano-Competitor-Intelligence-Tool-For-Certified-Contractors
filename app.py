"""
app.py
PULSO-Standard Competitor Intelligence & Market Risk Terminal (Full Executive Edition).
Enforces Boxy Navy Blue Terminal Design System (0-radius geometry, monospaced typography).
Includes:
1. Executive Terminal UI (0-radius borders, Navy #1B1C36, Monospaced)
2. Embedded SQLite Evidence Persistence (competitor_store.db)
3. CRO / ERM Risk Framework (ISO 31000 & COSO - Inherent vs Residual Threat, KCIs, RST, Polarity-VaR)
4. Head-to-Head Scorecard with Evidence Citations (Clean HTML links, NO code-block leakage)
5. Dynamic Sales Battlecards & Objection Handling Playbooks
6. Silent Website & Pricing Diff Detector (DOM change radar)
7. Patent, Trademark & IP Moat Radar (USPTO, WIPO, CIPO)
8. Contractor & Dealer Channel Intelligence (Applicator churn & poaching radar)
9. Technical Formulation & ASTM Testing Teardown Lab (ASTM D3462, D3161, UL 2218)
10. Regional Geographic Territory Audit (US Sunbelt, Canada, Midwest, PacNW, APAC)
11. Brand Promise vs Customer Reality (Marketing Reality Gap Divergence Index)
12. Historical Trend Analysis (1900 to Present)
13. Domain Analytics & Google Sheets Competitor Tracker (Live Synced Roster)
14. YouTube & OSINT Multi-Source Stream (In-app video embed, Reddit, News, Ads)
15. Red Team War Room Simulator (AI rival executive persona via Gemini)
16. C-Suite Automated Alerting & Webhook Dispatch Engine
17. Board-Ready Export Engine (UTF-8 BOM .csv, SpreadsheetML .xls, Executive Memo .md)
"""
import os
import sys
import re
import json
import urllib
import urllib.parse
import base64
from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Core Databases & Analytical Engines
from db_manager import (
    get_connection,
    save_signals_to_db,
    get_all_signals_for_competitor,
    get_marketing_gaps,
    get_erm_risks,
    get_all_competitor_names,
    get_tracker_reports,
    add_custom_competitor,
    get_competitor_profile,
    get_all_competitor_profiles
)
from erm_engine import calculate_erm_threat_matrix, generate_erm_kpi_table
from head_to_head import get_head_to_head_comparison, COMPARATIVE_ENTITIES
from historical_trends import get_historical_era_comparison, HISTORICAL_ERA_DATABASE
from regional_audit import get_territory_audit_data
from messaging_gap import get_marketing_reality_gaps
from domain_analytics import get_domain_analytics
from export_engine import (
    generate_utf8_bom_csv,
    generate_spreadsheetml_xls,
    generate_csuite_markdown_memo
)

# New High-Leverage Engines
from battlecards import get_battlecard, BATTLECARDS_DATABASE
from site_diff_radar import compute_text_diff, HISTORICAL_PAGE_SNAPSHOTS
from ip_radar import get_competitor_ip_records, COMPETITOR_IP_PORTFOLIO
from dealer_intel import get_dealer_intel_records
from astm_teardown import get_astm_teardown_df
from alerting_engine import format_alert_payload, dispatch_webhook_alert, dispatch_telegram_alert
from red_team_simulator import simulate_rival_counter_attack

# Open-Source Ingestion Engines
from youtube_tracker import search_youtube_videos
from osint_listener import fetch_reddit_mentions, fetch_web_and_news_signals
from ads_tracker import get_public_ad_transparency_links, fetch_meta_ad_library_api
from analytics_engine import analyze_sentiment, compute_share_of_voice
from summarizer import generate_competitor_summary
from sheets_syncer import SPREADSHEET_URL, SPREADSHEET_ID
import textwrap
import heatmap_engine
import textwrap
import heatmap_engine


# -----------------------------------------------------------------------------
# BRAND ASSETS & LOGO RENDERER (LOCAL + CDN + TYPOGRAPHIC FALLBACK)
# -----------------------------------------------------------------------------
CDN_BASE = "https://cdn.jsdelivr.net/gh/mglcrlo18/GoNano-Competitor-Intelligence-Tool-For-Certified-Contractors@main/assets"

def get_logo_base64(is_light_logo: bool = True) -> str:
    filename = "gonano_light_color_logo.png" if is_light_logo else "gonano_logo_dark.png"
    local_path = Path(__file__).resolve().parent / "assets" / filename
    if local_path.exists():
        try:
            with open(local_path, "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8")
        except Exception:
            pass
    return ""

LOGO_B64_LIGHT = get_logo_base64(is_light_logo=True)
LOGO_B64_DARK = get_logo_base64(is_light_logo=False)

def render_logo_html(is_light: bool = True, height: int = 90, max_width: int = 280) -> str:
    b64 = LOGO_B64_LIGHT if is_light else LOGO_B64_DARK
    if b64:
        return f'<img src="data:image/png;base64,{b64}" style="height:{height}px; max-width:{max_width}px; width:auto; display:inline-block; vertical-align:middle; filter:drop-shadow(0 3px 6px rgba(0,0,0,0.22));" alt="GoNano Logo" />'
    fallback_color = "#FFFFFF" if is_light else "#1B1C36"
    return f"""<span style="font-family:'Montserrat', sans-serif; font-size:26px; font-weight:800; color:{fallback_color}; letter-spacing:0.04em;">GONANO</span>"""

# Page Configuration
st.set_page_config(
    page_title="GoNano Competitor Intelligence Dashboard // Certified Contractor Portal",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 1. VISUAL IDENTITY: FLOWY TACTILE DESIGN SYSTEM (EXECUTIVE EDITION UPGRADE)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400;1,600&family=JetBrains+Mono:wght@400;500;600&display=swap');

    :root {
        --canvas: #EEF1F6;
        --surface: #FFFFFF;
        --surface-soft: #F5F7FB;
        --primary: #675CE7;
        --primary-accent: #8583F2;
        --ink: #1B1C36;
        --slate: #596078;
        --pill-green-bg: #E6F8F3;
        --pill-green-fg: #087965;
        --pill-blue-bg: #EFEDFF;
        --pill-blue-fg: #5148C5;
        --pill-amber-bg: #FFF5DF;
        --pill-amber-fg: #9A6408;
        --pill-red-bg: #FFF0EA;
        --pill-red-fg: #AE481F;
    }

    html, body, [data-testid="stAppViewContainer"], .stMarkdown, p, h1, h2, h3, h4, h5, h6, [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
        font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    }

    button, input, select, textarea, .stSelectbox, .stTextInput {
        font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    code, pre, .terminal-mono {
        font-family: 'JetBrains Mono', 'Montserrat', monospace !important;
    }

    /* Preserve icon ligatures */
    [data-testid*="Icon"], [data-testid*="icon"], [data-testid="stExpanderToggleIcon"],
    .material-symbols-rounded, .material-symbols-outlined, .material-icons,
    span[data-testid*="Icon"], span[data-testid*="icon"], details summary span {
        font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
        font-feature-settings: 'liga' 1 !important;
    }

    /* Matte Neutral Canvas */
    [data-testid="stAppViewContainer"] {
        background-color: var(--canvas) !important;
    }

    /* BORDERLESS DUAL-SOURCE SOFT LIGHTING (Continuous G2 Curvature - No 1px borders) */
    .tactile-card, .pulso-tile {
        background: var(--surface) !important;
        border: none !important;
        outline: none !important;
        border-radius: 28px !important;
        box-shadow: -5px -5px 10px rgba(255, 255, 255, 0.85), 6px 6px 12px rgba(0, 0, 0, 0.06) !important;
        padding: 24px !important;
        margin-bottom: 20px !important;
        transition: all 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    }
    .tactile-card:hover, .pulso-tile:hover {
        box-shadow: -6px -6px 14px rgba(255, 255, 255, 0.95), 8px 8px 18px rgba(0, 0, 0, 0.08) !important;
    }

    .tactile-card-dark, .pulso-tile-dark {
        background: var(--ink) !important;
        border: none !important;
        outline: none !important;
        border-radius: 28px !important;
        box-shadow: -4px -4px 10px rgba(255, 255, 255, 0.15), 6px 6px 14px rgba(0, 0, 0, 0.25) !important;
        padding: 24px !important;
        color: #F8FAFC !important;
        margin-bottom: 20px !important;
    }

    /* Tactile Header Bar */
    .terminal-header {
        background-color: var(--ink) !important;
        border: none !important;
        border-radius: 28px !important;
        box-shadow: -4px -4px 10px rgba(255, 255, 255, 0.15), 6px 6px 14px rgba(0, 0, 0, 0.25) !important;
        padding: 22px 28px !important;
        margin-bottom: 24px !important;
        color: #F8FAFC !important;
    }
    .terminal-title {
        font-family: 'Montserrat', sans-serif !important;
        font-size: 19px !important;
        font-weight: 800 !important;
        letter-spacing: 0.02em !important;
        color: #F8FAFC !important;
        margin: 0 !important;
    }
    .terminal-sub {
        font-family: 'Montserrat', sans-serif !important;
        font-size: 11.5px !important;
        color: #94A3B8 !important;
        margin-top: 5px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.04em !important;
    }

    .tile-header {
        font-family: 'Montserrat', sans-serif !important;
        font-size: 12px !important;
        font-weight: 800 !important;
        color: var(--slate) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
        margin-bottom: 8px !important;
    }
    .tile-header-dark {
        font-family: 'Montserrat', sans-serif !important;
        font-size: 12px !important;
        font-weight: 800 !important;
        color: var(--primary-accent) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
        margin-bottom: 8px !important;
    }

    /* INSET DUAL-SOURCE SOFT LIGHTING (Recessed Controls) */
    input, textarea, .stTextInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"] {
        background: var(--canvas) !important;
        border: none !important;
        outline: none !important;
        border-radius: 9999px !important;
        box-shadow: inset -3px -3px 7px rgba(255, 255, 255, 0.85), inset 3px 3px 7px rgba(0, 0, 0, 0.06) !important;
        color: var(--ink) !important;
        padding: 10px 18px !important;
        font-family: 'Montserrat', sans-serif !important;
    }
    textarea, .stTextArea textarea {
        border-radius: 22px !important;
    }

    /* File uploader styling */
    [data-testid="stFileUploader"] {
        background: var(--surface) !important;
        border-radius: 24px !important;
        padding: 16px !important;
        box-shadow: -4px -4px 8px rgba(255, 255, 255, 0.85), 5px 5px 10px rgba(0, 0, 0, 0.05) !important;
        border: none !important;
    }

    /* CAPSULE BUTTONS (Physics-based spring motion) */
    .stButton>button {
        border: none !important;
        outline: none !important;
        border-radius: 9999px !important;
        background: var(--surface) !important;
        color: var(--ink) !important;
        font-weight: 700 !important;
        font-size: 13px !important;
        letter-spacing: 0.02em !important;
        padding: 10px 22px !important;
        box-shadow: -4px -4px 8px rgba(255, 255, 255, 0.85), 5px 5px 10px rgba(0, 0, 0, 0.06) !important;
        transition: all 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    }
    .stButton>button:hover {
        color: var(--primary) !important;
        box-shadow: -6px -6px 12px rgba(255, 255, 255, 0.95), 7px 7px 14px rgba(0, 0, 0, 0.09) !important;
        transform: translateY(-1px);
    }
    .stButton>button:active {
        box-shadow: inset -2px -2px 5px rgba(255, 255, 255, 0.85), inset 2px 2px 5px rgba(0, 0, 0, 0.07) !important;
        transform: translateY(1px);
    }

    /* Primary Capsule */
    button[kind="primary"], .stButton>button[kind="primary"] {
        background: var(--primary) !important;
        color: #FFFFFF !important;
        box-shadow: -3px -3px 8px rgba(255, 255, 255, 0.6), 5px 5px 12px rgba(103, 92, 231, 0.35) !important;
    }
    button[kind="primary"]:hover, .stButton>button[kind="primary"]:hover {
        background: #5B50D6 !important;
        color: #FFFFFF !important;
        box-shadow: -4px -4px 10px rgba(255, 255, 255, 0.8), 7px 7px 16px rgba(103, 92, 231, 0.45) !important;
    }

    /* SIDEBAR RAIL (Continuous Borderless Full-Bleed) */
    [data-testid="stSidebar"] {
        background-color: var(--ink) !important;
        border: none !important;
        box-shadow: 4px 0 16px rgba(0, 0, 0, 0.08) !important;
    }
    [data-testid="stSidebar"] * {
        color: #BEC2D6 !important;
    }
    [data-testid="stSidebar"] strong, [data-testid="stSidebar"] b {
        color: #F8FAFC !important;
    }

    /* SOLID CAPSULE STATUS PILLS & BADGES */
    .capsule-pill, .badge-terminal {
        display: inline-flex !important;
        align-items: center !important;
        border-radius: 9999px !important;
        padding: 5px 12px !important;
        font-size: 11px !important;
        font-weight: 700 !important;
        letter-spacing: 0.04em !important;
        text-transform: uppercase !important;
        border: none !important;
        margin-right: 6px !important;
        background: var(--pill-blue-bg) !important;
        color: var(--pill-blue-fg) !important;
    }
    .capsule-pill .bead {
        width: 7px;
        height: 7px;
        border-radius: 9999px;
        margin-right: 6px;
        display: inline-block;
    }
    .capsule-green, .badge-safe { background: var(--pill-green-bg) !important; color: var(--pill-green-fg) !important; }
    .capsule-green .bead { background: var(--pill-green-fg); }
    .capsule-blue { background: var(--pill-blue-bg) !important; color: var(--pill-blue-fg) !important; }
    .capsule-blue .bead { background: var(--pill-blue-fg); }
    .capsule-amber, .badge-moderate { background: var(--pill-amber-bg) !important; color: var(--pill-amber-fg) !important; }
    .capsule-amber .bead { background: var(--pill-amber-fg); }
    .capsule-red, .badge-critical { background: var(--pill-red-bg) !important; color: var(--pill-red-fg) !important; }
    .capsule-red .bead { background: var(--pill-red-fg); }

    /* Social Mentions Stream Card */
    .mention-card {
        background: var(--surface) !important;
        border: none !important;
        border-radius: 20px !important;
        box-shadow: -4px -4px 8px rgba(255, 255, 255, 0.85), 5px 5px 10px rgba(0, 0, 0, 0.05) !important;
        padding: 18px 22px !important;
        margin-bottom: 14px !important;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    }
    .mention-card:hover {
        box-shadow: -5px -5px 12px rgba(255, 255, 255, 0.95), 7px 7px 14px rgba(0, 0, 0, 0.08) !important;
        transform: translateY(-1px);
    }

    /* Clean, Verified Citation Hyperlinks */
    .citation-block {
        margin-top: 12px !important;
        padding-top: 10px !important;
        border-top: 1px solid rgba(0, 0, 0, 0.05) !important;
    }
    .citation-item {
        font-size: 12.5px !important;
        margin-bottom: 6px !important;
        line-height: 1.5 !important;
        color: var(--slate) !important;
    }
    .citation-link {
        font-weight: 700 !important;
        color: var(--primary) !important;
        text-decoration: none !important;
    }
    .citation-link:hover {
        text-decoration: underline !important;
    }
    .citation-tag {
        font-family: 'Montserrat', sans-serif !important;
        font-size: 10px !important;
        font-weight: 700 !important;
        color: var(--primary) !important;
        background: var(--pill-blue-bg) !important;
        padding: 2px 8px !important;
        border-radius: 9999px !important;
        margin-left: 6px !important;
    }

    /* Expanders styling */
    [data-testid="stExpander"] {
        background: var(--surface) !important;
        border-radius: 20px !important;
        border: none !important;
        box-shadow: -4px -4px 8px rgba(255, 255, 255, 0.85), 5px 5px 10px rgba(0, 0, 0, 0.05) !important;
        margin-bottom: 14px !important;
    }
</style>
""", unsafe_allow_html=True)

# AUTHENTICATION: ACCOUNT SIGN-IN
# -----------------------------------------------------------------------------
if "authenticated_contractor" not in st.session_state:
    st.session_state.authenticated_contractor = None

if not st.session_state.authenticated_contractor:
    st.html(f"""
    <div style="text-align:center; margin: 24px auto 14px auto; max-width: 520px;">
        {render_logo_html(is_light=False, height=75, max_width=250)}
    </div>
    <div class="tactile-card" style="max-width:520px; margin: 0 auto 18px auto; padding:28px 32px;">
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:10px;">
            <span class="capsule-pill capsule-blue" style="font-size:10px;">
                <span class="bead"></span>Contractor Authentication
            </span>
        </div>
        <div style="font-family:'Montserrat', sans-serif; font-size:20px; font-weight:800; color:var(--ink); margin-bottom:4px;">
            Account Sign-In
        </div>
        <div style="font-size:12.5px; color:var(--slate); line-height:1.5;">
            GoNano Competitor Intelligence Dashboard. Enter your registered credentials to access your verified contractor terminal.
        </div>
    </div>
    """)
    with st.container():
        _, login_col, _ = st.columns([1, 2.2, 1])
        with login_col:
            from db_manager import authenticate_contractor, log_contractor_account_request

            with st.form("contractor_account_login_form"):
                st.markdown("##### 🔑 Account Sign-In")
                login_email = st.text_input(
                    "User",
                    placeholder="User",
                    key="c_login_email"
                )
                login_password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Password",
                    key="c_login_password"
                )

                submit_login = st.form_submit_button("Sign In", width="stretch", type="primary")

                if submit_login:
                    clean_email = (login_email or "").strip().lower()
                    clean_pass = (login_password or "").strip()

                    if not clean_email:
                        st.error("Please enter your User.")
                    elif not clean_pass:
                        st.error("Please enter your Password.")
                    else:
                        account = authenticate_contractor(clean_email, clean_pass)
                        if account:
                            st.session_state.authenticated_contractor = {
                                "name": account["name"],
                                "company": account["business_name"],
                                "area": account.get("business_area", "Certified Territory"),
                                "email": account["email"],
                                "phone": "",
                                "role": account.get("role", "certified_contractor")
                            }
                            st.success(f"Welcome back, {account['name']} ({account['business_name']})! Access granted.")
                            st.rerun()
                        else:
                            st.error("Invalid user or password. Contractor accounts must be provisioned by GoNano. Please verify your credentials or submit an account request below.")

            # Self-Service Account Request Expander
            st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
            with st.expander("📝 Need an Account? Request Contractor Credentials"):
                st.markdown("##### New Certified Contractor Access Request")
                st.caption("Accounts must be created from our end. Submit your business information below and our team will verify your territory and email your login credentials.")
                
                with st.form("contractor_access_request_form", clear_on_submit=True):
                    req_name = st.text_input("1. Name *", placeholder="e.g. Marc Leclerc")
                    req_biz = st.text_input("2. Name of Business *", placeholder="e.g. Apex Roofing Solutions")
                    req_area = st.text_input("3. Area of Business *", placeholder="e.g. Montreal, QC / Ottawa, ON")
                    req_email = st.text_input("4. Email * (We will send your login credentials here)", placeholder="e.g. marc@apexroofing.ca")
                    
                    submit_acc_req = st.form_submit_button("Submit Account Request to GoNano", width="stretch", type="primary")

                    if submit_acc_req:
                        if not req_name.strip() or not req_biz.strip() or not req_area.strip() or not req_email.strip():
                            st.error("Please complete all 4 required fields.")
                        elif "@" not in req_email:
                            st.error("Please enter a valid email address.")
                        else:
                            log_contractor_account_request(req_name, req_biz, req_area, req_email)
                            
                            # Send administrative alert to Miguel Gonzales
                            try:
                                from email_dispatcher import send_contractor_analysis_request
                                send_contractor_analysis_request(
                                    competitor_name=f"NEW ACCOUNT REQUEST: {req_biz}",
                                    location=req_area,
                                    url="https://docs.google.com/spreadsheets/d/1NcjhmtfFDHRWnf5SqT4GABzTvPVFZ3Z6RHMH2QvrU3A/edit",
                                    contractor_name=req_name,
                                    contractor_email=req_email,
                                    contractor_phone="",
                                    notes=f"New Certified Contractor account requested by {req_name} from {req_biz} in territory {req_area}. Registered email: {req_email}. Please provision credentials in the Google Sheet tracker.",
                                    recipient_email="miguel.gonzales@gonano.com"
                                )
                            except Exception:
                                pass

                            st.success(f"✅ Account request submitted! Your details have been routed to GoNano administration. Miguel Gonzales will review your territory ({req_area}) and email your login credentials to {req_email}.")
                            st.markdown("[📊 View Account Request Tracker & Access Management Sheet](https://docs.google.com/spreadsheets/d/1NcjhmtfFDHRWnf5SqT4GABzTvPVFZ3Z6RHMH2QvrU3A/edit)")

    st.stop()

# -----------------------------------------------------------------------------
# SIDEBAR: TERMINAL NAVIGATION & FLEXIBLE SEARCH CONTROLS
# -----------------------------------------------------------------------------
contractor_user = st.session_state.authenticated_contractor

# Prominent Official GoNano Logo
st.sidebar.markdown(f"""
<div style="padding: 12px 0 18px 0; text-align:center;">
    {render_logo_html(is_light=True, height=75, max_width=260)}
</div>
""", unsafe_allow_html=True)
st.sidebar.html(f"""
<div class="tactile-card-dark" style="padding:18px 20px; margin-bottom:18px; border-radius:22px !important;">
    <div class="capsule-pill capsule-green" style="font-size:9.5px; padding:3px 10px; margin-bottom:8px;">
        <span class="bead"></span>VERIFIED CONTRACTOR
    </div>
    <div style="font-family:'Montserrat', sans-serif; font-weight:800; color:#F8FAFC; font-size:14px; margin-top:2px;">{contractor_user['name']}</div>
    <div style="font-family:'Montserrat', sans-serif; font-size:11.5px; color:#BEC2D6; margin-top:2px;">{contractor_user['company']}</div>
    <div style="font-family:'Montserrat', sans-serif; font-size:10.5px; color:#8583F2; margin-top:4px;">{contractor_user['email']}</div>
</div>
""")
if st.sidebar.button("Log Out / Switch Account", width="stretch"):
    st.session_state.authenticated_contractor = None
    st.rerun()


# Load ALL monitored competitors dynamically from database / Google Sheet
ALL_COMPETITORS = get_all_competitor_names()

st.sidebar.markdown("**Time Horizon**")
time_horizon = st.sidebar.selectbox(
    "TIME_HORIZON_FILTER",
    ["24 Hours", "7 Days", "30 Days", "90 Days", "1 Year", "All Time"],
    index=2,
    help="Filters signals, risk metrics, and threat heatmaps across the selected time horizon."
)

# Maintain active target in session state (default is None unless searched)
if "active_target" not in st.session_state:
    st.session_state.active_target = None

st.sidebar.markdown("**Target Competitor**")
search_term = st.sidebar.text_input(
    "Search Competitor",
    value="",
    placeholder="Type competitor name (e.g. Roof Maxx)...",
    key="sidebar_search_input",
    label_visibility="collapsed"
)

if search_term.strip():
    st.session_state.active_target = search_term.strip()

active_target = st.session_state.active_target
if active_target:
    st.sidebar.caption(f"Active Subject: **{active_target}**")
else:
    st.sidebar.caption("Active Subject: *None (Search to isolate)*")

# Safe fallback for analytical engines when in Global/Unselected mode

# Quick Expand Tool: Add any custom competitor to monitor
with st.sidebar.expander("Add Custom Competitor"):
    with st.form("add_comp_form", clear_on_submit=True):
        new_name = st.text_input("Competitor Name", placeholder="e.g. Acme Roof Rejuvenation")
        new_dom = st.text_input("Domain / Website", placeholder="e.g. acmeroof.com")
        new_cat = st.selectbox(
            "Category",
            ["Topical Bio-Oil Roof Rejuvenator", "Nanotechnology / Surface Coating", "Architectural & Elastomeric Coatings", "Roof Restoration & Preservation"]
        )
        new_notes = st.text_input("Notes / Intelligence", placeholder="Flagged by sales team...")
        submitted = st.form_submit_button("Add to Monitored Roster")
        if submitted and new_name.strip():
            add_custom_competitor(new_name, new_dom, new_cat, new_notes)
            st.success(f"Added {new_name} to monitored roster!")
            st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("**Database Status**")
conn = get_connection()
c_count = conn.cursor().execute("SELECT COUNT(*) as c FROM signals").fetchone()["c"]
p_count = conn.cursor().execute("SELECT COUNT(*) as c FROM competitor_profiles").fetchone()["c"]
g_count = conn.cursor().execute("SELECT COUNT(*) as c FROM marketing_gap_records").fetchone()["c"]
t_count = conn.cursor().execute("SELECT COUNT(*) as c FROM tracker_reports").fetchone()["c"]
conn.close()

st.sidebar.markdown(f"- Persistent SQLite Store: `ONLINE`")
st.sidebar.markdown(f"- Monitored Competitors: `{p_count}` entities")
st.sidebar.markdown(f"- Google Sheets Reports Logged: `{t_count}` records")
st.sidebar.markdown(f"- Verified Marketing Gaps: `{g_count}` dossiers")
st.sidebar.markdown(f"- Live Signals Ingested: `{c_count}` records")

if st.sidebar.button("RE-INDEX EVIDENCE DATABASE"):
    st.cache_data.clear()
    st.rerun()

# External Integrations hidden per certified contractor terminal requirements

# -----------------------------------------------------------------------------
# TOP EXECUTIVE TERMINAL BANNER
# -----------------------------------------------------------------------------
subject_str = active_target.upper() if active_target else "ALL COMPETITORS (GLOBAL OVERVIEW)"
st.html(f"""
<div class="terminal-header" style="padding:22px 28px; margin-bottom:24px;">
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
        <div>
            <div class="terminal-title">
                GONANO COMPETITOR INTELLIGENCE DASHBOARD // CONTRACTOR PORTAL
            </div>
            <div class="terminal-sub">
                Contractor Field Terminal &bull; Active Subject: <span style="color:#8583F2; font-weight:700;">{subject_str}</span> &bull; Verified Sales Battlecards & Teardown Requests
            </div>
        </div>
        <div>
            <span class="capsule-pill capsule-blue" style="font-size:10.5px;">
                <span class="bead"></span>LIVE RADAR
            </span>
        </div>
    </div>
</div>
""")

# Top-level quick search & reset
top_c1, top_c2 = st.columns([3, 1])
with top_c1:
    top_search = st.text_input(
        "Direct Competitor Search",
        value="",
        placeholder="Type any brand (e.g. Roof Maxx, PEAK301, DuraSeal, Ever Roof, Nasiol, or custom entity)...",
        key="top_main_search_input",
        label_visibility="collapsed"
    )
    if top_search.strip():
        st.session_state.active_target = top_search.strip()
        active_target = st.session_state.active_target
with top_c2:
    if st.button("Clear Active Subject", width="stretch"):
        st.session_state.active_target = None
        st.rerun()

# -----------------------------------------------------------------------------
# TAB NAVIGATION (COMPREHENSIVE 16-ENGINE ARCHITECTURE)
# -----------------------------------------------------------------------------
# Determine C-Suite executive privilege
is_csuite_user = contractor_user.get('email', '').lower() in [
    'miguel.gonzales@gonano.com',
    'gonzalesmiguelcarlo@gmail.com',
    'mcbgonzales@outlook.com'
] or 'Executive' in contractor_user.get('company', '') or 'Strategic Intelligence' in contractor_user.get('company', '')

base_tab_names = [
    "1. Request Competitor Analysis",
    "2. Sales Battlecards",
    "3. Head-to-Head Scorecard",
    "4. Brand Promise vs Reality",
    "5. Silent DOM Diff Radar",
    "6. Patent & IP Radar",
    "7. Contractor Channel Intel",
    "8. Technical ASTM Lab",
    "9. Territory Audit",
    "10. Enterprise Domain Analytics",
    "11. YouTube & OSINT Stream",
    "12. Red Team War Room",
    "13. Risk Analysis Register",
    "14. Export Infrastructure",
    "15. Threat & Sentiment Heatmap"
]

if is_csuite_user:
    base_tab_names.append("16. C-Suite Request Dispatch & Gemini Auto-Tracker")

base_tab_names.append("17. Commercial APIs & AEO Radar")

tabs = st.tabs(base_tab_names)

# -----------------------------------------------------------------------------
# TAB 1: ERM RISK MATRIX & CRO ANALYSIS ENGINE
# -----------------------------------------------------------------------------
with tabs[0]:
    try:
        st.markdown("### Request Competitor Analysis")
        st.caption("Encountered a rival coating brand or new applicator in your market? Submit the competitor details and marketing screenshots below. Our GoNano Competitive Intelligence team will analyze their chemistry, benchmark their claims against ASTM standards, and equip you with actionable sales battlecards.")

        with st.form("contractor_inquiry_form", clear_on_submit=False):
            st.markdown("##### 1. Competitor Identification")
            r_col1, r_col2 = st.columns(2)
            with r_col1:
                req_comp = st.text_input("1. Competitor Name *", placeholder="e.g. Apex Roof Solutions, BioGuard Spray, ShieldTech...")
            with r_col2:
                req_loc = st.text_input("2. Location / Market Area *", placeholder="e.g. Ottawa, ON or Dallas-Fort Worth, TX...")

            st.markdown("##### 2. Online & Social Presence")
            u_col1, u_col2, u_col3 = st.columns(3)
            with u_col1:
                req_url = st.text_input("3. Website URL", placeholder="https://competitorwebsite.com")
            with u_col2:
                req_fb = st.text_input("4. Facebook Link", placeholder="https://facebook.com/competitorpage")
            with u_col3:
                req_ig = st.text_input("5. Instagram Link", placeholder="https://instagram.com/competitorhandle")

            st.markdown("##### 3. Submitting Certified Contractor Info (Verified Identity)")
            c_col1, c_col2, c_col3 = st.columns(3)
            with c_col1:
                c_name = st.text_input("Your Name / Entity", value=f"{contractor_user['name']} ({contractor_user['company']})", disabled=True)
            with c_col2:
                c_email = st.text_input("Your Email Address (Originating Account)", value=contractor_user['email'], disabled=True)
            with c_col3:
                c_phone = st.text_input("Your Phone Number", value=contractor_user.get('phone', ''), placeholder="e.g. (555) 123-4567")

            st.markdown("##### 4. Field Notes & Commercial Observations")
            c_notes = st.text_area(
                "Observations, Claims, or Pricing Encountered",
                placeholder="What claims did this competitor make to homeowners? Did they offer a specific warranty, quote a per-sqft price, or claim bio-oil/ceramic superiority? Describe what you're seeing in the field...",
                height=110
            )

            st.markdown("##### 5. Upload Evidence & Screenshots")
            st.caption("Upload homeowner quotes, marketing flyers, warranty certificates, or social media ad screenshots.")
            uploaded_screenshots = st.file_uploader(
                "Upload Screenshots / Evidence",
                type=["png", "jpg", "jpeg", "webp", "pdf"],
                accept_multiple_files=True,
                help="You can upload multiple screenshots. They will be archived and attached directly to the inquiry email sent to miguel.gonzales@gonano.com."
            )

            submit_inquiry = st.form_submit_button("Send Competitor Analysis Request", width="stretch", type="primary")

            if submit_inquiry:
                if not req_comp.strip():
                    st.error("Please provide the Competitor Name before submitting.")
                elif not req_loc.strip():
                    st.error("Please provide the Competitor Location / Market Area before submitting.")
                else:
                    with st.spinner("Dispatching request and archiving evidence to GoNano Intelligence..."):
                        from email_dispatcher import send_contractor_analysis_request
                        from db_manager import log_contractor_request, add_custom_competitor

                        res = send_contractor_analysis_request(
                            competitor_name=req_comp.strip(),
                            location=req_loc.strip(),
                            url=req_url.strip(),
                            facebook_link=req_fb.strip(),
                            instagram_link=req_ig.strip(),
                            contractor_name=contractor_user['name'],
                            contractor_email=contractor_user['email'],
                            contractor_phone=c_phone.strip(),
                            contractor_company=contractor_user['company'],
                            contractor_smtp_password=contractor_user.get('smtp_pass', ''),
                            notes=c_notes.strip(),
                            uploaded_files=uploaded_screenshots,
                            recipient_email="miguel.gonzales@gonano.com"
                        )

                        att_names = ", ".join([f.name for f in uploaded_screenshots]) if uploaded_screenshots else ""
                        log_contractor_request({
                            "contractor_name": c_name.strip() or "GoNano Certified Contractor",
                            "contractor_email": c_email.strip(),
                            "contractor_phone": c_phone.strip(),
                            "competitor_name": req_comp.strip(),
                            "location": req_loc.strip(),
                            "url": req_url.strip(),
                            "facebook_link": req_fb.strip(),
                            "instagram_link": req_ig.strip(),
                            "notes": c_notes.strip(),
                            "attachment_names": att_names
                        })

                        add_custom_competitor(
                            name=req_comp.strip(),
                            domain=req_url.strip(),
                            category="Field-Reported Competitor",
                            notes=f"Reported in {req_loc.strip()} by {c_name.strip() or 'Certified Contractor'}: {c_notes.strip()[:100]}"
                        )

                        if res.get("status") == "success":
                            st.html(f"""
                            <div style="background:#F0FDF4; border:1px solid #BBF7D0; border-left:4px solid #16A34A; padding:18px; margin-top:16px;">
                                <div style="font-family:'Montserrat', sans-serif; font-size:16px; font-weight:700; color:#14532D; margin-bottom:6px;">
                                    REQUEST DISPATCHED FROM YOUR ACCOUNT
                                </div>
                                <div style="font-size:13px; color:#166534; line-height:1.5;">
                                    Your analysis request for <strong>{req_comp}</strong> ({req_loc}) has been dispatched from your verified account (<strong>{contractor_user['email']}</strong>) to <strong>miguel.gonzales@gonano.com</strong>.<br>
                                    A confirmation receipt has also been routed to your inbox. When Miguel responds, the reply will route directly to <strong>{contractor_user['email']}</strong>.<br>
                                    Our technical intelligence team will review the submitted links and {len(uploaded_screenshots) if uploaded_screenshots else 0} screenshot(s), benchmark the competitor against GoNano, and prepare updated sales objection battlecards.
                                </div>
                            </div>
                            """)
                        else:
                            st.error(f"⚠️ Email delivery failed: {res.get('message', 'Please check SMTP settings in Streamlit secrets.')}")

        st.markdown("---")
        st.markdown("##### Previously Submitted Field Requests")
        from db_manager import get_all_contractor_requests
        req_list = get_all_contractor_requests()
        if req_list:
            req_df = pd.DataFrame(req_list)[["timestamp_pht", "competitor_name", "location", "url", "contractor_name", "status"]]
            req_df.columns = ["Submitted Date", "Competitor Name", "Location", "Website", "Submitted By", "Review Status"]
            st.dataframe(req_df, hide_index=True, width="stretch")
        else:
            st.caption("No competitor requests logged yet. Use the form above to submit your first inquiry.")

    except Exception as tab_err:
        st.error(f"Intelligence Module Advisory: Encountered a non-fatal exception ({type(tab_err).__name__}: {tab_err}). The rest of the terminal remains fully functional.")

with tabs[1]:
    try:
        target_header = active_target if active_target else "All Competitors"
        st.markdown(f"#### Sales Battlecards & Objection Playbook: {target_header}")
        st.caption("Actionable counter-arguments, fact-checked rebuttals, and landmine questions for field sales reps.")
        if not active_target:
            st.info("💡 **Battlecard Search:** Type any competitor name in the search box to load its dedicated sales objection playbook.")

        bcard = get_battlecard(active_target if active_target else "RoofLife Canada")
    
        b_col1, b_col2 = st.columns([1.2, 1])
        with b_col1:
            st.html(f"""
            <div class="pulso-tile">
                <div class="tile-header">Rival Commercial Positioning & Pricing Anchor</div>
                <div style="font-size:13px; font-weight:700; color:#1B1C36;">Target: {bcard['competitor_name']} ({bcard['category']})</div>
                <div style="font-family:'Montserrat', sans-serif; font-size:12px; color:#675CE7; margin:6px 0;">Estimated Pricing: {bcard['rival_pricing_anchor']}</div>
                <div style="font-size:12px; font-style:italic; color:#475569; background:#F8FAFC; border:1px solid #E2E8F0; padding:8px;">"{bcard['rival_core_hook']}"</div>
                <div style="margin-top:10px; font-size:12px; line-height:1.5;"><strong>Executive Rebuttal:</strong><br>{bcard['quick_rebuttal']}</div>
            </div>
            """)

            st.markdown("##### Fact-Checked Rebuttal Matrix")
            for item in bcard["claims_vs_facts"]:
                st.html(f"""
                <div style="background:#FFFFFF; border:1px solid #CBD5E1; border-left:3px solid #DC2626; padding:10px; margin-bottom:10px;">
                    <div style="font-size:12px; color:#DC2626; font-weight:700;">RIVAL CLAIM: "{item['claim']}"</div>
                    <div style="font-size:12px; color:#166534; font-weight:600; margin-top:4px;">SCIENTIFIC FACT: {item['fact']}</div>
                </div>
                """)

        with b_col2:
            st.markdown("##### Strategic Landmines for Buyers")
            st.caption("Advise the customer or property manager to ask the competitor these direct technical questions:")
            for lm in bcard["landmines_to_plant"]:
                st.html(f"""
                <div style="background:#FFFBEB; border:1px solid #FCD34D; border-left:3px solid #D97706; padding:10px; margin-bottom:8px; font-size:12px; color:#92400E; font-weight:600;">
                    Key Question: {lm}
                </div>
                """)

            st.markdown("##### Objection Handling Scripts")
            for obj in bcard["objection_handling"]:
                with st.expander(f"Q: '{obj['objection'][:45]}...'"):
                    obj_txt = obj['objection']
                    resp_txt = obj['response']
                    st.markdown(f"**Customer Objection:** *{obj_txt}*")
                    st.markdown(f"**GoNano Field Response:**\n\n{resp_txt}")

    # -----------------------------------------------------------------------------
    # TAB 3: HEAD-TO-HEAD COMPARATIVE SCORECARD (CLEAN CITATIONS)
    # -----------------------------------------------------------------------------
    except Exception as tab_err:
        st.error(f"Intelligence Module Advisory: Encountered a non-fatal exception ({type(tab_err).__name__}: {tab_err}). The rest of the terminal remains fully functional.")

with tabs[2]:
    try:
        st.markdown("#### Head-to-Head Scorecard - Empirical Benchmark")
        st.caption("Side-by-side scorecard where every single metric is backed by verified evidence citations. Flexible selection across all 60+ monitored entities.")

        h2h_c1, h2h_c2 = st.columns(2)
        with h2h_c1:
            def_a = ALL_COMPETITORS.index("GoNano (Your Brand)") if "GoNano (Your Brand)" in ALL_COMPETITORS else 0
            comp_a = st.selectbox("ENTITY_A (Baseline)", ALL_COMPETITORS, index=def_a)
        with h2h_c2:
            def_b = ALL_COMPETITORS.index(active_target) if active_target in ALL_COMPETITORS and active_target != comp_a else (1 if len(ALL_COMPETITORS) > 1 else 0)
            comp_b = st.selectbox("ENTITY_B (Comparison)", ALL_COMPETITORS, index=def_b)

        h2h_data = get_head_to_head_comparison(comp_a, comp_b)
        da = h2h_data["brand_a_data"]
        db = h2h_data["brand_b_data"]

        st.markdown("<br>", unsafe_allow_html=True)

        # Build clean HTML citation blocks
        def render_citations_html(citations_list):
            h = "<div class='citation-block'><div class='tile-header'>Underlying Evidence Citations</div>"
            for cit in citations_list:
                h += f"<div class='citation-item'>• <a href='{cit['url']}' target='_blank' class='citation-link'>{cit['title']}</a> <span class='citation-tag'>SOURCE -></span> <span style='font-size:11px; color:#64748B;'>({cit['outlet']})</span></div>"
            h += "</div>"
            return h

        c_a, c_b = st.columns(2)
        with c_a:
            st.html(f"""
            <div class="pulso-tile">
                <div style="font-family:'Montserrat', sans-serif; font-size:14px; font-weight:700; color:#1B1C36; border-bottom:2px solid #1B1C36; padding-bottom:4px; margin-bottom:12px;">{comp_a} - Baseline Profile</div>
                <p style="font-size:12px; margin:4px 0;"><strong>Core Chemistry / Tech:</strong><br>{da['technology_class']}</p>
                <p style="font-size:12px; margin:4px 0;"><strong>Durability & Warranty:</strong><br>{da['durability_warranty']}</p>
                <p style="font-size:12px; margin:4px 0;"><strong>Impact & Hail Resistance:</strong><br>{da['impact_hail_rating']}</p>
                <p style="font-size:12px; margin:4px 0;"><strong>Insurance Compliance:</strong><br>{da['insurance_compliance']}</p>
                <p style="font-size:12px; margin:4px 0;"><strong>Estimated Cost / Sq.Ft:</strong><br>{da['avg_sqft_cost']}</p>
                <p style="font-size:12px; margin:4px 0;"><strong>Net Polarity Index:</strong> <span style="font-family:'Montserrat', sans-serif; font-weight:700; color:#675CE7;">{da['net_polarity_index']}</span></p>
                {render_citations_html(da['evidence_citations'])}
            </div>
            """)

        with c_b:
            st.html(f"""
            <div class="pulso-tile">
                <div style="font-family:'Montserrat', sans-serif; font-size:14px; font-weight:700; color:#1B1C36; border-bottom:2px solid #1B1C36; padding-bottom:4px; margin-bottom:12px;">{comp_b} - Rival Profile</div>
                <p style="font-size:12px; margin:4px 0;"><strong>Core Chemistry / Tech:</strong><br>{db['technology_class']}</p>
                <p style="font-size:12px; margin:4px 0;"><strong>Durability & Warranty:</strong><br>{db['durability_warranty']}</p>
                <p style="font-size:12px; margin:4px 0;"><strong>Impact & Hail Resistance:</strong><br>{db['impact_hail_rating']}</p>
                <p style="font-size:12px; margin:4px 0;"><strong>Insurance Compliance:</strong><br>{db['insurance_compliance']}</p>
                <p style="font-size:12px; margin:4px 0;"><strong>Estimated Cost / Sq.Ft:</strong><br>{db['avg_sqft_cost']}</p>
                <p style="font-size:12px; margin:4px 0;"><strong>Net Polarity Index:</strong> <span style="font-family:'Montserrat', sans-serif; font-weight:700; color:#DC2626;">{db['net_polarity_index']}</span></p>
                {render_citations_html(db['evidence_citations'])}
            </div>
            """)

    # -----------------------------------------------------------------------------
    # TAB 4: BRAND PROMISE VS. CUSTOMER REALITY (MARKETING REALITY GAP)
    # -----------------------------------------------------------------------------
    except Exception as tab_err:
        st.error(f"Intelligence Module Advisory: Encountered a non-fatal exception ({type(tab_err).__name__}: {tab_err}). The rest of the terminal remains fully functional.")

with tabs[3]:
    try:
        st.markdown("#### Marketing Reality Gap - Narrative Divergence Index")
        st.caption("Contrasting official brand assertions against ground-level customer feedback to calculate narrative divergence. Completely rendered via native HTML cards to prevent markdown code leakage.")

        col_g1, col_g2 = st.columns([1.5, 1])
        with col_g1:
            gap_search = st.text_input("SEARCH_GAP_REPORTS", placeholder="Type any competitor, keyword (e.g. warranty, bio-oil, hail)...")
        with col_g2:
            gap_filter_opts = ["All Competitors"] + ALL_COMPETITORS
            def_gap_idx = gap_filter_opts.index(active_target) if active_target in gap_filter_opts else 0
            gap_filter = st.selectbox("FILTER_BY_COMPETITOR", gap_filter_opts, index=def_gap_idx)

        effective_filter = gap_search.strip() if gap_search.strip() else gap_filter
        gaps = get_marketing_reality_gaps(effective_filter)

        if not gaps:
            st.info(f"No marketing gap records found matching '{effective_filter}'.")

        # Render each gap report card via st.html() to guarantee 0 code leakage
        for g in gaps:
            sev_class = "badge-critical" if g.get("gap_severity") == "CRITICAL" else ("badge-moderate" if g.get("gap_severity") == "HIGH" else "badge-terminal")
            gap_card_html = f"""<div style="background:#FFFFFF; border:1px solid #CBD5E1; border-left:4px solid #1B1C36; padding:16px; margin-bottom:16px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <span style="font-family:'Montserrat', sans-serif; font-weight:700; font-size:13px; color:#1B1C36;">{g.get('competitor', '')} - Gap Analysis</span>
                    <div>
                        <span class="badge-terminal {sev_class}">SEVERITY: {g.get('gap_severity', 'MODERATE')}</span>
                        <span class="badge-terminal">DIVERGENCE: {g.get('divergence_score', 50)}%</span>
                    </div>
                </div>
            
                <div style="display:grid; grid-template-columns: 1fr 1fr; gap:16px; margin:12px 0;">
                    <div style="background:#F0FDF4; border:1px solid #BBF7D0; padding:12px;">
                        <div style="font-family:'Montserrat', sans-serif; font-size:11px; font-weight:700; color:#166534; text-transform:uppercase;">Official Brand Promise</div>
                        <div style="font-size:13px; font-weight:600; color:#14532D; margin:4px 0;">"{g.get('claim_headline', '')}"</div>
                        <div style="font-size:11px; color:#166534; line-height:1.4;">{g.get('claim_quote', '')}</div>
                        <div style="margin-top:6px;"><a href="{g.get('claim_url', '#')}" target="_blank" class="citation-link">{g.get('claim_source', 'Official Source')} <span class="citation-tag">CLAIM_SOURCE -></span></a></div>
                    </div>

                    <div style="background:#FEF2F2; border:1px solid #FECACA; padding:12px;">
                        <div style="font-family:'Montserrat', sans-serif; font-size:11px; font-weight:700; color:#991B1B; text-transform:uppercase;">Customer & Market Reality</div>
                        <div style="font-size:13px; font-weight:600; color:#7F1D1D; margin:4px 0;">"{g.get('reality_headline', '')}"</div>
                        <div style="font-size:11px; color:#991B1B; line-height:1.4;">{g.get('reality_quote', '')}</div>
                        <div style="margin-top:6px;"><a href="{g.get('reality_url', '#')}" target="_blank" class="citation-link">{g.get('reality_source', 'Customer Audit')} <span class="citation-tag">EVIDENCE_SOURCE -></span></a></div>
                    </div>
                </div>

                <div style="background:#F8FAFC; border:1px solid #E2E8F0; padding:10px; font-size:12px;">
                    <strong style="font-family:'Montserrat', sans-serif; color:#1B1C36;">GONANO STRATEGIC EXPLOITATION:</strong> {g.get('strategic_takeaway', '')}
                </div>
            </div>"""
            st.html(gap_card_html)

    # -----------------------------------------------------------------------------
    # TAB 5: SILENT WEBSITE & PRICING DIFF DETECTOR
    # -----------------------------------------------------------------------------
    except Exception as tab_err:
        st.error(f"Intelligence Module Advisory: Encountered a non-fatal exception ({type(tab_err).__name__}: {tab_err}). The rest of the terminal remains fully functional.")

with tabs[4]:
    try:
        target_diff_title = active_target if active_target else "All Monitored Portals"
        st.markdown(f"#### Website Change Radar - Stealth Changes: {target_diff_title}")
        st.caption("Detects unannounced competitor warranty changes, price increases, and stealth terms modifications.")

        diff_data = compute_text_diff(active_target if active_target else "Roof Maxx")
    
        if diff_data.get('url'):
            st.markdown(f"**Target Monitored Endpoint:** [{diff_data['url']}]({diff_data['url']})")
        else:
            st.markdown("**Target Monitored Endpoint:** *Pricing Not Publicly Disclosed — Available via Field Sales Inquiries (Offline Intelligence Tracking)*")
        st.caption(f"Comparing **{diff_data['baseline_date']}** against **{diff_data['current_date']}**")

        d_col1, d_col2 = st.columns(2)
        with d_col1:
            st.markdown("##### Deletions - Removed or Weakened Clauses")
            for del_line in diff_data["deletions"]:
                st.html(f"""
                <div style="background:#FEF2F2; border:1px solid #F87171; border-left:3px solid #DC2626; padding:8px; margin-bottom:6px; font-family:'Montserrat', sans-serif; font-size:11px; color:#991B1B;">
                    - {del_line}
                </div>
                """)
            
        with d_col2:
            st.markdown("##### Additions - Silent Pricing and Exclusions")
            for add_line in diff_data["additions"]:
                st.html(f"""
                <div style="background:#F0FDF4; border:1px solid #86EFAC; border-left:3px solid #16A34A; padding:8px; margin-bottom:6px; font-family:'Montserrat', sans-serif; font-size:11px; color:#166534;">
                    + {add_line}
                </div>
                """)

    # -----------------------------------------------------------------------------
    # TAB 6: PATENT, TRADEMARK & IP MOAT RADAR
    # -----------------------------------------------------------------------------
    except Exception as tab_err:
        st.error(f"Intelligence Module Advisory: Encountered a non-fatal exception ({type(tab_err).__name__}: {tab_err}). The rest of the terminal remains fully functional.")

with tabs[5]:
    try:
        st.markdown("#### Intellectual Property - Patent & Trademark Radar")
        st.caption("Tracking competitor patent filings, molecular claims, and IP moats across USPTO, WIPO, and CIPO.")

        ip_target = active_target if active_target else "All Competitors"
        ip_records = get_competitor_ip_records(ip_target)
        if not ip_records:
            st.info(f"No proprietary patent filings found for '{ip_target}'. Competitor operates primarily with unpatented off-the-shelf formulations or regional trade secrets.")
        else:
            for ip in ip_records:
                st.html(f"""
                <div style="background:#FFFFFF; border:1px solid #CBD5E1; border-left:4px solid #1B1C36; padding:16px; margin-bottom:12px;">
                    <div style="display:flex; justify-content:space-between;">
                        <strong style="font-family:'Montserrat', sans-serif; font-size:13px; color:#1B1C36;">{ip['competitor'].upper()} // {ip['doc_number']}</strong>
                        <span class="badge-terminal">{ip['status']}</span>
                    </div>
                    <div style="font-size:14px; font-weight:700; color:#0369A1; margin:6px 0;">{ip['patent_title']}</div>
                    <div style="font-size:12px; color:#475569;"><strong>Jurisdiction:</strong> {ip['jurisdiction']} | <strong>Filing Date:</strong> {ip['filing_date']}</div>
                    <div style="background:#F8FAFC; border:1px solid #E2E8F0; padding:10px; font-size:12px; margin:8px 0;">
                        <strong>Abstract & Chemical Claim:</strong><br>{ip['chemical_claim']}
                    </div>
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-family:'Montserrat', sans-serif; font-size:11px; font-weight:700; color:#1B1C36;">MOAT DEFENSE: {ip['moat_defense_score']}</span>
                        <a href="{ip['patent_url']}" target="_blank" class="citation-link">VIEW_USPTO_PATENT_DOCUMENT -></a>
                    </div>
                </div>
                """)

    # -----------------------------------------------------------------------------
    # TAB 7: CONTRACTOR & DEALER CHANNEL INTEL
    # -----------------------------------------------------------------------------
    except Exception as tab_err:
        st.error(f"Intelligence Module Advisory: Encountered a non-fatal exception ({type(tab_err).__name__}: {tab_err}). The rest of the terminal remains fully functional.")

with tabs[6]:
    try:
        st.markdown("#### Dealer Intelligence - Applicator Churn & Poaching Radar")
        st.caption("Detects contractor dissatisfaction with rival products to identify prime certified applicator recruitment targets.")

        dealers = get_dealer_intel_records()
        for dl in dealers:
            st.html(f"""
            <div style="background:#FFFFFF; border:1px solid #CBD5E1; border-left:4px solid #1B1C36; padding:16px; margin-bottom:12px;">
                <div style="display:flex; justify-content:space-between;">
                    <strong style="font-family:'Montserrat', sans-serif; font-size:13px; color:#1B1C36;">[{dl['contractor_id']}] {dl['region'].upper()} // {dl['current_rival_brand']}</strong>
                    <span class="badge-terminal">{dl['sentiment_status']}</span>
                </div>
                <div style="font-size:12px; color:#DC2626; margin:6px 0;"><strong>Reported Field Friction:</strong> {dl['reported_friction']}</div>
                <div style="background:#F1F5F9; border:1px solid #E2E8F0; padding:8px; font-size:12px; margin:6px 0;">
                    <strong>GoNano Recruitment Action:</strong> {dl['recruitment_strategy']}
                </div>
                <div>
                    <a href="{dl['source_url']}" target="_blank" class="citation-link">OPEN VERIFIED FORUM THREAD -> ({dl['forum_source']})</a>
                </div>
            </div>
            """)

    # -----------------------------------------------------------------------------
    # TAB 8: TECHNICAL FORMULATION & ASTM LABORATORY TEARDOWN LAB
    # -----------------------------------------------------------------------------
    except Exception as tab_err:
        st.error(f"Intelligence Module Advisory: Encountered a non-fatal exception ({type(tab_err).__name__}: {tab_err}). The rest of the terminal remains fully functional.")

with tabs[7]:
    try:
        st.markdown("#### Technical Laboratory - ASTM Engineering Benchmarks")
        st.caption("Hard physical testing standards: ASTM D3462 (Tear), ASTM D3161 (Wind Uplift), UL 2218 (Hail Impact).")

        astm_df = get_astm_teardown_df()
        st.dataframe(astm_df, hide_index=True, width="stretch")

        st.markdown("##### Molecular Cross-Linking vs Bio-Oil Audit")
        st.html("""
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:16px; margin-top:10px;">
            <div class="pulso-tile">
                <div class="tile-header" style="color:#16A34A;">GoNano Molecular Silica Transformation</div>
                <ul style="font-size:12px; line-height:1.6; margin:0; padding-left:16px;">
                    <li>Nanoparticles covalently cross-link into bitumen polymer chains.</li>
                    <li>Forms breathable matrix: vapor escapes, liquid water repelled.</li>
                    <li>ASTM D3462 tear strength increases by +45% permanently.</li>
                    <li>Passes Class 4 hail impact and 130 mph wind uplift.</li>
                </ul>
            </div>
            <div class="pulso-tile">
                <div class="tile-header" style="color:#DC2626;">Rival Topical Agricultural Bio-Oils (Soy/Veg Ester)</div>
                <ul style="font-size:12px; line-height:1.6; margin:0; padding-left:16px;">
                    <li>Topical plant oil temporarily swells oxidized surface bitumen.</li>
                    <li>Zero covalent bonding to fiberglass mat or underlying granules.</li>
                    <li>Volatile bio-oils evaporate under UV within 12-18 months.</li>
                    <li>Uncertified for ASTM hail impact or building code compliance.</li>
                </ul>
            </div>
        </div>
        """)

    # -----------------------------------------------------------------------------
    # TAB 9: REGIONAL GEOGRAPHIC TERRITORY AUDIT
    # -----------------------------------------------------------------------------
    except Exception as tab_err:
        st.error(f"Intelligence Module Advisory: Encountered a non-fatal exception ({type(tab_err).__name__}: {tab_err}). The rest of the terminal remains fully functional.")

with tabs[8]:
    try:
        st.markdown("#### Regional Audit - Geographic Market Dynamics")
        st.caption("Competitive concentration and weather vulnerability mapping across key market territories.")

        territory_data = get_territory_audit_data()
        for terr in territory_data:
            region = terr.get('region_name') or terr.get('region', 'Region')
            sentiment = terr.get('sentiment_label', 'MODERATE')
            volume = f"{terr.get('market_volume_pct', 0)}%" if 'market_volume_pct' in terr else terr.get('market_share_at_risk', 'N/A')
            dominant = terr.get('dominant_competitor', 'Multiple Competitors')
            climate = terr.get('climate_stress') or terr.get('weather_vector', 'Severe Climate Stress')
            friction = terr.get('key_friction_driver', '')
            opportunity = terr.get('opportunity_for_gonano') or terr.get('strategic_countermove', 'Deploy GoNano certified applicators.')

            citations_html = ""
            if terr.get('citations'):
                citations_html = "<div class='citation-block' style='margin-top:8px; padding-top:6px; border-top:1px solid #E2E8F0;'>"
                for c in terr['citations']:
                    citations_html += f"<div class='citation-item'>• <a href='{c.get('url', '#')}' target='_blank' class='citation-link'>{c.get('title', 'Source')}</a> <span class='citation-tag'>SOURCE -></span> <span style='font-size:11px; color:#64748B;'>({c.get('outlet', 'Industry Journal')})</span></div>"
                citations_html += "</div>"

            friction_html = f"<div style='font-size:12px; color:#DC2626; margin:4px 0;'><strong>Reported Friction Driver:</strong> {friction}</div>" if friction else ""

            st.html(f"""
            <div class="pulso-tile">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-family:'Montserrat', sans-serif; font-size:14px; font-weight:700; color:#1B1C36;">{region.upper()} // {sentiment}</span>
                    <span class="badge-terminal">MARKET VOLUME SHARE: {volume}</span>
                </div>
                <div style="font-size:12px; margin:6px 0;"><strong>Active Competitor Threat:</strong> {dominant}</div>
                <div style="font-size:12px; color:#475569;"><strong>Climate & Weather Stress:</strong> {climate}</div>
                {friction_html}
                <div style="background:#F8FAFC; border:1px solid #E2E8F0; padding:8px; font-size:12px; margin-top:6px;">
                    <strong>GoNano Strategic Opportunity:</strong> {opportunity}
                </div>
                {citations_html}
            </div>
            """)

    # -----------------------------------------------------------------------------
    # TAB 10: HISTORICAL TREND ANALYSIS (1900 TO PRESENT)
    # -----------------------------------------------------------------------------
    except Exception as tab_err:
        st.error(f"Intelligence Module Advisory: Encountered a non-fatal exception ({type(tab_err).__name__}: {tab_err}). The rest of the terminal remains fully functional.")


with tabs[9]:
    try:
        st.markdown("#### Enterprise Domain Analytics & Vertical Risk Audit")
        st.caption("Structured threat assessments, signal volume, and strategic takeaways across 5 core enterprise domains.")

        domains = get_domain_analytics()
        for d in domains:
            with st.expander(f"[{d['domain_id']}] {d['domain_name'].upper()} // {d['risk_level']} (Signals: {d['volume_mentions']})"):
                st.markdown(f"**Enterprise Threat Synthesis:** {d['summary']}")
                st.markdown("---")
                st.markdown("**Evidence Citations:**")
                for cit in d["citations"]:
                    st.html(f"<div style='font-size:12px; margin-bottom:4px;'>• <a href='{cit['url']}' target='_blank' class='citation-link'>{cit['title']}</a> <span class='citation-tag'>SOURCE -></span> <span style='font-size:11px; color:#64748B;'>({cit['source']})</span></div>")

    # -----------------------------------------------------------------------------
    # TAB 12: YOUTUBE & OSINT MULTI-SOURCE FEED (WITH IN-APP EMBEDS)
    # -----------------------------------------------------------------------------
    except Exception as tab_err:
        st.error(f"Intelligence Module Advisory: Encountered a non-fatal exception ({type(tab_err).__name__}: {tab_err}). The rest of the terminal remains fully functional.")

with tabs[10]:
    try:
        if active_target:
            st.markdown(f"#### Real-Time Intelligence Stream: **{active_target.upper()}**")
        else:
            st.markdown("#### Real-Time Intelligence Stream: All Monitored Competitors")
        st.caption("Enhanced Multi-Source OSINT Radar: Reddit Contractor Communities, BBB & Consumer Grievances, Trade Press, YouTube Demonstrations, and Patent Filings with automated relevance verification.")

        feed_type = st.selectbox(
            "FILTER BY INTELLIGENCE CHANNEL",
            [
                "All Channels (Aggregated)",
                "Reddit & Contractor Forums",
                "Consumer Grievances & BBB",
                "Trade Press & Industry News",
                "YouTube Video Demonstrations",
                "Patent & IP Filings"
            ],
            key="osint_channel_filter"
        )

        if active_target:
            scrape_target = active_target
        else:
            col_sc_pick, _ = st.columns([1.5, 1])
            with col_sc_pick:
                chosen_stream = st.selectbox(
                    "Select Subject for Live Intelligence Scan",
                    ["All Monitored Competitors"] + ALL_COMPETITORS,
                    index=0,
                    key="stream_subject_picker"
                )
            scrape_target = "Roof Rejuvenation" if chosen_stream == "All Monitored Competitors" else chosen_stream

        col_scrape, col_ads = st.columns([2, 1])
        with col_scrape:
            if st.button("EXECUTE MULTI-SOURCE VERIFIED SCAN & PERSIST", width="stretch", type="primary"):
                with st.spinner(f"Ingesting verified multi-channel intelligence for {scrape_target}..."):
                    from osint_listener import (
                        fetch_reddit_mentions,
                        fetch_consumer_grievance_signals,
                        fetch_trade_and_news_signals,
                        fetch_patent_and_ip_signals
                    )
                    from youtube_tracker import search_youtube_videos

                    reds = fetch_reddit_mentions(scrape_target, limit=6)
                    bbbs = fetch_consumer_grievance_signals(scrape_target, limit=5)
                    news = fetch_trade_and_news_signals(scrape_target, limit=6)
                    vids = search_youtube_videos(scrape_target, limit=5)
                    pats = fetch_patent_and_ip_signals(scrape_target, limit=3)

                    save_signals_to_db(reds, scrape_target)
                    save_signals_to_db(bbbs, scrape_target)
                    save_signals_to_db(news, scrape_target)
                    save_signals_to_db(vids, scrape_target)
                    save_signals_to_db(pats, scrape_target)

                    total_ingested = len(reds) + len(bbbs) + len(news) + len(vids) + len(pats)
                    st.success(f"Ingested {total_ingested} verified signals across 5 channels into database.")

        with col_ads:
            ad_search_term = active_target if active_target else (scrape_target if scrape_target != "Roof Rejuvenation" else "roof rejuvenation")
            st.markdown(f"[Inspect Meta Ad Library ↗](https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&q={urllib.parse.quote(ad_search_term)})")
            st.markdown(f"[Inspect Google Ads Transparency ↗](https://adstransparency.google.com/?region=anywhere&domain={ad_search_term.lower().replace(' ', '')}.com)")

        persisted_signals = get_all_signals_for_competitor(active_target, limit=50)

        # Chronological sorting function (Newest First)
        def parse_signal_epoch(sig):
            ts = sig.get("timestamp") or sig.get("published") or ""
            if not ts:
                return 0.0
            try:
                import email.utils
                dt = email.utils.parsedate_to_datetime(ts)
                if dt:
                    return dt.timestamp()
            except Exception:
                pass
            try:
                dt = pd.to_datetime(ts, errors='coerce')
                if pd.notnull(dt):
                    return dt.timestamp()
            except Exception:
                pass
            return 0.0

        if persisted_signals:
            persisted_signals = sorted(persisted_signals, key=parse_signal_epoch, reverse=True)

        if persisted_signals:
            for s in persisted_signals:
                plat = s.get("platform", "")
                if feed_type == "Reddit & Contractor Forums" and "Reddit" not in plat:
                    continue
                if feed_type == "Consumer Grievances & BBB" and "Consumer" not in plat and "BBB" not in plat:
                    continue
                if feed_type == "Trade Press & Industry News" and "Trade" not in plat and "News" not in plat:
                    continue
                if feed_type == "YouTube Video Demonstrations" and "YouTube" not in plat:
                    continue
                if feed_type == "Patent & IP Filings" and "Patent" not in plat and "IP" not in plat:
                    continue

                sentiment_val = s.get("sentiment", "Neutral")
                sentiment_color = "#DC2626" if "Negative" in sentiment_val or "Critical" in sentiment_val else ("#16A34A" if "Favorable" in sentiment_val else "#64748B")

                st.html(f"""
                <div class="mention-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <span class="badge-terminal">{s['platform'].upper()}</span>
                            <span style="font-size:11px; font-weight:700; color:{sentiment_color}; margin-left:8px;">● {sentiment_val}</span>
                        </div>
                        <span style="font-family:'Montserrat', sans-serif; font-size:11px; color:#64748B;">{s['timestamp']}</span>
                    </div>
                    <div style="font-weight:700; font-size:14px; margin:8px 0 4px 0;"><a href="{s['url']}" target="_blank" style="color:#1B1C36; text-decoration:none;">{s['title']}</a></div>
                    <div style="font-size:12px; color:#334155; line-height:1.4;">{s['snippet']}</div>
                    <div style="margin-top:8px;"><a href="{s['url']}" target="_blank" class="citation-link">OPEN VERIFIED SOURCE CITATION -></a></div>
                </div>
                """)

                # If YouTube video, render playable embed
                if "youtube.com/watch" in s["url"]:
                    with st.expander(f"Watch '{s['title'][:40]}...' in Terminal"):
                        st.video(s["url"])
        else:
            st.info(f"No indexed signals found yet for {scrape_target}. Click 'EXECUTE MULTI-SOURCE VERIFIED SCAN' above to fetch.")

    # -----------------------------------------------------------------------------
    # TAB 13: COMPETITOR "RED TEAM" WAR ROOM SIMULATOR
    # -----------------------------------------------------------------------------
    except Exception as tab_err:
        st.error(f"Intelligence Module Advisory: Encountered a non-fatal exception ({type(tab_err).__name__}: {tab_err}). The rest of the terminal remains fully functional.")

with tabs[11]:
    try:
        st.markdown("#### Red Team War Room - Rival Executive Simulator")
        st.caption("Roleplay as the CEO/CSO of the rival firm to stress-test GoNano's strategic offensive moves.")

        gonano_action_input = st.text_area(
            "PROPOSED_GONANO_STRATEGIC_MOVE",
            value="GoNano launches a certified contractor partnership program in Ontario offering homeowners a 15-Year non-prorated hail warranty backed by third-party ASTM D3462 lab tear tests.",
            height=90
        )

        if st.button("SIMULATE RIVAL EXECUTIVE COUNTER-ATTACK", width="stretch", type="primary"):
            sim_target = active_target if active_target else "RoofLife Canada"
            with st.spinner(f"Simulating {sim_target} executive war room reaction..."):
                war_room_output = simulate_rival_counter_attack(sim_target, gonano_action_input)
                
                st.markdown(f"""
                <div style="background-color:#1B1C36; border:1px solid #1E293B; border-left:4px solid #675CE7; padding:14px 18px; margin-top:16px; margin-bottom:12px;">
                    <div style="font-family:'Gotham', 'Montserrat', sans-serif; font-size:12px; font-weight:700; color:#818CF8; letter-spacing:0.8px; text-transform:uppercase;">
                        WAR ROOM SIMULATION DOSSIER // {sim_target.upper()} STRATEGIC COUNTER-ATTACK
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Render cleanly parsed markdown cards
                st.markdown(war_room_output)

    # -----------------------------------------------------------------------------
    # TAB 14: C-SUITE AUTOMATED ALERTING & WEBHOOK ENGINE
    # -----------------------------------------------------------------------------
    except Exception as tab_err:
        st.error(f"Intelligence Module Advisory: Encountered a non-fatal exception ({type(tab_err).__name__}: {tab_err}). The rest of the terminal remains fully functional.")

with tabs[12]:
    try:
        st.markdown("### Enterprise Risk Register & Threat Posture")
        st.caption("Quantitative risk scores, disruption vectors, and reverse-stress testing benchmarks across monitored competitors.")

        erm = calculate_erm_threat_matrix(active_target if active_target else "RoofLife Canada")
        r1, r2, r3, r4 = st.columns(4)
        with r1:
            st.html(f"""
            <div class="pulso-tile">
                <div class="tile-header">Inherent Competitive Threat</div>
                <div style="font-family:'Montserrat', sans-serif; font-size:26px; font-weight:700; color:#1B1C36;">
                    {erm['inherent_threat_score']}/10.0
                </div>
                <span class="badge-terminal badge-critical">LEVEL: {erm['inherent_threat_level']}</span>
            </div>
            """)
        with r2:
            st.html(f"""
            <div class="pulso-tile">
                <div class="tile-header">GoNano Control Moat Efficacy</div>
                <div style="font-family:'Montserrat', sans-serif; font-size:26px; font-weight:700; color:#1B1C36;">
                    {erm['control_efficacy_score']}/10.0
                </div>
                <span class="badge-terminal badge-safe">DEFENSE: {erm['control_efficacy_level']}</span>
            </div>
            """)
        with r3:
            st.html(f"""
            <div class="pulso-tile">
                <div class="tile-header">Residual Threat Rating</div>
                <div style="font-family:'Montserrat', sans-serif; font-size:26px; font-weight:700; color:#1B1C36;">
                    {erm['residual_threat_score']}/10.0
                </div>
                <span class="badge-terminal badge-moderate">NET EXPOSURE: {erm['residual_threat_level']}</span>
            </div>
            """)
        with r4:
            st.html(f"""
            <div class="pulso-tile">
                <div class="tile-header">Polarity-VaR (90-Day Downside)</div>
                <div style="font-family:'Montserrat', sans-serif; font-size:26px; font-weight:700; color:#DC2626;">
                    -{erm['polarity_var_90d']}%
                </div>
                <span class="badge-terminal">MARKET SHARE AT RISK</span>
            </div>
            """)

        st.markdown("##### Full Competitor Risk Register")
        erm_df = generate_erm_kpi_table()
        st.dataframe(erm_df, hide_index=True, width="stretch")
    except Exception as tab_err:
        st.error(f"Intelligence Module Advisory: Encountered a non-fatal exception ({type(tab_err).__name__}: {tab_err}). The rest of the terminal remains fully functional.")

with tabs[13]:
    try:
        st.markdown("#### Export Infrastructure - Executive Board Reports")
        st.caption("Generate verifiable audit documents formatted for Excel and C-suite strategy committees.")

        dl_dir = '/Users/macbook/Downloads'
        target_slug = active_target.replace(' ', '_') if active_target else "Global_Portfolio"
        target_memo_name = active_target if active_target else "Market Overview"
        audit_label = f"{active_target[:20]} Audit" if active_target else "Global Market Audit"

        if st.button("⚡ Save All Reports Directly to Mac Downloads (~/Downloads)", width="stretch"):
            erm_df_exp = generate_erm_kpi_table()
            p_csv = os.path.join(dl_dir, f"GoNano_Competitive_ERM_Risk_Register_{target_slug}.csv")
            p_xls = os.path.join(dl_dir, f"GoNano_Executive_Spreadsheet_{target_slug}.xls")
            p_md = os.path.join(dl_dir, f"GoNano_Executive_Memo_{target_slug}.md")
            with open(p_csv, "wb") as f:
                f.write(generate_utf8_bom_csv(erm_df_exp))
            with open(p_xls, "w", encoding="utf-8") as f:
                f.write(generate_spreadsheetml_xls(erm_df_exp, audit_label))
            with open(p_md, "w", encoding="utf-8") as f:
                f.write(generate_csuite_markdown_memo(target_memo_name))
            st.success(f"Saved all 3 files to !")

        st.markdown("<br>", unsafe_allow_html=True)
        exp_col1, exp_col2, exp_col3 = st.columns(3)
    
        target_slug = active_target.replace(' ', '_') if active_target else "Global_Portfolio"
        target_memo_name = active_target if active_target else "Market Overview"
        audit_label = f"{active_target[:20]} Audit" if active_target else "Global Market Audit"

        with exp_col1:
            st.html("""
            <div class="pulso-tile">
                <div class="tile-header">1. Universal Excel (.CSV with BOM)</div>
                <p style="font-size:12px;">UTF-8 with Byte Order Mark (\uFEFF) to guarantee character rendering in Microsoft Excel.</p>
            </div>
            """)
        
            erm_export_df = generate_erm_kpi_table()
            csv_bytes = generate_utf8_bom_csv(erm_export_df)
            st.download_button(
                label="Download Excel (.CSV)",
                data=csv_bytes,
                file_name=f"GoNano_Competitive_ERM_Risk_Register_{target_slug}.csv",
                mime="text/csv"
            )

        with exp_col2:
            st.html("""
            <div class="pulso-tile">
                <div class="tile-header">2. Native SpreadsheetML (.XLS)</div>
                <p style="font-size:12px;">XML Spreadsheet 2003 format with frozen header panes, column widths, and styled Navy headers.</p>
            </div>
            """)
        
            xls_str = generate_spreadsheetml_xls(erm_export_df, audit_label)
            st.download_button(
                label="Download SpreadsheetML (.xls)",
                data=xls_str.encode("utf-8"),
                file_name=f"GoNano_Executive_Spreadsheet_{target_slug}.xls",
                mime="application/vnd.ms-excel"
            )

        with exp_col3:
            st.html("""
            <div class="pulso-tile">
                <div class="tile-header">3. Executive Strategy Briefing (.MD)</div>
                <p style="font-size:12px;">Formatted C-Suite intelligence memo including executive summary, KCI alerts, and playbooks.</p>
            </div>
            """)
        
            memo_str = generate_csuite_markdown_memo(target_memo_name)
            st.download_button(
                label="Download Memo (.md)",
                data=memo_str.encode("utf-8"),
                file_name=f"GoNano_Executive_Memo_{target_slug}.md",
                mime="text/markdown"
            )

    # -----------------------------------------------------------------------------
    # TAB 16: COMPETITOR THREAT & SENTIMENT HEATMAP MATRIX
    # -----------------------------------------------------------------------------
    except Exception as tab_err:
        st.error(f"Intelligence Module Advisory: Encountered a non-fatal exception ({type(tab_err).__name__}: {tab_err}). The rest of the terminal remains fully functional.")

with tabs[14]:
    try:
        st.markdown("#### Threat Heatmap - Multi-Factor Sentiment & Market Impact Matrix")
        st.caption(f"Real-time comparative quadrant positioning and multi-factor vulnerability heatmap across 60+ monitored competitors. Sliced by **{time_horizon}**.")

        hm_col1, hm_col2 = st.columns([2, 1])
        with hm_col1:
            hm_category = st.selectbox(
                "HEATMAP_CATEGORY_FILTER",
                ["All", "Bio-Oil", "Ceramic", "Paint", "Contractor"],
                index=0,
                help="Filter heatmap matrix by technology vertical."
            )
        with hm_col2:
            st.write("")
            st.write("")
            hm_df = heatmap_engine.get_heatmap_dataframe(time_horizon=time_horizon, category_filter=hm_category)
            csv_data = hm_df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="EXPORT HEATMAP DATA (.CSV)",
                data=csv_data,
                file_name=f"GoNano_Competitor_Threat_Heatmap_{time_horizon.replace(' ', '_')}.csv",
                mime="text/csv",
                width="stretch"
            )

        # Render 2D Quadrant Matrix Visual
        heatmap_items = heatmap_engine.compute_competitor_heatmap_data(time_horizon=time_horizon, category_filter=hm_category)
    
        q1_items = [i for i in heatmap_items if "Q1" in i["quadrant"]]
        q2_items = [i for i in heatmap_items if "Q2" in i["quadrant"]]
        q3_items = [i for i in heatmap_items if "Q3" in i["quadrant"]]
        q4_items = [i for i in heatmap_items if "Q4" in i["quadrant"]]

        qc1, qc2, qc3, qc4 = st.columns(4)
        with qc1:
            st.html(textwrap.dedent(f"""
            <div style="background:#FEF2F2; border:1px solid #FECACA; border-top:3px solid #DC2626; padding:12px;">
                <div style="font-family:'Montserrat', sans-serif; font-size:10px; font-weight:700; color:#991B1B;">QUADRANT 1 // PRIME TARGETS</div>
                <div style="font-size:22px; font-weight:800; color:#7F1D1D;">{len(q1_items)} BRANDS</div>
                <div style="font-size:10px; color:#991B1B; margin-top:4px;">High Volume + High Customer Friction. Prime targets for GoNano sales displacement.</div>
            </div>
            """).strip())
        with qc2:
            st.html(textwrap.dedent(f"""
            <div style="background:#EFF6FF; border:1px solid #BFDBFE; border-top:3px solid #2563EB; padding:12px;">
                <div style="font-family:'Montserrat', sans-serif; font-size:10px; font-weight:700; color:#1E40AF;">QUADRANT 2 // INCUMBENTS</div>
                <div style="font-size:22px; font-weight:800; color:#1E3A8A;">{len(q2_items)} BRANDS</div>
                <div style="font-size:10px; color:#1E40AF; margin-top:4px;">High Volume + Low Friction. Entrenched technical players; target with ASTM lab data.</div>
            </div>
            """).strip())
        with qc3:
            st.html(textwrap.dedent(f"""
            <div style="background:#FFFBEB; border:1px solid #FDE68A; border-top:3px solid #D97706; padding:12px;">
                <div style="font-family:'Montserrat', sans-serif; font-size:10px; font-weight:700; color:#92400E;">QUADRANT 3 // REGIONAL SPRAY</div>
                <div style="font-size:22px; font-weight:800; color:#78350F;">{len(q3_items)} BRANDS</div>
                <div style="font-size:10px; color:#92400E; margin-top:4px;">Low-to-Mid Volume + High Washout Complaints. Local contractor applicators.</div>
            </div>
            """).strip())
        with qc4:
            st.html(textwrap.dedent(f"""
            <div style="background:#F0FDF4; border:1px solid #BBF7D0; border-top:3px solid #16A34A; padding:12px;">
                <div style="font-family:'Montserrat', sans-serif; font-size:10px; font-weight:700; color:#166534;">QUADRANT 4 // DISRUPTORS</div>
                <div style="font-size:22px; font-weight:800; color:#14532D;">{len(q4_items)} BRANDS</div>
                <div style="font-size:10px; color:#166534; margin-top:4px;">Niche / Emerging Nanotech Startups. Monitor for patent filings and regional growth.</div>
            </div>
            """).strip())

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("##### Multi-Factor Competitor Heatmap Grid")

        st.dataframe(
            hm_df,
            width="stretch",
            height=500
        )
    except Exception as tab_err:
        st.error(f"Intelligence Module Advisory: Encountered a non-fatal exception ({type(tab_err).__name__}: {tab_err}). The rest of the terminal remains fully functional.")


# -----------------------------------------------------------------------------
# TAB 17: C-SUITE REQUEST DISPATCH & GEMINI 3.1 PRO AUTO-TRACKER (MIGUEL'S PORTAL)
# -----------------------------------------------------------------------------
if is_csuite_user and len(tabs) >= 16:
    with tabs[15]:
        try:
            from csuite_workflow import (
                get_all_pending_competitor_requests,
                analyze_document_with_gemini_3_pro,
                dispatch_analysis_to_requester,
                DEFAULT_CC_LIST
            )
            
            st.markdown("### 👔 C-Suite Executive Command: Pending Competitor Requests & Gemini 3.1 Pro Fulfillment")
            st.caption("Centralized executive workflow to review pending competitor inquiries from contractors, analyze uploaded dossiers with Gemini 3.1 Pro, auto-record findings into the Google Sheet tracker, and dispatch reports with Joel, Jonathan, and Charles CC'd.")

            # 1. PENDING REQUESTS WORKFLOW TABLE
            st.markdown("#### 1. Pending Competitor Analysis Requests Queue")
            pending_reqs = get_all_pending_competitor_requests()

            if pending_reqs:
                st.dataframe(
                    pd.DataFrame([
                        {
                            "Request ID": r["id"],
                            "Source": r["source_type"],
                            "Competitor Name": r["competitor_name"],
                            "Requester": r["requester_name"],
                            "Requester Email": r["requester_email"],
                            "Territory / Market": r["location"],
                            "Date Requested": r["date_requested"],
                            "Field Notes / Subject": r["field_notes"][:100] + ("..." if len(r["field_notes"]) > 100 else ""),
                            "Evidence Files": r["evidence_files"],
                            "Status": r["status"]
                        }
                        for r in pending_reqs
                    ]),
                    width="stretch",
                    hide_index=True
                )
            else:
                st.info("No pending requests currently queued in database.")

            st.markdown("---")

            # 2. DOCUMENT UPLOAD & FULFILLMENT FORM
            st.markdown("#### 2. Fulfill Request & Document Upload")

            with st.form("csuite_fulfillment_form", clear_on_submit=False):
                f_col1, f_col2 = st.columns(2)
                with f_col1:
                    req_options = ["-- Custom Competitor Entry --"] + [f"{r['id']} - {r['competitor_name']} (Requested by: {r['requester_name']})" for r in pending_reqs]
                    selected_req_idx = st.selectbox("Select Pending Request to Fulfill", req_options)
                with f_col2:
                    if selected_req_idx != "-- Custom Competitor Entry --":
                        chosen_r = next((r for r in pending_reqs if r["id"] == selected_req_idx.split(" - ")[0]), None)
                        default_comp = chosen_r["competitor_name"] if chosen_r else ""
                        default_email = chosen_r["requester_email"] if chosen_r else ""
                        default_name = chosen_r["requester_name"] if chosen_r else ""
                        req_id_val = chosen_r["id"] if chosen_r else ""
                    else:
                        default_comp = ""
                        default_email = ""
                        default_name = "GoNano Partner"
                        req_id_val = None

                    target_comp_input = st.text_input("Competitor Name *", value=default_comp, placeholder="e.g. Roof Juice RX, Inexso, Team Nano...")

                u_col1, u_col2 = st.columns(2)
                with u_col1:
                    target_requester_email = st.text_input("Send Completed Analysis To (Requester Email) *", value=default_email, placeholder="e.g. charles.dumont@gonano.com or contractor@apexroofing.ca")
                with u_col2:
                    cc_recipients_input = st.text_input("CC Stakeholders (Comma Separated) *", value="joel@gonano.com, jonathan@gonano.com, charles@gonano.com, mathieu@gonano.com, jason@gonano.com")

                uploaded_doc = st.file_uploader(
                    "Upload Completed Competitor Analysis Document / Dossier *",
                    type=["pdf", "docx", "xlsx", "pptx", "txt", "png", "jpg"],
                    help="Upload the finished report. Gemini 3.1 Pro will read the document, benchmark it, and commit it to the intelligence tracker."
                )

                exec_cover_notes = st.text_area(
                    "Executive Cover Notes / Context for Recipients",
                    placeholder="e.g. Attached is the completed technical teardown on Roof Juice RX. Chemistry fails ASTM D3462; recommend sales team counter with GoNano molecular nanoparticle data.",
                    height=85
                )

                c_btn_sub = st.form_submit_button("🚀 Analyze with Gemini 3.1 Pro, Update Tracker & Dispatch to Requester", width="stretch", type="primary")

                if c_btn_sub:
                    if not target_comp_input.strip():
                        st.error("Please provide the Competitor Name.")
                    elif not target_requester_email.strip():
                        st.error("Please provide the Requester Email.")
                    elif not uploaded_doc:
                        st.error("Please upload the analysis document to proceed.")
                    else:
                        with st.spinner("Gemini 3.1 Pro analyzing document and extracting competitive benchmarks..."):
                            file_bytes = uploaded_doc.getvalue()
                            fname = uploaded_doc.name
                            
                            # 1. Analyze with Gemini 3.1 Pro
                            gemini_data = analyze_document_with_gemini_3_pro(
                                file_bytes=file_bytes,
                                filename=fname,
                                target_competitor=target_comp_input.strip()
                            )
                            
                            # 2. Parse CCs
                            parsed_ccs = [c.strip() for c in cc_recipients_input.split(",") if c.strip() and "@" in c]
                            
                            # 3. Dispatch Email with attachment
                            dispatch_res = dispatch_analysis_to_requester(
                                competitor_name=target_comp_input.strip(),
                                requester_name=default_name,
                                requester_email=target_requester_email.strip(),
                                uploaded_file_bytes=file_bytes,
                                filename=fname,
                                cc_emails=parsed_ccs,
                                executive_notes=exec_cover_notes.strip(),
                                gemini_summary=gemini_data.get("executive_summary", ""),
                                request_id=req_id_val
                            )
                            
                            if dispatch_res.get("status") == "success":
                                st.success(f"✅ Dossier successfully dispatched to {target_requester_email} with Joel, Jonathan, and Charles CC'd!")
                                st.info(f"📊 Auto-Recorded into Tracker: Competitor Profile for '{target_comp_input.strip()}' created/updated and committed to Reports Sent.")
                                
                                with st.expander("🔍 View Gemini 3.1 Pro Analysis Breakdown", expanded=True):
                                    st.json(gemini_data)
                            else:
                                st.error(f"⚠️ Email dispatch failed: {dispatch_res.get('message')}")
        except Exception as tab_err:
            st.error(f"Intelligence Module Advisory: Encountered a non-fatal exception ({type(tab_err).__name__}: {tab_err}). The rest of the terminal remains fully functional.")


# -----------------------------------------------------------------------------
# TAB 17: COMMERCIAL DATA APIS & AEO GENERATIVE SEARCH RADAR
# -----------------------------------------------------------------------------
with tabs[-1]:
    try:
        from paid_apis_radar import render_paid_apis_and_aeo_tab
        render_paid_apis_and_aeo_tab()
    except Exception as tab_err:
        st.error(f"Intelligence Module Advisory: Encountered a non-fatal exception ({type(tab_err).__name__}: {tab_err}). The rest of the terminal remains fully functional.")
