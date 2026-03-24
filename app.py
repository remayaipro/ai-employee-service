"""
AI Employee Service - Landing Page with Stripe Checkout
"""
import os
import json
from flask import Flask, request, jsonify, render_template_string
import stripe

app = Flask(__name__)

# Configuration - Set these in environment variables
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY', 'sk_test_placeholder')
STRIPE_PRICE_BASIC = os.environ.get('STRIPE_PRICE_BASIC', 'price_basic_placeholder')
STRIPE_PRICE_PRO = os.environ.get('STRIPE_PRICE_PRO', 'price_pro_placeholder')
STRIPE_PRICE_ENTERPRISE = os.environ.get('STRIPE_PRICE_ENTERPRISE', 'price_enterprise_placeholder')
STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET', 'whsec_placeholder')

# Simple user storage (use a database in production)
USERS_FILE = 'users.json'

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Employee - 24/7 Virtual Staff</title>
    <meta name="description" content="Hire an AI employee that works 24/7. Sales, marketing, support, research - all automated.">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
            min-height: 100vh;
            color: #333;
        }
        .hero {
            text-align: center;
            padding: 80px 20px 60px;
            color: white;
        }
        .hero h1 {
            font-size: 3.5rem;
            margin-bottom: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .hero p {
            font-size: 1.4rem;
            color: #ccc;
            max-width: 600px;
            margin: 0 auto 40px;
        }
        .telegram-btn {
            display: inline-block;
            background: #0088cc;
            color: white;
            padding: 16px 32px;
            border-radius: 50px;
            text-decoration: none;
            font-size: 1.1rem;
            font-weight: 600;
            margin-top: 20px;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .telegram-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(0,136,204,0.4);
        }
        .features {
            background: white;
            padding: 80px 20px;
        }
        .features h2 {
            text-align: center;
            font-size: 2.5rem;
            margin-bottom: 50px;
            color: #1a1a2e;
        }
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 30px;
            max-width: 1100px;
            margin: 0 auto;
        }
        .feature-card {
            padding: 30px;
            border-radius: 16px;
            background: #f8f9fa;
            text-align: center;
            transition: transform 0.3s;
        }
        .feature-card:hover {
            transform: translateY(-5px);
        }
        .feature-icon { font-size: 48px; margin-bottom: 15px; }
        .feature-card h3 { color: #1a1a2e; margin-bottom: 10px; }
        .feature-card p { color: #666; line-height: 1.6; }
        
        .pricing {
            padding: 80px 20px;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        }
        .pricing h2 {
            text-align: center;
            font-size: 2.5rem;
            margin-bottom: 50px;
            color: white;
        }
        .pricing-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            max-width: 1000px;
            margin: 0 auto;
        }
        .pricing-card {
            background: white;
            border-radius: 20px;
            padding: 40px;
            text-align: center;
            transition: transform 0.3s;
        }
        .pricing-card.popular {
            border: 3px solid #667eea;
            position: relative;
        }
        .pricing-card.popular::before {
            content: 'Most Popular';
            position: absolute;
            top: -12px;
            left: 50%;
            transform: translateX(-50%);
            background: #667eea;
            color: white;
            padding: 4px 16px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }
        .pricing-card h3 { font-size: 1.5rem; margin-bottom: 10px; }
        .price {
            font-size: 3rem;
            font-weight: bold;
            color: #1a1a2e;
            margin: 20px 0;
        }
        .price span { font-size: 1rem; color: #666; }
        .pricing-card ul {
            list-style: none;
            text-align: left;
            margin: 20px 0;
        }
        .pricing-card li {
            padding: 10px 0;
            color: #555;
        }
        .pricing-card li::before {
            content: '✓';
            color: #10b981;
            margin-right: 10px;
            font-weight: bold;
        }
        .subscribe-btn {
            display: block;
            width: 100%;
            padding: 16px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .subscribe-btn:hover { transform: translateY(-2px); }
        .pricing-card.basic .subscribe-btn { background: #6b7280; }
        .pricing-card.enterprise .subscribe-btn { background: #f59e0b; }
        
        .footer {
            background: #0f0c29;
            color: #888;
            text-align: center;
            padding: 40px 20px;
        }
        .footer a { color: #667eea; text-decoration: none; }
        
        .success-modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.8);
            align-items: center;
            justify-content: center;
            z-index: 1000;
        }
        .success-modal.show { display: flex; }
        .success-content {
            background: white;
            padding: 40px;
            border-radius: 20px;
            text-align: center;
            max-width: 500px;
        }
        .success-content h2 { color: #10b981; margin-bottom: 20px; }
        .success-content p { margin-bottom: 15px; line-height: 1.6; }
    </style>
</head>
<body>
    <div class="hero">
        <h1>🤖 Hire an AI Employee</h1>
        <p>Your 24/7 virtual staff for sales, marketing, support, and research. Never sleeps, never takes vacations.</p>
        <a href="https://t.me/StableRemayBot" class="telegram-btn">💬 Start on Telegram</a>
    </div>
    
    <div class="features">
        <h2>What Can Your AI Employee Do?</h2>
        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-icon">📈</div>
                <h3>Sales Closer</h3>
                <p>Engage leads, answer questions, and close deals automatically via Telegram.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">✍️</div>
                <h3>Content Marketer</h3>
                <p>Generate posts, write emails, and schedule social media content daily.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🎧</div>
                <h3>Customer Support</h3>
                <p>Instant responses to customer inquiries, 24/7, in multiple languages.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🔍</div>
                <h3>Research Assistant</h3>
                <p>Daily briefings, market analysis, competitor research - fully automated.</p>
            </div>
        </div>
    </div>
    
    <div class="pricing">
        <h2>Choose Your AI Employee</h2>
        <div class="pricing-grid">
            <div class="pricing-card basic">
                <h3>Starter</h3>
                <div class="price">$29<span>/month</span></div>
                <ul>
                    <li>1 AI Employee</li>
                    <li>Basic tasks</li>
                    <li>500 messages/month</li>
                    <li>Email support</li>
                </ul>
                <button class="subscribe-btn" onclick="subscribe('basic')">Get Started</button>
            </div>
            <div class="pricing-card popular">
                <h3>Professional</h3>
                <div class="price">$59<span>/month</span></div>
                <ul>
                    <li>2 AI Employees</li>
                    <li>Advanced tasks</li>
                    <li>Unlimited messages</li>
                    <li>Image generation</li>
                    <li>Web automation</li>
                    <li>Priority support</li>
                </ul>
                <button class="subscribe-btn" onclick="subscribe('pro')">Get Started</button>
            </div>
            <div class="pricing-card enterprise">
                <h3>Enterprise</h3>
                <div class="price">$99<span>/month</span></div>
                <ul>
                    <li>5 AI Employees</li>
                    <li>Custom skills</li>
                    <li>Everything in Pro</li>
                    <li>Dedicated agent</li>
                    <li>API access</li>
                    <li>White-label</li>
                </ul>
                <button class="subscribe-btn" onclick="subscribe('enterprise')">Contact Sales</button>
            </div>
        </div>
    </div>
    
    <div class="footer">
        <p>© 2026 AI Employee Service. All rights reserved.</p>
        <p><a href="#">Privacy Policy</a> | <a href="#">Terms of Service</a></p>
    </div>

    <script src="https://js.stripe.com/v3/"></script>
    <script>
        const prices = {
            basic: '{{ stripe_price_basic }}',
            pro: '{{ stripe_price_pro }}',
            enterprise: '{{ stripe_price_enterprise }}'
        };
        
        async function subscribe(plan) {
            const priceId = prices[plan];
            if (!priceId) {
                alert('Please contact us for Enterprise pricing!');
                return;
            }
            
            const btn = document.querySelector(`.${plan} .subscribe-btn`);
            btn.textContent = 'Processing...';
            btn.disabled = true;
            
            try {
                const response = await fetch('/create-checkout-session', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ price_id: priceId, plan: plan })
                });
                
                const { sessionId } = await response.json();
                
                const stripe = Stripe('{{ stripe_pub_key }}');
                await stripe.redirectToCheckout({ sessionId });
                
            } catch (err) {
                alert('Error: ' + err.message);
                btn.textContent = 'Get Started';
                btn.disabled = false;
            }
        }
    </script>
</body>
</html>'''


@app.route('/')
def index():
    return render_template_string(html,
        stripe_price_basic=STRIPE_PRICE_BASIC,
        stripe_price_pro=STRIPE_PRICE_PRO,
        stripe_price_enterprise=STRIPE_PRICE_ENTERPRISE,
        stripe_pub_key=os.environ.get('STRIPE_PUB_KEY', 'pk_test_placeholder'))


@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        data = request.json
        price_id = data.get('price_id')
        plan = data.get('plan')
        
        # Get user's Telegram username or generate a code
        telegram_username = data.get('telegram_username', '')
        
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='subscription',
            success_url=request.host_url + 'success?session_id={CHECKOUT_SESSION_ID}&plan=' + plan,
            cancel_url=request.host_url,
            metadata={
                'plan': plan,
                'telegram': telegram_username
            }
        )
        
        return jsonify({'sessionId': session.id})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/success')
def success():
    session_id = request.args.get('session_id')
    plan = request.args.get('plan', 'unknown')
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Welcome!</title>
        <meta http-equiv="refresh" content="3;url=/">
        <style>
            body {{ font-family: -apple-system, sans-serif; text-align: center; padding: 100px; background: #f0fdf4; }}
            h1 {{ color: #10b981; }}
            p {{ color: #666; }}
        </style>
    </head>
    <body>
        <h1>🎉 Welcome aboard!</h1>
        <p>Your {plan} subscription is activated.</p>
        <p>Redirecting to Telegram to meet your AI Employee...</p>
    </body>
    </html>
    '''


@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.data
    sig_header = request.headers.get('stripe-signature')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError:
        return 'Invalid signature', 400
    
    # Handle events
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        handle_subscription_created(session)
    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        handle_subscription_cancelled(subscription)
    
    return '', 200


def handle_subscription_created(session):
    """Add user to allowed list"""
    users = load_users()
    email = session.get('customer_email', '')
    plan = session.get('metadata', {}).get('plan', 'basic')
    customer_id = session.get('customer')
    
    users[email] = {
        'plan': plan,
        'customer_id': customer_id,
        'status': 'active'
    }
    save_users(users)
    print(f"New subscription: {email} - {plan}")


def handle_subscription_cancelled(subscription):
    """Remove user from allowed list"""
    users = load_users()
    customer_id = subscription.get('customer')
    
    # Find and remove user
    for email, data in list(users.items()):
        if data.get('customer_id') == customer_id:
            users[email]['status'] = 'cancelled'
            save_users(users)
            print(f"Cancelled: {email}")
            break


@app.route('/check-subscription', methods=['POST'])
def check_subscription():
    """API endpoint for Hermes to check if user has active subscription"""
    data = request.json
    telegram_username = data.get('telegram_username', '')
    
    users = load_users()
    
    # Check by Telegram username
    for email, user_data in users.items():
        if user_data.get('telegram') == telegram_username and user_data.get('status') == 'active':
            return jsonify({
                'active': True,
                'plan': user_data.get('plan', 'basic')
            })
    
    return jsonify({'active': False})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
