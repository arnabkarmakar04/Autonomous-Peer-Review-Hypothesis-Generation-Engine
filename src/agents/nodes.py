import json
from langchain_core.prompts import ChatPromptTemplate
from src.config import get_llm
from src.graph.state import GraphState, MethodologyExtraction, HypothesisGeneration
from src.tools.arxiv_client import fetch_and_parse_arxiv

def fetch_paper_node(state: GraphState) -> dict:
    """Node 1: Retrieves the paper and updates state."""
    print(f"\n-Fetching Paper...: {state['arxiv_id']}")
    result = fetch_and_parse_arxiv(state["arxiv_id"])
    
    if "error" in result:
        return {"status": "error", "raw_text": result["error"]}
        
    return {
        "paper_metadata": result["metadata"],
        "raw_text": result["text"],
        "status": "paper_fetched"
    }

def extract_methodology_node(state: GraphState) -> dict:
    """Node 2: Forces the LLM to output structured JSON representing the methodology."""
    print("\n-Extracting Methodology...")
    llm = get_llm(temperature=0.0)
    structured_llm = llm.with_structured_output(MethodologyExtraction)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert Machine Learning researcher. Extract the core methodology from the provided text."),
        ("human", "Paper Title: {title}\n\nPaper Text:\n{text}")
    ])
    
    chain = prompt | structured_llm
    # Truncating text slightly just in case it exceeds massive limits
    extraction = chain.invoke({"title": state["paper_metadata"]["title"], "text": state["raw_text"][:300000]})
    
    return {"extracted_methodology": extraction, "status": "methodology_extracted"}

def critique_node(state: GraphState) -> dict:
    """Node 3: The Sparring Partner. Identifies flaws in the methodology."""
    print("\n-Critiquing Methodology...")
    llm = get_llm(temperature=0.4)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a ruthless but fair AI conference reviewer (e.g., NeurIPS, ICLR). Analyze this methodology and identify logical flaws, outdated baselines, or dataset biases."),
        ("human", "Methodology to critique:\n{methodology}")
    ])
    
    # Safely handle the methodology whether it's a dict or a Pydantic object
    methodology = state["extracted_methodology"]
    methodology_str = json.dumps(methodology) if isinstance(methodology, dict) else methodology.model_dump_json()
    
    chain = prompt | llm
    critique = chain.invoke({"methodology": methodology_str})
    
    return {"critique": critique.content, "status": "critiqued"}

def synthesis_node(state: GraphState) -> dict:
    """Node 4: Proposes new research directions based on the critique."""
    print("\n-Synthesizing Novel Hypotheses...")
    llm = get_llm(temperature=0.7) # Higher temperature for creativity, but strictly structured
    structured_llm = llm.with_structured_output(HypothesisGeneration)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a visionary AI architect. Based on the flaws identified in a recent paper, propose 3 novel, highly technical, and untested hypotheses or architectural changes that would solve these flaws."),
        ("human", "Original Claims: {claims}\n\nIdentified Flaws: {critique}\n\nGenerate exactly 3 novel hypotheses.")
    ])
    
    chain = prompt | structured_llm
    
    # Safely extract claims regardless of whether it's a dict or Pydantic object
    methodology = state.get("extracted_methodology")
    claims = methodology.get("core_claims", "") if isinstance(methodology, dict) else methodology.core_claims
    
    # Execute the structured generation
    extraction: HypothesisGeneration = chain.invoke({
        "claims": claims,
        "critique": state["critique"]
    })
    
    # Format the structured JSON back into highly readable markdown strings for our final report
    formatted_hypotheses = []
    for h in extraction.hypotheses:
        formatted_text = (
            f"### {h.title}\n"
            f"**Problem Addressed:** {h.problem_addressed}\n"
            f"**Core Idea:** {h.core_idea}\n"
            f"**Technical Details:** {h.technical_details}\n"
        )
        formatted_hypotheses.append(formatted_text)
    
    return {"novel_hypotheses": formatted_hypotheses, "status": "completed"}