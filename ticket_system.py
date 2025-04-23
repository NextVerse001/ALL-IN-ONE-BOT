import discord
from discord.ext import commands
from discord.ui import Button, View
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

class TicketSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ticket_counter = 1  # เริ่มนับที่ 1 ทุกครั้งที่โหลด cog

    @commands.Cog.listener()
    async def on_ready(self):
        print("✅ Bot is ready")

        # รีเซต ticket_counter
        self.ticket_counter = 1

        channel_id = os.getenv("BOT_CHANNEL_ID")
        if not channel_id:
            print("BOT_CHANNEL_ID not found in .env")
            return

        channel = self.bot.get_channel(int(channel_id))
        if not channel:
            print(f"Channel ID {channel_id} not found or bot has no access")
            return

        # ลบข้อความบอทเก่า
        try:
            async for msg in channel.history(limit=20):
                if msg.author == self.bot.user:
                    await msg.delete()
        except Exception as e:
            print(f"ไม่สามารถลบข้อความเก่าได้: {e}")

        embed = discord.Embed(
            title="🎟️ NEXTVERSE X STORE SUPPORT TICKET",
            description="```● อย่าเปิด Ticket เล่น ไม่งั้นแบนทุกกรณี\n"
                        "● หาติดปัญหาให้อ่านห้อง fixerror ก่อน\n"
                        "● หากเปิดไม่ตรงหัวข้อจะทำการปิด Ticket ทันที\n"
                        "● Ticket จะเคลียร์ทุก 22.00 ของทุกวัน\n"
                        "● กรุณาเซฟข้อมูลของท่านใว้ด้วย```",
            color=discord.Color.blue()
        )
        embed.set_image(url="https://images-ext-1.discordapp.net/external/GPG4lkT4XoFAcdgOZMJ1yxD2T2ZeXH35JXyz0_Hq0wQ/https/i.pinimg.com/originals/e7/b4/ae/e7b4aebdedfa75a3d6382b09ec81867d.gif")
        embed.set_footer(text="NEXTVERSE X STORE")

        button = Button(label="🎟️ สอบถาม / เลือกหัวข้อ", style=discord.ButtonStyle.primary, custom_id="open_ticket_button")
        view = View()
        view.add_item(button)

        await channel.send(embed=embed, view=view)
        print("✅ Embed ใหม่ถูกส่งแล้ว")

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.data.get("custom_id") == "open_ticket_button":
            guild = interaction.guild
            user = interaction.user

            # สร้างชื่อ ticket ถัดไป
            ticket_name = f"ticket-{self.ticket_counter:03}"
            self.ticket_counter += 1

            category_id = os.getenv("CATEGORY_ID")
            if not category_id:
                await interaction.response.send_message("⚠️ ไม่พบ CATEGORY_ID ใน .env!", ephemeral=True)
                return

            category = discord.utils.get(guild.categories, id=int(category_id))
            if not category:
                await interaction.response.send_message(f"⚠️ ไม่พบ category ที่มี ID {category_id}!", ephemeral=True)
                return

            overwrites = {
                guild.default_role: discord.PermissionOverwrite(view_channel=False),
                user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
                guild.me: discord.PermissionOverwrite(view_channel=True),
            }

            admin_role_id = int(os.getenv("ROLE_ID"))
            admin_role = discord.utils.get(guild.roles, id=admin_role_id)
            if admin_role:
                overwrites[admin_role] = discord.PermissionOverwrite(view_channel=True)

            ticket_channel = await guild.create_text_channel(name=ticket_name, overwrites=overwrites, category=category)
            await interaction.response.send_message(f"✅ สร้างตั๋วของคุณแล้ว: {ticket_channel.mention}", ephemeral=True)

            embed = discord.Embed(
                title="🎟️ NEXTVERSE X STORE SUPPORT TICKET",
                description="● อย่าเปิด Ticket เล่น ไม่งั้นแบนทุกกรณี\n"
                            "● หาติดปัญหาให้อ่านห้อง fixerror ก่อน\n"
                            "● หากเปิดไม่ตรงหัวข้อจะทำการปิด Ticket ทันที\n\n"
                            "● Ticket จะเคลียร์ทุก 22.00 ของทุกวัน\n"
                            "● กรุณาเซฟข้อมูลของท่านใว้ด้วย",
                color=discord.Color.blue()
            )
            embed.set_image(url="https://images-ext-1.discordapp.net/external/GPG4lkT4XoFAcdgOZMJ1yxD2T2ZeXH35JXyz0_Hq0wQ/https/i.pinimg.com/originals/e7/b4/ae/e7b4aebdedfa75a3d6382b09ec81867d.gif")
            embed.set_footer(text="NEXTVERSE X STORE - การสนับสนุน")

            close_button = Button(label="🔒 ปิดตั๋ว Ticket", style=discord.ButtonStyle.red, custom_id="close_ticket")
            view = View()
            view.add_item(close_button)

            await ticket_channel.send(content=user.mention, embed=embed, view=view)

            await asyncio.sleep(300)
            if ticket_channel and ticket_channel.permissions_for(guild.me).manage_channels:
                try:
                    await ticket_channel.send("🕒 เวลาหมด ตั๋วนี้จะถูกลบอัตโนมัติ")
                    await ticket_channel.delete()
                except:
                    pass

        elif interaction.data.get("custom_id") == "close_ticket":
            channel = interaction.channel
            user = interaction.user

            await interaction.response.send_message("📨 ตั๋วนี้กำลังจะถูกลบโดย ADMIN", ephemeral=True)

            log_channel_id = os.getenv("LOG_CHANNEL_ID")
            if log_channel_id:
                log_channel = self.bot.get_channel(int(log_channel_id))
                if log_channel:
                    embed = discord.Embed(
                        title="📁 Ticket นี้ถูกปิด",
                        description=f"โดย: {user.mention}\nช่อง: {channel.name}",
                        color=discord.Color.red()
                    )
                    await log_channel.send(embed=embed)

            await asyncio.sleep(2)
            await channel.delete()

async def setup(bot):
    await bot.add_cog(TicketSystem(bot))
