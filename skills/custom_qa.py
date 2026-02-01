"""
Custom Q&A Skill

Checks user-defined question/answer database before other skills.
Allows users to add their own custom responses to specific questions.
"""

import yaml
import logging
import sys
import os
from pathlib import Path
from typing import Optional, Dict, Any
from skills import BaseSkill


def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class CustomQASkill(BaseSkill):
    """
    Custom Question & Answer skill.
    
    Checks custom_qa.yaml for matching questions and returns predefined answers.
    This skill runs with HIGHEST PRIORITY to override default responses.
    """
    
    def __init__(self, config: dict):
        super().__init__(config)
        self.logger = logging.getLogger("jarvis.skills.custom_qa")
        self.qa_pairs = self._load_qa_pairs()
        self.logger.info(f"Loaded {len(self.qa_pairs)} custom Q&A pairs")
    
    def _load_qa_pairs(self) -> list:
        """Load Q&A pairs from custom_qa.yaml."""
        try:
            qa_file = get_resource_path("custom_qa.yaml")
            
            if not os.path.exists(qa_file):
                # Fallback to current directory
                qa_file = "custom_qa.yaml"
                if not os.path.exists(qa_file):
                    self.logger.warning("custom_qa.yaml not found")
                    return []
            
            with open(qa_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                
            if not data or 'qa_pairs' not in data:
                self.logger.warning("No qa_pairs found in custom_qa.yaml")
                return []
            
            qa_pairs = data['qa_pairs']
            self.logger.info(f"Loaded {len(qa_pairs)} Q&A pairs")
            
            return qa_pairs
            
        except Exception as e:
            self.logger.error(f"Error loading custom_qa.yaml: {e}", exc_info=True)
            return []
    
    def _calculate_match_score(self, user_text: str, qa_pair: dict) -> float:
        """
        Calculate how well user text matches a Q&A pair.
        
        Args:
            user_text: User's input text (lowercase)
            qa_pair: Q&A pair dictionary
            
        Returns:
            Match score (0.0 to 1.0)
        """
        score = 0.0
        question = qa_pair['question'].lower()
        
        # Exact match = perfect score
        if user_text == question:
            return 1.0
        
        # Check if question is contained in user text or vice versa
        if question in user_text:
            score += 0.7
        elif user_text in question:
            score += 0.6
        
        # Check keywords if provided
        if 'keywords' in qa_pair and qa_pair['keywords']:
            keywords = [kw.lower() for kw in qa_pair['keywords']]
            matched_keywords = sum(1 for kw in keywords if kw in user_text)
            
            if matched_keywords > 0:
                keyword_score = matched_keywords / len(keywords)
                score += keyword_score * 0.5
        
        # Check individual word matches in question
        question_words = set(question.split())
        user_words = set(user_text.split())
        common_words = question_words & user_words
        
        if len(question_words) > 0:
            word_match_score = len(common_words) / len(question_words)
            score += word_match_score * 0.3
        
        return min(score, 1.0)
    
    def can_handle(self, intent: str, entities: dict) -> bool:
        """
        Check if user input matches any Q&A pair.
        
        This skill uses the raw text, not the intent classification.
        
        Args:
            intent: Detected intent (not used here)
            entities: Detected entities (contains 'raw_text')
            
        Returns:
            True if a good match is found
        """
        if not entities.get('raw_text'):
            return False
        
        user_text = entities['raw_text'].lower().strip()
        
        # Find best match
        best_score = 0.0
        for qa_pair in self.qa_pairs:
            score = self._calculate_match_score(user_text, qa_pair)
            if score > best_score:
                best_score = score
        
        # Require at least 50% match confidence
        threshold = 0.5
        match_found = best_score >= threshold
        
        if match_found:
            self.logger.debug(f"Match found with score {best_score:.2f}")
        
        return match_found
    
    def execute(self, intent: str, entities: dict, raw_text: str = "") -> str:
        """
        Return the answer for the matched question.
        
        Args:
            intent: Detected intent
            entities: Detected entities (contains 'raw_text')
            raw_text: Original user input (from BaseSkill signature)
            
        Returns:
            Predefined answer
        """
        if not entities.get('raw_text'):
            return "I didn't catch that, sir."
        
        user_text = entities['raw_text'].lower().strip()
        
        # Find best match
        best_match = None
        best_score = 0.0
        
        for qa_pair in self.qa_pairs:
            score = self._calculate_match_score(user_text, qa_pair)
            if score > best_score:
                best_score = score
                best_match = qa_pair
        
        if best_match:
            self.logger.info(f"Matched Q&A: '{best_match['question']}' (score: {best_score:.2f})")
            return best_match['answer']
        
        return "I don't have an answer for that in my database, sir."
