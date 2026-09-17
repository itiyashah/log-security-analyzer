import sqlite3
import os

def init_firewall_db(db_path="data/security_logs.db"):
    """Creates the blocked_ips table if it doesn't exist."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blocked_ips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT UNIQUE,
            reason TEXT,
            blocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def block_ip(ip_address, reason="Suspicious Activity", db_path="data/security_logs.db"):
    """Adds an IP address to the firewall blocklist database."""
    init_firewall_db(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO blocked_ips (ip, reason)
            VALUES (?, ?)
        ''', (ip_address, reason))
        conn.commit()
        print(f"🧱 [FIREWALL BLOCK] Successfully added {ip_address} to active blocklist! (Reason: {reason})")
        success = True
    except sqlite3.IntegrityError:
        print(f"ℹ️ IP {ip_address} is already in the blocklist database.")
        success = False
        
    conn.close()
    return success

def get_blocked_ips(db_path="data/security_logs.db"):
    """Retrieves all currently blocked IPs."""
    init_firewall_db(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT ip, reason, blocked_at FROM blocked_ips")
    blocked_list = cursor.fetchall()
    conn.close()
    return blocked_list

if __name__ == "__main__":
    block_ip("198.51.100.22", reason="Brute-Force Attack")
    print("Blocked IPs List:", get_blocked_ips())