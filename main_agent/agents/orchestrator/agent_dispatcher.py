"""
Agent Dispatcher Module
Routes user requests to appropriate agents based on intent and context.
"""

from typing import Dict, Any, Optional, List
from enum import Enum


class AgentType(Enum):
    """Enumeration of available agent types."""
    ORCHESTRATOR = "orchestrator"
    ANALYZER = "analyzer"
    RECOMMENDER = "recommender"


class AgentDispatcher:
    """Dispatches user requests to appropriate agents based on intent."""
    
    def __init__(self):
        self.agent_capabilities = {
            AgentType.ANALYZER: [
                'weather',
                'analysis',
                'data_processing',
                'information_gathering'
            ],
            AgentType.RECOMMENDER: [
                'recommendation',
                'activities',
                'suggestions',
                'planning'
            ],
            AgentType.ORCHESTRATOR: [
                'general',
                'complex',
                'multi_step',
                'coordination'
            ]
        }
        
        self.routing_rules = {}
        self._initialize_routing_rules()
    
    def _initialize_routing_rules(self):
        """Initialize routing rules for request dispatching."""
        self.routing_rules = {
            'weather': AgentType.ANALYZER,
            'activities': AgentType.RECOMMENDER,
            'recommendation': AgentType.RECOMMENDER,
            'analysis': AgentType.ANALYZER,
            'general': AgentType.ORCHESTRATOR,
        }
    
    def determine_agent(self, intent: str, context: Optional[Dict[str, Any]] = None) -> AgentType:
        """
        Determine which agent should handle the request.
        
        Args:
            intent: User intent extracted from query
            context: Additional context information
            
        Returns:
            AgentType to handle the request
        """
        # Check routing rules first
        if intent in self.routing_rules:
            return self.routing_rules[intent]
        
        # Check if context suggests a specific agent
        if context:
            if 'requires_analysis' in context and context['requires_analysis']:
                return AgentType.ANALYZER
            if 'requires_recommendation' in context and context['requires_recommendation']:
                return AgentType.RECOMMENDER
        
        # Default to orchestrator for complex/unknown requests
        return AgentType.ORCHESTRATOR
    
    def can_handle(self, agent_type: AgentType, task: str) -> bool:
        """
        Check if a specific agent can handle a task.
        
        Args:
            agent_type: Type of agent to check
            task: Task description or category
            
        Returns:
            bool: True if agent can handle the task
        """
        if agent_type not in self.agent_capabilities:
            return False
        
        task_lower = task.lower()
        capabilities = self.agent_capabilities[agent_type]
        
        return any(capability in task_lower for capability in capabilities)
    
    def route_request(self, processed_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Route a processed request to the appropriate agent.
        
        Args:
            processed_input: Processed user input with query and metadata
            
        Returns:
            Dictionary with routing information
        """
        intent = processed_input.get('intent', 'general')
        context = processed_input.get('context', {})
        query = processed_input.get('query', '')
        
        # Determine target agent
        target_agent = self.determine_agent(intent, context)
        
        # Build routing info
        routing_info = {
            'target_agent': target_agent.value,
            'intent': intent,
            'query': query,
            'context': context,
            'confidence': self._calculate_confidence(intent, target_agent),
            'fallback_agent': AgentType.ORCHESTRATOR.value
        }
        
        return routing_info
    
    def _calculate_confidence(self, intent: str, agent_type: AgentType) -> float:
        """
        Calculate confidence score for agent selection.
        
        Args:
            intent: Detected intent
            agent_type: Selected agent type
            
        Returns:
            Confidence score between 0 and 1
        """
        # High confidence if intent matches routing rules exactly
        if intent in self.routing_rules and self.routing_rules[intent] == agent_type:
            return 0.95
        
        # Medium confidence if agent can handle the task
        if self.can_handle(agent_type, intent):
            return 0.75
        
        # Lower confidence for default orchestrator routing
        if agent_type == AgentType.ORCHESTRATOR:
            return 0.60
        
        return 0.50
    
    def get_agent_chain(self, intent: str) -> List[AgentType]:
        """
        Get the chain of agents that should process a request.
        
        Args:
            intent: User intent
            
        Returns:
            List of AgentTypes in processing order
        """
        # For complex requests, might need multiple agents
        if intent in ['recommendation', 'activities']:
            # Analyzer first for data, then recommender for suggestions
            return [AgentType.ANALYZER, AgentType.RECOMMENDER]
        
        # Single agent for simple requests
        return [self.determine_agent(intent)]
    
    def add_routing_rule(self, intent: str, agent_type: AgentType):
        """
        Add or update a routing rule.
        
        Args:
            intent: Intent category
            agent_type: Agent to route this intent to
        """
        self.routing_rules[intent] = agent_type
    
    def get_available_agents(self) -> List[str]:
        """
        Get list of available agent types.
        
        Returns:
            List of agent type names
        """
        return [agent.value for agent in AgentType]


# Create singleton instance
agent_dispatcher = AgentDispatcher()


def dispatch_request(processed_input: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience function to dispatch requests using the singleton dispatcher.
    
    Args:
        processed_input: Processed user input
        
    Returns:
        Routing information dictionary
    """
    return agent_dispatcher.route_request(processed_input)
