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

class TestScenario(BaseModel):
    name: str
    purpose: str
    input_description: str
    expected_behavior: str
    priority: Literal["low", "medium", "high"]


class SwiftTestPlan(BaseModel):
    scenarios: list[TestScenario]