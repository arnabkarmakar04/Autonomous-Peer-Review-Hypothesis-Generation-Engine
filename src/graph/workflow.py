from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

# 1. New correct import for the serializer
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer

from src.graph.state import GraphState

# 2. Define a serializer that explicitly allows your custom models
# This tells LangGraph exactly which modules are safe to reconstruct
# using a list of tuples [(module_name, class_name)] to avoid the generic warning and ensure proper deserialization of Pydantic models
custom_serde = JsonPlusSerializer(
    allowed_msgpack_modules=[
        ("src.graph.state", "MethodologyExtraction"),
        ("src.graph.state", "HypothesisGeneration")
    ]
)

from src.agents.nodes import (
    fetch_paper_node, 
    extract_methodology_node, 
    critique_node, 
    synthesis_node
)

def build_graph():
    """Constructs the LangGraph state machine with custom serialization."""
    builder = StateGraph(GraphState)
    
    # Add nodes
    builder.add_node("fetcher", fetch_paper_node)
    builder.add_node("extractor", extract_methodology_node)
    builder.add_node("sparring_partner", critique_node)
    builder.add_node("synthesizer", synthesis_node)
    
    # Define the linear flow (edges)
    builder.add_edge(START, "fetcher")
    
    def check_fetch_status(state: GraphState):
        if state.get("status") == "error":
            return END
        return "extractor"
        
    builder.add_conditional_edges("fetcher", check_fetch_status)
    builder.add_edge("extractor", "sparring_partner")
    builder.add_edge("sparring_partner", "synthesizer")
    builder.add_edge("synthesizer", END)
    
    # 3. Pass the custom_serde to the MemorySaver
    # This ensures Pydantic models are handled natively without warnings
    memory = MemorySaver(serde=custom_serde)
    
    return builder.compile(checkpointer=memory)