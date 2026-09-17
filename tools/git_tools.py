import subprocess


def get_git_diff() -> str:
    result = subprocess.run(
        ["git", "diff", "HEAD", "--", "*.swift"],
        capture_output=True,
        text=True,
        check=True,
    )

    return result.stdout