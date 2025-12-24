# loganalyzer.py
import argparse
from analyzer import parse_logs

def main():
    # Set the program name to LogAnalyzer
    parser = argparse.ArgumentParser(description="LogAnalyzer: SSH Brute Force Detection Tool")
    parser.add_argument("filename", help="Path to the auth.log file")
    args = parser.parse_args()

    try:
        with open(args.filename, "r", encoding="utf-8") as f:
            content = f.read()

        results = parse_logs(content)

        print(f"\nrunning LogAnalyzer on: {args.filename}...")
        print("=" * 60)
        print(f"{'IP ADDRESS':<20} | {'COUNT':<10} | {'USERS TARGETED'}")
        print("=" * 60)

        if not results:
            print("No failed attempts found.")
        else:
            for item in results:
                users = ", ".join(item["users"])
                print(f"{item['ip']:<20} | {str(item['count']):<10} | {users}")
        print("=" * 60 + "\n")

    except FileNotFoundError:
        print("Error: File not found.")

if __name__ == "__main__":
    main()