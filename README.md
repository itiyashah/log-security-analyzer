# 🛡️ Log Security Analyzer & Threat Blocker

An automated SIEM & SOAR system that converts raw web access logs into structured database entries, detects active cyber threats, sends instant alerts, and blocks malicious IPs.

## 📌 Core Features

Regex Parsing: Ingests raw Apache/Nginx access.log entries into a structured SQLite database.

Threat Detection:🚨 Brute-Force: Detects repeated failed logins (401 on /login).

🔍 Directory Scanning: Detects unauthorized path scans (404 on /admin, /.env, /wp-login.php).

SOAR Automation: Executes an automated pipeline (Detect $\rightarrow$ Alert $\rightarrow$ Block).

Alerts & Mitigation: Sends notifications via Discord Webhooks (SIEM Security Lab), Slack, or mobile, and blocks IPs using a Windows Firewall simulator or Cloudflare API.

SOC Dashboard: React UI displaying live charts, visual maps, recent logs, blocklists, and manual IP blocking controls.

FastAPI Backend: Provides Swagger UI (/docs) for in-browser API testing without Postman.

## Data Flow & Limits

SQLite Database: Unlimited storage capacity.

Apache Backend API: Fetches up to 50 recent logs.

Nginx Frontend View: Displays the 15 most recent logs on the dashboard UI.

## Directory structure:

``` text
└── itiyashah-log-security-analyzer/
    ├── images.md
    ├── requirements.txt
    ├── app/
    │   ├── alerts.py
    │   ├── detector.py
    │   ├── firewall.py
    │   ├── main.py
    │   ├── parser.py
    │   └── soar_engine.py
    └── security-dashboard/
        ├── package.json
        └── src/
            ├── App.css
            └── App.js
```

to run the react app , first run uvicorn app.main:app --reload on one terminal then on another terminal run cd security-dashboard and then npm start , to run specefic python code script files run it in third terminal

then we also have option where admin can manually block the ip addresses






