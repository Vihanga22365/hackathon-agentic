# This file is kept for backward compatibility
# All agent definitions have been moved to agents/agents.py
from .agents import analyzer_agent, recommender_agent, root_agent

__all__ = ['analyzer_agent', 'recommender_agent', 'root_agent']