import discord
from discord.ext import commands
import random

class UtilityCommands(commands.Cog):
    """Comandos de utilidad"""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='howgay')
    async def howgay(self, ctx, member: discord.Member = None):
        """Mide cuán gay eres (o de un usuario mencionado) con un porcentaje aleatorio"""
        if member is None:
            member = ctx.author
        
        percentage = random.randint(0, 100)
        
        embed = discord.Embed(
            title="🏳️‍🌈 Medidor de Homosexualidad 🏳️‍🌈",
            description=f"{member.mention} es **{percentage}% gay**. 🏳️‍🌈",
            color=0xff69b4  # Rosa gay
        )
        
        await ctx.send(embed=embed)

    # Aquí puedes agregar comandos de utilidad

async def setup(bot):
    await bot.add_cog(UtilityCommands(bot))
