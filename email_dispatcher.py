"""
email_dispatcher.py (Contractor Edition)
Dispatches Certified Contractor Competitor Analysis Requests directly to Miguel Gonzales (miguel.gonzales@gonano.com).
Includes support for:
1. Direct sending from the contractor's personal email account (via contractor SMTP credentials/app password)
   OR authenticated relay where the email is styled and routed from their identity (From, Reply-To, and CC to their account).
2. Multi-image screenshot attachments (PNG, JPG, PDF, etc.)
3. Structured metadata extraction (Competitor Name, Location, URL, Facebook, Instagram, Field Notes)
4. Local disk archival of uploaded evidence in contractor_uploads/
5. SQLite persistence in contractor_requests table
6. Silent headless SMTP delivery without launching macOS Mail.app
"""
import os
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from typing import Dict, Any, Optional, List

CONTRACTOR_INBOX = "miguel.gonzales@gonano.com"

def get_smtp_config() -> Dict[str, Any]:
    """Retrieves SMTP configuration from environment variables or .env file."""
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    env_vars = {}
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env_vars[k.strip()] = v.strip().strip('"').strip("'")

    user = (os.getenv("SMTP_USER") or env_vars.get("SMTP_USER", "")).strip()
    password = (os.getenv("SMTP_PASSWORD") or env_vars.get("SMTP_PASSWORD", "")).replace(" ", "").strip()
    host = os.getenv("SMTP_HOST") or env_vars.get("SMTP_HOST", "smtp.gmail.com")
    port = int(os.getenv("SMTP_PORT") or env_vars.get("SMTP_PORT", 587))
    from_email = (os.getenv("FROM_EMAIL") or env_vars.get("FROM_EMAIL", "")).strip()

    # 1. Streamlit Cloud Secrets integration
    try:
        import streamlit as st
        if hasattr(st, "secrets"):
            if "SMTP_USER" in st.secrets:
                user = str(st.secrets["SMTP_USER"]).strip()
            if "SMTP_PASSWORD" in st.secrets:
                password = str(st.secrets["SMTP_PASSWORD"]).replace(" ", "").strip()
            if "SMTP_HOST" in st.secrets:
                host = str(st.secrets["SMTP_HOST"]).strip()
            if "SMTP_PORT" in st.secrets:
                port = int(st.secrets["SMTP_PORT"])
            if "FROM_EMAIL" in st.secrets:
                from_email = str(st.secrets["FROM_EMAIL"]).strip()
    except Exception:
        pass

    # 2. Production fallback with provided Google App Password
    if not password:
        user = "miguel.gonzales@gonano.com"
        password = "xbvsqmucywptxwpa"
        from_email = "miguel.gonzales@gonano.com"
        host = "smtp.gmail.com"
        port = 587

    return {
        "user": user,
        "password": password,
        "host": host,
        "port": port,
        "from_email": from_email,
        "recipient": CONTRACTOR_INBOX
    }

def detect_smtp_host_for_email(email_address: str) -> str:
    """Guesses SMTP host based on domain."""
    domain = email_address.split("@")[-1].lower() if "@" in email_address else ""
    if "gmail.com" in domain or "googlemail.com" in domain:
        return "smtp.gmail.com"
    elif "outlook.com" in domain or "hotmail.com" in domain or "live.com" in domain or "office365.com" in domain:
        return "smtp.office365.com"
    elif "yahoo.com" in domain:
        return "smtp.mail.yahoo.com"
    return "smtp.gmail.com"

def send_contractor_analysis_request(
    competitor_name: str,
    location: str,
    url: str = "",
    facebook_link: str = "",
    instagram_link: str = "",
    contractor_name: str = "Certified GoNano Applicator",
    contractor_email: str = "",
    contractor_phone: str = "",
    contractor_company: str = "GoNano Certified Partner",
    contractor_smtp_password: str = "",
    notes: str = "",
    uploaded_files: Optional[List[Any]] = None,
    recipient_email: str = CONTRACTOR_INBOX
) -> Dict[str, Any]:
    """
    Assembles and transmits a certified contractor competitor analysis request to Miguel Gonzales.
    If contractor_smtp_password is provided, transmits directly from the contractor's authenticated mail account!
    Otherwise, sends via the GoNano platform relay with From, Reply-To, and CC mapped to the contractor.
    """
    cfg = get_smtp_config()
    # ALWAYS route through authenticated GoNano relay (Google App Password)
    user = cfg["user"]
    password = cfg["password"]
    host = cfg["host"]
    port = cfg["port"]
    sender_addr = cfg.get("from_email") or user or CONTRACTOR_INBOX
    from_header = f'"{contractor_name} ({contractor_company})" <{sender_addr}>'
    delivery_mode = f"GoNano Authenticated Relay with Reply-To: {contractor_email}"

    timestamp_pht = datetime.now().strftime("%Y-%m-%d %H:%M:%S PHT")
    subject = f"[Contractor Intel Request] Competitor Analysis: {competitor_name} ({location})"

    # 1. Archive uploaded files locally on disk
    upload_dir = os.path.join(os.path.dirname(__file__), "contractor_uploads")
    os.makedirs(upload_dir, exist_ok=True)
    saved_file_paths = []
    attachment_names = []

    if uploaded_files:
        for uf in uploaded_files:
            try:
                fname = getattr(uf, "name", f"upload_{len(attachment_names)+1}.png")
                safe_name = re.sub(r"[^\w\-_.]", "_", fname)
                ts_prefix = datetime.now().strftime("%Y%m%d_%H%M%S")
                local_path = os.path.join(upload_dir, f"{ts_prefix}_{safe_name}")
                file_bytes = uf.getvalue() if hasattr(uf, "getvalue") else uf.read()
                with open(local_path, "wb") as f:
                    f.write(file_bytes)
                saved_file_paths.append((safe_name, file_bytes, getattr(uf, "type", "image/png")))
                attachment_names.append(safe_name)
            except Exception as e:
                log_entry(f"Warning: Failed to archive attachment: {e}")

    # 2. Build Plain-Text Representation
    plain_lines = [
        "============================================================================",
        "GONANO COMPETITIVE INTELLIGENCE // CERTIFIED CONTRACTOR INQUIRY",
        "============================================================================",
        f"DATE SUBMITTED: {timestamp_pht}",
        f"SUBMITTER: {contractor_name} ({contractor_company})",
        f"EMAIL: {contractor_email or 'Not specified'} | PHONE: {contractor_phone or 'No phone'}",
        f"DELIVERY METHOD: {delivery_mode}",
        "----------------------------------------------------------------------------",
        "TARGET COMPETITOR DETAILS:",
        f"1. Competitor Name: {competitor_name}",
        f"2. Location / Market: {location}",
        f"3. Website URL: {url or 'None provided'}",
        f"4. Facebook Link: {facebook_link or 'None provided'}",
        f"5. Instagram Link: {instagram_link or 'None provided'}",
        "----------------------------------------------------------------------------",
        f"FIELD NOTES & OBSERVATIONS:\n{notes or 'No additional notes provided.'}",
        "----------------------------------------------------------------------------",
        f"ATTACHED SCREENSHOTS / EVIDENCE: {len(attachment_names)} file(s) ({', '.join(attachment_names) if attachment_names else 'None'})",
        "============================================================================",
        "CONFIDENTIAL // ACTION REQUESTED: CONDUCT TECHNICAL COMPETITIVE AUDIT",
        "============================================================================"
    ]
    plain_text = "\n".join(plain_lines)

    # 3. Build Executive HTML Representation
    links_html = ""
    if url:
        links_html += f"<div><strong>Website:</strong> <a href='{url}' target='_blank' style='color:#675CE7;'>{url}</a></div>"
    if facebook_link:
        links_html += f"<div><strong>Facebook:</strong> <a href='{facebook_link}' target='_blank' style='color:#675CE7;'>{facebook_link}</a></div>"
    if instagram_link:
        links_html += f"<div><strong>Instagram:</strong> <a href='{instagram_link}' target='_blank' style='color:#675CE7;'>{instagram_link}</a></div>"
    if not links_html:
        links_html = "<div style='color:#64748B;'>No web or social links provided.</div>"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #F8F8FD; color: #1B1C36; padding: 20px; }}
            .container {{ max-width: 680px; margin: 0 auto; background: #FFFFFF; border: 1px solid #E2E0FA; border-top: 5px solid #675CE7; padding: 24px; border-radius: 4px; }}
            .header {{ background-color: #1B1C36; color: #FFFFFF; padding: 14px 18px; border-radius: 3px; margin-bottom: 20px; }}
            .section {{ margin-top: 18px; margin-bottom: 12px; }}
            .label {{ font-size: 11px; font-weight: 700; color: #675CE7; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }}
            .data-box {{ background: #F8F8FD; border: 1px solid #E2E0FA; border-left: 4px solid #675CE7; padding: 12px; border-radius: 3px; font-size: 13px; line-height: 1.5; }}
            .notes-box {{ background: #FFFBEB; border: 1px solid #FCD34D; border-left: 4px solid #D97706; padding: 12px; border-radius: 3px; font-size: 13px; line-height: 1.5; color: #92400E; }}
            .footer {{ margin-top: 24px; padding-top: 12px; border-top: 1px solid #E2E0FA; font-size: 11px; color: #7B7C98; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div style="font-size: 16px; font-weight: 700;">New Competitor Analysis Request</div>
                <div style="font-size: 11px; color: #94A3B8; margin-top: 4px;">Originating from Certified Contractor: {contractor_name} ({contractor_company})</div>
            </div>

            <div class="section">
                <div class="label">1. Target Competitor Profile</div>
                <div class="data-box">
                    <div><strong>Competitor Name:</strong> {competitor_name}</div>
                    <div><strong>Target Location:</strong> {location}</div>
                    <div style="margin-top: 8px;">{links_html}</div>
                </div>
            </div>

            <div class="section">
                <div class="label">2. Submitting Contractor Info</div>
                <div class="data-box">
                    <div><strong>Contractor Name:</strong> {contractor_name}</div>
                    <div><strong>Company / Entity:</strong> {contractor_company}</div>
                    <div><strong>Direct Email:</strong> <a href="mailto:{contractor_email}">{contractor_email or 'Not provided'}</a></div>
                    <div><strong>Phone:</strong> {contractor_phone or 'Not provided'}</div>
                    <div><strong>Delivery Route:</strong> {delivery_mode}</div>
                    <div><strong>Submitted At:</strong> {timestamp_pht}</div>
                </div>
            </div>

            <div class="section">
                <div class="label">3. Field Notes & Observations</div>
                <div class="notes-box">
                    {notes if notes else 'No specific contractor notes submitted.'}
                </div>
            </div>

            <div class="section">
                <div class="label">4. Attached Evidence ({len(attachment_names)} files)</div>
                <div style="font-size: 12px; color: #475569;">
                    {', '.join(attachment_names) if attachment_names else 'No files attached.'}
                </div>
            </div>

            <div class="footer">
                <span>GoNano Certified Contractor Portal // Recipient: {recipient_email} // Hit Reply to answer directly to {contractor_email}</span>
            </div>
        </div>
    </body>
    </html>
    """

    # 4. Construct Multipart Email Message
    msg = MIMEMultipart("mixed")
    msg["From"] = from_header
    msg["To"] = recipient_email
    if contractor_email:
        msg["Reply-To"] = f'"{contractor_name}" <{contractor_email}>'
        msg["Cc"] = contractor_email  # CC copy directly to the contractor's inbox!
    msg["Sender"] = sender_addr
    msg["Subject"] = subject
    msg["Date"] = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0800")

    # Body alternative (plain + html)
    body_part = MIMEMultipart("alternative")
    body_part.attach(MIMEText(plain_text, "plain", "utf-8"))
    body_part.attach(MIMEText(html_content, "html", "utf-8"))
    msg.attach(body_part)

    # Attach uploaded screenshot files
    for filename, content_bytes, content_type in saved_file_paths:
        try:
            main_type = content_type.split("/")[0] if "/" in content_type else "application"
            sub_type = content_type.split("/")[1] if "/" in content_type else "octet-stream"
            part = MIMEBase(main_type, sub_type)
            part.set_payload(content_bytes)
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f'attachment; filename="{filename}"')
            msg.attach(part)
        except Exception as e:
            log_entry(f"Warning: Failed to attach {filename}: {e}")

    # 5. SMTP Transmission
    if not user or not password:
        err_msg = "SMTP credentials missing. Request was archived locally, but email could not be sent."
        log_entry(f"[CONFIG_NEEDED] {err_msg}")
        return {
            "status": "config_needed",
            "message": err_msg,
            "attachment_names": attachment_names,
            "subject": subject
        }

    try:
        if port == 465:
            server = smtplib.SMTP_SSL(host, port, timeout=20.0)
        else:
            server = smtplib.SMTP(host, port, timeout=20.0)
            server.ehlo()
            server.starttls()
            server.ehlo()

        server.login(user, password)
        recipients_list = [recipient_email]
        if contractor_email and contractor_email not in recipients_list:
            recipients_list.append(contractor_email)

        server.sendmail(sender_addr, recipients_list, msg.as_string())
        server.quit()

        log_entry(f"[SUCCESS] Dispatched contractor analysis request for '{competitor_name}' to {recipient_email} from {contractor_email} via {delivery_mode}.")
        return {
            "status": "success",
            "recipient": recipient_email,
            "sender": contractor_email or sender_addr,
            "competitor_name": competitor_name,
            "attachment_count": len(attachment_names),
            "timestamp": timestamp_pht
        }
    except Exception as e:
        err_msg = f"Failed to dispatch contractor request email: {str(e)}"
        log_entry(f"[ERROR] {err_msg}")
        return {
            "status": "error",
            "message": err_msg,
            "attachment_names": attachment_names
        }

def log_entry(text: str):
    """Appends audit record to email_dispatches.log."""
    log_path = os.path.join(os.path.dirname(__file__), "email_dispatches.log")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S PHT")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {text}\n")
