"""
API Server for Remote Control - REST API for mobile app integration

Provides REST API endpoints for controlling Jarvis remotely.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import threading
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.jarvis import Jarvis


class APIServer:
    """REST API server for remote Jarvis control."""
    
    def __init__(self, config: dict, jarvis: 'Jarvis'):
        """
        Initialize API server.
        
        Args:
            config: API configuration
            jarvis: Jarvis instance
        """
        self.config = config.get('api', {})
        self.jarvis = jarvis
        self.logger = logging.getLogger("jarvis.api")
        
        self.enabled = self.config.get('enabled', False)
        self.host = self.config.get('host', '0.0.0.0')
        self.port = self.config.get('port', 5000)
        self.api_key = self.config.get('api_key', '')
        
        if self.enabled:
            self.app = Flask(__name__)
            CORS(self.app)  # Enable CORS for mobile apps
            self._setup_routes()
            self.server_thread = None
    
    def _setup_routes(self):
        """Setup API routes."""
        
        @self.app.route('/api/status', methods=['GET'])
        def status():
            """Get Jarvis status."""
            if not self._check_auth():
                return jsonify({'error': 'Unauthorized'}), 401
            
            return jsonify({
                'status': 'online',
                'version': '3.0',
                'listening': getattr(self.jarvis, 'is_listening', False)
            })
        
        @self.app.route('/api/command', methods=['POST'])
        def execute_command():
            """Execute a voice command via text."""
            if not self._check_auth():
                return jsonify({'error': 'Unauthorized'}), 401
            
            data = request.get_json()
            command = data.get('command', '')
            
            if not command:
                return jsonify({'error': 'No command provided'}), 400
            
            try:
                # Process command through Jarvis
                response = self.jarvis.process_text_command(command)
                
                return jsonify({
                    'success': True,
                    'command': command,
                    'response': response
                })
            except Exception as e:
                self.logger.error(f"Command execution error: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/speak', methods=['POST'])
        def speak():
            """Make Jarvis speak text."""
            if not self._check_auth():
                return jsonify({'error': 'Unauthorized'}), 401
            
            data = request.get_json()
            text = data.get('text', '')
            
            if not text:
                return jsonify({'error': 'No text provided'}), 400
            
            try:
                self.jarvis.tts.speak(text)
                return jsonify({'success': True})
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/history', methods=['GET'])
        def get_history():
            """Get conversation history."""
            if not self._check_auth():
                return jsonify({'error': 'Unauthorized'}), 401
            
            limit = request.args.get('limit', 10, type=int)
            
            try:
                history = self.jarvis.memory.get_recent_context(limit=limit)
                return jsonify({
                    'success': True,
                    'history': history
                })
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/skills', methods=['GET'])
        def list_skills():
            """List available skills."""
            if not self._check_auth():
                return jsonify({'error': 'Unauthorized'}), 401
            
            try:
                skills = []
                for skill in self.jarvis.skills_engine.skills:
                    skills.append({
                        'name': skill.__class__.__name__,
                        'description': skill.__class__.__doc__ or 'No description'
                    })
                
                return jsonify({
                    'success': True,
                    'skills': skills
                })
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/preferences', methods=['GET', 'POST'])
        def preferences():
            """Get or set preferences."""
            if not self._check_auth():
                return jsonify({'error': 'Unauthorized'}), 401
            
            if request.method == 'GET':
                key = request.args.get('key')
                if key:
                    value = self.jarvis.memory.get_preference(key)
                    return jsonify({'success': True, 'key': key, 'value': value})
                else:
                    return jsonify({'error': 'Key parameter required'}), 400
            
            elif request.method == 'POST':
                data = request.get_json()
                key = data.get('key')
                value = data.get('value')
                
                if not key or value is None:
                    return jsonify({'error': 'Key and value required'}), 400
                
                self.jarvis.memory.set_preference(key, str(value))
                return jsonify({'success': True})
    
    def _check_auth(self) -> bool:
        """Check API authentication."""
        if not self.api_key:
            return True  # No auth required if no key set
        
        auth_header = request.headers.get('Authorization', '')
        
        if auth_header.startswith('Bearer '):
            token = auth_header[7:]
            return token == self.api_key
        
        return False
    
    def start(self):
        """Start API server in background thread."""
        if not self.enabled:
            self.logger.info("API server disabled")
            return
        
        def run_server():
            self.logger.info(f"Starting API server on {self.host}:{self.port}")
            self.app.run(
                host=self.host,
                port=self.port,
                debug=False,
                use_reloader=False
            )
        
        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()
        
        self.logger.info(f"API server started at http://{self.host}:{self.port}")
    
    def stop(self):
        """Stop API server."""
        # Flask server will stop when main thread exits (daemon thread)
        self.logger.info("API server stopped")
