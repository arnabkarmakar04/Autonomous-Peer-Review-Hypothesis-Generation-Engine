from typing import TypedDict, List, Dict, Any
from pydantic import BaseModel, Field

# 1. Pydantic Model for Strict LLM Output Validation
class MethodologyExtraction(BaseModel):
    objective_function: str = Field(description="The primary mathematical objective or loss function")
    dataset_details: str = Field(description="Datasets used, including augmentations or splits")
    baselines: List[str] = Field(description="List of baseline models compared against")
    core_claims: str = Field(description="The main performance or theoretical claims made")

# 2. Pydantic Model for Novel Hypothesis Generation
class NovelHypothesis(BaseModel):
    title: str = Field(description="A highly technical, academic title for the hypothesis")
    problem_addressed: str = Field(description="The specific flaw from the critique this hypothesis solves")
    core_idea: str = Field(description="A 2-sentence summary of the main architectural change")
    technical_details: str = Field(description="A deep, rigorous explanation of the implementation")

# 3. Wrapper for a list of hypotheses to enforce exactly 3 outputs
class HypothesisGeneration(BaseModel):
    hypotheses: List[NovelHypothesis] = Field(description="A list containing exactly 3 hypotheses")

# 3. Graph State Definition
class GraphState(TypedDict):
    arxiv_id: str
    paper_metadata: Dict[str, str]
    raw_text: str
    extracted_methodology: MethodologyExtraction | None
    critique: str
    novel_hypotheses: List[str]
    status: str # "success" or "error"