const { spawn } = require('child_process');
const path = require('path');

module.exports = async (req, res) => {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  
  // Handle preflight
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }
  
  if (req.method !== 'POST') {
    return res.status(405).json({ 
      valid: false, 
      error: 'Method not allowed',
      code: 'METHOD_NOT_ALLOWED'
    });
  }

  try {
    const { license_key, device_id, app_version } = req.body;
    
    if (!license_key) {
      return res.status(400).json({
        valid: false,
        error: 'License key is required',
        code: 'NO_LICENSE_KEY'
      });
    }

    // Demo license database
    const LICENSE_DATABASE = {
      'DEMO-PRO-2026': {
        email: 'demo@jarvisomega.com',
        tier: 'pro',
        expires: '2027-12-31',
        status: 'active',
        max_devices: 2
      },
      'DEMO-BUSINESS-2026': {
        email: 'business@jarvisomega.com',
        tier: 'business',
        expires: '2027-12-31',
        status: 'active',
        max_devices: 5
      }
    };

    // Check if license exists
    if (!LICENSE_DATABASE[license_key]) {
      return res.status(403).json({
        valid: false,
        error: 'Invalid license key',
        code: 'INVALID_KEY',
        timestamp: new Date().toISOString()
      });
    }

    const licenseInfo = LICENSE_DATABASE[license_key];

    // Check if license is active
    if (licenseInfo.status !== 'active') {
      return res.status(403).json({
        valid: false,
        error: `License is ${licenseInfo.status}`,
        code: 'LICENSE_INACTIVE',
        timestamp: new Date().toISOString()
      });
    }

    // Check expiration
    const expirationDate = new Date(licenseInfo.expires);
    if (expirationDate < new Date()) {
      return res.status(403).json({
        valid: false,
        error: 'License expired',
        code: 'LICENSE_EXPIRED',
        expired_date: licenseInfo.expires,
        timestamp: new Date().toISOString()
      });
    }

    // Get features for tier
    const getFeatures = (tier) => {
      const features = {
        free: {
          ai_model: 'basic',
          voice_commands: true,
          custom_skills: false,
          email_integration: false,
          smart_home: false,
          api_access: false,
          priority_support: false
        },
        pro: {
          ai_model: 'advanced',
          voice_commands: true,
          custom_skills: true,
          email_integration: true,
          smart_home: true,
          api_access: false,
          priority_support: true
        },
        business: {
          ai_model: 'premium',
          voice_commands: true,
          custom_skills: true,
          email_integration: true,
          smart_home: true,
          api_access: true,
          priority_support: true
        }
      };
      return features[tier] || features.free;
    };

    // License is valid
    return res.status(200).json({
      valid: true,
      license_key: license_key,
      tier: licenseInfo.tier,
      expires: licenseInfo.expires,
      email: licenseInfo.email,
      max_devices: licenseInfo.max_devices,
      features: getFeatures(licenseInfo.tier),
      timestamp: new Date().toISOString(),
      device_id: device_id,
      app_version: app_version
    });

  } catch (error) {
    console.error('Validation error:', error);
    return res.status(500).json({
      valid: false,
      error: `Server error: ${error.message}`,
      code: 'SERVER_ERROR',
      timestamp: new Date().toISOString()
    });
  }
};
