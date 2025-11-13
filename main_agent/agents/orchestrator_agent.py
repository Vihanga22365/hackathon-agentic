import os
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StreamableHTTPConnectionParams
from ..prompts.orchestrator_prompt import ORCHESTRATOR_AGENT_INSTRUCTION, ORCHESTRATOR_AGENT_DESCRIPTION
from .analyzer_agent import analyzer_agent
from .recommender_agent import recommender_agent

load_dotenv()

# os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Orchestrator Agent Definition
root_agent = LlmAgent(
    name="OrchestratorAgent",
    model=LiteLlm(model="openai/gpt-4.1"),
    tools=[
        MCPToolset(
            connection_params=StreamableHTTPConnectionParams(
                url="http://localhost:8000/mcp"
            ),
            tool_filter=['get_nearby_location_activities', 'get_weather']
        )
    ],
    instruction=ORCHESTRATOR_AGENT_INSTRUCTION,
    description=ORCHESTRATOR_AGENT_DESCRIPTION,
    sub_agents=[
        analyzer_agent,
        recommender_agent
    ],
)
