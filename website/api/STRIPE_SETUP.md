# JARVIS Omega - Stripe Payment Setup Guide

## Prerequisites

1. **Stripe Account**: Sign up at https://stripe.com
2. **Python packages**: 
   ```bash
   pip install stripe flask flask-cors
   ```

## Setup Steps

### 1. Get Stripe API Keys

1. Go to https://dashboard.stripe.com/test/apikeys
2. Copy your **Publishable key** (starts with `pk_test_`)
3. Copy your **Secret key** (starts with `sk_test_`)

### 2. Create Products and Prices in Stripe

1. Go to https://dashboard.stripe.com/test/products
2. Click "Add product"
3. Create the following products:

**Product 1: JARVIS Omega Pro**
- Name: JARVIS Omega Pro
- Description: Advanced AI voice assistant with priority support
- Create two prices:
  - Monthly: $9/month (recurring)
  - Yearly: $84/year (recurring, save 20%)

**Product 2: JARVIS Omega Business**
- Name: JARVIS Omega Business
- Description: Commercial license with team features
- Create two prices:
  - Monthly: $29/month (recurring)
  - Yearly: $288/year (recurring, save 20%)

4. Copy all price IDs (start with `price_`)

### 3. Configure Your API

Edit `website/api/checkout.py`:

```python
# Replace these with your actual keys
stripe.api_key = 'sk_test_YOUR_SECRET_KEY'

PRICES = {
    'pro_monthly': 'price_YOUR_PRO_MONTHLY_ID',
    'pro_yearly': 'price_YOUR_PRO_YEARLY_ID',
    'business_monthly': 'price_YOUR_BUSINESS_MONTHLY_ID',
    'business_yearly': 'price_YOUR_BUSINESS_YEARLY_ID',
}
```

Edit `website/pricing.html`:

```javascript
const stripe = Stripe('pk_test_YOUR_PUBLISHABLE_KEY');
```

### 4. Update Success/Cancel URLs

In `website/api/checkout.py`, update these URLs to your actual website:

```python
success_url='https://yourwebsite.com/success?session_id={CHECKOUT_SESSION_ID}',
cancel_url='https://yourwebsite.com/pricing',
```

### 5. Set Up Webhook (Important!)

1. Go to https://dashboard.stripe.com/test/webhooks
2. Click "Add endpoint"
3. URL: `https://yourwebsite.com/api/webhook`
4. Select events to listen to:
   - `checkout.session.completed`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
5. Copy the webhook secret (starts with `whsec_`)
6. Update in `checkout.py`:
   ```python
   webhook_secret = 'whsec_YOUR_WEBHOOK_SECRET'
   ```

### 6. Environment Variables (Recommended)

Create a `.env` file:

```
STRIPE_SECRET_KEY=sk_test_YOUR_SECRET_KEY
STRIPE_WEBHOOK_SECRET=whsec_YOUR_WEBHOOK_SECRET
```

Then use:
```python
import os
from dotenv import load_dotenv

load_dotenv()
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
```

### 7. Run the API Server

```bash
cd website/api
python checkout.py
```

The API will run on http://localhost:5000

### 8. Deploy

**Option 1: Vercel (Recommended for static site + API)**
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd website
vercel
```

**Option 2: Heroku**
```bash
# Create Procfile
echo "web: python api/checkout.py" > Procfile

# Deploy
heroku create jarvis-omega-api
git push heroku main
```

**Option 3: AWS Lambda + API Gateway**
- Use Serverless Framework or AWS SAM
- Convert Flask app to Lambda handlers

## Testing

### Test Mode
Stripe provides test card numbers:
- Success: `4242 4242 4242 4242`
- Requires authentication: `4000 0027 6000 3184`
- Decline: `4000 0000 0000 0002`

Use any future expiry date and any CVC.

### Test the Flow
1. Go to your pricing page
2. Click "Start Pro Trial"
3. Use test card: 4242 4242 4242 4242
4. Complete checkout
5. Check Stripe Dashboard for successful payment

## Security Checklist

- [ ] Use environment variables for API keys
- [ ] Never commit API keys to Git
- [ ] Add `.env` to `.gitignore`
- [ ] Verify webhook signatures
- [ ] Use HTTPS in production
- [ ] Implement rate limiting
- [ ] Add CORS restrictions in production
- [ ] Log all payment events

## Going Live

1. Switch from Test mode to Live mode in Stripe
2. Create products again in Live mode
3. Update API keys to live keys (sk_live_, pk_live_)
4. Update webhook endpoint to production URL
5. Test thoroughly before announcing

## Customer Portal

Users can manage subscriptions at:
`https://billing.stripe.com/p/login/YOUR_PORTAL_ID`

Or create portal sessions programmatically with `/api/create-portal-session`

## Pricing Strategy Implemented

### Free Personal
- $0 forever
- All core features
- For personal use only

### Pro ($9/month or $7/month billed yearly)
- 14-day free trial
- Save $24/year with yearly
- Priority support
- Advanced features

### Business ($29/month or $24/month billed yearly)
- 14-day free trial
- Save $60/year with yearly
- Commercial license
- Team features

### Enterprise (Custom)
- Contact sales
- Custom pricing
- Full white-label

## Support

For Stripe integration questions:
- Stripe Docs: https://stripe.com/docs
- Stripe Support: https://support.stripe.com
