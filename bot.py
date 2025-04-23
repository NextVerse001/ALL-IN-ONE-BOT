import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio

# โหลด .env
load_dotenv()

# ตั้งค่า intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# สร้าง instance ของ bot
bot = commands.Bot(command_prefix="!", intents=intents)

# ฟังก์ชันหลัก
async def main():
    async with bot:
        # โหลด cogs ต่างๆ รวมถึง notification
        await bot.load_extension("cogs.welcome")
        await bot.load_extension("cogs.ticket_system")
        await bot.load_extension("cogs.notification")  # เพิ่มการโหลด notification cog
        await bot.start(os.getenv("TOKEN"))

# เรียก main
asyncio.run(main())
