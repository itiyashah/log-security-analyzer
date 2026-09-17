from app.detector import run_threat_analysis
from app.alerts import send_security_alert
from app.firewall import block_ip

def execute_soar_playbook():
    """Runs automated security playbook: Detects threats, sends alerts, and blocks malicious IPs."""
    print("⚡ Starting SOAR Automated Defense Engine...\n")
    
    # 1. Detect Threats
    threats = run_threat_analysis()
    
    if not threats:
        print("✅ System clean. No automated actions needed.")
        return

    print("\n🤖 Executing Automated Response Playbook...\n")
    
    # 2. Loop through detected threats to Alert & Block
    for threat in threats:
        # Step A: Send Alert
        send_security_alert(threat)
        
        # Step B: Auto-block HIGH and MEDIUM severity threats
        if threat['severity'] in ["HIGH", "MEDIUM"]:
            block_ip(threat['ip'], reason=threat['type'])
            
    print("\n✅ SOAR Playbook Execution Complete!")

if __name__ == "__main__":
    execute_soar_playbook()