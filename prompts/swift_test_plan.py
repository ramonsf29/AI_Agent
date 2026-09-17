import json

from model.analysis_schema import SwiftDiffAnalysis


SYSTEM_PROMPT = (
    "You are a senior Swift developer specialized in software testing. "
    "Your job is to design focused test scenarios from analyzed code changes. "
    "Do not generate XCTest code yet. "
    "Do not invent business requirements that are not supported by the analysis."
)


def build_swift_test_plan_messages(
    diff_analysis: SwiftDiffAnalysis,
    git_diff: str,
) -> list[dict]:

    analysis_json = json.dumps(
        diff_analysis.model_dump(),
        indent=2,
    )

    user_prompt = f"""
Create a test plan for the following analyzed Swift code changes.

Analysis:

```json
{analysis_json}
```

Original Git diff:

```diff
{git_diff}
```

Return ONLY valid JSON using this exact structure:

{{
  "scenarios": [
    {{
      "name": "descriptive test scenario name",
      "purpose": "what this scenario is trying to verify",
      "input_description": "inputs or preconditions required",
      "expected_behavior": "observable behavior that should be checked",
      "priority": "low | medium | high"
    }}
  ]
}}

Rules:

- Do not generate XCTest code.
- Focus on behavior changed or potentially affected by the diff.
- Prefer boundary cases and regression risks.
- Use the original Git diff as the source of truth.
- Use the analysis only as supporting reasoning.
- Do not invent APIs.
- Do not invent business requirements.
- Make each scenario independently understandable.
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