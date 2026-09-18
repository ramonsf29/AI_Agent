import json

from model.analysis_schema import (
    TestExecutionResult,
    TestScenario,
)


SYSTEM_PROMPT = (
    "You are a senior Swift developer specialized in XCTest. "
    "Generate concise, compilable XCTest code from verified scenarios. "
    "Use the verified runtime output as the expected value. "
    "Do not invent APIs."
)


def build_xctest_generation_messages(
    source_code: str,
    function_name: str,
    scenarios: list[TestScenario],
    execution_results: list[TestExecutionResult],
) -> list[dict]:

    verified_cases = []

    result_by_name = {
        result.scenario_name: result
        for result in execution_results
    }

    for scenario in scenarios:
        result = result_by_name[scenario.name]

        verified_cases.append(
            {
                "name": scenario.name,
                "purpose": scenario.purpose,
                "inputs": [
                    test_input.model_dump()
                    for test_input in scenario.inputs
                ],
                "expected_output": result.actual_output,
            }
        )

    cases_json = json.dumps(
        verified_cases,
        indent=2,
    )

    user_prompt = f"""
Generate XCTest code for the following verified Swift behavior.

Production code:

```swift
{source_code}
```

Function under test:

{function_name}

Verified scenarios:

```json
{cases_json}
```

Requirements:

- Import XCTest.
- Create one XCTestCase subclass.
- Create one test method per verified scenario.
- Use XCTAssertEqual.
- Use the verified expected_output values exactly.
- Use the exact Swift parameter names.
- Do not modify or duplicate the production function.
- Return only Swift code.
"""

    return [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": user_prompt,
        },
    ]