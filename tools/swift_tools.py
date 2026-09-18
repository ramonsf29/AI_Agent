# import subprocess
# import tempfile
# from pathlib import Path
#
#
def run_swift_code(source_code: str) -> str:
    with tempfile.TemporaryDirectory() as temp_dir:
        swift_file = Path(temp_dir) / "example.swift"
        swift_file.write_text(source_code)

        result = subprocess.run(
            ["swift", str(swift_file)],
            capture_output=True,
            text=True,
            check=True,
        )

        return result.stdout.strip()
#
# import subprocess
# from pathlib import Path
#
#
# def typecheck_swift_files(
#     file_paths: list[str],
# ) -> tuple[bool, str]:
#
#     developer_dir_result = subprocess.run(
#         ["xcode-select", "-p"],
#         capture_output=True,
#         text=True,
#         check=True,
#     )
#
#     developer_dir = Path(
#         developer_dir_result.stdout.strip()
#     )
#
#     frameworks_path = (
#         developer_dir
#         / "Platforms"
#         / "MacOSX.platform"
#         / "Developer"
#         / "Library"
#         / "Frameworks"
#     )
#
#     result = subprocess.run(
#         [
#             "xcrun",
#             "swiftc",
#             "-typecheck",
#             "-F",
#             str(frameworks_path),
#             *file_paths,
#         ],
#         capture_output=True,
#         text=True,
#     )
#
#     if result.returncode == 0:
#         return True, ""
#
#     return False, result.stderr

import subprocess
import tempfile
from pathlib import Path


def run_generated_xctests(
    production_code: str,
    test_code: str,
) -> tuple[bool, str]:

    with tempfile.TemporaryDirectory() as temp_dir:
        package_root = Path(temp_dir)

        sources_dir = (
            package_root
            / "Sources"
            / "AgentTarget"
        )

        tests_dir = (
            package_root
            / "Tests"
            / "AgentTargetTests"
        )

        sources_dir.mkdir(parents=True)
        tests_dir.mkdir(parents=True)

        package_file = package_root / "Package.swift"

        package_file.write_text(
            """
// swift-tools-version: 6.0

import PackageDescription

let package = Package(
    name: "AgentValidation",
    platforms: [
        .macOS(.v13)
    ],
    targets: [
        .target(
            name: "AgentTarget"
        ),
        .testTarget(
            name: "AgentTargetTests",
            dependencies: ["AgentTarget"]
        )
    ]
)
"""
        )

        production_file = (
            sources_dir / "Production.swift"
        )

        production_file.write_text(
            "public " + production_code
        )

        test_file = (
            tests_dir / "GeneratedTests.swift"
        )

        test_file.write_text(
            """
import XCTest
@testable import AgentTarget

"""
            + test_code.replace(
                "import XCTest",
                "",
            )
        )

        result = subprocess.run(
            ["swift", "test"],
            cwd=package_root,
            capture_output=True,
            text=True,
        )

        output = (
            result.stdout
            + "\n"
            + result.stderr
        )

        return (
            result.returncode == 0,
            output,
        )