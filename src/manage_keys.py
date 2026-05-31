#!/usr/bin/env python3
"""Manage API keys for the AI API Gateway"""
import json
import hashlib
import secrets
import sys
import os

API_KEYS_FILE = os.path.join(os.path.dirname(__file__), "api_keys.json")

def load_keys():
    try:
        with open(API_KEYS_FILE) as f:
            return json.load(f)
    except:
        return {}

def save_keys(keys):
    with open(API_KEYS_FILE, "w") as f:
        json.dump(keys, f, indent=2)

def generate_key():
    return "ag-" + secrets.token_hex(24)

def create_key(tier="starter", email="unknown"):
    keys = load_keys()
    api_key = generate_key()
    keys[api_key] = {
        "tier": tier,
        "email": email,
        "created": __import__('time').strftime("%Y-%m-%d"),
        "active": True
    }
    save_keys(keys)
    print(f"✅ Created {tier} key for {email}")
    print(f"   Key: {api_key}")
    print(f"   Usage: curl -H 'Authorization: Bearer {api_key}' http://localhost:8899/v1/chat/completions")
    return api_key

def list_keys():
    keys = load_keys()
    if not keys:
        print("No API keys found.")
        return
    for k, v in keys.items():
        status = "✅" if v.get("active", True) else "❌"
        print(f"{status} {v['tier']:10s} | {v['email']:20s} | {v['created']} | {k[:16]}...")

def revoke_key(api_key):
    keys = load_keys()
    if api_key in keys:
        keys[api_key]["active"] = False
        save_keys(keys)
        print(f"❌ Revoked: {api_key[:16]}...")
    else:
        print("Key not found")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 manage_keys.py [create|list|revoke] [tier] [email]")
        print("  create pro user@email.com")
        print("  list")
        print("  revoke ag-xxxxx")
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd == "create":
        tier = sys.argv[2] if len(sys.argv) > 2 else "starter"
        email = sys.argv[3] if len(sys.argv) > 3 else "unknown"
        create_key(tier, email)
    elif cmd == "list":
        list_keys()
    elif cmd == "revoke":
        revoke_key(sys.argv[2])
