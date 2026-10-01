"""
db_manager.py
Embedded SQLite Persistence Engine for Competitor Intelligence Platform.
Stores signals, competitor profiles, pricing updates, customer reviews,
marketing gap dossiers, ERM evaluations, and Google Sheets tracker records.
"""
import sqlite3
import os
import json
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "competitor_store.db")

# Supabase Cloud REST Connector
SUPABASE_URL = (os.getenv("SUPABASE_URL") or "https://kckcwfatcyrunbgxwhhe.supabase.co").rstrip("/")
SUPABASE_KEY = (os.getenv("SUPABASE_KEY") or "sb_publishable_S417FSPdzpmBHdcyxzyQuQ_MeAEDlV4").strip()

def supabase_request(endpoint: str, method: str = "GET", payload: Optional[Any] = None) -> Optional[Any]:
    """Performs direct PostgREST calls to Supabase with silent SQLite fallback."""
    try:
        url = f"{SUPABASE_URL}/rest/v1/{endpoint}"
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
        data = json.dumps(payload).encode("utf-8") if payload is not None else None
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        with urllib.request.urlopen(req, timeout=5.0) as resp:
            if resp.status in (200, 201):
                res_text = resp.read().decode("utf-8")
                return json.loads(res_text) if res_text else []
    except Exception:
        pass
    return None

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Signals & Mentions Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS signals (\n        id INTEGER PRIMARY KEY AUTOINCREMENT,\n        competitor TEXT NOT NULL,\n        platform TEXT NOT NULL,\n        channel_badge TEXT,\n        author TEXT,\n        title TEXT NOT NULL,\n        snippet TEXT,\n        sentiment TEXT DEFAULT 'Neutral',\n        polarity REAL DEFAULT 0.0,\n        url TEXT,\n        timestamp TEXT,\n        created_at DATETIME DEFAULT CURRENT_TIMESTAMP\n    )
    """)
    
    # 2. Competitor Corporate & Strategy Profiles
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS competitor_profiles (\n        id INTEGER PRIMARY KEY AUTOINCREMENT,\n        name TEXT UNIQUE NOT NULL,\n        domain TEXT,\n        category TEXT,\n        core_technology TEXT,\n        inherent_threat_score REAL DEFAULT 5.0,\n        control_efficacy_score REAL DEFAULT 5.0,\n        residual_threat_score REAL DEFAULT 2.5,\n        target_regions TEXT,\n        report_status TEXT,\n        reports_count INTEGER DEFAULT 0,\n        latest_report_date TEXT,\n        notes TEXT,\n        source_sheet TEXT,\n        gmail_link TEXT,\n        last_updated DATETIME DEFAULT CURRENT_TIMESTAMP\n    )
    """)
    
    # 3. Pricing & Commercial Claims
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pricing_records (\n        id INTEGER PRIMARY KEY AUTOINCREMENT,\n        competitor TEXT NOT NULL,\n        product_name TEXT NOT NULL,\n        price_model TEXT,\n        estimated_sqft_cost REAL,\n        claim_warranty_years INTEGER,\n        source_url TEXT,\n        created_at DATETIME DEFAULT CURRENT_TIMESTAMP\n    )
    """)
    
    # 4. Brand Promise vs Customer Reality (Marketing Gap)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS marketing_gap_records (\n        id INTEGER PRIMARY KEY AUTOINCREMENT,\n        competitor TEXT NOT NULL,\n        marketing_claim TEXT NOT NULL,\n        claim_channel TEXT,\n        customer_reality TEXT NOT NULL,\n        reality_source TEXT,\n        gap_severity TEXT DEFAULT 'MODERATE',\n        divergence_score REAL DEFAULT 50.0,\n        source_url TEXT,\n        strategic_takeaway TEXT,\n        created_at DATETIME DEFAULT CURRENT_TIMESTAMP\n    )
    """)
    
    # 5. ERM Risk & KCI Register
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS erm_risk_register (\n        id INTEGER PRIMARY KEY AUTOINCREMENT,\n        competitor TEXT NOT NULL,\n        risk_category TEXT NOT NULL,\n        inherent_threat TEXT NOT NULL,\n        control_defense TEXT NOT NULL,\n        residual_threat TEXT NOT NULL,\n        kci_early_warning TEXT NOT NULL,\n        reverse_stress_scenario TEXT NOT NULL,\n        var_downside_pct REAL DEFAULT 15.0,\n        created_at DATETIME DEFAULT CURRENT_TIMESTAMP\n    )
    """)

    # 6. Google Sheets Tracker Reports (Reports Sent & Open Requests)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tracker_reports (\n        id INTEGER PRIMARY KEY AUTOINCREMENT,\n        competitor TEXT NOT NULL,\n        report_type TEXT,\n        date_pht TEXT,\n        subject TEXT,\n        attachment_name TEXT,\n        to_recipients TEXT,\n        cc_recipients TEXT,\n        requested_by TEXT,\n        request_date TEXT,\n        gmail_link TEXT,\n        drive_link TEXT,\n        status TEXT,\n        notes TEXT,\n        sheet_name TEXT\n    )
    """)
    
    # Indices
        # 7. Contractor Analysis Requests
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contractor_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp_pht TEXT NOT NULL,
        contractor_name TEXT,
        contractor_email TEXT,
        contractor_phone TEXT,
        competitor_name TEXT NOT NULL,
        location TEXT NOT NULL,
        url TEXT,
        facebook_link TEXT,
        instagram_link TEXT,
        notes TEXT,
        attachment_names TEXT,
        status TEXT DEFAULT 'PENDING_REVIEW'
    )
    """)

    # 8. Certified Contractor Provisioned Accounts
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contractor_accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        name TEXT NOT NULL,
        business_name TEXT NOT NULL,
        business_area TEXT NOT NULL,
        status TEXT DEFAULT 'active',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 9. Account Requests from Contractors
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contractor_account_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        business_name TEXT NOT NULL,
        business_area TEXT NOT NULL,
        email TEXT NOT NULL,
        status TEXT DEFAULT 'NEW_REQUEST',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_signals_comp ON signals (competitor)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_signals_time ON signals (created_at)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tracker_comp ON tracker_reports (competitor)")
    
    conn.commit()
    conn.close()

def seed_baseline_data():
    """Populates baseline intelligence dossiers and syncs sheet data if needed."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as count FROM competitor_profiles")
    count = cursor.fetchone()["count"]
    conn.close()

    if count < 20:
        try:
            import sync_competitor_tracker
            sync_competitor_tracker.run_sync()
        except Exception as e:
            print(f"Error seeding competitor tracker data: {e}")

def get_all_competitor_names() -> List[str]:
    """Returns sorted list of all competitor names in the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM competitor_profiles ORDER BY name ASC")
    names = [r["name"] for r in cursor.fetchall() if r["name"]]
    conn.close()
    if not names:
        names = ["RoofLife Canada", "Nasiol (Artekya)", "RevivaRoof", "Spray-Net", "ArmoveX", "Zinox Coating", "GoNano (Your Brand)"]
    return names

def get_all_monitored_competitors() -> List[Dict[str, str]]:
    """Returns list of all competitors with their domains for background monitoring."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, domain FROM competitor_profiles WHERE name != 'GoNano (Your Brand)' ORDER BY name ASC")
    rows = []
    for r in cursor.fetchall():
        name = r["name"]
        domain = r["domain"] or f"{name.lower().replace(' ', '')}.com"
        rows.append({"name": name, "domain": domain})
    conn.close()
    return rows

def get_competitor_profile(name: Optional[str]) -> Optional[Dict[str, Any]]:
    """Retrieves full profile for a competitor by exact or partial match."""
    if not name or not str(name).strip():
        return None
    name = str(name).strip()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM competitor_profiles WHERE LOWER(name) = LOWER(?)", (name.strip(),))
    row = cursor.fetchone()
    if not row:
        cursor.execute("SELECT * FROM competitor_profiles WHERE LOWER(name) LIKE ? LIMIT 1", (f"%{name.strip().lower()}%",))
        row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_all_competitor_profiles() -> List[Dict[str, Any]]:
    """Returns all competitor profile records."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM competitor_profiles ORDER BY inherent_threat_score DESC, name ASC")
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def get_tracker_reports(competitor: Optional[str] = None, sheet_name: Optional[str] = None) -> List[Dict[str, Any]]:
    """Returns historical competitor reports sent or open requests from the Google Sheet."""
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM tracker_reports WHERE 1=1"
    params = []
    if competitor and competitor != "All Competitors":
        query += " AND (LOWER(competitor) LIKE ? OR LOWER(?) LIKE '%' || LOWER(competitor) || '%')"
        params.extend([f"%{competitor.lower()}%", competitor.lower()])
    if sheet_name:
        query += " AND sheet_name = ?"
        params.append(sheet_name)
    query += " ORDER BY id DESC"
    cursor.execute(query, params)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def add_custom_competitor(name: str, domain: str, category: str, notes: str = "") -> bool:
    """Adds or updates a custom competitor to the monitored roster."""
    if not name or not name.strip():
        return False
    name = name.strip()
    domain = domain.strip() if domain else f"{name.lower().replace(' ', '')}.com"
    category = category.strip() if category else "Roof Restoration & Preservation"
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO competitor_profiles (
        name, domain, category, core_technology, inherent_threat_score,
        control_efficacy_score, residual_threat_score, target_regions,
        report_status, notes, source_sheet
    ) VALUES (?, ?, ?, ?, 6.0, 7.0, 3.2, 'North America', 'Custom Monitored Target', ?, 'User Added')
    ON CONFLICT(name) DO UPDATE SET
        domain = excluded.domain,
        category = excluded.category,
        notes = excluded.notes,
        last_updated = CURRENT_TIMESTAMP
    """, (name, domain, category, f"{category} formulation", notes))
    conn.commit()
    conn.close()
    return True

def save_signals_to_db(signals_list: List[Dict[str, Any]], competitor: str):
    """Saves scraped signals safely to SQLite database."""
    if not signals_list:
        return
    conn = get_connection()
    cursor = conn.cursor()
    for s in signals_list:
        cursor.execute("""
        INSERT INTO signals (competitor, platform, channel_badge, author, title, snippet, sentiment, polarity, url, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            competitor,
            s.get("source", "Web"),
            s.get("channel_badge", s.get("source", "Web")),
            s.get("author", s.get("channel", "Unknown")),
            s.get("title", ""),
            s.get("snippet", ""),
            s.get("sentiment", "Neutral"),
            s.get("polarity", 0.0),
            s.get("url", "#"),
            s.get("published", s.get("timestamp", datetime.now().strftime("%Y-%m-%d")))
        ))
    conn.commit()
    conn.close()

def parse_signal_datetime(ts_str: Optional[str]) -> Optional[datetime]:
    if not ts_str:
        return None
    ts_clean = str(ts_str).strip()
    rel_match = re.match(r'(\d+)\s*(d|day|days|mo|month|months|y|year|years)\s*ago', ts_clean, re.I)
    if rel_match:
        val = int(rel_match.group(1))
        unit = rel_match.group(2).lower()
        now = datetime.now()
        if unit in ('d', 'day', 'days'):
            return now - timedelta(days=val)
        elif unit in ('mo', 'month', 'months'):
            return now - timedelta(days=val * 30)
        elif unit in ('y', 'year', 'years'):
            return now - timedelta(days=val * 365)
    for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%Y-%m-%dT%H:%M:%S'):
        try:
            return datetime.strptime(ts_clean[:19], fmt)
        except Exception:
            pass
    try:
        from email.utils import parsedate_to_datetime
        return parsedate_to_datetime(ts_clean)
    except Exception:
        pass
    return None

def get_all_signals_for_competitor(competitor: Optional[str] = None, limit: int = 50, time_horizon: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    if competitor and competitor != "All Competitors":
        cursor.execute("""
        SELECT * FROM signals WHERE LOWER(competitor) LIKE ? ORDER BY id DESC LIMIT 150
        """, (f"%{competitor.lower()}%",))
    else:
        cursor.execute("""
        SELECT * FROM signals ORDER BY id DESC LIMIT 150
        """)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()

    if not time_horizon or str(time_horizon).lower() in ("all", "all time"):
        return rows[:limit]

    th = str(time_horizon).lower()
    max_days = 30
    if "24" in th or "1 day" in th or "today" in th:
        max_days = 1
    elif "7" in th:
        max_days = 7
    elif "30" in th:
        max_days = 30
    elif "90" in th:
        max_days = 90
    elif "12" in th or "year" in th:
        max_days = 365

    cutoff = datetime.now() - timedelta(days=max_days)
    filtered = []
    for r in rows:
        dt = parse_signal_datetime(r.get("timestamp"))
        if dt:
            if dt.tzinfo:
                dt = dt.replace(tzinfo=None)
            if dt >= cutoff:
                filtered.append(r)
    return filtered[:limit]


def get_marketing_gaps(competitor: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    if competitor and competitor != "All Competitors":
        cursor.execute("""
        SELECT * FROM marketing_gap_records 
        WHERE LOWER(competitor) LIKE ? 
           OR LOWER(?) LIKE '%' || LOWER(competitor) || '%'
           OR LOWER(marketing_claim) LIKE ?
           OR LOWER(customer_reality) LIKE ?
        ORDER BY divergence_score DESC
        """, (f"%{competitor.lower()}%", competitor.lower(), f"%{competitor.lower()}%", f"%{competitor.lower()}%"))
    else:
        cursor.execute("SELECT * FROM marketing_gap_records ORDER BY divergence_score DESC")
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def get_erm_risks(competitor: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    if competitor and competitor != "All Competitors":
        cursor.execute("SELECT * FROM erm_risk_register WHERE LOWER(competitor) LIKE ? ORDER BY var_downside_pct DESC", (f"%{competitor.lower()}%",))
    else:
        cursor.execute("SELECT * FROM erm_risk_register ORDER BY var_downside_pct DESC")
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

# Initialize on import
init_db()
seed_baseline_data()

def log_contractor_request(data: Dict[str, Any]) -> int:
    """Logs a submitted contractor competitor inquiry into Supabase Cloud and SQLite."""
    # 1. Mirror to Supabase Cloud
    try:
        supabase_request("contractor_requests", method="POST", payload={
            "timestamp_pht": data.get("timestamp_pht", ""),
            "contractor_name": data.get("contractor_name", "Certified Contractor"),
            "contractor_email": data.get("contractor_email", ""),
            "contractor_phone": data.get("contractor_phone", ""),
            "competitor_name": data.get("competitor_name", ""),
            "location": data.get("location", ""),
            "url": data.get("url", ""),
            "facebook_link": data.get("facebook_link", ""),
            "instagram_link": data.get("instagram_link", ""),
            "notes": data.get("notes", ""),
            "attachment_names": data.get("attachment_names", ""),
            "status": "SUBMITTED_TO_MIGUEL"
        })
    except Exception:
        pass

    # 2. Local SQLite
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO contractor_requests (
        timestamp_pht, contractor_name, contractor_email, contractor_phone,
        competitor_name, location, url, facebook_link, instagram_link,
        notes, attachment_names, status
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'SUBMITTED_TO_MIGUEL')
    """, (
        data.get("timestamp_pht", ""),
        data.get("contractor_name", "Certified Contractor"),
        data.get("contractor_email", ""),
        data.get("contractor_phone", ""),
        data.get("competitor_name", ""),
        data.get("location", ""),
        data.get("url", ""),
        data.get("facebook_link", ""),
        data.get("instagram_link", ""),
        data.get("notes", ""),
        data.get("attachment_names", "")
    ))
    row_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return row_id

def get_all_contractor_requests() -> List[Dict[str, Any]]:
    """Retrieves all submitted contractor competitor analysis requests from Supabase or SQLite."""
    # 1. Attempt Supabase Cloud Read
    try:
        res = supabase_request("contractor_requests?order=id.desc&select=*")
        if res and isinstance(res, list) and len(res) > 0:
            return res
    except Exception:
        pass

    # 2. Fallback to SQLite
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contractor_requests ORDER BY id DESC")
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def seed_contractor_accounts():
    """Seeds initial pre-approved contractor accounts if table is empty."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as c FROM contractor_accounts")
    if cursor.fetchone()["c"] == 0:
        cursor.execute("""
        INSERT INTO contractor_accounts (email, password, name, business_name, business_area, status)
        VALUES 
        ('marc.leclerc@apexroofing.ca', 'GoNano#2026', 'Marc Leclerc', 'Apex Roofing Solutions', 'Montreal, QC', 'active'),
        ('contractor@gonano.com', 'GoNano#Cert', 'GoNano Certified Partner', 'GoNano Applicator Network', 'North America', 'active'),
        ('miguel.gonzales@gonano.com', 'GoNano#Exec', 'Miguel Gonzales', 'GoNano Strategic Intelligence', 'National', 'active'),
        ('mcbgonzales@outlook.com', 'GoNano#2026', 'Miguel Gonzales', 'Lunsad Pilipinas', 'Consulting', 'active'),
        ('gonzalesmiguelcarlo@gmail.com', 'GoNano#2026', 'Miguel Gonzales', 'GoNano Management', 'National', 'active')
        """)
        conn.commit()
    conn.close()

def authenticate_contractor(email: str, pass_val: str) -> Optional[Dict[str, Any]]:
    """Authenticates contractor credentials against Supabase Cloud with SQLite fallback."""
    email_clean = (email or "").strip().lower()
    p_clean = (pass_val or "").strip()
    if not email_clean or not p_clean:
        return None

    # 1. Attempt Supabase Cloud Authentication
    try:
        q_email = urllib.parse.quote(email_clean)
        q_pass = urllib.parse.quote(p_clean)
        endpoint = f"contractor_accounts?email=eq.{q_email}&password=eq.{q_pass}&status=eq.active&select=*"
        res = supabase_request(endpoint)
        if res and isinstance(res, list) and len(res) > 0:
            return dict(res[0])
    except Exception:
        pass

    # 2. Local SQLite Fallback
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM contractor_accounts 
    WHERE LOWER(email) = ? AND password = ? AND status = 'active'
    """, (email_clean, p_clean))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def log_contractor_account_request(name: str, business_name: str, business_area: str, email: str) -> int:
    """Logs a new account request to Supabase Cloud and SQLite."""
    # 1. Mirror to Supabase Cloud
    try:
        supabase_request("contractor_account_requests", method="POST", payload={
            "name": name.strip(),
            "business_name": business_name.strip(),
            "business_area": business_area.strip(),
            "email": email.strip().lower(),
            "status": "NEW_REQUEST"
        })
    except Exception:
        pass

    # 2. Local SQLite
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO contractor_account_requests (name, business_name, business_area, email, status)
    VALUES (?, ?, ?, ?, 'NEW_REQUEST')
    """, (name.strip(), business_name.strip(), business_area.strip(), email.strip().lower()))
    row_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return row_id

def get_all_contractor_account_requests() -> List[Dict[str, Any]]:
    """Retrieves all contractor account requests from Supabase or SQLite."""
    # 1. Attempt Supabase Cloud Read
    try:
        res = supabase_request("contractor_account_requests?order=id.desc&select=*")
        if res and isinstance(res, list) and len(res) > 0:
            return res
    except Exception:
        pass

    # 2. Fallback to SQLite
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contractor_account_requests ORDER BY id DESC")
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

# Ensure contractor tables and default seeds exist
seed_contractor_accounts()
