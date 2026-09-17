import requests # this is used to send http api requests over the internet

# Optional: If you have a Discord Webhook URL, paste it here!
# Otherwise, keep it empty and the script will automatically run in Simulation Mode.
DISCORD_WEBHOOK_URL = ""

def send_security_alert(threat):
    """Sends a real-time threat alert to Discord via Webhook (or simulates it locally)."""
    payload = {
        "username": "🛡️ Security Bot",
        "embeds": [ # embed card
            {
                "title": f"🚨 [{threat['severity']}] {threat['type']} Detected!",
                "color": 15158332 if threat['severity'] == "HIGH" else 15844367, # Red or Yellow
                "fields": [
                    {"name": "Attacker IP", "value": f"`{threat['ip']}`", "inline": True},
                    {"name": "Location", "value": f"{threat['city']}, {threat['country']}", "inline": True},
                    {"name": "ISP", "value": threat['isp'], "inline": True},
                    {"name": "Trigger Count", "value": f"{threat['count']} requests", "inline": False}
                ],
                "footer": {"text": "Log Security Analyzer & Threat Blocker"}
            }
        ]
    }
    
    if DISCORD_WEBHOOK_URL:
        try:
            response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=5)
            if response.status_code == 204: # if alert message in form of json payload is successfully sent then it shows the success message 
                print(f"📩 Sent Discord alert for IP: {threat['ip']}")
                return True
        except Exception as e:
            print(f"⚠️ Failed to send Discord webhook alert: {e}")
            
    # Fallback / Simulation Mode
    print(f"📢 [SIMULATION ALERT] Webhook Triggered for IP {threat['ip']} ({threat['type']})")
    return True

if __name__ == "__main__":
    sample_threat = { # sample dataset
        "ip": "198.51.100.22",
        "type": "Brute-Force Attack",
        "count": 5,
        "severity": "HIGH",
        "country": "United States",
        "city": "New York",
        "isp": "Example ISP"
    }
    send_security_alert(sample_threat)
