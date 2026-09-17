import json
from model.analysis_schema import SwiftTestPlan

SYSTEM_PROMPT = (
    "You are a senior Swift developer acting as a strict test-plan reviewer. "
    "Your job is to verify whether each proposed test scenario is consistent "
    "with the actual code shown in the Git diff. "
    "Do not assume business requirements that are not present in the code. "
    "Mark scenarios as uncertain when the expected behavior cannot be proven."
)


def build_test_plan_validation_messages(
    git_diff: str,
    test_plan: SwiftTestPlan,
) -> list[dict]:

    test_plan_json = json.dumps(
        test_plan.model_dump(),
        indent=2,
    )

    user_prompt = f"""
Review the following proposed Swift test plan against the original Git diff.

Original Git diff:

```diff
{git_diff}
```

Proposed test plan:

```json
{test_plan_json}
```

Validate every scenario independently.

Return ONLY valid JSON using this exact structure:

{{
  "validations": [
    {{
      "scenario_name": "exact scenario name from the test plan",
      "status": "valid | invalid | uncertain",
      "reason": "short technical explanation"
    }}
  ]
}}

Validation rules:

- Check whether the expected behavior follows from the actual code.
- Recalculate simple expressions when possible.
- Mark a scenario as "invalid" if its expected result contradicts the code.
- Mark a scenario as "uncertain" if correctness depends on a business rule
  or requirement that is not visible in the diff.
- Mark a scenario as "valid" only when the expectation is consistent with
  the observable implementation.
- Do not invent APIs or surrounding implementation.
- Do not modify the test plan.
- Return one validation entry for every scenario.
- Return JSON only.
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