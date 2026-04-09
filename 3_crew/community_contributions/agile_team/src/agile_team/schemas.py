from pydantic import BaseModel, Field
from typing import List, Optional

class CodeFile(BaseModel):
    """Represents a single source code file to be written to disk."""
    filename: str = Field(..., description="The name of the file including extension (e.g., 'app.py')")
    content: str = Field(..., description="The full source code of the file")
    path: str = Field(..., description="The relative directory path where the file should be saved")

class PRD(BaseModel):
    """Product Requirements Document"""
    title: str
    functional_requirements: List[str]
    non_functional_requirements: List[str]
    user_stories: List[str]
    acceptance_criteria: List[str]
    markdown_content: str = Field(..., description="The full PRD in markdown format")

class ArchitectureDesign(BaseModel):
    """Technical Architecture Design"""
    design_patterns: List[str]
    data_model: str
    api_endpoints: List[str]
    deployment_strategy: str
    markdown_content: str = Field(..., description="The full architecture design in markdown format")

class ImplementationOutput(BaseModel):
    """Output for Backend/Frontend Engineers"""
    summary: str = Field(..., description="Brief summary of implemented features")
    files: List[CodeFile] = Field(..., description="List of files to be created")

class SecurityReport(BaseModel):
    """Security Audit Report"""
    vulnerabilities: List[str]
    criticality_levels: List[str]
    mitigation_plan: str
    validation_scripts: List[CodeFile] = Field(..., description="Python scripts to verify security fixes")
    markdown_content: str = Field(..., description="The full security report in markdown format")

class QAManifest(BaseModel):
    """Quality Assurance Manifest"""
    test_plan: str
    test_suites: List[CodeFile] = Field(..., description="Pytest/unittest files")
    coverage_goals: str

class SprintReview(BaseModel):
    """Sprint Review Summary"""
    achievements: List[str]
    pending_items: List[str]
    retrospective: str
    markdown_content: str = Field(..., description="The full sprint review in markdown format")
