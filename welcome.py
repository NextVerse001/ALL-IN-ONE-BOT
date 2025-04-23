import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            # ตรวจสอบว่า channel ID ถูกต้องและบอทสามารถส่งข้อความได้
            channel = self.bot.get_channel(int(os.getenv("CHANNEL_ID")))
            if channel is None:
                print(f"ไม่พบช่องทางที่มี ID {os.getenv('CHANNEL_ID')}")
                return  # หากไม่พบช่องทาง ให้หยุดการทำงาน

            # สร้างข้อความยินดีต้อนรับ โดยใช้สีดำ
            embed = discord.Embed(
                title="🎉 ยินดีต้อนรับสู่เซิร์ฟเวอร์! NextVerse X Store",
                description=f"👋🏻 ยินดีต้อนรับ {member.mention} เข้าร่วมในเซิฟเวอร์ NextVerse X Store!",
                color=discord.Colour(0x000000)  # ใช้สีดำแทน
            )
            # ใส่ภาพขยับ (ตรวจสอบ URL ให้ถูกต้อง)
            embed.set_image(url="https://images-ext-1.discordapp.net/external/kaZLgqgp52suCENJ7o6D1WKBA1TBN4PHlxCHPqRE8N4/https/i.pinimg.com/originals/5e/8a/37/5e8a37c353e6c59120438c276e78f4e2.gif?width=400&height=169")

            # เพิ่ม avatar ของสมาชิกลงใน embed
            embed.set_thumbnail(url=member.avatar.url)  # เพิ่ม avatar ของสมาชิก

            await channel.send(embed=embed)

            # มอบยศอัตโนมัติ
            if member.bot:  # ถ้าเป็นบอท
                # มอบยศสำหรับบอท
                bot_role = discord.utils.get(member.guild.roles, id=int(os.getenv("BOT_ROLE_ID")))
                if bot_role:
                    await member.add_roles(bot_role)
                    print(f"มอบยศ {bot_role.name} ให้กับบอท {member.name}")
                else:
                    print(f"ไม่พบยศที่มี ID {os.getenv('BOT_ROLE_ID')}")
            else:  # ถ้าเป็นสมาชิกธรรมดา
                # มอบยศสำหรับสมาชิกธรรมดา
                role = discord.utils.get(member.guild.roles, id=int(os.getenv("ROLE_ID")))
                if role:
                    await member.add_roles(role)
                    print(f"มอบยศ {role.name} ให้กับ {member.name}")
                else:
                    print(f"ไม่พบยศที่มี ID {os.getenv('ROLE_ID')}")

        except Exception as e:
            print(f"เกิดข้อผิดพลาดใน on_member_join: {e}")

# ลงทะเบียน cog
async def setup(bot):
    await bot.add_cog(Welcome(bot))
