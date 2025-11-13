# This file is kept for backward compatibility
# All prompt definitions have been moved to separate files:
# - orchestrator_prompt.py
# - analyzer_prompt.py
# - recommender_prompt.py

from .orchestrator_prompt import (
    ORCHESTRATOR_AGENT_INSTRUCTION,
    ORCHESTRATOR_AGENT_DESCRIPTION
)
from .analyzer_prompt import (
    ANALYZER_AGENT_INSTRUCTION,
    ANALYZER_AGENT_DESCRIPTION
)
from .recommender_prompt import (
    RECCOMMENDER_AGENT_INSTRUCTION,
    RECCOMMENDER_AGENT_DESCRIPTION
)

__all__ = [
    'ORCHESTRATOR_AGENT_INSTRUCTION',
    'ORCHESTRATOR_AGENT_DESCRIPTION',
    'ANALYZER_AGENT_INSTRUCTION',
    'ANALYZER_AGENT_DESCRIPTION',
    'RECCOMMENDER_AGENT_INSTRUCTION',
    'RECCOMMENDER_AGENT_DESCRIPTION'
]
