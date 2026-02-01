# License Validation - Quick Reference Card

## 🚀 Quick Setup (30 seconds)

```powershell
# 1. Install dependency
pip install requests

# 2. Set license key
$env:JARVIS_LICENSE_KEY = "DEMO-PRO-2026"

# 3. Test
python test_license.py

# 4. Run
python main.py
```

## 📋 Key Files

| File | Purpose |
|------|---------|
| `api/license-validate.py` | API endpoint |
| `core/license_validator.py` | Client validation logic |
| `main.py` | Startup validation |
| `core/jarvis.py` | Background validation |

## ⏰ Validation Timeline

```
Startup → Validate immediately
Hour 24 → Re-validate
Hour 48 → Re-validate
...continues every 24 hours
```

## 🔌 Offline Mode

```
Day 0: ✓ Online validation → Cached
Day 1: ✗ Offline → Use cache (2 days grace)
Day 2: ✗ Offline → Use cache (1 day grace)
Day 3: ✗ Offline → Use cache (0 days grace)
Day 4: ❌ Grace expired → Must reconnect
```

## 🎯 Feature Access

```python
from core.license_validator import get_validator

validator = get_validator()

# Check feature
if validator.is_feature_enabled('custom_skills'):
    # Execute feature
    pass

# Check tier
tier = validator.get_tier()  # 'free', 'pro', 'business'
```

## 🔑 Demo License Keys

```
Pro Tier:      DEMO-PRO-2026
Business Tier: DEMO-BUSINESS-2026
Both expire:   2027-12-31
```

## 📊 Validation Response

```json
{
  "valid": true,
  "tier": "pro",
  "expires": "2027-12-31",
  "features": {
    "custom_skills": true,
    "api_access": false,
    ...
  }
}
```

## ⚠️ Error Codes

| Code | Meaning | Fix |
|------|---------|-----|
| `INVALID_KEY` | Not found | Check key |
| `LICENSE_EXPIRED` | Past expiration | Renew |
| `NETWORK_ERROR` | No connection | Check internet |
| `OFFLINE_GRACE_EXPIRED` | Offline > 3 days | Reconnect |

## 📁 Cache Location

```
data/license_cache.json    → Validation cache
data/device_id.txt         → Device identifier
```

## 🛠️ Commands

```powershell
# Setup wizard
python setup_license.py

# Test validation
python test_license.py

# Visual demo
python demo_license.py

# Run app
python main.py
```

## 🌐 API Endpoint

```
Default: https://jarvisomega.vercel.app/api/license/validate

Custom:  $env:JARVIS_LICENSE_API = "https://your-api.com/validate"
```

## 📝 Configuration

### Environment Variable (Recommended)
```powershell
$env:JARVIS_LICENSE_KEY = "YOUR-KEY"
```

### Config File
```yaml
# config.yaml
license_key: YOUR-KEY
```

## ✅ Startup Messages

**Valid License:**
```
✓ License validated successfully
  Tier: PRO
  Expires: 2027-12-31
  Mode: ONLINE
```

**Offline Mode:**
```
✓ License validated successfully
  Tier: PRO
  Expires: 2027-12-31
  Mode: OFFLINE (Grace period: 2 days remaining)
```

**Invalid:**
```
❌ License validation failed: License expired
Error code: LICENSE_EXPIRED
Exiting...
```

## 🎨 Tier Comparison

| Feature | Free | Pro | Business |
|---------|:----:|:---:|:--------:|
| AI Model | Basic | Advanced | Premium |
| Custom Skills | ✗ | ✓ | ✓ |
| Email | ✗ | ✓ | ✓ |
| Smart Home | ✗ | ✓ | ✓ |
| API Access | ✗ | ✗ | ✓ |
| Support | ✗ | ✓ | ✓ |

## 🔍 Debug

Check logs:
```
logs/jarvis.log
```

Look for:
```
License validated: PRO tier (expires 2027-12-31)
Performing scheduled license validation...
Using offline grace period (2 days remaining)
```

## 💡 Tips

1. **First run** - Must be online to cache validation
2. **Offline usage** - Max 3 days without internet
3. **Daily checks** - Automatic every 24 hours
4. **Background thread** - Runs silently during operation
5. **Cache** - Stored in `data/` directory

## 📞 Support

**Email:** support@jarvisomega.com  
**Web:** https://jarvisomega.vercel.app  
**Docs:** LICENSE_VALIDATION_GUIDE.md

---

**Version:** 1.0.0 | **Updated:** Feb 1, 2026
