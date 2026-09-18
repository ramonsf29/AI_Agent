# from model.analysis_schema import (
#     BehaviorComparison,
#     TestExecutionResult,
#     TestScenario,
# )
#
# from tools.swift_tools import run_swift_code
#
#
# def execute_scenario(
#     source_code: str,
#     scenario: TestScenario,
#     function_name: str,
# ) -> TestExecutionResult:
#
#     arguments = ",\n        ".join(
#         f"{test_input.name}: {test_input.value}"
#         for test_input in scenario.inputs
#     )
#
#     executable_source = f"""
# {source_code}
#
# let result = {function_name}(
#         {arguments}
# )
#
# print(result)
# """
#
#     output = run_swift_code(executable_source)
#
#     actual_output = int(output)
#
#     return TestExecutionResult(
#         scenario_name=scenario.name,
#         expected_output=scenario.expected_output,
#         actual_output=actual_output,
#         matches_expected=(
#             actual_output == scenario.expected_output
#         ),
#     )
#
#
# def compare_behavior(
#     scenario: TestScenario,
#     new_source_code: str,
#     old_source_code: str | None,
#     function_name: str,
# ) -> BehaviorComparison:
#
#     new_result = execute_scenario(
#         source_code=new_source_code,
#         scenario=scenario,
#         function_name=function_name,
#     )
#
#     if old_source_code is None:
#         return BehaviorComparison(
#             scenario_name=scenario.name,
#             old_output=None,
#             new_output=new_result.actual_output,
#             behavior_changed=None,
#         )
#
#     old_result = execute_scenario(
#         source_code=old_source_code,
#         scenario=scenario,
#         function_name=function_name,
#     )
#
#     return BehaviorComparison(
#         scenario_name=scenario.name,
#         old_output=old_result.actual_output,
#         new_output=new_result.actual_output,
#         behavior_changed=(
#             old_result.actual_output
#             != new_result.actual_output
#         ),
#     )

from model.analysis_schema import (
    BehaviorComparison,
    TestExecutionResult,
    TestScenario,
)

from tools.swift_tools import run_swift_code


def execute_scenario(
    source_code: str,
    scenario: TestScenario,
    function_name: str,
) -> TestExecutionResult:

    arguments = ",\n        ".join(
        f"{test_input.name}: {test_input.value}"
        for test_input in scenario.inputs
    )

    executable_source = f"""
{source_code}

let result = {function_name}(
        {arguments}
)

print(result)
"""

    output = run_swift_code(executable_source)

    actual_output = int(output)

    return TestExecutionResult(
        scenario_name=scenario.name,
        expected_output=scenario.expected_output,
        actual_output=actual_output,
        matches_expected=(
            actual_output == scenario.expected_output
        ),
    )


def compare_behavior(
    scenario: TestScenario,
    new_source_code: str,
    old_source_code: str | None,
    function_name: str,
) -> BehaviorComparison:

    new_result = execute_scenario(
        source_code=new_source_code,
        scenario=scenario,
        function_name=function_name,
    )

    if old_source_code is None:
        return BehaviorComparison(
            scenario_name=scenario.name,
            old_output=None,
            new_output=new_result.actual_output,
            behavior_changed=None,
        )

    old_result = execute_scenario(
        source_code=old_source_code,
        scenario=scenario,
        function_name=function_name,
    )

    return BehaviorComparison(
        scenario_name=scenario.name,
        old_output=old_result.actual_output,
        new_output=new_result.actual_output,
        behavior_changed=(
            old_result.actual_output
            != new_result.actual_output
        ),
    )