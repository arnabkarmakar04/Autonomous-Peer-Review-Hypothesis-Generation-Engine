# 🧠 Autonomous AI Peer-Review & Hypothesis Generation Engine

An end-to-end **agentic workflow** for automated critical analysis of Deep Learning research papers.

Unlike traditional summarization tools, this system uses a **multi-agent architecture** to:

* Deconstruct methodologies
* Identify logical flaws
* Generate novel, untested research hypotheses

---

## 🧠 System Architecture

The project is built on **LangGraph**, utilizing a state-machine approach to manage complex reasoning loops and memory persistence.

### The Agentic Workflow:

1. **Fetcher (Tool):** Deterministically retrieves papers from the ArXiv API, implementing a local PDF caching layer to optimize bandwidth and respect API rate limits.

2. **Extractor (Agent):** Uses Gemini 2.5 to parse unstructured PDF text into a strictly typed Pydantic schema, isolating core mathematical claims and datasets.

3. **Sparring Partner (Agent):** A "ruthless" reviewer agent that critiques the extracted methodology for biases, outdated baselines, and logical inconsistencies.

4. **Synthesizer (Agent):** A creative architect agent that proposes 3 high-level technical hypotheses to solve the identified flaws, outputting structured JSON for artifact generation.

---

## 🛠️ Tech Stack

* **Orchestration:** LangGraph (StateGraph with MemorySaver persistence)
* **LLM:** Google Gemini 2.5 Flash (via LangChain)
* **Data Engineering:** PyMuPDF (PDF Parsing), Arxiv API, Pydantic v2 (Data Validation)
* **Environment:** Python 3.12, Structured Logging, Dotenv

---

## 📁 Project Structure

```text
.
├── data/
│   ├── raw_pdfs/          # Local cache for downloaded ArXiv papers
│   └── processed/         # AI-generated Markdown review reports
├── src/
│   ├── agents/            # Multi-agent logic and LLM nodes
│   ├── graph/             # LangGraph workflow and state definitions
│   ├── tools/             # Deterministic PDF parsing and API clients
│   └── config.py          # Model and API configurations
├── main.py                # Interactive CLI entry point
└── requirements.txt       # Version-locked dependencies
```

---

## 🚀 Getting Started

### 1. Prerequisites

* Python 3.12
* Google AI Studio API Key (Gemini)

---

### 2. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd autonomous-peer-review-engine

# Create and activate virtual environment
python -m venv myvenv
source myvenv/bin/activate  # On Windows: myvenv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

### 3. Configuration

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

---

### 4. Execution

Run the interactive pipeline:

```bash
python main.py
```

When prompted, enter an ArXiv ID (e.g., 1706.03762). The system will process the paper and save a detailed Markdown report in `data/processed/`.

---

## 🛡️ Engineering Highlights

* **Future-Proof Serialization:** Implements a custom JsonPlusSerializer with module whitelisting to ensure stable checkpointing and prevent deserialization errors.

* **Structured Output:** Utilizes with_structured_output across all nodes to guarantee data integrity between generative steps.

* **Decoupled Architecture:** Separates deterministic ingestion logic from probabilistic reasoning nodes, adhering to the Single Responsibility Principle.

* **Production Logging:** Replaces standard print statements with a structured logging configuration for professional system monitoring.

---

## 📜 License

MIT License

---

## 🤝 Contributions

Contributions, issues, and feature requests are welcome!
