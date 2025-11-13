from .entrypoint import root_agent, analyzer_agent, recommender_agent
from .agents import analyzer_agent as agents_analyzer, recommender_agent as agents_recommender, root_agent as agents_root
from .prompts import (
    ORCHESTRATOR_AGENT_INSTRUCTION,
    ORCHESTRATOR_AGENT_DESCRIPTION,
    ANALYZER_AGENT_INSTRUCTION,
    ANALYZER_AGENT_DESCRIPTION,
    RECCOMMENDER_AGENT_INSTRUCTION,
    RECCOMMENDER_AGENT_DESCRIPTION
)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

__all__ = [
    'root_agent',
    'analyzer_agent',
    'recommender_agent',
    'app',
    'ORCHESTRATOR_AGENT_INSTRUCTION',
    'ORCHESTRATOR_AGENT_DESCRIPTION',
    'ANALYZER_AGENT_INSTRUCTION',
    'ANALYZER_AGENT_DESCRIPTION',
    'RECCOMMENDER_AGENT_INSTRUCTION',
    'RECCOMMENDER_AGENT_DESCRIPTION'
]
