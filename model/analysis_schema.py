from typing import Literal
from pydantic import BaseModel

class PotentialIssue(BaseModel):
    description: str
    confidence: Literal["low", "medium", "high"]


class SwiftAnalysis(BaseModel):
    summary: str
    edge_cases: list[str]
    potential_issues: list[PotentialIssue]

class RiskArea(BaseModel):
    description: str
    confidence: Literal["low", "medium", "high"]


class SwiftDiffAnalysis(BaseModel):
    summary: str
    behavior_changes: list[str]
    risk_areas: list[RiskArea]

class TestInput(BaseModel):
    name: str
    value: int


class TestScenario(BaseModel):
    name: str
    purpose: str
    inputs: list[TestInput]
    expected_output: int
    priority: Literal["low", "medium", "high"]


class SwiftTestPlan(BaseModel):
    scenarios: list[TestScenario]

class TestExecutionResult(BaseModel):
    scenario_name: str
    expected_output: int
    actual_output: int
    matches_expected: bool

class BehaviorComparison(BaseModel):
    scenario_name: str
    old_output: int | None
    new_output: int
    behavior_changed: bool | None


class SwiftTestPlan(BaseModel):
    scenarios: list[TestScenario]


class TestScenarioValidation(BaseModel):
    scenario_name: str
    status: Literal["valid", "invalid", "uncertain"]
    reason: str


class SwiftTestPlanValidation(BaseModel):
    validations: list[TestScenarioValidation]