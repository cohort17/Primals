import json

def parse_report(report_file="slither-report.json"):
    with open(report_file, "r") as f:
        data = json.load(f)
    issues = data.get("results", {}).get("detectors", [])
    for issue in issues:
        print(f"\n[Slither] Severity: {issue['impact']}")
        print(f"Check: {issue['check']}")
        print(f"Description: {issue['description']}")
        print(f"Location: {issue['elements'][0]['source_mapping']['filename']}:{issue['elements'][0]['source_mapping']['lines'][0]}")
        print("-" * 40)

if __name__ == "__main__":
    parse_report()
