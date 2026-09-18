from pathlib import Path

from agent.swift_analisys_agent import SwiftAnalysisAgent
from model.local_model import LocalModel
from tools.git_tools import (
    get_changed_swift_files,
    get_file_from_head,
)
from tools.test_execution import (
    compare_behavior,
    execute_scenario,
)
from tools.test_file_tools import save_generated_test
from tools.swift_tools import run_generated_xctests


MODEL = "mlx-community/Qwen2.5-Coder-14B-Instruct-4bit"

FUNCTION_NAME = "refillAmount"


def main():
    model = LocalModel(MODEL)
    agent = SwiftAnalysisAgent(model)

    # --------------------------------------------------
    # 1. Analyze Git changes
    # --------------------------------------------------

    git_diff, diff_analysis = agent.analyze_git_diff()

    print("\n--- DIFF SUMMARY ---")
    print(diff_analysis.summary)

    # --------------------------------------------------
    # 2. Generate proposed test scenarios
    # --------------------------------------------------

    test_plan = agent.create_test_plan(
        diff_analysis,
        git_diff,
    )

    # --------------------------------------------------
    # 3. Locate changed Swift source
    # --------------------------------------------------

    changed_files = get_changed_swift_files()

    if not changed_files:
        print("No Swift files changed.")
        return

    # V1 limitation:
    # only analyze the first changed Swift file.
    file_path = changed_files[0]

    new_source_code = Path(file_path).read_text()
    old_source_code = get_file_from_head(file_path)

    print("\n--- FILE ---")
    print(file_path)

    # --------------------------------------------------
    # 4. Execute scenarios against real Swift code
    # --------------------------------------------------

    execution_results = []

    print("\n--- EXECUTION RESULTS ---")

    for scenario in test_plan.scenarios:

        result = execute_scenario(
            source_code=new_source_code,
            scenario=scenario,
            function_name=FUNCTION_NAME,
        )

        execution_results.append(result)

        print(f"\nScenario: {result.scenario_name}")
        print(f"LLM expected: {result.expected_output}")
        print(f"Actual Swift output: {result.actual_output}")
        print(
            f"Planner was correct: "
            f"{result.matches_expected}"
        )

    # --------------------------------------------------
    # 5. Compare old vs new behavior
    # --------------------------------------------------

    print("\n--- BEHAVIOR COMPARISON ---")

    for scenario in test_plan.scenarios:

        comparison = compare_behavior(
            scenario=scenario,
            new_source_code=new_source_code,
            old_source_code=old_source_code,
            function_name=FUNCTION_NAME,
        )

        print(f"\nScenario: {comparison.scenario_name}")
        print(f"Old: {comparison.old_output}")
        print(f"New: {comparison.new_output}")
        print(
            f"Behavior changed: "
            f"{comparison.behavior_changed}"
        )

    # --------------------------------------------------
    # 6. Generate XCTest from VERIFIED runtime behavior
    # --------------------------------------------------

    xctest_code = agent.generate_xctest(
        source_code=new_source_code,
        function_name=FUNCTION_NAME,
        scenarios=test_plan.scenarios,
        execution_results=execution_results,
    )

    print("\n--- GENERATED XCTEST ---\n")
    print(xctest_code)

    test_file = save_generated_test(
        test_code=xctest_code,
        output_path="GeneratedTests.swift",
    )

    print("\n--- TEST EXECUTION ---")

    tests_passed, test_output = run_generated_xctests(
        production_code=new_source_code,
        test_code=xctest_code,
    )

    if tests_passed:
        print("Generated XCTest compiled and passed.")
    else:
        print("Generated XCTest failed.")
        print(test_output)

if __name__ == "__main__":
    main()