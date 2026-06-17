# kol-tweet-alert-bot

[![License: MIT](https://img.shields.io/github/license/SisoSol/kol-tweet-alert-bot?style=flat-square&color=blue)](LICENSE) [![Last commit](https://img.shields.io/github/last-commit/SisoSol/kol-tweet-alert-bot?style=flat-square)](https://github.com/SisoSol/kol-tweet-alert-bot/commits) [![CI](https://github.com/SisoSol/kol-tweet-alert-bot/actions/workflows/ci.yml/badge.svg)](https://github.com/SisoSol/kol-tweet-alert-bot/actions/workflows/ci.yml) [![Built for 1322.io](https://img.shields.io/badge/built%20for-1322.io-3b82f6?style=flat-square)](https://1322.io) [![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square)](https://github.com/SisoSol/kol-tweet-alert-bot/pulls)

A real-time **crypto KOL tweet alert bot** in ~50 lines of Python. Watches the
X (Twitter) accounts you track over a **WebSocket**, detects contract addresses
and tickers the instant a tweet lands, and fires a **Telegram alert in under a
second**.

Polling the X API v2 caps your worst-case latency at the poll interval and burns
read quota. This bot holds a persistent WebSocket and reacts the moment a tracked
KOL posts, which is the whole point for memecoin entries and KOL-driven trades.

It runs against the [1322](https://1322.io/use-cases/crypto-kol-tracking) feed
(X posts in ~150-250ms; Binance Square on the same socket with coin pairs
parsed). The consumer pattern is generic.

- Crypto KOL tracking: https://1322.io/use-cases/crypto-kol-tracking
- Full walkthrough: https://1322.io/blog/kol-tweet-alert-bot-python
- Event schema / docs: https://1322.io/docs

## What you need

- Python 3.10+ and `pip install websockets aiohttp`
- A 1322 API key + your WebSocket path (dashboard, after signup, from $250/mo)
- A Telegram bot token (free, from @BotFather) and your chat id

## Run

```bash
pip install websockets aiohttp
API_KEY=your-key WS_URL=wss://1322.io/your-ws-path \
TELEGRAM_TOKEN=your-bot-token TELEGRAM_CHAT=your-chat-id \
python main.py
```

## How it works

1. Open a WebSocket to the 1322 feed (no polling, no X developer account).
2. For each tweet event, match a regex for Solana / EVM contract addresses.
3. On a hit, forward the tweet + address to Telegram.

Filter on `platform == "binance"` too and you get Binance Square posts on the
same connection.

## Related

- Social alerts for trading bots: https://github.com/SisoSol/social-trading-signals
- Twitter/X client: https://github.com/SisoSol/twitter-websocket-client
- All six platforms: https://github.com/SisoSol/social-monitor-examples

MIT licensed.
