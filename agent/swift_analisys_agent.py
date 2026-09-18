import json

from pydantic import ValidationError
from model.local_model import LocalModel
from prompts.swift_analysis import build_swift_analysis_messages
from prompts.swift_test_plan_validation import build_test_plan_validation_messages
from tools.file_tools import read_text_file
from prompts.swift_diff_analysis import build_swift_diff_analysis_messages
from tools.git_tools import get_git_diff
from model.analysis_schema import (
    SwiftAnalysis,
    SwiftDiffAnalysis,
    SwiftTestPlan,
    SwiftTestPlanValidation,
    TestExecutionResult,
    TestScenario,
)
from prompts.swift_xctest_generation import (
    build_xctest_generation_messages,
)

from prompts.swift_test_plan import build_swift_test_plan_messages

class SwiftAnalysisAgent:

    def __init__(self, model: LocalModel):
        self.model = model

    def analyze(self, source_code: str) -> SwiftAnalysis:
        messages = build_swift_analysis_messages(source_code)

        response = self.model.generate(
            messages=messages,
            max_tokens=600,
        )

        clean_response = self._clean_response(response)

        try:
            data = json.loads(clean_response)

        except json.JSONDecodeError as error:
            raise ValueError(
                "The model returned invalid JSON."
            ) from error

        try:
            return SwiftAnalysis.model_validate(data)

        except ValidationError as error:
            raise ValueError(
                "The model returned JSON with an invalid structure."
            ) from error

    def analyze_file(self, file_path: str) -> SwiftAnalysis:
        source_code = read_text_file(file_path)
        return self.analyze(source_code)

    def analyze_git_diff(self) -> tuple[str, SwiftDiffAnalysis]:
        git_diff = get_git_diff()

        if not git_diff.strip():
            raise ValueError("No Git changes found.")

        messages = build_swift_diff_analysis_messages(git_diff)

        response = self.model.generate(
            messages=messages,
            max_tokens=800,
        )

        clean_response = self._clean_response(response)

        try:
            data = json.loads(clean_response)

        except json.JSONDecodeError as error:
            raise ValueError(
                "The model returned invalid JSON."
            ) from error

        try:
            analysis = SwiftDiffAnalysis.model_validate(data)
            return git_diff, analysis

        except ValidationError as error:
            raise ValueError(
                "The model returned JSON with an invalid structure."
            ) from error

    def create_test_plan(self, diff_analysis: SwiftDiffAnalysis, git_diff: str) -> SwiftTestPlan:
        messages = build_swift_test_plan_messages(diff_analysis, git_diff)
        response = self.model.generate(
            messages=messages,
            max_tokens=1200,
        )

        clean_response = self._clean_response(response)

        try:
            data = json.loads(clean_response)

        except json.JSONDecodeError as error:
            raise ValueError(
                "The model returned invalid JSON while creating the test plan."
            ) from error

        try:
            return SwiftTestPlan.model_validate(data)

        except ValidationError as error:
            raise ValueError(
                "The model returned an invalid test plan structure."
            ) from error

    def verify_test_plan(
            self,
            git_diff: str,
            test_plan: SwiftTestPlan,
    ) -> SwiftTestPlanValidation:

        messages = build_test_plan_validation_messages(
            git_diff,
            test_plan,
        )

        response = self.model.generate(
            messages=messages,
            max_tokens=1200,
        )

        clean_response = self._clean_response(response)

        try:
            data = json.loads(clean_response)

        except json.JSONDecodeError as error:
            raise ValueError(
                "The model returned invalid JSON while validating the test plan."
            ) from error

        try:
            return SwiftTestPlanValidation.model_validate(data)

        except ValidationError as error:
            raise ValueError(
                "The model returned an invalid test-plan validation structure."
            ) from error

    def generate_xctest(
            self,
            source_code: str,
            function_name: str,
            scenarios: list[TestScenario],
            execution_results: list[TestExecutionResult],
    ) -> str:

        messages = build_xctest_generation_messages(
            source_code=source_code,
            function_name=function_name,
            scenarios=scenarios,
            execution_results=execution_results,
        )

        response = self.model.generate(
            messages=messages,
            max_tokens=1800,
        )

        return self._clean_swift_response(response)

    @staticmethod
    def _clean_swift_response(response: str) -> str:
        clean_response = response.strip()

        if clean_response.startswith("```swift"):
            clean_response = clean_response.removeprefix("```swift")

        if clean_response.endswith("```"):
            clean_response = clean_response.removesuffix("```")

        return clean_response.strip()

    @staticmethod
    def _clean_response(response: str) -> str:
        clean_response = response.strip()

        if clean_response.startswith("```json"):
            clean_response = clean_response.removeprefix("```json")

        if clean_response.endswith("```"):
            clean_response = clean_response.removesuffix("```")

        return clean_response.strip()
