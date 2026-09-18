import subprocess


def get_git_diff() -> str:
    result = subprocess.run(
        ["git", "diff", "HEAD", "--", "*.swift"],
        capture_output=True,
        text=True,
        check=True,
    )

    return result.stdout


def get_file_from_head(file_path: str) -> str | None:
    result = subprocess.run(
        ["git", "show", f"HEAD:{file_path}"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        return None

    return result.stdout

def get_changed_swift_files() -> list[str]:
    result = subprocess.run(
        ["git", "diff", "HEAD", "--name-only", "--", "*.swift"],
        capture_output=True,
        text=True,
        check=True,
    )

    return [
        line.strip()
        for line in result.stdout.splitlines()
        if line.strip()
    ]