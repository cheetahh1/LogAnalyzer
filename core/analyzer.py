# core/analyzer.py

from collections import defaultdict


def analyze(events, threshold=3):
    """
    Analyzes parsed log events and detects suspicious IPs.

    :param events: list of parsed log events
    :param threshold: number of failed attempts to mark IP as suspicious
    :return: dictionary with analysis results
    """

    total_failed = 0
    total_success = 0
    failed_by_ip = defaultdict(int)

    for event in events:
        if event["status"] == "failed":
            total_failed += 1
            failed_by_ip[event["ip"]] += 1
        elif event["status"] == "success":
            total_success += 1

    suspicious_ips = [
        ip for ip, count in failed_by_ip.items() if count >= threshold
    ]

    return {
        "total_failed": total_failed,
        "total_success": total_success,
        "failed_by_ip": dict(failed_by_ip),
        "suspicious_ips": suspicious_ips
    }


# ---------------- TEST BLOCK ----------------
if __name__ == "__main__":
    test_events = [
        {"status": "failed", "ip": "192.168.1.15"},
        {"status": "failed", "ip": "192.168.1.15"},
        {"status": "success", "ip": "10.0.0.7"},
        {"status": "failed", "ip": "192.168.1.15"},
    ]

    result = analyze(test_events, threshold=2)
    print("Analysis result:")
    for key, value in result.items():
        print(f"{key}: {value}")
