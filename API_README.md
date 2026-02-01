# JARVIS Omega License API

Production license validation API for JARVIS Omega.

## Endpoints

### POST /api/license/validate
Validate a license key.

**Request:**
```json
{
  "license_key": "DEMO-PRO-2026",
  "device_id": "abc123...",
  "app_version": "1.0.0"
}
```

**Response (Success):**
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
  "timestamp": "2026-02-01T12:00:00.000Z"
}
```

### GET /api/license/status
Check API status.

**Response:**
```json
{
  "service": "JARVIS Omega License Validation",
  "status": "online",
  "version": "1.0.0",
  "timestamp": "2026-02-01T12:00:00.000Z"
}
```

## Demo License Keys

- **Pro Tier**: `DEMO-PRO-2026` (expires 2027-12-31)
- **Business Tier**: `DEMO-BUSINESS-2026` (expires 2027-12-31)

## Deployment

Deployed on Vercel:
```bash
vercel deploy --prod
```

## Environment Variables

None required for demo. In production, configure:
- `LICENSE_DATABASE_URL` - Database connection
- `LICENSE_SECRET_KEY` - Signing key
