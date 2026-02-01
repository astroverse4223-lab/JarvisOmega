"""
Stripe Checkout API for JARVIS Omega
Handles payment processing via Stripe
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import stripe
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for local development

# Configure Stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY', 'sk_test_51QaUqML4yFVJABCD_YOUR_KEY')  # Replace with your key

# Your website URL (change for production)
DOMAIN = os.getenv('DOMAIN', 'http://localhost:8000')

# Price IDs from Stripe Dashboard (create these in Stripe)
PRICES = {
    'pro_monthly': os.getenv('PRICE_PRO_MONTHLY', 'price_1ProMonthly_REPLACE'),
    'pro_yearly': os.getenv('PRICE_PRO_YEARLY', 'price_1ProYearly_REPLACE'),
    'business_monthly': os.getenv('PRICE_BUSINESS_MONTHLY', 'price_1BusinessMonthly_REPLACE'),
    'business_yearly': os.getenv('PRICE_BUSINESS_YEARLY', 'price_1BusinessYearly_REPLACE'),
}

@app.route('/api/create-checkout-session', methods=['POST', 'OPTIONS'])
def create_checkout_session():
    """Create a Stripe Checkout session"""
    # Handle preflight requests
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        data = request.json
        plan = data.get('plan')  # 'pro' or 'business'
        billing = data.get('billing')  # 'monthly' or 'yearly'
        
        print(f"Creating checkout session for {plan} - {billing}")
        
        # Determine price ID
        price_key = f"{plan}_{billing}"
        price_id = PRICES.get(price_key)
        
        if not price_id or 'REPLACE' in price_id:
            return jsonify({
                'error': 'Stripe not configured. Please set up your price IDs in .env file.'
            }), 400
        
        # Create Checkout Session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': price_id,
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=f'{DOMAIN}/website/success.html?session_id={{CHECKOUT_SESSION_ID}}',
            cancel_url=f'{DOMAIN}/website/pricing.html',
            allow_promotion_codes=True,
            billing_address_collection='auto',
            subscription_data={
                'trial_period_days': 14,  # 14-day free trial
                'metadata': {
                    'plan': plan,
                    'billing': billing
                }
            },
        )
        
        print(f"Checkout session created: {checkout_session.id}")
        
        return jsonify({
            'sessionId': checkout_session.id
        })
    
    except stripe.error.StripeError as e:
        print(f"Stripe error: {str(e)}")
        return jsonify({'error': f'Stripe error: {str(e)}'}), 400
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 400


@app.route('/api/get-session-details', methods=['GET'])
def get_session_details():
    """Get checkout session details"""
    try:
        session_id = request.args.get('session_id')
        if not session_id:
            return jsonify({'error': 'Session ID required'}), 400
        
        session = stripe.checkout.Session.retrieve(session_id)
        
        return jsonify({
            'plan': session.get('metadata', {}).get('plan', 'Pro'),
            'status': session.get('payment_status')
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/create-portal-session', methods=['POST'])
def create_portal_session():
    """Create a Stripe Customer Portal session for subscription management"""
    try:
        data = request.json
        customer_id = data.get('customer_id')
        
        if not customer_id:
            return jsonify({'error': 'Customer ID required'}), 400
        
        # Create portal session
        portal_session = stripe.billing_portal.Session.create(
            customer=customer_id,
            return_url='https://yourwebsite.com/account',
        )
        
        return jsonify({
            'url': portal_session.url
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/webhook', methods=['POST'])
def webhook():
    """Handle Stripe webhook events"""
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET', 'whsec_YOUR_WEBHOOK_SECRET')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError as e:
        return jsonify({'error': 'Invalid payload'}), 400
    except stripe.error.SignatureVerificationError as e:
        return jsonify({'error': 'Invalid signature'}), 400
    
    # Handle different event types
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # Fulfill the purchase (send license key, etc.)
        handle_checkout_complete(session)
    
    elif event['type'] == 'customer.subscription.updated':
        subscription = event['data']['object']
        # Handle subscription updates
        handle_subscription_update(subscription)
    
    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        # Handle subscription cancellation
        handle_subscription_cancel(subscription)
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'message': 'JARVIS Omega Stripe API is running',
        'stripe_configured': 'REPLACE' not in PRICES['pro_monthly']
    })


if __name__ == '__main__':
    print("=" * 60)
    print("JARVIS OMEGA - Stripe Payment API")
    print("=" * 60)
    print(f"Domain: {DOMAIN}")
    print(f"Stripe configured: {'REPLACE' not in PRICES['pro_monthly']}")
    print("\nEndpoints:")
    print("  POST   /api/create-checkout-session")
    print("  POST   /api/create-portal-session")
    print("  POST   /api/webhook")
    print("  GET    /api/get-session-details")
    print("  GET    /api/health")
    print("\nTo configure Stripe:")
    print("  1. Copy .env.example to .env")
    print("  2. Add your Stripe keys")
    print("  3. Create products in Stripe Dashboard")
    print("  4. Add price IDs to .env")
    print("=" * 60)
    print("\nStarting server on http://localhost:5000")
    print("Press Ctrl+C to stop\n")
    
    app.run(debug=True, port=5000, host='0.0.0.0')


def handle_checkout_complete(session):
    """Handle successful checkout"""
    # Send welcome email
    # Generate and send license key
    # Activate user account
    print(f"Checkout completed: {session['id']}")
    pass


def handle_subscription_update(subscription):
    """Handle subscription updates"""
    print(f"Subscription updated: {subscription['id']}")
    pass


def handle_subscription_cancel(subscription):
    """Handle subscription cancellation"""
    print(f"Subscription cancelled: {subscription['id']}")
    pass


if __name__ == '__main__':
    app.run(debug=True, port=5000)
