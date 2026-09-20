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

## 🚀 How to Run
1. Setup

``` text
git clone https://github.com/itiyashah/itiyashah-log-security-analyzer.git

cd itiyashah-log-security-analyzer

pip install -r requirements.txt
```

2. Configure Discord Alert (Optional)
   
``` text
Add your webhook to app/alerts.py:

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/YOUR_WEBHOOK_URL"
```

3. Execution

Terminal 1 (Backend API):

``` text
uvicorn app.main:app --reload

(Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs))
```

Terminal 2 (React Frontend):

``` text
cd security-dashboard

npm install && npm start

(Dashboard UI: http://localhost:3000)
```

Terminal 3 (Individual Scripts):

``` text
python -m app.parser      # Parse raw logs into SQLite

python -m app.detector    # Run threat detection standalone

python -m app.soar_engine # Execute automated SOAR pipeline
```






