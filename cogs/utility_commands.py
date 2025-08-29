import discord
from discord.ext import commands

class UtilityCommands(commands.Cog):
    """Comandos de utilidad"""
    
    def __init__(self, bot):
        self.bot = bot

    # Aquí puedes agregar comandos de utilidad

async def setup(bot):
    await bot.add_cog(UtilityCommands(bot))
