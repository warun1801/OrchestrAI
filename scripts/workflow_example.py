import sys
from pathlib import Path

# Add project root to sys.path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from app.agent.graph_multi_agent import workflow
from app.agent.state import AgentState


# Initialize state
state = AgentState(
    query="What does this do and how can we improve documentation?",
    repo_url="https://github.com/warun1801/OrchestrAI.git"
)

# Run multi-agent workflow
final_state = workflow.invoke(state)

# Print structured JSON tasks
print("Final Tasks Output:")
print(final_state.tasks)
