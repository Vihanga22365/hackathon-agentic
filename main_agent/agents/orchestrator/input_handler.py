"""
Input Handler Module
Processes and validates user inputs for the orchestrator agent.
"""

from typing import Dict, Any, Optional
import re


class InputHandler:
    """Handles user input validation and preprocessing for the agent system."""
    
    def __init__(self):
        self.required_fields = ['query', 'user_id']
        
    def validate_input(self, user_input: Dict[str, Any]) -> bool:
        """
        Validate user input structure and required fields.
        
        Args:
            user_input: Dictionary containing user request data
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not isinstance(user_input, dict):
            return False
            
        # Check for required fields
        for field in self.required_fields:
            if field not in user_input or not user_input[field]:
                return False
                
        return True
    
    def sanitize_query(self, query: str) -> str:
        """
        Sanitize user query to prevent injection attacks.
        
        Args:
            query: Raw user query string
            
        Returns:
            str: Sanitized query
        """
        if not isinstance(query, str):
            return ""
            
        # Remove excessive whitespace
        query = re.sub(r'\s+', ' ', query.strip())
        
        # Basic sanitization - remove potentially harmful characters
        # Adjust based on your security requirements
        query = re.sub(r'[<>]', '', query)
        
        return query
    
    def parse_user_request(self, raw_input: str) -> Dict[str, Any]:
        """
        Parse raw user input into structured format.
        
        Args:
            raw_input: Raw string input from user
            
        Returns:
            Dict containing parsed input data
        """
        # Default structure
        parsed = {
            'query': '',
            'user_id': 'default_user',
            'context': {},
            'preferences': {}
        }
        
        # Sanitize the query
        parsed['query'] = self.sanitize_query(raw_input)
        
        return parsed
    
    def process_input(self, user_input: Any) -> Optional[Dict[str, Any]]:
        """
        Main entry point for processing user input.
        
        Args:
            user_input: Can be string or dict
            
        Returns:
            Processed input dict or None if invalid
        """
        # Handle string input
        if isinstance(user_input, str):
            processed = self.parse_user_request(user_input)
        # Handle dict input
        elif isinstance(user_input, dict):
            processed = user_input.copy()
            if 'query' in processed:
                processed['query'] = self.sanitize_query(processed['query'])
        else:
            return None
        
        # Validate processed input
        if not self.validate_input(processed):
            return None
            
        return processed
    
    def extract_location(self, query: str) -> Optional[str]:
        """
        Extract location information from query if present.
        
        Args:
            query: User query string
            
        Returns:
            Extracted location or None
        """
        # Simple pattern matching for locations
        # Can be enhanced with NER or more sophisticated methods
        location_patterns = [
            r'in ([A-Z][a-zA-Z\s]+)',
            r'at ([A-Z][a-zA-Z\s]+)',
            r'near ([A-Z][a-zA-Z\s]+)',
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, query)
            if match:
                return match.group(1).strip()
        
        return None
    
    def extract_intent(self, query: str) -> str:
        """
        Extract user intent from query.
        
        Args:
            query: User query string
            
        Returns:
            Detected intent category
        """
        query_lower = query.lower()
        
        # Weather-related keywords
        if any(word in query_lower for word in ['weather', 'temperature', 'forecast', 'rain', 'sunny']):
            return 'weather'
        
        # Activity-related keywords
        if any(word in query_lower for word in ['activity', 'activities', 'things to do', 'places', 'visit']):
            return 'activities'
        
        # Recommendation-related keywords
        if any(word in query_lower for word in ['recommend', 'suggest', 'best', 'top']):
            return 'recommendation'
        
        return 'general'


# Create a singleton instance
input_handler = InputHandler()


def process_user_input(user_input: Any) -> Optional[Dict[str, Any]]:
    """
    Convenience function to process user input using the singleton handler.
    
    Args:
        user_input: Raw user input (string or dict)
        
    Returns:
        Processed input dict or None if invalid
    """
    return input_handler.process_input(user_input)
