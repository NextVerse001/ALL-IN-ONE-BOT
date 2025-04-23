import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os

# โหลด .env
load_dotenv()

class NotificationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = int(os.getenv("ALERT_CHANNEL_ID"))  # 📢 ช่องแจ้งเตือน
        self.ticket_channel_id = int(os.getenv("BOT_CHANNEL_ID"))  # 🔗 ช่อง Ticket
        self.guild_id = int(os.getenv("DISCORD_GUILD_ID"))  # 🏠 ไอดีเซิร์ฟเวอร์
        self.role_id = int(os.getenv("NOTIFY_ROLE_ID"))  # 🏷️ ไอดี Role ที่ต้องแท็ก
        self.notify_task.start()

    @tasks.loop(minutes=15)
    async def notify_task(self):
        channel = self.bot.get_channel(self.channel_id)
        if channel:
            embed = discord.Embed(
                title="✨🔔 การแจ้งเตือนจากบอท 🔔✨",
                description=(
                    "🚫 **ตอนนี้ใครจะปลดแบนได้เฉพาะ** **BT**, **Global**\n"
                    "🎮 **โดนแบน **FiveM** ก็ปลดได้!**\n"
                    "✅ **ทางร้านมีบริการปลดแบนให้ฟรี!**\n\n"
                    f"💸 **ซื้อมาแล้ว** **[คลิกที่นี่เพื่อเปิด Ticket](https://discord.com/channels/{self.guild_id}/{self.ticket_channel_id})**\n"
                    f"📩 หรือคลิกที่นี้ <#{self.ticket_channel_id}> เพื่อเริ่มสอบถามสินค้า"
                ),
                color=discord.Color.dark_theme()
            )

            embed.set_thumbnail(
                url="https://media.discordapp.net/attachments/1355882050921693296/1364535941850730539/1.png"
            )
            embed.set_image(
                url="https://images-ext-1.discordapp.net/external/dA5sJ-pnB7PI_CFCkaZxEaNDIedVfwmuyJASiRU5nG8/https/i.pinimg.com/originals/78/74/c0/7874c0e66600b57ea535a332911071f9.gif"
            )
            embed.set_footer(text="🛡️ ปลดแบนฟรี พร้อมดูแลทุกคนในเซิร์ฟเวอร์ 🛡️")

            await channel.send(content=f"<@&{self.role_id}>", embed=embed)

    @notify_task.before_loop
    async def before_notify(self):
        print("🟡 | เริ่มระบบแจ้งเตือน ⏳ กรุณารอสักครู่...")

    @notify_task.after_loop
    async def after_notify(self):
        print("🔴 | การแจ้งเตือนหยุดทำงานแล้ว ❌")

# เพิ่ม Cog เข้าไปใน Bot
async def setup(bot):
    await bot.add_cog(NotificationCog(bot))
