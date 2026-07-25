import asyncio
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("BOT_PREFIX", "!")

EXTENSIONS = (
    "cogs.basic_commands",
    "cogs.utility_commands",
    "cogs.music_commands",
)


class CanchonBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(
            command_prefix=PREFIX,
            intents=intents,
            max_messages=100,
            help_command=None,
        )

    async def setup_hook(self) -> None:
        """Carga los módulos después de autenticar el bot."""
        for extension in EXTENSIONS:
            try:
                await self.load_extension(extension)
                print(f"Cargado: {extension}")
            except Exception as error:
                print(f"Error cargando {extension}: {error}")

    async def on_ready(self) -> None:
        if self.user is None:
            return

        print(f"Bot conectado como {self.user}")
        print(f"ID: {self.user.id}")
        print(f"Prefijo: {PREFIX}")
        print("------")


async def main() -> None:
    if not TOKEN:
        raise RuntimeError("Falta DISCORD_TOKEN en el archivo .env")

    bot = CanchonBot()
    async with bot:
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
