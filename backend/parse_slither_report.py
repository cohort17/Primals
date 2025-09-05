import json


def parse_slither_report(report_file="slither-report.json"):
    """
Parses a Slither JSON report and prints a formatted summary of the findings.
    """
    try:
        with open(report_file, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: The report file '{report_file}' was not found.")
        return

    issues = data.get("results", {}).get("detectors", [])
    if not issues:
        print("No issues found in the Slither report.")
        return

    print("--- Slither Analysis Report ---")
    for issue in issues:
        # Safely get data to prevent KeyErrors
        impact = issue.get("impact", "N/A")
        check = issue.get("check", "N/A")
        description = issue.get("description", "No description available.")

        # Safely handle source mapping
        source_location = "N/A"
        elements = issue.get("elements", [])
        if elements:
            source_mapping = elements[0].get("source_mapping", {})
            filename = source_mapping.get("filename", "N/A")
            lines = source_mapping.get("lines", ["N/A"])[0]
            source_location = f"{filename}:{lines}"

        print(f"\n[Slither] Severity: {impact}")
        print(f"Check: {check}")
        print(f"Description: {description}")
        print(f"Location: {source_location}")
        print("-" * 40)
    print("--- End of Report ---")


if __name__ == "__main__":
    parse_slither_report()
