import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import aiohttp
import json

# ================== تنظیمات ==================
TOKEN = "8930543418:AAFT5AACwt9fIpzjhlWr8kgfC-RBtcuutcM"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# CoinGecko API
COINGECKO_API = "https://api.coingecko.com/api/v3/simple/price?ids=notcoin&vs_currencies=usd&include_24hr_change=true"

# ================== دستورات ==================

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 Welcome to Notcoin Bot!\n\n"
        "Tap the commands below or type /help",
        parse_mode="Markdown"
    )

@dp.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer(
        "📋 Available Commands:\n\n"
        "/price - Latest $NOT price\n"
        "/info - About Notcoin\n"
        "/tokenomics - Token information\n"
        "/community - Join community\n"
        "/links - Important links",
        parse_mode="Markdown"
    )

@dp.message(Command("price"))
async def price(message: types.Message):
    async with aiohttp.ClientSession() as session:
        async with session.get(COINGECKO_API) as resp:
            if resp.status == 200:
                data = await resp.json()
                price = data["notcoin"]["usd"]
                change = data["notcoin"]["usd_24h_change"]
                
                change_text = f"{'📈' if change > 0 else '📉'} {change:.2f}%"
                
                text = f"""
🪙 Notcoin ($NOT)

Price: ${price:.6f}
24h Change: {change_text}

_Last updated: now_
                """
                await message.answer(text, parse_mode="Markdown")
            else:
                await message.answer("❌ Unable to fetch price right now. Try again later.")

@dp.message(Command("info"))
async def info(message: types.Message):
    await message.answer(
        "Notcoin is a Tap-to-Earn game on TON blockchain with over 35 million users.\n\n"
        "Strongest community in crypto pushing $NOT to $1 and beyond!",
        parse_mode="Markdown"
    )

@dp.message(Command("tokenomics"))
async def tokenomics(message: types.Message):
    await message.answer(
        "🔹 Total Supply: 102.7 Billion\n"
        "🔹 78% to Community\n"
        "🔹 Fully Circulated at launch\n"
        "🔹 No VC dumps",
        parse_mode="Markdown"
    )

@dp.message(Command("community"))
async def community(message: types.Message):
    await message.answer(
        "🌐 Join the community:\n\n"
        "• Official Channel: @notcoin\n"
        "• Twitter: @notcoin\n"
        "• Telegram Chat: Search for Notcoin community",
        parse_mode="Markdown"
    )

@dp.message(Command("links"))
async def links(message: types.Message):
    await message.answer(
        "🔗 Important Links:\n\n"
        "• Website: notcoin.com\n"
        "• Telegram Bot: @Notcoin\n"
        "• DEX: ton.app (search NOT)",
        parse_mode="Markdown"
    )

# ================== اجرا ==================
async def main():
    logging.basicConfig(level=logging.INFO)
    print("✅ Notcoin Bot is running...")
    await dp.start_polling(bot)

if name == "main":
    asyncio.run(main())
