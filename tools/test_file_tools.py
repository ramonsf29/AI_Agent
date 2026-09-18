from pathlib import Path


def save_generated_test(
    test_code: str,
    output_path: str,
) -> Path:
    path = Path(output_path)
    path.write_text(test_code)
    return path