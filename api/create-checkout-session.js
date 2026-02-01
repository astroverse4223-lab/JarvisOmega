const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

module.exports = async (req, res) => {
  // Handle CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }
  
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }
  
  try {
    // Debug: Check if env vars are loaded
    if (!process.env.STRIPE_SECRET_KEY) {
      return res.status(500).json({ 
        error: 'STRIPE_SECRET_KEY not found in environment variables',
        debug: 'Environment variables are not properly configured'
      });
    }
    
    const { plan, billing } = req.body;
    
    // Get price ID from environment
    const priceKey = `PRICE_${plan.toUpperCase()}_${billing.toUpperCase()}`;
    const priceId = process.env[priceKey];
    
    if (!priceId) {
      return res.status(400).json({ error: `Price not found: ${priceKey}` });
    }
    
    // Create checkout session
    const domain = process.env.DOMAIN || 'https://jarvisomega.vercel.app';
    
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      line_items: [{
        price: priceId,
        quantity: 1,
      }],
      mode: 'subscription',
      success_url: `${domain}/success.html?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${domain}/pricing.html`,
      subscription_data: {
        trial_period_days: 14,
      },
    });
    
    res.status(200).json({ sessionId: session.id });
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ 
      error: error.message,
      type: error.type 
    });
  }
};
