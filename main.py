"""Real-time crypto KOL tweet alert bot.

Watches tracked X (Twitter) accounts over a WebSocket, detects contract
addresses the instant a tweet lands, and fires a Telegram alert. Set the env
vars below (see README). ~50 lines, no polling, no X developer account.
"""
import asyncio
import json
import os
import re

import aiohttp
import websockets

API_KEY = os.environ.get("API_KEY")
WS_URL = os.environ.get("WS_URL")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT = os.environ.get("TELEGRAM_CHAT")

# Solana base58 (32-44 chars) or EVM 0x-address.
CONTRACT = re.compile(r"\b([1-9A-HJ-NP-Za-km-z]{32,44}|0x[a-fA-F0-9]{40})\b")


async def alert(session, text):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT:
        print("ALERT:", text)
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        await session.post(url, json={"chat_id": TELEGRAM_CHAT, "text": text})
    except Exception as exc:  # noqa: BLE001
        print(f"telegram send failed ({exc})")


async def run():
    if not API_KEY or not WS_URL:
        raise SystemExit("set API_KEY and WS_URL (see README)")
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with websockets.connect(WS_URL, additional_headers={"X-Api-Key": API_KEY}) as ws:
                    print("connected: watching tracked KOLs")
                    async for raw in ws:
                        try:
                            e = json.loads(raw)
                        except ValueError:
                            continue
                        if e.get("platform") != "x":
                            continue
                        text = e.get("content", "")
                        hit = CONTRACT.search(text)
                        if hit:
                            handle = e.get("handle", "?")
                            await alert(session, f"@{handle} dropped a contract:\n{hit.group(0)}\n\n{text}")
                            print(f"ALERT @{handle}: {hit.group(0)}")
            except Exception as exc:  # noqa: BLE001
                print(f"disconnected ({exc}); reconnecting in 1s")
                await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(run())
