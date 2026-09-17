SYSTEM_PROMPT = (
    "You are a senior Swift developer specialized in software testing. "
    "Analyze code changes carefully. "
    "Focus on behavior introduced or modified by the diff. "
    "Do not assume that suspicious behavior is automatically a bug. "
    "Distinguish observable changes from assumptions."
)


def build_swift_diff_analysis_messages(git_diff: str) -> list[dict]:
    user_prompt = f"""
Analyze the following Git diff from a Swift project:

```diff
{git_diff}
```

Return ONLY valid JSON using this exact structure:

{{
  "summary": "short explanation of what changed",
  "behavior_changes": [
    "behavior change 1",
    "behavior change 2"
  ],
  "risk_areas": [
    {{
      "description": "potential risk introduced by the change",
      "confidence": "low | medium | high"
    }}
  ]
}}

Rules:

- Analyze only what can reasonably be inferred from the diff.
- Do not invent surrounding code.
- Do not call something a bug unless the diff proves it.
- Focus on behavior that should probably be tested.
- Do not include Markdown.
- Do not include text before or after the JSON.
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