"""
Memory System Module

Handles persistent storage of conversations, preferences, and context using SQLite.
"""

import logging
import sqlite3
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path


class MemorySystem:
    """
    Persistent memory storage for Jarvis.
    
    Stores:
    - Conversation history
    - User preferences
    - Command statistics
    - Context for LLM
    """
    
    def __init__(self, config: dict):
        """
        Initialize memory system.
        
        Args:
            config: Memory configuration from config.yaml
        """
        self.config = config
        self.logger = logging.getLogger("jarvis.memory")
        
        # Database path
        db_path = Path(config['database'])
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.db_path = str(db_path)
        
        # Initialize database
        self._init_database()
        
        self.logger.info(f"Memory system initialized: {self.db_path}")
    
    def _init_database(self):
        """Create database tables if they don't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Conversations table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    user_input TEXT NOT NULL,
                    response TEXT NOT NULL,
                    intent TEXT,
                    success BOOLEAN,
                    metadata TEXT
                )
            """)
            
            # Preferences table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS preferences (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            
            # Statistics table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS statistics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT NOT NULL,
                    event_data TEXT,
                    timestamp TEXT NOT NULL
                )
            """)
            
            # User context and learning table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_context (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    context_type TEXT NOT NULL,
                    context_key TEXT NOT NULL,
                    context_value TEXT NOT NULL,
                    frequency INTEGER DEFAULT 1,
                    last_used TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    UNIQUE(context_type, context_key)
                )
            """)
            
            # Agent debates table - stores internal multi-agent reasoning
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS agent_debates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    interaction_id INTEGER,
                    timestamp TEXT NOT NULL,
                    user_input TEXT NOT NULL,
                    analyst_response TEXT,
                    analyst_confidence REAL,
                    skeptic_response TEXT,
                    skeptic_confidence REAL,
                    architect_response TEXT,
                    architect_confidence REAL,
                    expert_response TEXT,
                    expert_confidence REAL,
                    expert_domain TEXT,
                    overall_confidence REAL,
                    jarvis_decision TEXT,
                    duration_seconds REAL,
                    debate_metadata TEXT,
                    FOREIGN KEY (interaction_id) REFERENCES conversations(id)
                )
            """)
            
            # Agent beliefs table - tracks agent opinions over time
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS agent_beliefs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_name TEXT NOT NULL,
                    topic_key TEXT NOT NULL,
                    opinion TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    interaction_count INTEGER,
                    timestamp TEXT NOT NULL,
                    UNIQUE(agent_name, topic_key)
                )
            """)
            
            # Migrate existing agent_debates table to add new columns
            # Check if columns exist, add them if they don't
            cursor.execute("PRAGMA table_info(agent_debates)")
            columns = [col[1] for col in cursor.fetchall()]
            
            if 'analyst_confidence' not in columns:
                self.logger.info("Migrating agent_debates table - adding confidence columns")
                cursor.execute("ALTER TABLE agent_debates ADD COLUMN analyst_confidence REAL")
                cursor.execute("ALTER TABLE agent_debates ADD COLUMN skeptic_confidence REAL")
                cursor.execute("ALTER TABLE agent_debates ADD COLUMN architect_confidence REAL")
                cursor.execute("ALTER TABLE agent_debates ADD COLUMN expert_response TEXT")
                cursor.execute("ALTER TABLE agent_debates ADD COLUMN expert_confidence REAL")
                cursor.execute("ALTER TABLE agent_debates ADD COLUMN expert_domain TEXT")
                cursor.execute("ALTER TABLE agent_debates ADD COLUMN overall_confidence REAL")
                self.logger.info("Migration complete - confidence tracking enabled")
            
            conn.commit()
            self.logger.debug("Database schema initialized")
    
    def store_interaction(
        self,
        user_input: str,
        response: str,
        intent: str = None,
        success: bool = True,
        metadata: Dict = None
    ) -> Optional[int]:
        """
        Store a conversation interaction.
        
        Args:
            user_input: User's input text
            response: Jarvis's response
            intent: Classified intent
            success: Whether the interaction was successful
            metadata: Additional metadata (optional)
            
        Returns:
            ID of inserted interaction, or None if failed
        """
        try:
            import json
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO conversations 
                    (timestamp, user_input, response, intent, success, metadata)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    datetime.now().isoformat(),
                    user_input,
                    response,
                    intent,
                    success,
                    json.dumps(metadata) if metadata else None
                ))
                interaction_id = cursor.lastrowid
                conn.commit()
            
            # Cleanup old conversations if limit exceeded
            self._cleanup_old_conversations()
            
            return interaction_id
            
        except Exception as e:
            self.logger.error(f"Failed to store interaction: {e}")
            return None
    
    def get_recent_context(self, limit: int = 5) -> List[Dict[str, str]]:
        """
        Get recent conversation context for LLM.
        
        Args:
            limit: Number of recent interactions to retrieve
            
        Returns:
            List of recent interactions
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT user_input, response, intent
                    FROM conversations
                    ORDER BY id DESC
                    LIMIT ?
                """, (limit,))
                
                rows = cursor.fetchall()
                
                # Reverse to chronological order
                return [
                    {
                        'input': row[0],
                        'response': row[1],
                        'intent': row[2]
                    }
                    for row in reversed(rows)
                ]
        except Exception as e:
            self.logger.error(f"Failed to retrieve context: {e}")
            return []
    
    def _cleanup_old_conversations(self):
        """Remove old conversations beyond retention limit."""
        retention = self.config['retention']['conversations']
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Count total conversations
                cursor.execute("SELECT COUNT(*) FROM conversations")
                total = cursor.fetchone()[0]
                
                if total > retention:
                    # Delete oldest entries
                    to_delete = total - retention
                    cursor.execute("""
                        DELETE FROM conversations
                        WHERE id IN (
                            SELECT id FROM conversations
                            ORDER BY id ASC
                            LIMIT ?
                        )
                    """, (to_delete,))
                    conn.commit()
                    self.logger.debug(f"Cleaned up {to_delete} old conversations")
        except Exception as e:
            self.logger.error(f"Failed to cleanup conversations: {e}")
    
    def set_preference(self, key: str, value: str):
        """
        Store a user preference.
        
        Args:
            key: Preference key
            value: Preference value
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO preferences (key, value, updated_at)
                    VALUES (?, ?, ?)
                """, (key, value, datetime.now().isoformat()))
                conn.commit()
        except Exception as e:
            self.logger.error(f"Failed to set preference: {e}")
    
    def get_preference(self, key: str, default: Any = None) -> Optional[str]:
        """
        Retrieve a user preference.
        
        Args:
            key: Preference key
            default: Default value if not found
            
        Returns:
            Preference value or default
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT value FROM preferences WHERE key = ?", (key,))
                row = cursor.fetchone()
                return row[0] if row else default
        except Exception as e:
            self.logger.error(f"Failed to get preference: {e}")
            return default
    
    def log_statistic(self, event_type: str, event_data: Dict = None):
        """
        Log a statistical event.
        
        Args:
            event_type: Type of event (e.g., 'command_executed', 'error')
            event_data: Additional event data
        """
        try:
            import json
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO statistics (event_type, event_data, timestamp)
                    VALUES (?, ?, ?)
                """, (
                    event_type,
                    json.dumps(event_data) if event_data else None,
                    datetime.now().isoformat()
                ))
                conn.commit()
        except Exception as e:
            self.logger.error(f"Failed to log statistic: {e}")
    
    def get_statistics(self, event_type: str = None, limit: int = 100) -> List[Dict]:
        """
        Retrieve statistics.
        
        Args:
            event_type: Filter by event type (optional)
            limit: Maximum number of records
            
        Returns:
            List of statistics records
        """
        try:
            import json
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                if event_type:
                    cursor.execute("""
                        SELECT event_type, event_data, timestamp
                        FROM statistics
                        WHERE event_type = ?
                        ORDER BY id DESC
                        LIMIT ?
                    """, (event_type, limit))
                else:
                    cursor.execute("""
                        SELECT event_type, event_data, timestamp
                        FROM statistics
                        ORDER BY id DESC
                        LIMIT ?
                    """, (limit,))
                
                rows = cursor.fetchall()
                
                return [
                    {
                        'type': row[0],
                        'data': json.loads(row[1]) if row[1] else None,
                        'timestamp': row[2]
                    }
                    for row in rows
                ]
        except Exception as e:
            self.logger.error(f"Failed to get statistics: {e}")
            return []
    
    def close(self):
        """Close database connection."""
        self.logger.info("Memory system closed")
    
    # Context-aware learning methods
    
    def learn_preference(self, context_type: str, key: str, value: str):
        """
        Learn user preferences from interactions.
        
        Args:
            context_type: Type of context (e.g., 'favorite_app', 'common_search')
            key: Context key (e.g., 'browser', 'news_category')
            value: Context value
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if context exists
                cursor.execute("""
                    SELECT frequency FROM user_context
                    WHERE context_type = ? AND context_key = ?
                """, (context_type, key))
                
                row = cursor.fetchone()
                
                if row:
                    # Update frequency and last used
                    cursor.execute("""
                        UPDATE user_context
                        SET context_value = ?,
                            frequency = frequency + 1,
                            last_used = ?
                        WHERE context_type = ? AND context_key = ?
                    """, (value, datetime.now().isoformat(), context_type, key))
                else:
                    # Insert new context
                    now = datetime.now().isoformat()
                    cursor.execute("""
                        INSERT INTO user_context
                        (context_type, context_key, context_value, frequency, last_used, created_at)
                        VALUES (?, ?, ?, 1, ?, ?)
                    """, (context_type, key, value, now, now))
                
                conn.commit()
        except Exception as e:
            self.logger.error(f"Failed to learn preference: {e}")
    
    def get_learned_preference(self, context_type: str, key: str) -> Optional[str]:
        """
        Get learned user preference.
        
        Args:
            context_type: Type of context
            key: Context key
            
        Returns:
            Most frequently used value or None
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT context_value, frequency
                    FROM user_context
                    WHERE context_type = ? AND context_key = ?
                    ORDER BY frequency DESC, last_used DESC
                    LIMIT 1
                """, (context_type, key))
                
                row = cursor.fetchone()
                return row[0] if row else None
        except Exception as e:
            self.logger.error(f"Failed to get learned preference: {e}")
            return None
    
    def get_frequent_commands(self, limit: int = 10) -> List[Dict]:
        """
        Get most frequently used commands.
        
        Args:
            limit: Number of commands to return
            
        Returns:
            List of frequent commands with usage counts
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT intent, COUNT(*) as count
                    FROM conversations
                    WHERE intent IS NOT NULL
                    GROUP BY intent
                    ORDER BY count DESC
                    LIMIT ?
                """, (limit,))
                
                return [{'intent': row[0], 'count': row[1]} for row in cursor.fetchall()]
        except Exception as e:
            self.logger.error(f"Failed to get frequent commands: {e}")
            return []
    
    def get_contextual_suggestions(self, current_context: str) -> List[str]:
        """
        Get contextual suggestions based on history.
        
        Args:
            current_context: Current user input or context
            
        Returns:
            List of suggested actions
        """
        try:
            suggestions = []
            
            # Get similar past interactions
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT response, COUNT(*) as count
                    FROM conversations
                    WHERE user_input LIKE ? AND success = 1
                    GROUP BY response
                    ORDER BY count DESC
                    LIMIT 3
                """, (f'%{current_context}%',))
                
                suggestions = [row[0] for row in cursor.fetchall()]
            
            return suggestions
        except Exception as e:
            self.logger.error(f"Failed to get suggestions: {e}")
            return []
    
    def store_agent_debate(
        self,
        user_input: str,
        debate_result: Dict,
        jarvis_decision: str,
        interaction_id: int = None
    ):
        """
        Store multi-agent debate results with confidence tracking.
        
        Args:
            user_input: Original user request
            debate_result: Dictionary from MultiAgentDebate.debate()
            jarvis_decision: Final decision/response from Jarvis
            interaction_id: Link to conversations table (optional)
        """
        try:
            import json
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO agent_debates (
                        interaction_id,
                        timestamp,
                        user_input,
                        analyst_response,
                        analyst_confidence,
                        skeptic_response,
                        skeptic_confidence,
                        architect_response,
                        architect_confidence,
                        expert_response,
                        expert_confidence,
                        expert_domain,
                        overall_confidence,
                        jarvis_decision,
                        duration_seconds,
                        debate_metadata
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    interaction_id,
                    debate_result.get('timestamp'),
                    user_input,
                    debate_result.get('analyst_response'),
                    debate_result.get('analyst_confidence', 0.7),
                    debate_result.get('skeptic_response'),
                    debate_result.get('skeptic_confidence', 0.7),
                    debate_result.get('architect_response'),
                    debate_result.get('architect_confidence', 0.7),
                    debate_result.get('expert_response'),
                    debate_result.get('expert_confidence'),
                    debate_result.get('expert_domain'),
                    debate_result.get('overall_confidence', 0.7),
                    jarvis_decision,
                    debate_result.get('duration_seconds'),
                    json.dumps({
                        'enabled': debate_result.get('enabled', False),
                        'error': debate_result.get('error')
                    })
                ))
                
                conn.commit()
                self.logger.debug(f"Agent debate stored (confidence: {debate_result.get('overall_confidence', 0.7):.2f})")
                
        except Exception as e:
            self.logger.error(f"Failed to store agent debate: {e}")
    
    def get_recent_debates(self, limit: int = 10) -> List[Dict]:
        """
        Get recent agent debates for analysis/UI with confidence levels.
        
        Args:
            limit: Maximum number of debates to retrieve
            
        Returns:
            List of debate records with all agent responses and confidence
        """
        try:
            import json
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT 
                        id,
                        timestamp,
                        user_input,
                        analyst_response,
                        analyst_confidence,
                        skeptic_response,
                        skeptic_confidence,
                        architect_response,
                        architect_confidence,
                        expert_response,
                        expert_confidence,
                        expert_domain,
                        overall_confidence,
                        jarvis_decision,
                        duration_seconds,
                        debate_metadata
                    FROM agent_debates
                    ORDER BY timestamp DESC
                    LIMIT ?
                """, (limit,))
                
                debates = []
                for row in cursor.fetchall():
                    debates.append({
                        'id': row[0],
                        'timestamp': row[1],
                        'user_input': row[2],
                        'analyst_response': row[3],
                        'analyst_confidence': row[4],
                        'skeptic_response': row[5],
                        'skeptic_confidence': row[6],
                        'architect_response': row[7],
                        'architect_confidence': row[8],
                        'expert_response': row[9],
                        'expert_confidence': row[10],
                        'expert_domain': row[11],
                        'overall_confidence': row[12],
                        'jarvis_decision': row[13],
                        'duration_seconds': row[14],
                        'metadata': json.loads(row[15]) if row[15] else {},
                        'enabled': True
                    })
                
                return debates
                
        except Exception as e:
            self.logger.error(f"Failed to get debates: {e}")
            return []
    
    def store_agent_belief(self, agent_name: str, topic_key: str, opinion: str, 
                          confidence: float, interaction_count: int):
        """Store agent belief/opinion for learning over time."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO agent_beliefs
                    (agent_name, topic_key, opinion, confidence, interaction_count, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (agent_name, topic_key, opinion, confidence, 
                     interaction_count, datetime.now().isoformat()))
                conn.commit()
        except Exception as e:
            self.logger.error(f"Failed to store agent belief: {e}")
    
    def get_agent_belief(self, agent_name: str, topic_key: str) -> Optional[Dict]:
        """Retrieve agent's previous opinion on topic."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT opinion, confidence, interaction_count, timestamp
                    FROM agent_beliefs
                    WHERE agent_name = ? AND topic_key = ?
                """, (agent_name, topic_key))
                row = cursor.fetchone()
                if row:
                    return {
                        'opinion': row[0],
                        'confidence': row[1],
                        'interaction_count': row[2],
                        'timestamp': row[3]
                    }
        except Exception as e:
            self.logger.error(f"Failed to get agent belief: {e}")
        return None
