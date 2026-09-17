from fastapi import FastAPI, HTTPException # import fast api modules which we are using as our backend server
from fastapi.middleware.cors import CORSMiddleware # cors allows to exchange api requests between frontend and backend with the permissions of browser
from pydantic import BaseModel # checks whether ip and reason is provided 
import sqlite3

from app.detector import run_threat_analysis
from app.firewall import block_ip, get_blocked_ips
from app.soar_engine import execute_soar_playbook

app = FastAPI(
    title="🛡️ Log Security Analyzer API",
    description="REST API for real-time security log parsing, threat detection, and automated IP blocking.",
    version="1.0.0"
)

# Enable CORS for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # * is a wild card character which allows all type / any type of origins 
    allow_credentials=True, # allows sensiitve information like cookies,etc
    allow_methods=["*"], # ""
    allow_headers=["*"], # ""
)

# Pydantic Model for Manual IP Blocking
class BlockIPRequest(BaseModel):
    ip: str
    reason: str = "Manual Admin Block" # this reason is provided when admin manually blocks the ip address

@app.get("/")
def read_root():
    """Root endpoint to verify API server status."""
    return {"status": "online", "system": "Log Security Analyzer & SOAR Engine", "version": "1.0.0"}

@app.get("/logs") # collects logs of web server log file
def fetch_logs(limit: int = 50):
    """Retrieves recent parsed web access logs from the database."""
    conn = sqlite3.connect("data/security_logs.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, ip, timestamp, method, url, status, user_agent FROM access_logs ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    
    logs = [
        {
            "id": r[0], "ip": r[1], "timestamp": r[2], 
            "method": r[3], "url": r[4], "status": r[5], "user_agent": r[6]
        }
        for r in rows
    ]
    return {"count": len(logs), "logs": logs}

@app.get("/threats")
def analyze_threats():
    """Runs the threat detection rules and returns active security threats."""
    threats = run_threat_analysis()
    return {"threat_count": len(threats), "threats": threats}

@app.get("/blocked-ips")
def list_blocked_ips():
    """Returns all currently blocked IP addresses from the firewall database."""
    blocked = get_blocked_ips()
    formatted = [{"ip": b[0], "reason": b[1], "blocked_at": b[2]} for b in blocked]
    return {"count": len(formatted), "blocked_ips": formatted}

@app.post("/block-ip")
def manual_block_ip(request: BlockIPRequest):
    """Manually adds an IP address to the firewall blocklist."""
    success = block_ip(request.ip, reason=request.reason)
    if not success:
        raise HTTPException(status_code=400, detail=f"IP {request.ip} is already blocked.")
    return {"status": "success", "message": f"Successfully blocked IP {request.ip}"}

@app.post("/run-soar")
def trigger_soar_playbook():
    """Triggers the automated SOAR playbook (Detect -> Alert -> Auto-Block)."""
    execute_soar_playbook()
    return {"status": "success", "message": "SOAR automated playbook executed successfully."}
