from http.server import BaseHTTPRequestHandler
import json
import os

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
    def do_POST(self):
        try:
            # Lazy import stripe inside the function
            import stripe
            stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
            
            # Read body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length) if content_length > 0 else b'{}'
            data = json.loads(body.decode('utf-8'))
            
            plan = data.get('plan', 'pro')
            billing = data.get('billing', 'monthly')
            
            # Get price ID
            price_key = f'PRICE_{plan.upper()}_{billing.upper()}'
            price_id = os.environ.get(price_key)
            
            if not price_id:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': f'Price not found: {price_key}'}).encode())
                return
            
            # Create session
            domain = os.environ.get('DOMAIN', 'https://jarvisomega.vercel.app')
            
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{'price': price_id, 'quantity': 1}],
                mode='subscription',
                success_url=f'{domain}/success.html?session_id={{CHECKOUT_SESSION_ID}}',
                cancel_url=f'{domain}/pricing.html',
                subscription_data={'trial_period_days': 14}
            )
            
            # Success response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'sessionId': session.id}).encode())
            
        except Exception as e:
            import traceback
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            error_data = {
                'error': str(e),
                'type': type(e).__name__,
                'trace': traceback.format_exc()
            }
            self.wfile.write(json.dumps(error_data).encode())
