from agent.swift_analisys_agent import SwiftAnalysisAgent
from model.local_model import LocalModel


MODEL = "mlx-community/Qwen2.5-Coder-14B-Instruct-4bit"


def main():
    model = LocalModel(MODEL)
    agent = SwiftAnalysisAgent(model)

    git_diff, diff_analysis = agent.analyze_git_diff()

    print("\n--- DIFF SUMMARY ---")
    print(diff_analysis.summary)

    test_plan = agent.create_test_plan(
        diff_analysis,
        git_diff,
    )

    print("\n--- TEST PLAN ---")

    for scenario in test_plan.scenarios:
        print(f"\nName: {scenario.name}")
        print(f"Purpose: {scenario.purpose}")
        print(f"Input: {scenario.input_description}")
        print(f"Expected: {scenario.expected_behavior}")
        print(f"Priority: {scenario.priority}")

    validation = agent.verify_test_plan(
        git_diff,
        test_plan,
    )

    print("\n--- TEST PLAN VALIDATION ---")

    for item in validation.validations:
        print(f"\nScenario: {item.scenario_name}")
        print(f"Status: {item.status}")
        print(f"Reason: {item.reason}")


if __name__ == "__main__":
    main()