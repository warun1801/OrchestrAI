Perfect! Then let’s update your README to use **OrchestrAI** instead of AgentForge and tweak a few places so it reads naturally. Here’s the polished version:

---

````markdown
# OrchestrAI 🎯

**Multi-Agent AI for Code Analysis, Task Planning, and Execution**

OrchestrAI is a **multi-agent AI system** designed to intelligently analyze code repositories, plan actionable development tasks, and produce structured outputs. It leverages multiple specialized agents that collaborate autonomously:

- **Retriever Agent** – Fetches relevant code context from repositories.  
- **Planner Agent** – Breaks down user queries into detailed, structured plans.  
- **Worker Agent** – Executes plans and produces actionable tasks with validation and self-correction.  
- **Referee Agent** – Reviews and critiques Worker Agent outputs to ensure correctness and completeness.  

This system is ideal for building **autonomous code assistants**, refactoring tools, or code intelligence dashboards.

---

## Features

- **Multi-Agent Architecture**: Each agent has a defined role, memory, and reasoning capabilities.  
- **Dynamic Retrieval**: Planner and Worker agents can request additional code context on demand.  
- **Self-Correcting Loops**: Worker Agent retries outputs until valid JSON is produced.  
- **Referee Validation**: Ensures tasks are accurate, structured, and actionable.  
- **Incremental Ingestion**: Embed repository code incrementally into a vectorstore for efficient retrieval.  
- **Extensible**: Add specialized agents for security auditing, testing, documentation, or deployment.  
- **Persistent Storage**: Vectorstore supports on-disk storage for long-term memory.

---

## Architecture

```mermaid
flowchart TD
    A[User Query] --> B[Ingest Repo]
    B --> C[Retriever Agent]
    C --> D[Planner Agent]
    D --> E[Worker Agent]
    E --> F[Referee Agent]
    F --> G[Final Output: JSON Tasks]

    D -->|dynamic retrieval| C
    E -->|self-correct| E
    F -->|revision requests| E
````

---

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/OrchestrAI.git
cd OrchestrAI
```

2. **Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set OpenAI API key**

```bash
export OPENAI_API_KEY="your_key_here"  # Linux/Mac
setx OPENAI_API_KEY "your_key_here"    # Windows
```

---

## Usage

1. **Ingest a repository**

```python
from app.agent.nodes.ingest import ingest
state = ingest(repo_url="https://github.com/user/repo.git")
```

2. **Run the multi-agent workflow**

```python
from app.agent.graph_multi_agent import workflow
from app.agent.state import AgentState

state = AgentState(query="Refactor API endpoints for consistency", repo_url="https://github.com/user/repo.git")
final_state = workflow.run(state)
print(final_state.tasks)  # JSON structured tasks
```

---

## Vectorstore

OrchestrAI uses **Chroma + OpenAI embeddings** for semantic code retrieval.

```python
from app.services.vectorstore import add_embeddings, retrieve_embeddings, persist

# Add code chunks
add_embeddings(chunks, metadatas, ids)

# Retrieve relevant code
results = retrieve_embeddings(query="Refactor API endpoints", repo_url="repo_url")

# Persist to disk
persist()
```

---

## Extending OrchestrAI

You can easily add:

* **Security Auditor Agent** – Analyze code for vulnerabilities.
* **Test Agent** – Generate or run unit tests automatically.
* **Documentation Agent** – Produce README or API docs.
* **Deployment Agent** – Automate CI/CD tasks.

Agents can run **asynchronously**, call **external tools**, or maintain **memory for long-term reasoning**.

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a pull request

---

## License

MIT License © [Your Name]

---

## Acknowledgments

* [LangChain](https://www.langchain.com/) – For agent orchestration and LLM integrations
* [OpenAI](https://openai.com/) – For embeddings and language models
* [Chroma](https://www.trychroma.com/) – Vectorstore for code embeddings

---
```
