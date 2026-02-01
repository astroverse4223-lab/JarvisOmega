"""
License Validation API Endpoint

Validates JARVIS Omega license keys and returns license status.
"""

from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import hashlib
import hmac
import os

app = Flask(__name__)

# In production, store these in environment variables
LICENSE_SECRET_KEY = os.environ.get('LICENSE_SECRET_KEY', 'jarvis_omega_license_secret_2026')

# Demo license database (in production, use a real database)
# Format: license_key: {email, tier, expires, status}
LICENSE_DATABASE = {
    'DEMO-PRO-2026': {
        'email': 'demo@jarvisomega.com',
        'tier': 'pro',
        'expires': '2027-12-31',
        'status': 'active',
        'max_devices': 2
    },
    'DEMO-BUSINESS-2026': {
        'email': 'business@jarvisomega.com',
        'tier': 'business',
        'expires': '2027-12-31',
        'status': 'active',
        'max_devices': 5
    }
}


def verify_license_key(license_key: str) -> dict:
    """
    Verify a license key and return license information.
    
    Args:
        license_key: The license key to verify
        
    Returns:
        dict: License information or error
    """
    # Check if license exists
    if license_key not in LICENSE_DATABASE:
        return {
            'valid': False,
            'error': 'Invalid license key',
            'code': 'INVALID_KEY'
        }
    
    license_info = LICENSE_DATABASE[license_key]
    
    # Check if license is active
    if license_info['status'] != 'active':
        return {
            'valid': False,
            'error': f"License is {license_info['status']}",
            'code': 'LICENSE_INACTIVE'
        }
    
    # Check expiration
    try:
        expires = datetime.strptime(license_info['expires'], '%Y-%m-%d')
        if expires < datetime.now():
            return {
                'valid': False,
                'error': 'License expired',
                'code': 'LICENSE_EXPIRED',
                'expired_date': license_info['expires']
            }
    except Exception as e:
        return {
            'valid': False,
            'error': f'Invalid expiration date: {e}',
            'code': 'INVALID_EXPIRATION'
        }
    
    # License is valid
    return {
        'valid': True,
        'license_key': license_key,
        'tier': license_info['tier'],
        'expires': license_info['expires'],
        'email': license_info['email'],
        'max_devices': license_info.get('max_devices', 1),
        'features': get_tier_features(license_info['tier'])
    }


def get_tier_features(tier: str) -> dict:
    """Get features available for a specific tier."""
    features = {
        'free': {
            'ai_model': 'basic',
            'voice_commands': True,
            'custom_skills': False,
            'email_integration': False,
            'smart_home': False,
            'api_access': False,
            'priority_support': False
        },
        'pro': {
            'ai_model': 'advanced',
            'voice_commands': True,
            'custom_skills': True,
            'email_integration': True,
            'smart_home': True,
            'api_access': False,
            'priority_support': True
        },
        'business': {
            'ai_model': 'premium',
            'voice_commands': True,
            'custom_skills': True,
            'email_integration': True,
            'smart_home': True,
            'api_access': True,
            'priority_support': True
        }
    }
    return features.get(tier, features['free'])


@app.route('/api/license/validate', methods=['POST'])
def validate_license():
    """
    Validate a license key.
    
    Request body:
    {
        "license_key": "XXXX-XXXX-XXXX",
        "device_id": "unique-device-identifier",
        "app_version": "1.0.0"
    }
    
    Response:
    {
        "valid": true/false,
        "license_key": "...",
        "tier": "pro/business",
        "expires": "2027-12-31",
        "features": {...},
        "timestamp": "2026-02-01T12:00:00Z"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'valid': False,
                'error': 'No data provided',
                'code': 'NO_DATA'
            }), 400
        
        license_key = data.get('license_key')
        device_id = data.get('device_id', 'unknown')
        app_version = data.get('app_version', '1.0.0')
        
        if not license_key:
            return jsonify({
                'valid': False,
                'error': 'License key is required',
                'code': 'NO_LICENSE_KEY'
            }), 400
        
        # Verify the license
        result = verify_license_key(license_key)
        
        # Add timestamp
        result['timestamp'] = datetime.utcnow().isoformat() + 'Z'
        result['device_id'] = device_id
        result['app_version'] = app_version
        
        # Return appropriate status code
        status_code = 200 if result.get('valid') else 403
        
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({
            'valid': False,
            'error': f'Server error: {str(e)}',
            'code': 'SERVER_ERROR'
        }), 500


@app.route('/api/license/status', methods=['GET'])
def license_status():
    """
    Get license status (for testing).
    """
    return jsonify({
        'service': 'JARVIS Omega License Validation',
        'status': 'online',
        'version': '1.0.0',
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    })


# Root endpoint for testing
@app.route('/')
def index():
    """Root endpoint."""
    return jsonify({
        'service': 'JARVIS Omega License Validation API',
        'status': 'online',
        'endpoints': {
            'status': '/api/license/status',
            'validate': '/api/license/validate (POST)'
        }
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
