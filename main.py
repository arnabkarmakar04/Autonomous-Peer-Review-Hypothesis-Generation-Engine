import os
import logging
import uuid
from src.graph.workflow import build_graph

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def run_pipeline(arxiv_id: str, thread_id: str):
    """
    Executes the Autonomous Peer-Review Engine graph using structured logging
    and persists the final artifact to disk.
    """
    # 1. Build the compiled LangGraph
    graph = build_graph()
    
    # 2. Configure thread ID for LangGraph's MemorySaver
    config = {"configurable": {"thread_id": thread_id}}
    
    # 3. Initial state injection
    initial_state = {
        "arxiv_id": arxiv_id
    }
    
    logger.info(f"Initializing pipeline for Arxiv ID: {arxiv_id} (Thread: {thread_id})")
    
    # 4. Stream the output as the graph traverses nodes
    for output in graph.stream(initial_state, config=config):
        for node_name, state_update in output.items():
            logger.info(f"Node execution completed: '{node_name}'")
            
    # 5. Retrieve final state from memory
    final_state = graph.get_state(config).values
    
    # Check for pipeline failures
    if final_state.get('status') == 'error':
        logger.error(f"Pipeline failed during execution: {final_state.get('raw_text', 'Unknown error')}")
        return
        
    title = final_state.get('paper_metadata', {}).get('title', 'Unknown Title')
    
    # 6. Save the final report to data/processed/
    os.makedirs("data/processed", exist_ok=True)
    report_path = f"data/processed/{arxiv_id}_review.md"
    
    logger.info(f"Writing final AI analysis artifact to {report_path}")
    
    try:
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(f"# AI Peer Review: {title}\n")
            f.write(f"**Arxiv ID:** {arxiv_id}\n\n")
            
            f.write("## 1. Methodology Extraction\n")
            methodology = final_state.get('extracted_methodology')
            if methodology:
                methodology_dict = methodology if isinstance(methodology, dict) else methodology.model_dump()
                f.write(f"**Objective Function:** {methodology_dict.get('objective_function')}\n\n")
                f.write(f"**Dataset:** {methodology_dict.get('dataset_details')}\n\n")
                f.write(f"**Baselines:** {', '.join(methodology_dict.get('baselines', []))}\n\n")
                f.write(f"**Claims:** {methodology_dict.get('core_claims')}\n\n")
            else:
                f.write("*Methodology extraction failed or was skipped.*\n\n")
            
            f.write("## 2. Critique\n")
            f.write(final_state.get('critique', 'No critique generated.'))
            f.write("\n\n")
            
            f.write("## 3. Novel Hypotheses\n")
            hypotheses = final_state.get('novel_hypotheses', [])
            if hypotheses:
                for i, hyp in enumerate(hypotheses, 1):
                    f.write(f"{i}. {hyp}\n")
            else:
                f.write("*No novel hypotheses generated.*\n")
                
        logger.info(f"Pipeline execution successful. Artifact secured.")
        
    except Exception as e:
        logger.error(f"Failed to write artifact to disk: {str(e)}")

if __name__ == "__main__":

    print("\nAutonomous AI Peer-Review Engine")
    print("-"*50)
    
    target_paper = input("Please enter the ArXiv ID to review (e.g., 1706.03762): ").strip()
    print("\n")
    if target_paper:
        session_id = f"session_{uuid.uuid4().hex[:8]}"
        run_pipeline(arxiv_id=target_paper, thread_id=session_id)
    else:
        print("No ArXiv ID provided. Exiting.")