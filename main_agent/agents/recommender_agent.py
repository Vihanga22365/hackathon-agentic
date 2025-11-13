import os
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv
from ..prompts.recommender_prompt import RECCOMMENDER_AGENT_INSTRUCTION, RECCOMMENDER_AGENT_DESCRIPTION

load_dotenv()

# os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Recommender Agent Definition
recommender_agent = LlmAgent(
    name="ReccommenderAgent",
    model=LiteLlm(model="openai/gpt-4.1"),
    instruction=RECCOMMENDER_AGENT_INSTRUCTION,
    description=RECCOMMENDER_AGENT_DESCRIPTION,
    tools=[]
)
