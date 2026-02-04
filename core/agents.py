"""
Multi-Agent Debate System

Internal reasoning layer that runs before Jarvis makes final decisions.
Three agents debate each input to provide comprehensive analysis.
"""

import logging
import ollama
from typing import Dict, List, Any, Optional
from datetime import datetime


class Agent:
    """Base class for internal reasoning agents with confidence tracking."""
    
    def __init__(self, name: str, role: str, system_prompt: str, model: str, domain: str = "general"):
        """
        Initialize an agent.
        
        Args:
            name: Agent identifier (e.g., "Analyst")
            role: Brief role description
            system_prompt: Detailed system prompt for this agent
            model: Ollama model to use
            domain: Agent's area of expertise (general, science, finance, etc.)
        """
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.model = model
        self.domain = domain
        self.beliefs = {}  # Store agent opinions with confidence
        self.interaction_count = 0
        self.logger = logging.getLogger(f"jarvis.agent.{name.lower()}")
    
    def think(self, user_input: str, context: Optional[str] = None) -> str:
        """
        Generate agent's response to input.
        
        Args:
            user_input: Original user request
            context: Additional context (previous agent responses)
            
        Returns:
            Agent's analysis/response
        """
        try:
            # Build prompt
            prompt = f"User Request: {user_input}\n"
            if context:
                prompt += f"\nContext:\n{context}\n"
            prompt += f"\nProvide your {self.name.lower()} perspective:"
            
            # Get response from Ollama
            response = ollama.chat(
                model=self.model,
                messages=[
                    {'role': 'system', 'content': self.system_prompt},
                    {'role': 'user', 'content': prompt}
                ],
                options={
                    'temperature': 0.7,
                    'num_predict': 300  # Keep responses concise
                }
            )
            
            result = response['message']['content'].strip()
            self.logger.debug(f"{self.name} response: {result[:100]}...")
            
            # Extract confidence level if present
            confidence = self._extract_confidence(result)
            
            # Store belief/opinion for learning
            self._update_beliefs(user_input, result, confidence)
            
            self.interaction_count += 1
            return result
            
        except Exception as e:
            self.logger.error(f"{self.name} failed: {e}")
            return f"[{self.name} Error: {str(e)}]"
    
    def _extract_confidence(self, response: str) -> float:
        """Extract confidence level from agent response."""
        response_lower = response.lower()
        
        # Check for explicit confidence markers
        if any(x in response_lower for x in ['confidence: high', 'confidence:high', 'high confidence', 'very confident', 'highly confident', 'confidence level: high']):
            return 0.9
        elif any(x in response_lower for x in ['confidence: medium', 'confidence:medium', 'medium confidence', 'moderately confident', 'confidence level: medium']):
            return 0.7
        elif any(x in response_lower for x in ['confidence: low', 'confidence:low', 'low confidence', 'uncertain', 'not confident', 'confidence level: low']):
            return 0.4
        
        # Check for risk indicators that suggest low confidence
        if any(x in response_lower for x in ['unclear', 'ambiguous', 'need more info', 'insufficient', 'vague']):
            return 0.5
        
        # Check for strong language suggesting high confidence
        if any(x in response_lower for x in ['definitely', 'clearly', 'obviously', 'certain', 'absolutely']):
            return 0.85
        
        # Default medium-low if no indicators
        return 0.65
    
    def _update_beliefs(self, topic: str, response: str, confidence: float):
        """Store agent's opinion for future learning."""
        # Simple belief tracking - stores last opinion on topic
        topic_key = topic[:100].lower()  # Truncate for key
        self.beliefs[topic_key] = {
            'response': response[:500],  # Store summary
            'confidence': confidence,
            'timestamp': datetime.now().isoformat(),
            'interaction_count': self.interaction_count
        }
        
        # Keep only recent beliefs (max 50)
        if len(self.beliefs) > 50:
            # Remove oldest belief
            oldest = min(self.beliefs.items(), key=lambda x: x[1]['timestamp'])
            del self.beliefs[oldest[0]]
    
    def get_belief(self, topic: str) -> Optional[Dict]:
        """Retrieve agent's previous opinion on topic."""
        topic_key = topic[:100].lower()
        return self.beliefs.get(topic_key)


class MultiAgentDebate:
    """
    Orchestrates internal multi-agent debate before Jarvis decides.
    
    Flow:
    1. Analyst proposes logical response
    2. Skeptic identifies risks/issues
    3. Architect synthesizes refined solution
    4. Return all perspectives to Jarvis for final decision
    """
    
    def __init__(self, model: str, enabled: bool = True):
        """
        Initialize multi-agent debate system.
        
        Args:
            model: Ollama model to use for all agents
            enabled: Whether debate system is active
        """
        self.model = model
        self.enabled = enabled
        self.logger = logging.getLogger("jarvis.agents")
        
        if not enabled:
            self.logger.info("Multi-agent debate system is DISABLED")
            return
        
        # Initialize three specialized agents
        self.analyst = Agent(
            name="Analyst",
            role="Logical reasoner and action proposer",
            system_prompt="""You are the Analyst agent in Jarvis Omega's internal reasoning system.

Your role:
- Analyze user requests logically and objectively
- Propose clear, actionable responses or commands
- Identify the most likely intent and appropriate action
- Focus on efficiency and direct solutions
- ALWAYS end with your confidence level

Format your response as:
INTENT: [command/conversation/question]
PROPOSED ACTION: [what should be done]
REASONING: [why this is the best approach]
CONFIDENCE: [Low/Medium/High] - REQUIRED

Keep responses concise (3-5 sentences).""",
            model=model
        )
        
        self.skeptic = Agent(
            name="Skeptic",
            role="Risk assessor and critical thinker",
            system_prompt="""You are the Skeptic agent in Jarvis Omega's internal reasoning system.

Your role:
- Challenge the Analyst's proposal constructively
- Identify risks, edge cases, and potential issues
- Point out what could go wrong or be misunderstood
- Suggest safety checks or clarifications needed
- ALWAYS end with your confidence level

Format your response as:
CONCERNS: [specific issues identified]
RISKS: [what could go wrong]
RECOMMENDATIONS: [how to mitigate risks]
CONFIDENCE: [Low/Medium/High] - REQUIRED

Keep responses concise (3-5 sentences). Be critical but constructive.""",
            model=model
        )
        
        self.architect = Agent(
            name="Architect",
            role="Solution synthesizer and decision optimizer",
            system_prompt="""You are the Architect agent in Jarvis Omega's internal reasoning system.

Your role:
- Synthesize insights from both Analyst and Skeptic
- Create a refined, balanced solution
- Incorporate safety measures while maintaining efficiency
- Provide a clear recommendation for Jarvis' final decision
- ALWAYS include confidence level

Format your response as:
SYNTHESIS: [balanced view of the situation]
REFINED SOLUTION: [optimized approach]
CONFIDENCE: [Low/Medium/High] - REQUIRED
RISK LEVEL: [Low/Medium/High] - safety assessment

Keep responses concise (3-5 sentences).""",
            model=model,
            domain="general"
        )
        
        # Domain expert agents (initialized lazily)
        self.expert_agents = {}
        self._init_expert_agents(model)
        
        self.logger.info(f"Multi-agent debate system initialized with model: {model}")
    
    def _init_expert_agents(self, model: str):
        """Initialize domain-specific expert agents."""
        # Science Expert
        self.expert_agents['science'] = Agent(
            name="Science Expert",
            role="Scientific and technical analysis",
            system_prompt="""You are a Science Expert in Jarvis Omega's reasoning system.

Your expertise:
- Scientific facts, research, and methodology
- Technical explanations and accuracy
- Physics, chemistry, biology, astronomy
- Evidence-based reasoning

Provide scientifically accurate insights.
Always cite confidence in your scientific assessment.

Format: Brief scientific analysis (2-3 sentences) with CONFIDENCE: [Low/Medium/High]""",
            model=model,
            domain="science"
        )
        
        # Finance Expert
        self.expert_agents['finance'] = Agent(
            name="Finance Expert",
            role="Financial and economic analysis",
            system_prompt="""You are a Finance Expert in Jarvis Omega's reasoning system.

Your expertise:
- Financial concepts, markets, investments
- Economic principles and trends
- Personal finance and budgeting
- Risk assessment in financial contexts

Provide financially sound insights.
Always cite confidence in your financial assessment.

Format: Brief financial analysis (2-3 sentences) with CONFIDENCE: [Low/Medium/High]""",
            model=model,
            domain="finance"
        )
        
        # Entertainment Expert
        self.expert_agents['entertainment'] = Agent(
            name="Entertainment Expert",
            role="Entertainment and media analysis",
            system_prompt="""You are an Entertainment Expert in Jarvis Omega's reasoning system.

Your expertise:
- Movies, music, TV shows, gaming
- Pop culture and media trends
- Recommendations and reviews
- Creative content and storytelling

Provide entertainment-focused insights.
Always cite confidence in your assessment.

Format: Brief entertainment analysis (2-3 sentences) with CONFIDENCE: [Low/Medium/High]""",
            model=model,
            domain="entertainment"
        )
    
    def _detect_domain(self, user_input: str) -> Optional[str]:
        """Detect if input requires domain expert."""
        user_input_lower = user_input.lower()
        
        # Science keywords
        science_keywords = ['science', 'physics', 'chemistry', 'biology', 'experiment', 
                          'atom', 'molecule', 'energy', 'force', 'space', 'planet',
                          'theory', 'research', 'scientific', 'quantum', 'DNA']
        if any(kw in user_input_lower for kw in science_keywords):
            return 'science'
        
        # Finance keywords
        finance_keywords = ['money', 'stock', 'invest', 'finance', 'budget', 'cost',
                          'price', 'dollar', 'bank', 'credit', 'debt', 'economy',
                          'profit', 'loss', 'market', 'trading', 'crypto']
        if any(kw in user_input_lower for kw in finance_keywords):
            return 'finance'
        
        # Entertainment keywords
        entertainment_keywords = ['movie', 'song', 'music', 'game', 'play', 'watch',
                                'film', 'show', 'series', 'artist', 'album', 'concert',
                                'actor', 'director', 'streaming', 'netflix', 'spotify']
        if any(kw in user_input_lower for kw in entertainment_keywords):
            return 'entertainment'
        
        return None
    
    def debate(self, user_input: str, context: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """
        Run full multi-agent debate on user input.
        
        Args:
            user_input: User's request/command
            context: Recent conversation history
            
        Returns:
            Dictionary containing:
            - analyst_response: Analyst's proposal
            - skeptic_response: Skeptic's critique
            - architect_response: Architect's synthesis
            - timestamp: When debate occurred
            - enabled: Whether debate ran or was skipped
        """
        if not self.enabled:
            return {
                'analyst_response': None,
                'skeptic_response': None,
                'architect_response': None,
                'timestamp': datetime.now().isoformat(),
                'enabled': False
            }
        
        self.logger.info(f"Starting debate on: {user_input[:50]}...")
        start_time = datetime.now()
        
        try:
            # Detect if domain expert needed
            domain = self._detect_domain(user_input)
            expert_response = None
            expert_confidence = 0.7
            
            # Phase 1: Analyst proposes solution
            analyst_response = self.analyst.think(user_input)
            analyst_confidence = self.analyst._extract_confidence(analyst_response)
            
            # Phase 1.5: Domain expert if applicable
            if domain and domain in self.expert_agents:
                expert_agent = self.expert_agents[domain]
                expert_response = expert_agent.think(user_input)
                expert_confidence = expert_agent._extract_confidence(expert_response)
                self.logger.info(f"Domain expert ({domain}) consulted")
            
            # Phase 2: Skeptic critiques
            skeptic_context = f"Analyst's Proposal:\n{analyst_response}"
            if expert_response:
                skeptic_context += f"\n\n{self.expert_agents[domain].name}'s Input:\n{expert_response}"
            skeptic_response = self.skeptic.think(user_input, skeptic_context)
            skeptic_confidence = self.skeptic._extract_confidence(skeptic_response)
            
            # Phase 3: Architect synthesizes
            architect_context = f"Analyst's Proposal:\n{analyst_response}\n\nSkeptic's Concerns:\n{skeptic_response}"
            if expert_response:
                architect_context += f"\n\n{self.expert_agents[domain].name}'s Expertise:\n{expert_response}"
            architect_response = self.architect.think(user_input, architect_context)
            architect_confidence = self.architect._extract_confidence(architect_response)
            
            # Calculate overall confidence
            confidences = [analyst_confidence, skeptic_confidence, architect_confidence]
            if expert_response:
                confidences.append(expert_confidence)
            overall_confidence = sum(confidences) / len(confidences)
            
            duration = (datetime.now() - start_time).total_seconds()
            self.logger.info(f"Debate completed in {duration:.2f}s (confidence: {overall_confidence:.2f})")
            
            return {
                'analyst_response': analyst_response,
                'analyst_confidence': analyst_confidence,
                'skeptic_response': skeptic_response,
                'skeptic_confidence': skeptic_confidence,
                'architect_response': architect_response,
                'architect_confidence': architect_confidence,
                'expert_response': expert_response,
                'expert_confidence': expert_confidence,
                'expert_domain': domain,
                'overall_confidence': overall_confidence,
                'timestamp': start_time.isoformat(),
                'duration_seconds': duration,
                'enabled': True
            }
            
        except Exception as e:
            self.logger.error(f"Debate failed: {e}", exc_info=True)
            return {
                'analyst_response': f"[Error: {str(e)}]",
                'skeptic_response': None,
                'architect_response': None,
                'timestamp': start_time.isoformat(),
                'enabled': True,
                'error': str(e)
            }
    
    def get_summary(self, debate_result: Dict[str, Any]) -> str:
        """
        Create human-readable summary of debate for UI/logging.
        
        Args:
            debate_result: Output from debate()
            
        Returns:
            Formatted summary string
        """
        if not debate_result['enabled']:
            return "[Debate system disabled]"
        
        summary = "=== INTERNAL REASONING ===\n\n"
        
        if debate_result.get('analyst_response'):
            summary += f"📊 ANALYST:\n{debate_result['analyst_response']}\n\n"
        
        if debate_result.get('skeptic_response'):
            summary += f"⚠️ SKEPTIC:\n{debate_result['skeptic_response']}\n\n"
        
        if debate_result.get('architect_response'):
            summary += f"🏗️ ARCHITECT:\n{debate_result['architect_response']}\n\n"
        
        if debate_result.get('duration_seconds'):
            summary += f"⏱️ Duration: {debate_result['duration_seconds']:.2f}s"
        
        return summary
