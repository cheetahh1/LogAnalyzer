# analyzer.py
import re
from collections import defaultdict

def parse_logs(log_text):
    """
    Core logic for LogAnalyzer.
    """
    # Regex for standard SSH auth.log format
    pattern = r"Failed password for (?:invalid user )?(?P<user>.*) from (?P<ip>\d+\.\d+\.\d+\.\d+)"
    
    data = defaultdict(lambda: {"count": 0, "users": set()})
    
    for line in log_text.splitlines():
        if "Failed password" in line:
            match = re.search(pattern, line)
            if match:
                ip = match.group("ip")
                user = match.group("user")
                data[ip]["count"] += 1
                data[ip]["users"].add(user)

    # Format the results
    results = []
    for ip, info in data.items():
        results.append({
            "ip": ip,
            "count": info["count"],
            "users": list(info["users"])
        })

    return sorted(results, key=lambda x: x["count"], reverse=True)