import os
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StreamableHTTPConnectionParams
from ..prompts.analyzer_prompt import ANALYZER_AGENT_INSTRUCTION, ANALYZER_AGENT_DESCRIPTION
from google.genai import types

load_dotenv()

# os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Analyzer Agent Definition
analyzer_agent = LlmAgent(
    name="AnalyzerAgent",
    model=LiteLlm(model="openai/gpt-4.1"),
    tools=[
        MCPToolset(
            connection_params=StreamableHTTPConnectionParams(
                url="http://localhost:8000/mcp"
            ),
            tool_filter=['get_past_locations', 'get_past_activities']
        )
    ],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.0,
    ),
    instruction=ANALYZER_AGENT_INSTRUCTION,
    description=ANALYZER_AGENT_DESCRIPTION,
)
