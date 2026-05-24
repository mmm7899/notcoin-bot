import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import aiohttp

# ================== TOKEN ==================
TOKEN = "8930543418:AAFT5AACwt9fIpzjhlWr8kgfC-RBtcuutcM"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# API برای قیمت
COINGECKO_API = "https://api.coingecko.com/api/v3/simple/price?ids=notcoin&vs_currencies=usd&include_24hr_change=true"

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("👋 Welcome to **Notcoin Bot**!\n\nSend /price to see live price.", parse_mode="Markdown")

@dp.message(Command("price"))
async def price(message: types.Message):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(COINGECKO_API) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    p = data["notcoin"]["usd"]
                    ch = data["notcoin"].get("usd_24h_change", 0)
                    emoji = "📈" if ch >= 0 else "📉"
                    await message.answer(
                        f"🪙 **Notcoin ($NOT)**\n\n"
                        f"**Price:** `${p:.6f}`\n"
                        f"**24h Change:** {emoji} {ch:.2f}%",
                        parse_mode="Markdown"
                    )
                else:
                    await message.answer("❌ Error fetching price.")
    except:
        await message.answer("❌ Connection error. Try again.")

@dp.message(Command("help"))
async def help_cmd(message: types.Message):
    await message.answer("/start\n/price - Live Price\n/help")

async def main():
    logging.basicConfig(level=logging.INFO)
    print("✅ Notcoin Bot started successfully!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
