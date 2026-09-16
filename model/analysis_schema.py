VALID_CONFIDENCE_VALUES = {"low", "medium", "high"}


def validate_analysis(data: dict) -> bool:
    required_keys = {
        "summary",
        "edge_cases",
        "potential_issues",
    }

    if not required_keys.issubset(data.keys()):
        return False

    if not isinstance(data["summary"], str):
        return False

    if not isinstance(data["edge_cases"], list):
        return False

    if not all(isinstance(item, str) for item in data["edge_cases"]):
        return False

    if not isinstance(data["potential_issues"], list):
        return False

    for issue in data["potential_issues"]:
        if not isinstance(issue, dict):
            return False

        if "description" not in issue:
            return False

        if "confidence" not in issue:
            return False

        if not isinstance(issue["description"], str):
            return False

        if issue["confidence"] not in VALID_CONFIDENCE_VALUES:
            return False

    return True