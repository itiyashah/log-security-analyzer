import re
import sqlite3
import os

# 1. Define our Regex Pattern to break down the web server log line
# Standard Nginx/Apache Common Log Format pattern:
LOG_PATTERN = re.compile(
    r'(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+-\s+-\s+\['
    r'(?P<timestamp>[^\]]+)\]\s+"(?P<method>GET|POST|PUT|DELETE)\s+'
    r'(?P<url>\S+)\s+HTTP/[0-9\.]+"\s+'
    r'(?P<status>\d{3})\s+(?P<size>\d+)'
)

def init_db(db_path="data/security_logs.db"):
    """Creates the SQLite database and logs table if they don't exist."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS access_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT,
            timestamp TEXT,
            method TEXT,
            url TEXT,
            status INTEGER,
            size INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def parse_and_store_logs(log_file_path, db_path="data/security_logs.db"):
    """Reads raw log file, extracts structured data with Regex, and saves to SQLite."""
    if not os.path.exists(log_file_path):
        print(f"❌ Error: Log file not found at {log_file_path}")
        return

    init_db(db_path)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    parsed_count = 0

    with open(log_file_path, 'r') as file:
        for line in file:
            match = LOG_PATTERN.search(line)
            if match:
                data = match.groupdict()
                cursor.execute('''
                    INSERT INTO access_logs (ip, timestamp, method, url, status, size)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    data['ip'],
                    data['timestamp'],
                    data['method'],
                    data['url'],
                    int(data['status']),
                    int(data['size'])
                ))
                parsed_count += 1

    conn.commit()
    conn.close()
    
    print(f"✅ Successfully parsed and saved {parsed_count} log entries into SQLite database!")

if __name__ == "__main__":
    parse_and_store_logs("data/access.log")