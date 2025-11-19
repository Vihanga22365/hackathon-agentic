import os
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StreamableHTTPConnectionParams
from ...prompts.orchestrator_prompt import ORCHESTRATOR_AGENT_INSTRUCTION, ORCHESTRATOR_AGENT_DESCRIPTION
from ..analyzer_agent import analyzer_agent
from ..recommender_agent import recommender_agent
from .input_handler import InputHandler, process_user_input
from .agent_dispatcher import AgentDispatcher, dispatch_request, AgentType
from google.genai import types

load_dotenv()

# os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Initialize input handler and dispatcher
input_handler = InputHandler()
agent_dispatcher = AgentDispatcher()

# Orchestrator Agent Definition
root_agent = LlmAgent(
    name="OrchestratorAgent",
    model=LiteLlm(model="openai/gpt-4.1"),
    generate_content_config=types.GenerateContentConfig(
        temperature=0.0,
    ),
    tools=[
        MCPToolset(
            connection_params=StreamableHTTPConnectionParams(
                url="http://localhost:8000/mcp"
            ),
            tool_filter=['get_nearby_location_activities', 'get_weather', 'validate_future_date']
        )
    ],
    instruction=ORCHESTRATOR_AGENT_INSTRUCTION,
    description=ORCHESTRATOR_AGENT_DESCRIPTION,
    sub_agents=[
        analyzer_agent,
        recommender_agent
    ],
)


def process_request(user_input):
    """
    Process user request through input handler and dispatcher before routing to agents.
    
    Args:
        user_input: Raw user input (string or dict)
        
    Returns:
        Tuple of (processed_input, routing_info)
    """
    # Process and validate input
    processed = process_user_input(user_input)
    
    if processed is None:
        raise ValueError("Invalid input: could not process user request")
    
    # Extract intent and location if not already present
    if 'intent' not in processed:
        processed['intent'] = input_handler.extract_intent(processed['query'])
    
    if 'location' not in processed:
        processed['location'] = input_handler.extract_location(processed['query'])
    
    # Route to appropriate agent
    routing_info = dispatch_request(processed)
    
    return processed, routing_info


def execute_with_routing(user_input):
    """
    Execute user request with intelligent routing.
    
    Args:
        user_input: Raw user input
        
    Returns:
        Response from the appropriate agent
    """
    processed, routing_info = process_request(user_input)
    
    # Log routing decision
    print(f"Routing to: {routing_info['target_agent']}")
    print(f"Intent: {routing_info['intent']}")
    print(f"Confidence: {routing_info['confidence']}")
    
    # Execute with root agent (which manages sub-agents)
    # The orchestrator will use the routing info to optimize delegation
    response = root_agent.run(processed['query'])
    
    return response
