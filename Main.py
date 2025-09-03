
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

# Cargar variables de entorno desde .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True  # Necesario para leer contenido de mensajes
# Limitar cache de mensajes para ahorrar memoria en servidores pequeños
bot = commands.Bot(command_prefix='!', intents=intents, max_messages=100)

import os
import asyncio
from dotenv import load_dotenv
import discord
from discord.ext import commands

# Cargar variables de entorno desde .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True  # Necesario para leer contenido de mensajes
# Asegurarse de usar una configuración baja de cache si se redefine
bot = commands.Bot(command_prefix='!', intents=intents, max_messages=100)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    print(f'ID: {bot.user.id}')
    print('------')

# Cargar módulos automáticamente
async def load_extensions():
    """Carga todos los cogs disponibles"""
    initial_extensions = [
        'cogs.basic_commands',
        'cogs.utility_commands'
    ]
    
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            print(f'Cargado: {extension}')
        except Exception as e:
            print(f'Error cargando {extension}: {e}')

async def main():
    """Función principal para iniciar el bot"""
    await load_extensions()
    await bot.start(TOKEN)

if __name__ == '__main__':
    asyncio.run(main())
