"""
Web Skills - Web Operations

Handles:
- Web searches
- Opening URLs
- Browser control
"""

import logging
import webbrowser
import urllib.parse
from skills import BaseSkill


class WebSkills(BaseSkill):
    """Web-related skills."""
    
    def can_handle(self, intent: str, entities: dict) -> bool:
        """Check if this skill handles the intent."""
        web_intents = [
            'web_search',
            'open_url',
            'browse'
        ]
        return intent in web_intents
    
    def execute(self, intent: str, entities: dict, raw_text: str = "") -> str:
        """Execute web command."""
        if intent == 'web_search':
            return self._web_search(entities.get('query', ''))
        
        elif intent == 'open_url':
            return self._open_url(entities.get('url', ''))
        
        else:
            return f"Unknown web intent: {intent}"
    
    def _web_search(self, query: str) -> str:
        """Perform web search."""
        if not query:
            return "Please specify what to search for."
        
        try:
            # URL encode query
            encoded_query = urllib.parse.quote(query)
            
            # Construct Google search URL
            search_url = f"https://www.google.com/search?q={encoded_query}"
            
            # Open in default browser
            webbrowser.open(search_url)
            
            self.logger.info(f"Web search: {query}")
            return f"Searching for {query}."
            
        except Exception as e:
            self.logger.error(f"Web search failed: {e}")
            return f"I couldn't perform the search: {str(e)}"
    
    def _open_url(self, url: str) -> str:
        """Open URL in browser."""
        if not url:
            return "Please specify a URL to open."
        
        try:
            # Add protocol if missing
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            # Open in default browser
            webbrowser.open(url)
            
            self.logger.info(f"Opened URL: {url}")
            return f"Opening {url}."
            
        except Exception as e:
            self.logger.error(f"Failed to open URL: {e}")
            return f"I couldn't open that URL: {str(e)}"
