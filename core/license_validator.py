"""
License Validator Client

Handles license validation for JARVIS Omega:
- Validates license on startup
- Performs daily validation checks (every 24 hours)
- Allows 3-day offline grace period
- Stores validation cache locally
"""

import os
import json
import logging
import requests
from datetime import datetime, timedelta
from pathlib import Path
import uuid
import hashlib


class LicenseValidator:
    """Client-side license validation manager."""
    
    # Validation intervals
    VALIDATION_INTERVAL = timedelta(hours=24)  # Daily validation
    OFFLINE_GRACE_PERIOD = timedelta(days=3)   # 3 days offline grace
    
    def __init__(self, license_key: str = None, cache_file: str = "data/license_cache.json"):
        """
        Initialize the license validator.
        
        Args:
            license_key: The license key to validate
            cache_file: Path to the license cache file
        """
        self.logger = logging.getLogger("jarvis.license")
        self.license_key = license_key or os.environ.get('JARVIS_LICENSE_KEY')
        self.cache_file = Path(cache_file)
        self.device_id = self._get_or_create_device_id()
        
        # API endpoint (can be configured via environment variable)
        self.api_url = os.environ.get(
            'JARVIS_LICENSE_API',
            'https://jarvisomega.vercel.app/api/license/validate'
        )
        
        # Load cached license info
        self.cache = self._load_cache()
        
        self.logger.info(f"License validator initialized (Device ID: {self.device_id[:8]}...)")
    
    def _get_or_create_device_id(self) -> str:
        """
        Get or create a unique device identifier.
        
        Returns:
            str: Unique device ID
        """
        device_file = Path("data/device_id.txt")
        
        try:
            if device_file.exists():
                return device_file.read_text().strip()
            else:
                # Create new device ID
                device_file.parent.mkdir(exist_ok=True)
                
                # Use MAC address + hostname for device ID
                import platform
                mac = hex(uuid.getnode())
                hostname = platform.node()
                device_id = hashlib.sha256(f"{mac}-{hostname}".encode()).hexdigest()
                
                device_file.write_text(device_id)
                return device_id
        except Exception as e:
            self.logger.warning(f"Could not create device ID file: {e}")
            # Fallback to runtime-only ID
            return hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()
    
    def _load_cache(self) -> dict:
        """
        Load cached license information.
        
        Returns:
            dict: Cached license data or empty dict
        """
        try:
            if self.cache_file.exists():
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            self.logger.warning(f"Could not load license cache: {e}")
        
        return {}
    
    def _save_cache(self):
        """Save license cache to disk."""
        try:
            self.cache_file.parent.mkdir(exist_ok=True)
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f, indent=2)
        except Exception as e:
            self.logger.error(f"Could not save license cache: {e}")
    
    def _validate_online(self) -> dict:
        """
        Validate license key with online API.
        
        Returns:
            dict: Validation result
        """
        try:
            response = requests.post(
                self.api_url,
                json={
                    'license_key': self.license_key,
                    'device_id': self.device_id,
                    'app_version': '1.0.0'
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                self.logger.info(f"License validated online: {result.get('tier', 'unknown')} tier")
                return result
            else:
                error_data = response.json()
                self.logger.warning(f"License validation failed: {error_data.get('error', 'Unknown error')}")
                return error_data
                
        except requests.exceptions.RequestException as e:
            self.logger.warning(f"Online validation failed (network error): {e}")
            return {
                'valid': False,
                'error': 'Network error',
                'code': 'NETWORK_ERROR',
                'offline': True
            }
        except Exception as e:
            self.logger.error(f"Unexpected error during validation: {e}", exc_info=True)
            return {
                'valid': False,
                'error': str(e),
                'code': 'UNKNOWN_ERROR'
            }
    
    def should_validate(self) -> bool:
        """
        Check if license should be re-validated.
        
        Returns:
            bool: True if validation is needed
        """
        if not self.cache.get('last_validated'):
            return True
        
        try:
            last_validated = datetime.fromisoformat(self.cache['last_validated'])
            time_since_validation = datetime.now() - last_validated
            
            # Validate if more than 24 hours have passed
            return time_since_validation >= self.VALIDATION_INTERVAL
        except Exception as e:
            self.logger.warning(f"Error checking validation time: {e}")
            return True
    
    def validate(self, force: bool = False) -> dict:
        """
        Validate the license (with caching and offline grace period).
        
        Args:
            force: Force validation even if recently validated
            
        Returns:
            dict: Validation result with 'valid', 'tier', 'features', etc.
        """
        # Check if we need to validate
        if not force and not self.should_validate():
            self.logger.info("Using cached license validation (within 24h window)")
            return self.cache.get('validation_result', {'valid': False, 'error': 'No cache'})
        
        # Try online validation
        self.logger.info("Performing license validation...")
        result = self._validate_online()
        
        now = datetime.now()
        
        if result.get('valid'):
            # Online validation successful
            self.cache['validation_result'] = result
            self.cache['last_validated'] = now.isoformat()
            self.cache['last_successful_validation'] = now.isoformat()
            self._save_cache()
            return result
        
        # Online validation failed - check offline grace period
        if result.get('offline'):
            return self._handle_offline_validation()
        
        # Not offline, but validation failed (expired, invalid, etc.)
        self.cache['validation_result'] = result
        self.cache['last_validated'] = now.isoformat()
        self._save_cache()
        return result
    
    def _handle_offline_validation(self) -> dict:
        """
        Handle validation when offline using grace period.
        
        Returns:
            dict: Validation result
        """
        last_successful = self.cache.get('last_successful_validation')
        
        if not last_successful:
            self.logger.warning("No previous successful validation - cannot use offline mode")
            return {
                'valid': False,
                'error': 'Cannot validate license offline without previous validation',
                'code': 'NO_OFFLINE_CACHE'
            }
        
        try:
            last_success_time = datetime.fromisoformat(last_successful)
            time_offline = datetime.now() - last_success_time
            
            if time_offline <= self.OFFLINE_GRACE_PERIOD:
                # Within grace period - allow offline usage
                days_remaining = (self.OFFLINE_GRACE_PERIOD - time_offline).days
                self.logger.info(f"Using offline grace period ({days_remaining} days remaining)")
                
                cached_result = self.cache.get('validation_result', {})
                cached_result['offline_mode'] = True
                cached_result['offline_days_remaining'] = days_remaining
                return cached_result
            else:
                # Grace period expired
                self.logger.warning("Offline grace period expired")
                return {
                    'valid': False,
                    'error': f'License validation required (offline for {time_offline.days} days)',
                    'code': 'OFFLINE_GRACE_EXPIRED',
                    'offline_days': time_offline.days
                }
        except Exception as e:
            self.logger.error(f"Error handling offline validation: {e}", exc_info=True)
            return {
                'valid': False,
                'error': 'Cannot validate offline',
                'code': 'OFFLINE_ERROR'
            }
    
    def get_status(self) -> dict:
        """
        Get current license status summary.
        
        Returns:
            dict: License status information
        """
        status = {
            'license_key': self.license_key[:8] + '...' if self.license_key else None,
            'device_id': self.device_id[:8] + '...',
            'last_validated': self.cache.get('last_validated'),
            'last_successful': self.cache.get('last_successful_validation'),
            'cached_result': self.cache.get('validation_result', {})
        }
        
        # Calculate next validation time
        if status['last_validated']:
            try:
                last_val = datetime.fromisoformat(status['last_validated'])
                next_val = last_val + self.VALIDATION_INTERVAL
                status['next_validation'] = next_val.isoformat()
                status['needs_validation'] = datetime.now() >= next_val
            except:
                pass
        
        return status
    
    def is_feature_enabled(self, feature: str) -> bool:
        """
        Check if a specific feature is enabled for current license.
        
        Args:
            feature: Feature name (e.g., 'custom_skills', 'api_access')
            
        Returns:
            bool: True if feature is enabled
        """
        cached_result = self.cache.get('validation_result', {})
        if not cached_result.get('valid'):
            return False
        
        features = cached_result.get('features', {})
        return features.get(feature, False)
    
    def get_tier(self) -> str:
        """
        Get current license tier.
        
        Returns:
            str: License tier ('free', 'pro', 'business') or 'unknown'
        """
        cached_result = self.cache.get('validation_result', {})
        return cached_result.get('tier', 'free')


# Global validator instance
_validator_instance = None


def get_validator(license_key: str = None) -> LicenseValidator:
    """
    Get or create the global license validator instance.
    
    Args:
        license_key: License key (only used on first call)
        
    Returns:
        LicenseValidator: The validator instance
    """
    global _validator_instance
    
    if _validator_instance is None:
        _validator_instance = LicenseValidator(license_key)
    
    return _validator_instance
