import arxiv
import requests
import os
from src.tools.pdf_parser import extract_text_from_pdf

RAW_DATA_DIR = "data/raw_pdfs"

def fetch_and_parse_arxiv(arxiv_id: str) -> dict:
    """
    Fetches paper metadata via the arXiv API, caches the PDF locally 
    if it doesn't already exist, and returns the parsed text.
    """
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    
    # 1. Define the exact path for this specific paper
    file_path = os.path.join(RAW_DATA_DIR, f"{arxiv_id}.pdf")
    
    # Initialize the arXiv client
    client = arxiv.Client()
    search = arxiv.Search(id_list=[arxiv_id])
    
    try:
        # 2. Fetch Metadata
        paper = next(client.results(search))
        metadata = {
            "title": paper.title,
            "authors": [author.name for author in paper.authors],
            "published": str(paper.published)
        }
        
        # 3. Smart Caching: Only download if the file is missing
        if not os.path.exists(file_path):
            print(f"[Ingestion] Downloading PDF from arXiv to {file_path}...")
            response = requests.get(paper.pdf_url)
            response.raise_for_status()
            
            # Save the binary content to disk
            with open(file_path, "wb") as f:
                f.write(response.content)
        else:
            print(f"[Ingestion] Using cached PDF found at {file_path}...")

        # 4. Delegate text extraction to our dedicated parser
        full_text = extract_text_from_pdf(file_path)
        
        return {
            "metadata": metadata,
            "text": full_text
        }
        
    except StopIteration:
        return {"error": f"arXiv ID {arxiv_id} not found."}
    except Exception as e:
        return {"error": str(e)}