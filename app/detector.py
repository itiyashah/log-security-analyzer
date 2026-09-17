import sqlite3
import requests

def get_geoip_info(ip_address):
    """Fetches country, city, and ISP information for an IP using ip-api.com."""
    # Skip local private IP ranges
    if ip_address.startswith(("127.", "192.168.", "10.")):
        return {"country": "Local Network", "city": "Internal", "isp": "Private IP"}
    
    try:
        url = f"http://ip-api.com/json/{ip_address}?fields=status,country,city,isp"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                return {
                    "country": data.get("country", "Unknown"),
                    "city": data.get("city", "Unknown"),
                    "isp": data.get("isp", "Unknown")
                }
    except Exception as e:
        print(f"⚠️ GeoIP lookup failed for {ip_address}: {e}")
        
    return {"country": "Unknown", "city": "Unknown", "isp": "Unknown"}

def detect_brute_force(db_path="data/security_logs.db", threshold=2):
    """Flags IPs with failed login attempts exceeding the threshold."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Query for IPs hitting /login with 401 Unauthorized status
    query = '''
        SELECT ip, COUNT(*) as failed_attempts 
        FROM access_logs 
        WHERE url LIKE '%login%' AND status = 401 
        GROUP BY ip 
        HAVING failed_attempts >= ?
    '''
    cursor.execute(query, (threshold,))
    results = cursor.fetchall()
    conn.close()
    
    threats = []
    for ip, count in results:
        geo_info = get_geoip_info(ip)
        threats.append({
            "ip": ip,
            "type": "Brute-Force Attack",
            "count": count,
            "severity": "HIGH",
            **geo_info
        })
    return threats

def detect_directory_scanning(db_path="data/security_logs.db", threshold=2):
    """Flags IPs requesting multiple non-existent sensitive URLs (404 status)."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Query for IPs generating repeated 404 errors on administrative paths
    query = '''
        SELECT ip, COUNT(*) as scan_attempts 
        FROM access_logs 
        WHERE status = 404 
        GROUP BY ip 
        HAVING scan_attempts >= ?
    '''
    cursor.execute(query, (threshold,))
    results = cursor.fetchall()
    conn.close()
    
    threats = []
    for ip, count in results:
        geo_info = get_geoip_info(ip)
        threats.append({
            "ip": ip,
            "type": "Directory Scanning",
            "count": count,
            "severity": "MEDIUM",
            **geo_info
        })
    return threats

def run_threat_analysis():
    """Runs all detection rules and displays a summary of flagged threats."""
    print("🔍 Running Threat Detection Analysis...\n")
    
    brute_force_threats = detect_brute_force()
    scanning_threats = detect_directory_scanning()
    
    all_threats = brute_force_threats + scanning_threats
    
    if not all_threats:
        print("✅ No malicious activity detected.")
        return all_threats

    print(f"🚨 FLAG: Found {len(all_threats)} suspicious threat activity pattern(s):\n")
    for threat in all_threats:
        print(f"-[{threat['severity']}] {threat['type']}")
        print(f"  • Attacker IP: {threat['ip']}")
        print(f"  • Trigger Count: {threat['count']} suspicious requests")
        print(f"  • Location: {threat['city']}, {threat['country']} ({threat['isp']})")
        print("-" * 50)
        
    return all_threats

if __name__ == "__main__":
    run_threat_analysis()