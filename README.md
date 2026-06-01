# 🔌 AI API Gateway — White-Label AI Access

**Resell AI model access with a 30-50% markup. Drop-in OpenAI-compatible API.**

## What Is This?

A white-label API gateway that wraps OpenRouter/OpenAI/Anthropic APIs. You buy credits at wholesale, we handle the infrastructure, you sell at retail.

## 🌟 Featured In

This product is part of the **[ulnit Agent Store](https://ulnit.github.io/agent-store)** — 23 AI-powered products running 24/7 on a $35 Raspberry Pi.

> 💡 **Power Pairing:** Use **[AI Video Factory](https://github.com/ulnit/ai-video-factory)** to create faceless YouTube/TikTok content at zero cost, then offer your viewers AI API access through this gateway for recurring revenue.

## Features

- ✅ **OpenAI-compatible** — Drop-in replacement for any OpenAI SDK
- ✅ **Usage tracking** — Per-key token counting and rate limiting
- ✅ **Tiered pricing** — Free trial → Pro → Business
- ✅ **Zero dependencies** — Runs on Raspberry Pi, $0 hosting cost
- ✅ **White-label** — Your brand, your pricing, your customers

## Pricing Tiers

| Tier | Tokens/Month | Price | Use Case |
|------|-------------|-------|----------|
| 🆓 Starter | 100K | Free | Testing, personal use |
| ⭐ Pro | 1M | $9/mo | Solo developers, small projects |
| 🚀 Business | 10M | $29/mo | Teams, production apps |

## Quick Start

```bash
# Get your API key
curl -X POST https://paypal.me/ulnit/9 -d "email=you@example.com"

# Use it like OpenAI
curl https://your-gateway:8899/v1/chat/completions \
  -H "Authorization: Bearer ag-YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "openai/gpt-4o", "messages": [{"role": "user", "content": "Hello!"}]}'
```

## Supported Models

Via OpenRouter: GPT-4o, Claude 3.5 Sonnet, Gemini 2.0 Flash, DeepSeek V3, Llama 4, and 200+ more.

## Why Resell AI APIs?

1. **Growing market** — AI API usage is exploding (200% YoY)
2. **Recurring revenue** — Monthly subscriptions, not one-time sales
3. **Zero marginal cost** — Each additional customer costs nothing
4. **First-mover advantage** — Most developers don't know they can resell

## Architecture

```
Your Customers → AI API Gateway (Pi) → OpenRouter/OpenAI
                  ↓
            Usage tracking + Rate limiting
                  ↓
            PayPal.me billing ($9-29/mo)
```

## Get Started

1. **Buy Pro tier**: [paypal.me/ulnit/9](https://paypal.me/ulnit/9)
2. **Receive API key** via email within 24 hours
3. **Start building** — same API as OpenAI

---

*Built by AI agents. Runs on a Raspberry Pi. Scales to thousands of users.*

---

## 🔗 Related Products

| Product | Description | Price |
|---------|-------------|-------|
| [🤖 Agent Templates](https://github.com/ulnit/agent-templates) | Pre-built AI agent skills for 5 industries | $15-79 |
| [📊 Trading Signals](https://github.com/ulnit/ai-trading-signals) | Daily A-share market intelligence | $29-99/mo |
| [🎬 Video Factory](https://github.com/ulnit/ai-video-factory) | Automated video content pipeline | $9/mo |
| [🔌 API Gateway](https://github.com/ulnit/ai-api-gateway) | White-label AI model reselling | $9/mo |
| [📝 Resume Optimizer](https://github.com/ulnit/ai-resume-optimizer) | ATS-friendly resume enhancement | $5-15 |
| [🤖 CS Bot](https://github.com/ulnit/ai-cs-bot) | White-label customer service chatbot | $19-49/mo |

> 🏪 [View All 19 Products →](https://ulnit.github.io/agent-store)
