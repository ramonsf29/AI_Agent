SYSTEM_PROMPT = (
    "You are a senior Swift developer specialized in software testing. "
    "Analyze code carefully and identify edge cases and suspicious behavior. "
    "Do not modify the production code. "
    "Distinguish observable facts from assumptions."
)


def build_swift_analysis_messages(source_code: str) -> list[dict]:
    user_prompt = f"""
    Analyze this Swift code:
    
    ```swift
    {source_code}
    ```
    
    Return ONLY valid JSON using this exact structure:
    
    {{
      "summary": "short explanation of what the code does",
      "edge_cases": [
        "edge case 1",
        "edge case 2"
      ],
      "potential_issues": [
        {{
          "description": "description of the potential issue",
          "confidence": "low | medium | high"
        }}
      ]
    }}
    
    Rules:
    
    - Do not include Markdown.
    - Do not include text before or after the JSON.
    - Do not modify the production code.
    - Do not call something a bug unless the code proves it.
    - Treat uncertain business expectations as assumptions.
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