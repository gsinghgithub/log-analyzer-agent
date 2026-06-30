
def analyze_logs(log_text: str) -> dict:
    """
    Simple log analyzer tool.
    Extracts lines containing ERROR or Exception.
    """

    issues = []
    for line in log_text.splitlines():
        if "ERROR" in line or "Exception" in line:
            issues.append(line)

    return {
        "issue_count": len(issues),
        "issues": issues,
        "summary": f"Found {len(issues)} issues."
    }
