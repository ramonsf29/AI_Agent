import json
from pathlib import Path

from model.local_model import LocalModel
from prompts.swift_analysis import build_swift_analysis_messages
from model.analysis_schema import validate_analysis


MODEL = "mlx-community/Qwen2.5-Coder-14B-Instruct-4bit"


def main():
    source_code = Path("example.swift").read_text()

    llm = LocalModel(MODEL)

    messages = build_swift_analysis_messages(source_code)

    response = llm.generate(
        messages=messages,
        max_tokens=600,
    )

    clean_response = response.strip()

    if clean_response.startswith("```json"):
        clean_response = clean_response.removeprefix("```json")

    if clean_response.endswith("```"):
        clean_response = clean_response.removesuffix("```")

    clean_response = clean_response.strip()

    try:
        analysis = json.loads(clean_response)
        if not validate_analysis(analysis):
            print("\nERROR: JSON structure is invalid.")
            return

    except json.JSONDecodeError as error:
        print("\nERROR: The model returned invalid JSON.")
        print(error)
        return

    print("\n--- SUMMARY ---\n")
    print(analysis["summary"])

    print("\n--- EDGE CASES ---\n")
    for edge_case in analysis["edge_cases"]:
        print(f"- {edge_case}")

    print("\n--- POTENTIAL ISSUES ---\n")
    for issue in analysis["potential_issues"]:
        print(
            f"- {issue['description']} "
            f"(confidence: {issue['confidence']})"
        )


if __name__ == "__main__":
    main()