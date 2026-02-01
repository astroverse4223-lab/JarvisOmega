"""
Music Control Skills - Spotify and system media control

Controls music playback via Spotify API and system media.
"""

import subprocess
from typing import Dict
from skills import BaseSkill


class MusicSkills(BaseSkill):
    """Music and media control."""
    
    def __init__(self, config: dict):
        super().__init__(config)
        self.spotify_enabled = config.get('integrations', {}).get('spotify_enabled', False)
        self.spotify_client_id = config.get('integrations', {}).get('spotify_client_id', '')
        self.spotify_client_secret = config.get('integrations', {}).get('spotify_client_secret', '')
    
    def can_handle(self, intent: str, entities: dict) -> bool:
        """Check if this skill can handle the intent."""
        music_intents = [
            'play_music',
            'pause_music',
            'next_track',
            'previous_track',
            'volume_up',
            'volume_down',
            'current_track'
        ]
        return intent in music_intents
    
    def execute(self, intent: str, entities: dict, raw_text: str = "") -> str:
        """Execute music control commands."""
        try:
            if intent == 'play_music':
                return self._play_music(entities)
            elif intent == 'pause_music':
                return self._pause_music()
            elif intent == 'next_track':
                return self._next_track()
            elif intent == 'previous_track':
                return self._previous_track()
            elif intent in ['volume_up', 'volume_down']:
                return self._adjust_volume(intent)
            elif intent == 'current_track':
                return self._get_current_track()
            else:
                return "I can control music playback."
        except Exception as e:
            self.logger.error(f"Music control error: {e}")
            return f"Error controlling music: {str(e)}"
    
    def _play_music(self, entities: Dict) -> str:
        """Play music."""
        query = entities.get('query', '')
        
        if self.spotify_enabled and query:
            return self._play_spotify(query)
        else:
            # Use system media controls
            return self._system_play()
    
    def _play_spotify(self, query: str) -> str:
        """Play music on Spotify (requires spotipy library)."""
        if not self.spotify_client_id or not self.spotify_client_secret:
            return (
                "Spotify not configured. Set up credentials in config.yaml:\n"
                "1. Go to https://developer.spotify.com/dashboard\n"
                "2. Create an app and get Client ID and Secret\n"
                "3. Add them to config.yaml under integrations"
            )
        
        try:
            import spotipy
            from spotipy.oauth2 import SpotifyOAuth
            
            sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id=self.spotify_client_id,
                client_secret=self.spotify_client_secret,
                redirect_uri="http://localhost:8888/callback",
                scope="user-modify-playback-state,user-read-playback-state"
            ))
            
            # Search for track
            results = sp.search(q=query, limit=1, type='track')
            
            if results['tracks']['items']:
                track = results['tracks']['items'][0]
                track_uri = track['uri']
                track_name = track['name']
                artist_name = track['artists'][0]['name']
                
                # Play track
                sp.start_playback(uris=[track_uri])
                
                return f"Playing {track_name} by {artist_name}"
            else:
                return f"No results found for '{query}'"
                
        except ImportError:
            return "Spotify integration requires 'spotipy' library. Install it with: pip install spotipy"
        except Exception as e:
            self.logger.error(f"Spotify error: {e}")
            return f"Spotify error: {str(e)}"
    
    def _system_play(self) -> str:
        """Play/pause using system media controls."""
        try:
            # Windows media control
            subprocess.run(['nircmd', 'sendkeypress', 'play_pause'], check=False)
            return "Toggled playback"
        except:
            return "Media control not available. Install NirCmd or use Spotify integration."
    
    def _pause_music(self) -> str:
        """Pause music."""
        if self.spotify_enabled:
            return self._spotify_pause()
        else:
            return self._system_play()
    
    def _spotify_pause(self) -> str:
        """Pause Spotify."""
        try:
            import spotipy
            from spotipy.oauth2 import SpotifyOAuth
            
            sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id=self.spotify_client_id,
                client_secret=self.spotify_client_secret,
                redirect_uri="http://localhost:8888/callback",
                scope="user-modify-playback-state"
            ))
            
            sp.pause_playback()
            return "Paused"
        except:
            return "Could not pause Spotify"
    
    def _next_track(self) -> str:
        """Skip to next track."""
        if self.spotify_enabled:
            try:
                import spotipy
                from spotipy.oauth2 import SpotifyOAuth
                
                sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                    client_id=self.spotify_client_id,
                    client_secret=self.spotify_client_secret,
                    redirect_uri="http://localhost:8888/callback",
                    scope="user-modify-playback-state"
                ))
                
                sp.next_track()
                return "Skipped to next track"
            except:
                pass
        
        try:
            subprocess.run(['nircmd', 'sendkeypress', 'media_next'], check=False)
            return "Next track"
        except:
            return "Media control not available"
    
    def _previous_track(self) -> str:
        """Go to previous track."""
        if self.spotify_enabled:
            try:
                import spotipy
                from spotipy.oauth2 import SpotifyOAuth
                
                sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                    client_id=self.spotify_client_id,
                    client_secret=self.spotify_client_secret,
                    redirect_uri="http://localhost:8888/callback",
                    scope="user-modify-playback-state"
                ))
                
                sp.previous_track()
                return "Previous track"
            except:
                pass
        
        try:
            subprocess.run(['nircmd', 'sendkeypress', 'media_prev'], check=False)
            return "Previous track"
        except:
            return "Media control not available"
    
    def _adjust_volume(self, direction: str) -> str:
        """Adjust media volume."""
        # This overlaps with system volume control
        return "Use 'volume up' or 'volume down' for system volume control"
    
    def _get_current_track(self) -> str:
        """Get currently playing track info."""
        if not self.spotify_enabled:
            return "Spotify integration required for track info"
        
        try:
            import spotipy
            from spotipy.oauth2 import SpotifyOAuth
            
            sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id=self.spotify_client_id,
                client_secret=self.spotify_client_secret,
                redirect_uri="http://localhost:8888/callback",
                scope="user-read-playback-state"
            ))
            
            current = sp.current_playback()
            
            if current and current['is_playing']:
                track = current['item']
                track_name = track['name']
                artist_name = track['artists'][0]['name']
                album = track['album']['name']
                
                return f"Now playing: {track_name} by {artist_name} from {album}"
            else:
                return "Nothing is currently playing"
                
        except Exception as e:
            self.logger.error(f"Get track error: {e}")
            return "Could not get current track information"
