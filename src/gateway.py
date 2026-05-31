#!/usr/bin/env python3
"""
AI API Gateway — White-label AI model access with usage tracking and rate limiting.
Sell AI API access with a 30-50% markup. Supports OpenRouter, OpenAI, Anthropic.
"""
import http.server
import json
import hashlib
import time
import os
import sys
import urllib.request
import urllib.error

# Configuration
PORT = int(os.environ.get("AI_GATEWAY_PORT", "8899"))
UPSTREAM_URL = "https://openrouter.ai/api/v1/chat/completions"
UPSTREAM_KEY = os.environ.get("OPENROUTER_API_KEY", "")
API_KEYS_FILE = os.path.join(os.path.dirname(__file__), "api_keys.json")
USAGE_FILE = os.path.join(os.path.dirname(__file__), "usage.json")

# Pricing tiers (per 1M tokens)
TIERS = {
    "starter": {"limit": 100000, "price": 0},      # Free trial
    "pro": {"limit": 1000000, "price": 9},          # $9/month
    "business": {"limit": 10000000, "price": 29},   # $29/month
}

def load_json(path, default=None):
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return default if default is not None else {}

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def check_usage(api_key):
    """Check if API key has remaining tokens"""
    keys = load_json(API_KEYS_FILE, {})
    usage = load_json(USAGE_FILE, {})
    
    if api_key not in keys:
        return False, "Invalid API key"
    
    key_info = keys[api_key]
    tier = key_info.get("tier", "starter")
    limit = TIERS.get(tier, TIERS["starter"])["limit"]
    
    used = usage.get(api_key, 0)
    if used >= limit:
        return False, f"Monthly limit ({limit:,} tokens) exceeded. Used: {used:,}. Upgrade at paypal.me/ulnit"
    
    return True, {"remaining": limit - used, "tier": tier, "used": used}

def track_usage(api_key, token_count):
    usage = load_json(USAGE_FILE, {})
    usage[api_key] = usage.get(api_key, 0) + token_count
    save_json(USAGE_FILE, usage)

class GatewayHandler(http.server.BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()
    
    def do_GET(self):
        if self.path == "/":
            self.send_json({"service": "AI API Gateway", "version": "1.0.0", 
                          "endpoints": ["POST /v1/chat/completions", "GET /v1/usage", "GET /health"]})
        elif self.path == "/health":
            self.send_json({"status": "ok", "timestamp": time.time()})
        elif self.path == "/v1/usage":
            api_key = self.headers.get("Authorization", "").replace("Bearer ", "")
            if not api_key:
                self.send_error(401, "Missing API key")
                return
            ok, info = check_usage(api_key)
            if not ok:
                self.send_error(403, info)
            else:
                self.send_json(info)
        else:
            self.send_error(404, "Not found")
    
    def do_POST(self):
        if self.path == "/v1/chat/completions":
            self.handle_chat()
        else:
            self.send_error(404, "Not found")
    
    def handle_chat(self):
        api_key = self.headers.get("Authorization", "").replace("Bearer ", "")
        if not api_key:
            self.send_error(401, "Missing API key. Get one at paypal.me/ulnit")
            return
        
        ok, info = check_usage(api_key)
        if not ok:
            self.send_error(403, info)
            return
        
        # Read request body
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        
        try:
            req_data = json.loads(body)
        except:
            self.send_error(400, "Invalid JSON")
            return
        
        # Forward to upstream AI provider
        if not UPSTREAM_KEY:
            self.send_error(503, "Gateway not configured with upstream provider")
            return
        
        upstream_req = urllib.request.Request(
            UPSTREAM_URL,
            data=json.dumps(req_data).encode(),
            headers={
                "Authorization": f"Bearer {UPSTREAM_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://ulnit.github.io/agent-store",
                "X-Title": "AI API Gateway"
            }
        )
        
        try:
            with urllib.request.urlopen(upstream_req, timeout=60) as resp:
                resp_data = resp.read()
                resp_json = json.loads(resp_data)
                
                # Track usage (estimate tokens from response)
                if "usage" in resp_json:
                    tokens = resp_json["usage"].get("total_tokens", 0)
                    track_usage(api_key, tokens)
                
                self.send_response(resp.status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(resp_data)
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(e.read())
        except Exception as e:
            self.send_error(502, f"Upstream error: {str(e)}")
    
    def send_json(self, data):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def log_message(self, format, *args):
        sys.stderr.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {args[0]}\n")

if __name__ == "__main__":
    server = http.server.HTTPServer(("0.0.0.0", PORT), GatewayHandler)
    print(f"AI API Gateway running on port {PORT}")
    print(f"Get API keys: https://paypal.me/ulnit")
    server.serve_forever()
