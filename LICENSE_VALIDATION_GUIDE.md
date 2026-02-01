# License Validation System - Complete Guide

## Overview

JARVIS Omega now includes a comprehensive license validation system with:
- ✅ **Startup validation** - License checked when app launches
- ✅ **Daily validation** - Automatic re-validation every 24 hours
- ✅ **Offline grace period** - 3 days of offline usage allowed
- ✅ **Smart caching** - Reduces unnecessary API calls
- ✅ **Feature gating** - Tier-based feature access control

## Architecture

### Components

1. **API Endpoint** (`api/license-validate.py`)
   - REST API for license validation
   - Returns tier, features, and expiration info
   - Can be deployed to Vercel, AWS Lambda, etc.

2. **Client Validator** (`core/license_validator.py`)
   - Client-side validation logic
   - Handles caching and offline mode
   - Manages device identification

3. **Main Integration** (`main.py`)
   - Validates license on startup
   - Shows clear status messages
   - Exits if license is invalid

4. **Background Thread** (`core/jarvis.py`)
   - Validates license every 24 hours
   - Runs in background during app execution
   - Logs validation results

## Setup

### 1. Configure License Key

**Option A: Environment Variable (Recommended)**
```powershell
# Windows
$env:JARVIS_LICENSE_KEY = "YOUR-LICENSE-KEY-HERE"

# Or permanently:
[System.Environment]::SetEnvironmentVariable('JARVIS_LICENSE_KEY', 'YOUR-KEY', 'User')
```

**Option B: Config File**
```yaml
# config.yaml
license_key: YOUR-LICENSE-KEY-HERE
```

### 2. Configure API Endpoint (Optional)

Default: `https://jarvisomega.vercel.app/api/license/validate`

To use a custom endpoint:
```powershell
$env:JARVIS_LICENSE_API = "https://your-api.com/validate"
```

### 3. Install Dependencies

```powershell
pip install requests
```

## How It Works

### Startup Validation

When JARVIS launches:

1. Reads license key from config or environment
2. Calls validation API
3. Shows status to user:
   - ✓ Valid: Shows tier, expiration, online/offline status
   - ❌ Invalid: Shows error and exits (unless offline mode)
   - ⚠️ No key: Runs in FREE mode

### Daily Validation

While JARVIS runs:

1. Background thread checks every hour if validation is needed
2. If 24+ hours passed, validates license again
3. Updates cache with new validation result
4. Logs status (success/failure/offline)

### Offline Grace Period

If network is unavailable:

1. Uses cached validation result
2. Checks last successful validation time
3. Allows up to 3 days offline usage
4. After 3 days, requires online validation

## Validation Flow

```
[App Start]
    ↓
[Check License Key]
    ↓
[Has Key?] → NO → [Run in FREE mode]
    ↓ YES
[Validate Online]
    ↓
[Success?] → YES → [Cache result, continue]
    ↓ NO
[Network Error?] → YES → [Check offline grace]
    ↓                        ↓
    ↓                   [< 3 days?] → YES → [Use cache, continue]
    ↓                        ↓ NO
    ↓                   [Exit: Grace expired]
    ↓ NO
[License Invalid/Expired]
    ↓
[Exit with error]
```

## License Tiers

### Free Tier
- Basic AI model
- Voice commands
- No custom skills
- No email integration
- No smart home
- No API access
- No priority support

### Pro Tier ($19.99/month)
- Advanced AI model
- Voice commands ✓
- Custom skills ✓
- Email integration ✓
- Smart home ✓
- API access ✗
- Priority support ✓
- Max 2 devices

### Business Tier ($49.99/month)
- Premium AI model
- Voice commands ✓
- Custom skills ✓
- Email integration ✓
- Smart home ✓
- API access ✓
- Priority support ✓
- Max 5 devices

## Testing

Run the test script:
```powershell
python test_license.py
```

This will:
1. Test online validation
2. Test caching mechanism
3. Test offline mode simulation
4. Test feature checking
5. Show detailed results

## Demo License Keys

For testing purposes:

- **Pro Tier**: `DEMO-PRO-2026`
- **Business Tier**: `DEMO-BUSINESS-2026`

Both expire: 2027-12-31

## API Response Format

### Success Response
```json
{
  "valid": true,
  "license_key": "DEMO-PRO-2026",
  "tier": "pro",
  "expires": "2027-12-31",
  "email": "user@example.com",
  "max_devices": 2,
  "features": {
    "ai_model": "advanced",
    "voice_commands": true,
    "custom_skills": true,
    "email_integration": true,
    "smart_home": true,
    "api_access": false,
    "priority_support": true
  },
  "timestamp": "2026-02-01T12:00:00Z",
  "device_id": "abc123...",
  "app_version": "1.0.0"
}
```

### Error Response
```json
{
  "valid": false,
  "error": "License expired",
  "code": "LICENSE_EXPIRED",
  "expired_date": "2025-12-31",
  "timestamp": "2026-02-01T12:00:00Z"
}
```

### Error Codes

- `INVALID_KEY` - License key not found
- `LICENSE_EXPIRED` - License has expired
- `LICENSE_INACTIVE` - License is suspended/cancelled
- `NETWORK_ERROR` - Cannot connect to API
- `OFFLINE_GRACE_EXPIRED` - Offline for more than 3 days
- `NO_OFFLINE_CACHE` - No previous validation for offline mode

## Cached Data

License validation cache is stored in:
```
data/license_cache.json
```

Contains:
- Last validation timestamp
- Last successful validation timestamp  
- Cached validation result
- Offline mode status

Device ID stored in:
```
data/device_id.txt
```

## Deployment

### Deploy API to Vercel

1. Create API route in `website/api/`:
```javascript
// website/api/license-validate.js
const handler = require('../../api/license-validate.py');
module.exports = handler;
```

2. Deploy:
```powershell
vercel deploy
```

3. Update environment variable:
```powershell
$env:JARVIS_LICENSE_API = "https://your-app.vercel.app/api/license-validate"
```

## Feature Gating in Code

Check if feature is available:

```python
from core.license_validator import get_validator

validator = get_validator()

# Check specific feature
if validator.is_feature_enabled('custom_skills'):
    # Execute custom skill
    pass
else:
    return "This feature requires Pro or Business tier"

# Check tier
if validator.get_tier() in ['pro', 'business']:
    # Advanced feature
    pass
```

## Monitoring

Check validation status at runtime:

```python
from core.license_validator import get_validator

validator = get_validator()
status = validator.get_status()

print(f"Last validated: {status['last_validated']}")
print(f"Next validation: {status['next_validation']}")
print(f"Needs validation: {status['needs_validation']}")
```

## Troubleshooting

### "Cannot validate license offline without previous validation"
- **Solution**: Connect to internet and run app once to cache validation

### "Offline grace period expired"
- **Solution**: Connect to internet to re-validate license

### "License validation failed: Network error"
- **Solution**: Check internet connection and API endpoint URL

### License key not being read
- **Solution**: Verify environment variable or config.yaml entry

### Background validation not working
- **Solution**: Check logs/jarvis.log for validation thread messages

## Security Notes

1. **License keys are not encrypted** in cache - sensitive data should not be stored in license info
2. **Device ID** is generated from MAC address + hostname hash
3. **API calls** should use HTTPS in production
4. **Webhook secrets** should be stored in environment variables only

## Future Enhancements

Potential improvements:
- [ ] Hardware fingerprinting for device tracking
- [ ] License key encryption in cache
- [ ] Multiple device management
- [ ] License transfer between devices
- [ ] Usage analytics and reporting
- [ ] Automatic license renewal notifications
- [ ] Grace period notifications (e.g., "2 days of offline usage remaining")

## Support

For license issues:
- Email: support@jarvisomega.com
- Website: https://jarvisomega.vercel.app
- Documentation: See README.md

---

**Last Updated**: February 1, 2026
**Version**: 1.0.0
